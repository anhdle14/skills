#!/usr/bin/env -S deno run --allow-read

import { exists } from "@std/fs";
import { basename, join } from "@std/path";

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

interface Frontmatter {
  name?: string;
  description?: string;
  tags?: string[];
  args?: string;
}

interface Failure {
  file: string;
  message: string;
}

function parseScalar(value: string): string {
  const trimmed = value.trim();
  if (
    (trimmed.startsWith('"') && trimmed.endsWith('"')) ||
    (trimmed.startsWith("'") && trimmed.endsWith("'"))
  ) {
    return trimmed.slice(1, -1);
  }
  return trimmed;
}

function parseFrontmatter(content: string): Frontmatter | null {
  const match = content.match(/^---\n([\s\S]*?)\n---/);
  if (!match) return null;

  const lines = match[1].split("\n");
  const data: Record<string, string> = {};

  for (let index = 0; index < lines.length; index++) {
    const line = lines[index];
    const pair = line.match(/^([a-z]+):\s*(.*)$/);
    if (!pair) continue;

    const [, key, rawValue] = pair;
    if (rawValue === ">") {
      const folded: string[] = [];
      while (index + 1 < lines.length && /^\s+/.test(lines[index + 1])) {
        folded.push(lines[index + 1].trim());
        index++;
      }
      data[key] = folded.join(" ");
    } else {
      data[key] = key === "args" ? rawValue.trim() : parseScalar(rawValue);
    }
  }

  const tagsRaw = data.tags ?? "";
  const tags = tagsRaw.match(/^\[(.*)\]$/)
    ? tagsRaw
      .slice(1, -1)
      .split(",")
      .map((tag) => tag.trim())
      .filter(Boolean)
    : undefined;

  return {
    ...(data.name ? { name: data.name } : {}),
    ...(data.description ? { description: data.description } : {}),
    ...(tags ? { tags } : {}),
    ...(data.args ? { args: data.args } : {}),
  };
}

function findFrontmatterSyntaxFailures(content: string, file: string): Failure[] {
  const match = content.match(/^---\n([\s\S]*?)\n---/);
  if (!match) return [];

  const failures: Failure[] = [];
  const lines = match[1].split("\n");
  for (let index = 0; index < lines.length; index++) {
    const line = lines[index];
    const pair = line.match(/^([a-z]+):\s*(.*)$/);
    if (!pair) continue;

    const rawValue = pair[2].trim();
    const isQuoted =
      (rawValue.startsWith('"') && rawValue.endsWith('"')) ||
      (rawValue.startsWith("'") && rawValue.endsWith("'"));
    if (rawValue && rawValue !== ">" && !isQuoted && /:\s/.test(rawValue)) {
      failures.push({
        file,
        message:
          `line ${index + 2}: unquoted YAML scalar contains ': '; quote it or use folded block syntax`,
      });
    }
  }

  return failures;
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
  failures.push(...findFrontmatterSyntaxFailures(content, file));
  const folderName = basename(skillDir);

  if (lines > 100) {
    failures.push({
      file,
      message: `SKILL.md has ${lines} lines; keep it under 100`,
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
