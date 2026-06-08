export interface Frontmatter {
  name?: string;
  description?: string;
  tags?: string[];
  args?: string;
}

export interface FrontmatterSyntaxFailure {
  line: number;
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

function frontmatterLines(content: string): string[] | null {
  const match = content.match(/^---\n([\s\S]*?)\n---/);
  return match ? match[1].split("\n") : null;
}

export function parseFrontmatter(content: string): Frontmatter | null {
  const lines = frontmatterLines(content);
  if (!lines) return null;

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

export function findFrontmatterSyntaxFailures(
  content: string,
): FrontmatterSyntaxFailure[] {
  const lines = frontmatterLines(content);
  if (!lines) return [];

  const failures: FrontmatterSyntaxFailure[] = [];
  for (let index = 0; index < lines.length; index++) {
    const line = lines[index];
    const pair = line.match(/^([a-z]+):\s*(.*)$/);
    if (!pair) continue;

    const rawValue = pair[2].trim();
    const isQuoted = (rawValue.startsWith('"') && rawValue.endsWith('"')) ||
      (rawValue.startsWith("'") && rawValue.endsWith("'"));
    if (rawValue && rawValue !== ">" && !isQuoted && /:\s/.test(rawValue)) {
      failures.push({
        line: index + 2,
        message:
          "unquoted YAML scalar contains ': '; quote it or use folded block syntax",
      });
    }
  }

  return failures;
}
