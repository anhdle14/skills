#!/usr/bin/env bash
# Mechanical style checks for technical docs, from Google's Technical Writing
# course rules that a regex can decide. Judgment calls stay in REFERENCE.md.
#
# Usage: bash prose-check.sh <file.md> [more.md ...]
# Exit 1 if any check fires, 0 if clean.

set -uo pipefail

if [ "$#" -eq 0 ]; then
  echo "usage: prose-check.sh <file.md> [more.md ...]" >&2
  exit 2
fi

command -v rg >/dev/null || { echo "prose-check.sh requires ripgrep (rg)" >&2; exit 2; }

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT
hits=0

# Blank out lines inside fenced code blocks (mode=prose) or outside them
# (mode=code), preserving line numbers so reported lines match the source.
strip() {
  awk -v mode="$1" '
    /^[[:space:]]*(```|~~~)/ { fence = !fence; print ""; next }
    { print (fence == (mode == "code")) ? $0 : "" }
  ' "$2"
}

check() {
  local label="$1" pattern="$2" file="$3" flags="${4:--i}"
  local out
  out="$(rg -n $flags -e "$pattern" "$file" 2>/dev/null)" || return 0
  # shellcheck disable=SC2086
  [ -n "$out" ] || return 0
  printf '%s\n' "$out" | while IFS=: read -r line text; do
    printf '%s:%s: [%s] %s\n' "$SRC" "$line" "$label" "$(printf '%s' "$text" | sed 's/^[[:space:]]*//' | cut -c1-100)"
  done
  hits=1
}

for SRC in "$@"; do
  [ -f "$SRC" ] || { echo "prose-check.sh: no such file: $SRC" >&2; exit 2; }
  prose="$tmp/prose"; code="$tmp/code"
  strip prose "$SRC" > "$prose"
  strip code "$SRC" > "$code"

  before=$hits

  check passive-voice '(^|[^[:alnum:]])(is|are|was|were|be|been|being) [a-z]+(ed|en)([^[:alnum:]]|$)' "$prose"
  check ambiguous-pronoun '(^|\. )(This|That|These|Those|It) (is|are|was|were|will|can|does|lets|means|allows|provides|indicates|happens|helps)' "$prose" '-s'
  check filler '(^|[^[:alnum:]])(in order to|in spite of the fact that|due to the fact that|at this point in time|for the purpose of|in the event that|is able to|are able to|utiliz(e|es|ing)|prior to|subsequent to)([^[:alnum:]]|$)' "$prose"
  check allows-you-to '(^|[^[:alnum:]])allows? (you|users?|the user) to([^[:alnum:]]|$)' "$prose"
  check weak-requirement '(^|[^[:alnum:]])should([^[:alnum:]]|$)' "$prose"
  check latin-abbreviation '(^|[^[:alnum:]])(e\.g\.|i\.e\.|N\.B\.|etc\.)' "$prose"
  check please '(^|[^[:alnum:]])please([^[:alnum:]]|$)' "$prose"
  check expletive-opening '(^|\. )There (is|are|was|were) ' "$prose" '-s'
  check anthropomorphism '(the )?(server|service|system|API|model|database) (thinks|knows|wants|believes|decides|feels)' "$prose"
  check undescriptive-link '(click here|read (this|more) here|\[here\]\()' "$prose"
  check en-or-em-dash '(–|—)' "$prose"
  check placeholder-name '(^|[^[:alnum:]])(foo|bar|baz|qux|foobar|mything|test123)([^[:alnum:]]|$)' "$code"

  # Structural checks: sentence length, list/table lead-ins, list parallelism,
  # heading overview paragraphs, scope statement, unverified markers.
  awk -v src="$SRC" '
    function flag(line, label, msg) { printf "%s:%d: [%s] %s\n", src, line, label, msg; fired = 1 }

    /^[[:space:]]*(```|~~~)/ { fence = !fence; next }
    fence { next }

    {
      line = $0
      is_item  = (line ~ /^[[:space:]]*([-*+] |[0-9]+\. )/)
      is_table = (line ~ /^[[:space:]]*\|/)
      is_head  = (line ~ /^#+ /)
      blank    = (line ~ /^[[:space:]]*$/)
    }

    (is_item || is_table) && !in_block {
      in_block = 1
      if (prev_head_adjacent)
        flag(NR, "no-overview-paragraph", "heading is followed directly by a list or table; add an overview paragraph first")
      else if (prev_text !~ /:[[:space:]]*$/)
        flag(NR, "unintroduced-list", "introduce the list or table with a sentence ending in a colon")
      first_item_dot = -1
      first_item_cap = -1
    }

    is_item && in_block {
      item = line
      sub(/^[[:space:]]*([-*+]|[0-9]+\.)[[:space:]]*/, "", item)
      gsub(/[*`_]/, "", item)
      if (item != "") {
        dot = (item ~ /[.!?]$/) ? 1 : 0
        cap = (item ~ /^[A-Z]/) ? 1 : 0
        if (first_item_dot == -1) { first_item_dot = dot; first_item_cap = cap }
        else {
          if (dot != first_item_dot)
            flag(NR, "nonparallel-list", "list items mix terminal punctuation with earlier items")
          if (cap != first_item_cap)
            flag(NR, "nonparallel-list", "list items mix capitalization with earlier items")
        }
      }
    }

    blank && in_block { in_block = 0 }
    !is_item && !is_table && !blank { in_block = 0 }

    !blank && !is_item && !is_table && !is_head {
      n = split(line, sentences, /[.!?] +/)
      for (i = 1; i <= n; i++) {
        words = split(sentences[i], w, /[[:space:]]+/)
        if (words > 30) flag(NR, "long-sentence", "sentence runs " words " words; split it or convert it to a list")
      }
    }

    tolower($0) ~ /this (document|page|guide|runbook|readme|reference) (describes|covers|explains|documents|shows)/ { scope = 1 }
    /TODO\(unverified\)/ { todo++ }

    { prev_head_adjacent = is_head || (blank && prev_head_adjacent); if (!blank) prev_text = line }

    END {
      if (!scope) flag(1, "no-scope-statement", "no scope statement found (\"This document describes ...\")")
      if (todo) printf "%s: [info] %d TODO(unverified) marker(s) left in the draft\n", src, todo
      exit fired ? 1 : 0
    }
  ' "$SRC" || hits=1

  [ "$hits" != "$before" ] || echo "$SRC: clean"
done

exit $hits
