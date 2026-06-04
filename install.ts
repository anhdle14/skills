#!/usr/bin/env -S deno run --allow-read --allow-write --allow-env=HOME
/**
 * install.ts — link or copy skills to agent config directories
 *
 * Usage:
 *   deno task install                                        # symlink skills/ → ~/.claude/skills + ~/.agent/skills
 *   deno task install --copy-to /path/to/project            # copy all skills into a project
 *   deno task install --copy-to /path/to/project --skill diagnose --skill grill-me
 *   deno task install --update-index                        # regenerate CLAUDE.md skills index
 */

import { parseArgs } from "@std/cli/parse-args";
import { ensureDir, exists } from "@std/fs";
import { join, dirname, fromFileUrl } from "@std/path";

const REPO = dirname(fromFileUrl(import.meta.url));
const SKILLS_DIR = join(REPO, "skills");

interface SkillMeta {
  name: string;
  description: string;
  tags: string[];
  args?: string;
}

async function parseSkillMeta(skillDir: string): Promise<SkillMeta | null> {
  const skillMd = join(skillDir, "SKILL.md");
  if (!(await exists(skillMd))) return null;

  const content = await Deno.readTextFile(skillMd);
  const match = content.match(/^---\n([\s\S]*?)\n---/);
  if (!match) return null;

  const fm = match[1];
  const name = fm.match(/^name:\s*(.+)$/m)?.[1]?.trim() ?? "";
  const description = fm.match(/^description:\s*(.+)$/m)?.[1]?.trim() ?? "";
  const tagsLine = fm.match(/^tags:\s*\[(.+)\]$/m)?.[1] ?? "";
  const tags = tagsLine.split(",").map((t) => t.trim()).filter(Boolean);
  const args = fm.match(/^args:\s*(.+)$/m)?.[1]?.trim();

  return { name, description, tags, ...(args ? { args } : {}) };
}

async function listSkills(): Promise<string[]> {
  const names: string[] = [];
  for await (const entry of Deno.readDir(SKILLS_DIR)) {
    if (entry.isDirectory) {
      const skillMd = join(SKILLS_DIR, entry.name, "SKILL.md");
      if (await exists(skillMd)) names.push(entry.name);
    }
  }
  return names.sort();
}

function getSymlinkTargets(): string[] {
  const home = Deno.env.get("HOME");
  if (!home) throw new Error("HOME environment variable is not set");
  return [
    join(home, ".claude", "skills"),
    join(home, ".agent", "skills"),
  ];
}

async function symlinkSkills() {
  for (const target of getSymlinkTargets()) {
    const parent = dirname(target);
    await ensureDir(parent);

    try {
      const info = await Deno.lstat(target);
      if (info.isSymlink) {
        await Deno.remove(target);
      } else if (info.isDirectory) {
        console.log(
          `${target} is a real directory — skipping (remove it manually to replace with symlink)`,
        );
        continue;
      }
    } catch {
      // doesn't exist yet — fine
    }

    await Deno.symlink(SKILLS_DIR, target);
    console.log(`linked: ${target} → ${SKILLS_DIR}`);
  }
}

async function copyDir(src: string, dest: string) {
  await ensureDir(dest);
  for await (const entry of Deno.readDir(src)) {
    const srcPath = join(src, entry.name);
    const destPath = join(dest, entry.name);
    if (entry.isFile) {
      await Deno.copyFile(srcPath, destPath);
    } else if (entry.isDirectory) {
      await copyDir(srcPath, destPath);
    }
  }
}

async function copySkills(destDir: string, filter: string[]) {
  await ensureDir(destDir);
  const skills = filter.length > 0 ? filter : await listSkills();

  for (const name of skills) {
    const src = join(SKILLS_DIR, name);
    if (!(await exists(src))) {
      console.error(`skill not found: ${name}`);
      continue;
    }
    await copyDir(src, join(destDir, name));
    console.log(`copied: ${name} → ${join(destDir, name)}`);
  }
}

async function updateIndex() {
  const skillNames = await listSkills();
  const rows: string[] = [];

  for (const name of skillNames) {
    const meta = await parseSkillMeta(join(SKILLS_DIR, name));
    if (!meta) continue;
    const tags = meta.tags.join(", ");
    const args = meta.args ? ` Args: \`${meta.args}\`` : "";
    rows.push(
      `| [${meta.name}](skills/${name}/SKILL.md) | ${tags} | ${meta.description}${args} |`,
    );
  }

  const table = [
    "| skill | tags | description |",
    "|-------|------|-------------|",
    ...rows,
  ].join("\n");

  const claudeMd = join(REPO, "CLAUDE.md");
  let content = await Deno.readTextFile(claudeMd);
  content = content.replace(
    /<!-- skills-index-start -->[\s\S]*?<!-- skills-index-end -->/,
    `<!-- skills-index-start -->\n${table}\n<!-- skills-index-end -->`,
  );
  await Deno.writeTextFile(claudeMd, content);
  console.log(`updated CLAUDE.md skills index (${rows.length} skills)`);
}

// --- main ---

const args = parseArgs(Deno.args, {
  string: ["copy-to", "skill"],
  boolean: ["update-index", "help"],
  collect: ["skill"],
  alias: { h: "help" },
});

if (args.help) {
  console.log(`
install.ts — link or copy skills to agent config directories

Usage:
  deno task install                                   symlink skills/ to ~/.claude/skills and ~/.agent/skills
  deno task install --copy-to <dir>                   copy all skills into <dir>
  deno task install --copy-to <dir> --skill <name>    copy only named skills (repeat --skill for multiple)
  deno task install --update-index                    regenerate skills table in CLAUDE.md
`);
  Deno.exit(0);
}

if (args["update-index"]) {
  await updateIndex();
} else if (args["copy-to"]) {
  const filter = Array.isArray(args.skill)
    ? args.skill
    : args.skill
    ? [args.skill]
    : [];
  await copySkills(args["copy-to"] as string, filter);
} else {
  await symlinkSkills();
}
