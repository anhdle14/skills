#!/usr/bin/env -S deno run --allow-read

import { exists } from "@std/fs";
import { basename, join } from "@std/path";
import {
  findFrontmatterSyntaxFailures,
  parseFrontmatter,
} from "./skill-frontmatter.ts";

const SKILLS_DIR = "skills";
const VALID_TAGS = new Set([
  "analyze",
  "create",
  "plan",
  "transform",
  "manage",
  "productivity",
  "engineering",
  "writing",
]);
const PERSISTENCE_RULE = "Persistence rule: context is volatile RAM; filesystem is durable disk. Write important plans, progress checkboxes, failures, and verification to files; re-read them before decisions and done checks.";

interface Failure {
  file: string;
  message: string;
}

function isKebabCase(value: string): boolean {
  return /^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(value);
}

async function validateSkill(skillDir: string): Promise<Failure[]> {
  const file = join(skillDir, "SKILL.md");
  const failures: Failure[] = [];

  if (!(await exists(file))) {
    return [{ file, message: "missing SKILL.md" }];
  }

  const content = await Deno.readTextFile(file);
  const lines = content.split("\n").length;
  const frontmatter = parseFrontmatter(content);
  failures.push(
    ...findFrontmatterSyntaxFailures(content).map((failure) => ({
      file,
      message: `line ${failure.line}: ${failure.message}`,
    })),
  );
  const folderName = basename(skillDir);

  if (lines > 100) {
    failures.push({
      file,
      message: `SKILL.md has ${lines} lines; keep it under 100`,
    });
  }

  if (!content.includes(PERSISTENCE_RULE)) {
    failures.push({
      file,
      message:
        "missing persistence rule: treat context as RAM and filesystem as disk",
    });
  }

  if (!frontmatter) {
    failures.push({ file, message: "missing YAML frontmatter block" });
    return failures;
  }

  if (!frontmatter.name) {
    failures.push({ file, message: "missing name" });
  } else {
    if (!isKebabCase(frontmatter.name)) {
      failures.push({ file, message: "name must be kebab-case" });
    }
    if (frontmatter.name !== folderName) {
      failures.push({
        file,
        message: `name '${frontmatter.name}' must match folder '${folderName}'`,
      });
    }
  }

  if (!frontmatter.description) {
    failures.push({ file, message: "missing description" });
  } else {
    if (frontmatter.description.length > 1024) {
      failures.push({ file, message: "description exceeds 1024 characters" });
    }
    // Trigger-language rules only matter when the model can auto-select the
    // skill. A skill with `disable-model-invocation: true` is hidden from the
    // system prompt and only runs via an explicit human `/skill:name` call, so
    // "Use when ..." trigger phrasing serves no purpose for it.
    if (!frontmatter.disableModelInvocation) {
      if (!frontmatter.description.includes("Use when")) {
        failures.push({
          file,
          message: 'description must include "Use when" trigger language',
        });
      }
      if (!/^[^.]+\.\s+Use when .+\.$/.test(frontmatter.description)) {
        failures.push({
          file,
          message:
            'description should be two sentences: capability, then "Use when..."',
        });
      }
    }
  }

  if (!frontmatter.tags || frontmatter.tags.length === 0) {
    failures.push({ file, message: "missing tags array" });
  } else {
    for (const tag of frontmatter.tags) {
      if (!VALID_TAGS.has(tag)) {
        failures.push({ file, message: `invalid tag '${tag}'` });
      }
    }
  }

  if (frontmatter.args && !/^".+"$/.test(frontmatter.args)) {
    failures.push({ file, message: "args must be a quoted usage string" });
  }

  const disableLine = content.match(/^disable-model-invocation:\s*(.*)$/m);
  if (disableLine && !/^(true|false)$/.test(disableLine[1].trim())) {
    failures.push({
      file,
      message: "disable-model-invocation must be a boolean (true or false)",
    });
  }

  if (/\b20\d{2}\b/.test(content)) {
    failures.push({
      file,
      message: "avoid baking time-sensitive years into skill instructions",
    });
  }

  return failures;
}

const skillDirs: string[] = [];
for await (const entry of Deno.readDir(SKILLS_DIR)) {
  if (entry.isDirectory) {
    skillDirs.push(join(SKILLS_DIR, entry.name));
  }
}

const failures = (
  await Promise.all(skillDirs.sort().map((dir) => validateSkill(dir)))
).flat();

if (failures.length > 0) {
  for (const failure of failures) {
    console.error(`FAIL: ${failure.file}: ${failure.message}`);
  }
  Deno.exit(1);
}

console.log(`OK: validated ${skillDirs.length} skills`);
