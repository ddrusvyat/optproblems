#!/usr/bin/env python3
"""Update README and docs index tables from data/problems.yaml.

This parser is intentionally lightweight and dependency-free. It supports the
current repository schema fields used by the public tables:
number, prize, status.state, comments, tags.
"""

from __future__ import annotations

from pathlib import Path
import re
from html import escape


ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "problems.yaml"
README_FILE = ROOT / "README.md"
DOCS_INDEX_FILE = ROOT / "docs" / "index.html"
TABLE_START = "<!-- TABLE:START -->"
TABLE_END = "<!-- TABLE:END -->"


def parse_inline_list(value: str) -> list[str]:
    value = value.strip()
    if not (value.startswith("[") and value.endswith("]")):
        return []
    inner = value[1:-1].strip()
    if not inner:
        return []
    items = []
    for raw in inner.split(","):
        s = raw.strip()
        if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
            s = s[1:-1]
        items.append(s)
    return items


def parse_problems_yaml(text: str) -> list[dict[str, str | list[str]]]:
    problems: list[dict[str, str | list[str]]] = []
    current: dict[str, str | list[str]] | None = None
    in_status = False

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        if stripped.startswith("- number:"):
            if current:
                problems.append(current)
            number = stripped.split(":", 1)[1].strip().strip('"').strip("'")
            current = {
                "number": number,
                "prize": "no",
                "status": "open",
                "comments": "",
                "tags": [],
            }
            in_status = False
            continue

        if current is None:
            continue

        if stripped.startswith("status:"):
            in_status = True
            continue

        if in_status and stripped.startswith("state:"):
            current["status"] = stripped.split(":", 1)[1].strip().strip('"').strip("'")
            continue

        # Leaving status block when a non-indented top-level key appears.
        if not line.startswith("    "):
            in_status = False

        if stripped.startswith("prize:"):
            current["prize"] = stripped.split(":", 1)[1].strip().strip('"').strip("'")
        elif stripped.startswith("comments:"):
            current["comments"] = stripped.split(":", 1)[1].strip().strip('"').strip("'")
        elif stripped.startswith("tags:"):
            current["tags"] = parse_inline_list(stripped.split(":", 1)[1].strip())

    if current:
        problems.append(current)
    return problems


def replace_between_markers(text: str, replacement: str) -> str:
    pattern = re.compile(
        rf"(^[ \t]*{re.escape(TABLE_START)}[ \t]*\n)([\s\S]*?)(\n[ \t]*{re.escape(TABLE_END)}[ \t]*$)",
        re.MULTILINE,
    )
    if not pattern.search(text):
        raise ValueError(f"Missing markers {TABLE_START} / {TABLE_END}")
    return pattern.sub(rf"\1{replacement}\3", text, count=1)


def render_markdown_table(problems: list[dict[str, str | list[str]]]) -> str:
    lines = [f"There are {len(problems)} problems in total.", ""]
    lines.append("| # | Prize | Status | Tags | Comments |")
    lines.append("|---|---|---|---|---|")
    for p in problems:
        number = str(p["number"])
        prize = str(p["prize"])
        status = str(p["status"])
        tags = ", ".join(p["tags"]) if isinstance(p["tags"], list) else ""
        comments = str(p["comments"])
        lines.append(
            f"| [{number}](https://ddrusvyat.github.io/optproblems/problems/{number}.html) "
            f"| {prize} | {status} | {tags} | {comments} |"
        )
    return "\n".join(lines)


def render_html_table(problems: list[dict[str, str | list[str]]]) -> str:
    lines = [f"<h2>Table</h2>", "<table>", "  <thead>", "    <tr>"]
    lines += [
        "      <th>#</th>",
        "      <th>Prize</th>",
        "      <th>Status</th>",
        "      <th>Tags</th>",
        "      <th>Comments</th>",
        "    </tr>",
        "  </thead>",
        "  <tbody>",
    ]
    for p in problems:
        number = escape(str(p["number"]))
        prize = escape(str(p["prize"]))
        status = escape(str(p["status"]))
        tags = escape(", ".join(p["tags"])) if isinstance(p["tags"], list) else ""
        comments = escape(str(p["comments"]))
        lines += [
            "    <tr>",
            f'      <td><a href="./problems/{number}.html">{number}</a></td>',
            f"      <td>{prize}</td>",
            f"      <td>{status}</td>",
            f"      <td>{tags}</td>",
            f"      <td>{comments}</td>",
            "    </tr>",
        ]
    lines += ["  </tbody>", "</table>", f'<p class="meta">There are {len(problems)} problems in total.</p>']
    return "\n".join(lines)


def main() -> None:
    problems = parse_problems_yaml(DATA_FILE.read_text(encoding="utf-8"))

    readme_text = README_FILE.read_text(encoding="utf-8")
    readme_table = render_markdown_table(problems)
    README_FILE.write_text(replace_between_markers(readme_text, readme_table), encoding="utf-8")

    docs_text = DOCS_INDEX_FILE.read_text(encoding="utf-8")
    docs_table = render_html_table(problems)
    DOCS_INDEX_FILE.write_text(replace_between_markers(docs_text, docs_table), encoding="utf-8")

    print(f"Updated tables for {len(problems)} problems.")


if __name__ == "__main__":
    main()
