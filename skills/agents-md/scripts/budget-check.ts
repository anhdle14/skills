#!/usr/bin/env -S deno run --allow-read

import { parseArgs } from "@std/cli/parse-args";
import { basename } from "@std/path";

const SOFT_CAP = 80;
const HARD_CAP = 120;
const LONG_LINE = 100;
const CAPPED_FILES = new Set(["SKILL.md", "AGENTS.md", "CLAUDE.md"]);

interface Report {
  path: string;
  lines: number;
  status: "OK" | "WARN" | "FAIL";
  longest: { lineNo: number; len: number; text: string }[];
}

async function readInput(path: string | undefined): Promise<string> {
  if (path && path !== "-") return await Deno.readTextFile(path);
  const bytes = await new Response(Deno.stdin.readable).bytes();
  return new TextDecoder().decode(bytes);
}

function analyze(path: string, content: string): Report {
  const rawLines = content.split("\n");
  const lines = rawLines.length;
  const capped = path === "<stdin>" || CAPPED_FILES.has(basename(path));
  const status = !capped
    ? "OK"
    : lines > HARD_CAP
    ? "FAIL"
    : lines > SOFT_CAP
    ? "WARN"
    : "OK";
  const longest = rawLines
    .map((text, i) => ({ lineNo: i + 1, len: text.length, text }))
    .filter((l) => l.len > LONG_LINE)
    .sort((a, b) => b.len - a.len)
    .slice(0, 5);
  return { path, lines, status, longest };
}

const flags = parseArgs(Deno.args, { string: ["_"] });
const path = flags._[0]?.toString();
const content = await readInput(path);
const report = analyze(path ?? "<stdin>", content);

console.log(`${report.status}: ${report.path} — ${report.lines} lines (soft ${SOFT_CAP}, hard ${HARD_CAP})`);
if (report.status !== "OK") {
  console.log("Trim candidates (longest lines):");
  for (const l of report.longest) {
    console.log(`  L${l.lineNo} (${l.len} chars): ${l.text.slice(0, 60)}…`);
  }
}

if (report.status === "FAIL") Deno.exit(1);
