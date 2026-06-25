#!/usr/bin/env -S deno run --allow-read --allow-run=claude --allow-env=CLAUDECODE,EVAL_MODEL,EVAL_WORKERS

import { dirname, join } from "@std/path";
import { parseFrontmatter } from "./skill-frontmatter.ts";

const SKILLS_DIR = "skills";
const DEFAULT_CASES_PATH = "docs/evals/engineering-skills-trigger-cases.json";
const DEFAULT_RESULTS_PATH = "docs/evals/engineering-skills-trigger-results.json";

type Skill = {
  name: string;
  description: string;
  tags: string[];
  disableModelInvocation: boolean;
};

type EvalCase = {
  query: string;
  shouldTrigger: boolean;
};

type SkillCases = {
  skill: string;
  cases: EvalCase[];
};

type CaseFile = {
  version: number;
  cases: SkillCases[];
};

type CaseResult = EvalCase & {
  id: number;
  selectedSkills: string[];
  reason: string;
  passed: boolean;
};

type SkillResult = {
  skill: string;
  model: string;
  summary: { passed: number; total: number };
  results: CaseResult[];
};

type ResultsFile = {
  generatedAt: string;
  model: string;
  method: string;
  skills: SkillResult[];
  summary: { passed: number; total: number; passRate: number };
};

function argFlag(name: string): boolean {
  return Deno.args.includes(name);
}

function argValue(name: string, fallback: string): string {
  const index = Deno.args.indexOf(name);
  return index >= 0 && Deno.args[index + 1] ? Deno.args[index + 1] : fallback;
}

async function readJson<T>(path: string): Promise<T> {
  return JSON.parse(await Deno.readTextFile(path)) as T;
}

async function readSkills(): Promise<Skill[]> {
  const skills: Skill[] = [];
  for await (const entry of Deno.readDir(SKILLS_DIR)) {
    if (!entry.isDirectory) continue;
    const file = join(SKILLS_DIR, entry.name, "SKILL.md");
    const frontmatter = parseFrontmatter(await Deno.readTextFile(file));
    if (!frontmatter?.name || !frontmatter.description || !frontmatter.tags) {
      continue;
    }
    skills.push({
      name: frontmatter.name,
      description: frontmatter.description,
      tags: frontmatter.tags,
      disableModelInvocation: frontmatter.disableModelInvocation ?? false,
    });
  }
  return skills.sort((a, b) => a.name.localeCompare(b.name));
}

function requireNoFailures(failures: string[]): void {
  if (failures.length === 0) return;
  for (const failure of failures) console.error(`FAIL: ${failure}`);
  Deno.exit(1);
}

async function checkFixtures(
  casesPath: string,
  resultsPath: string,
  minPassRate: number,
): Promise<void> {
  const skills = await readSkills();
  const allSkillNames = new Set(skills.map((skill) => skill.name));
  // A skill hidden from the model (`disable-model-invocation: true`) can only
  // be invoked by an explicit human `/skill:name` call, so it is never part of
  // model trigger selection and must not be required to carry trigger cases.
  const triggerableSkills = skills.filter(
    (skill) => !skill.disableModelInvocation,
  );
  const disabledSkillNames = new Set(
    skills.filter((skill) => skill.disableModelInvocation).map((s) => s.name),
  );
  const engineeringSkills = triggerableSkills
    .filter((skill) => skill.tags.includes("engineering"))
    .map((skill) => skill.name)
    .sort();
  const caseFile = await readJson<CaseFile>(casesPath);
  const failures: string[] = [];

  if (caseFile.version !== 1) {
    failures.push(`${casesPath}: expected version 1`);
  }

  const seenCaseSkills = new Set<string>();
  for (const group of caseFile.cases) {
    if (seenCaseSkills.has(group.skill)) {
      failures.push(`${casesPath}: duplicate case group for ${group.skill}`);
    }
    seenCaseSkills.add(group.skill);

    if (!allSkillNames.has(group.skill)) {
      failures.push(`${casesPath}: unknown skill ${group.skill}`);
    }
    if (disabledSkillNames.has(group.skill)) {
      failures.push(
        `${casesPath}: ${group.skill} has disable-model-invocation: true and cannot be triggered; remove its trigger cases`,
      );
    }

    const shouldTriggerCount = group.cases.filter((item) =>
      item.shouldTrigger
    ).length;
    const shouldNotTriggerCount = group.cases.length - shouldTriggerCount;
    if (shouldTriggerCount < 3 || shouldNotTriggerCount < 3) {
      failures.push(
        `${casesPath}: ${group.skill} needs at least 3 trigger and 3 near-miss cases`,
      );
    }

    for (const [index, item] of group.cases.entries()) {
      if (!item.query.trim()) {
        failures.push(`${casesPath}: ${group.skill} case ${index + 1} has empty query`);
      }
      if (typeof item.shouldTrigger !== "boolean") {
        failures.push(
          `${casesPath}: ${group.skill} case ${index + 1} shouldTrigger must be boolean`,
        );
      }
    }
  }

  for (const skill of engineeringSkills) {
    if (!seenCaseSkills.has(skill)) {
      failures.push(`${casesPath}: missing eval cases for engineering skill ${skill}`);
    }
  }
  for (const skill of seenCaseSkills) {
    if (!engineeringSkills.includes(skill) && !disabledSkillNames.has(skill)) {
      failures.push(`${casesPath}: ${skill} is not tagged engineering`);
    }
  }

  let results: ResultsFile | null = null;
  try {
    results = await readJson<ResultsFile>(resultsPath);
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    failures.push(`${resultsPath}: cannot read results (${message})`);
  }

  if (results) {
    const totalCases = caseFile.cases.reduce(
      (sum, group) => sum + group.cases.length,
      0,
    );
    const resultBySkill = new Map(results.skills.map((item) => [item.skill, item]));
    if (results.summary.total !== totalCases) {
      failures.push(
        `${resultsPath}: summary total ${results.summary.total} does not match ${totalCases} cases`,
      );
    }
    if (results.summary.passRate < minPassRate) {
      failures.push(
        `${resultsPath}: pass rate ${results.summary.passRate} is below ${minPassRate}`,
      );
    }

    for (const group of caseFile.cases) {
      const result = resultBySkill.get(group.skill);
      if (!result) {
        failures.push(`${resultsPath}: missing results for ${group.skill}`);
        continue;
      }
      if (result.results.length !== group.cases.length) {
        failures.push(`${resultsPath}: ${group.skill} result count does not match cases`);
        continue;
      }
      for (const [index, item] of group.cases.entries()) {
        const resultItem = result.results[index];
        if (
          resultItem.query !== item.query ||
          resultItem.shouldTrigger !== item.shouldTrigger
        ) {
          failures.push(
            `${resultsPath}: ${group.skill} case ${index + 1} is stale versus ${casesPath}`,
          );
        }
      }
    }
  }

  requireNoFailures(failures);
  console.log(
    `OK: eval fixtures cover ${engineeringSkills.length} engineering skills (${caseFile.cases.reduce((sum, group) => sum + group.cases.length, 0)} cases)`,
  );
}

function buildSelectorPrompt(skills: Skill[], target: string, cases: EvalCase[]): string {
  const availableSkills = skills
    .map((skill) => `- ${skill.name}: ${skill.description}`)
    .join("\n");
  const requests = cases
    .map((item, index) => `${index + 1}. ${item.query}`)
    .join("\n");

  return `You are evaluating skill trigger descriptions for a coding agent.

Available skills (name: description):
${availableSkills}

For each user request below, choose the specialized skills that should be loaded before responding. Select no more than 2 skills. Select a skill only when its description directly applies and using it would materially change the response. Return JSON only with this exact shape:
{"results":[{"id":1,"selected_skills":["skill-name"],"reason":"short"}]}

User requests for target skill ${target}:
${requests}
`;
}

function parseSelectorResult(raw: string): Map<number, { selectedSkills: string[]; reason: string }> {
  const outer = JSON.parse(raw) as { result?: string };
  const result = outer.result ?? "";
  const match = result.match(/\{[\s\S]*\}/);
  if (!match) throw new Error("Claude response did not contain JSON result");
  const parsed = JSON.parse(match[0]) as {
    results?: Array<{ id?: number; selected_skills?: string[]; reason?: string }>;
  };
  const rows = new Map<number, { selectedSkills: string[]; reason: string }>();
  for (const item of parsed.results ?? []) {
    if (typeof item.id !== "number") continue;
    rows.set(item.id, {
      selectedSkills: Array.isArray(item.selected_skills) ? item.selected_skills : [],
      reason: item.reason ?? "",
    });
  }
  return rows;
}

async function runLiveEval(
  casesPath: string,
  resultsPath: string,
  targetFilter: string,
  writeResults: boolean,
): Promise<void> {
  const skills = (await readSkills()).filter(
    (skill) => !skill.disableModelInvocation,
  );
  const caseFile = await readJson<CaseFile>(casesPath);
  const model = Deno.env.get("EVAL_MODEL") ?? "haiku";
  const workerCount = Math.max(
    1,
    Number.parseInt(Deno.env.get("EVAL_WORKERS") ?? "3", 10) || 3,
  );
  const selectedGroups = targetFilter === "all"
    ? caseFile.cases
    : caseFile.cases.filter((group) => group.skill === targetFilter);

  if (selectedGroups.length === 0) {
    console.error(`FAIL: no eval cases matched target '${targetFilter}'`);
    Deno.exit(1);
  }

  async function runGroup(group: SkillCases): Promise<SkillResult> {
    const prompt = buildSelectorPrompt(skills, group.skill, group.cases);
    const command = new Deno.Command("claude", {
      args: ["-p", prompt, "--output-format", "json", "--model", model],
      stdout: "piped",
      stderr: "piped",
      env: { CLAUDECODE: "" },
    });
    const output = await command.output();
    const stdout = new TextDecoder().decode(output.stdout);
    const stderr = new TextDecoder().decode(output.stderr);
    if (!output.success) {
      throw new Error(stderr || stdout || `claude exited ${output.code}`);
    }

    const selectorRows = parseSelectorResult(stdout);
    const results = group.cases.map((item, index) => {
      const id = index + 1;
      const selectorRow = selectorRows.get(id) ?? { selectedSkills: [], reason: "" };
      const selectedSkills = selectorRow.selectedSkills;
      const passed = selectedSkills.includes(group.skill) === item.shouldTrigger;
      return {
        ...item,
        id,
        selectedSkills,
        reason: selectorRow.reason,
        passed,
      };
    });
    const passed = results.filter((item) => item.passed).length;
    console.log(`${group.skill}: ${passed}/${results.length}`);
    return {
      skill: group.skill,
      model,
      summary: { passed, total: results.length },
      results,
    };
  }

  let nextGroup = 0;
  const skillResults: SkillResult[] = new Array(selectedGroups.length);
  await Promise.all(
    Array.from({ length: Math.min(workerCount, selectedGroups.length) }, async () => {
      while (nextGroup < selectedGroups.length) {
        const index = nextGroup++;
        skillResults[index] = await runGroup(selectedGroups[index]);
      }
    }),
  );

  const passed = skillResults.reduce((sum, item) => sum + item.summary.passed, 0);
  const total = skillResults.reduce((sum, item) => sum + item.summary.total, 0);
  const results: ResultsFile = {
    generatedAt: new Date().toISOString(),
    model,
    method:
      "LLM selector trigger eval inspired by anthropic/skills skill-creator description optimization. One Claude call per engineering skill; each skill has trigger and near-miss prompts.",
    skills: skillResults,
    summary: { passed, total, passRate: Number((passed / total).toFixed(4)) },
  };

  if (writeResults) {
    await Deno.mkdir(dirname(resultsPath), { recursive: true });
    await Deno.writeTextFile(resultsPath, JSON.stringify(results, null, 2) + "\n");
  }

  console.log(
    `summary: ${passed}/${total} (${(results.summary.passRate * 100).toFixed(1)}%)`,
  );
}

const casesPath = argValue("--cases", DEFAULT_CASES_PATH);
const resultsPath = argValue("--results", DEFAULT_RESULTS_PATH);
const minPassRate = Number(argValue("--min-pass-rate", "0.95"));

if (argFlag("--live")) {
  await runLiveEval(
    casesPath,
    resultsPath,
    argValue("--target", "all"),
    argFlag("--write"),
  );
} else {
  await checkFixtures(casesPath, resultsPath, minPassRate);
}
