# Contributing

Edits and contributions to the [main table](README.md#table) are welcome.

## Quickstart (editing via GitHub UI)

1. Open [data/problems.yaml](data/problems.yaml).
2. Click **Edit** and add or modify an entry. Only the **number** field is mandatory; omit any field for which you have no information.
3. Open a Pull Request. Do not edit the table in README.md directly—any such edits will be overridden.

## Sample template

```yaml
- number: "1"
  prize: "no"
  status:
    state: "open"
    last_update: "2025-02-26"
  comments: ""
  tags: ["convex optimization", "complexity"]
```

## Field definitions

- **number**: Problem ID (string). Unique identifier for the problem.
- **prize**: "no" if no prize, or the currency amount (string).
- **status**: Logical status as of **last_update**:
  - "proved": Solved in the affirmative
  - "disproved": Solved in the negative
  - "solved": Resolved in some other fashion
  - "falsifiable": Open, but can be disproven by a finite counterexample if false
  - "verifiable": Open, but can be proven by a finite computation if true
  - "decidable": Both falsifiable and verifiable, not yet solved
  - "open": Completely open
- **comments**: Miscellaneous notes, alternative names, etc.
- **tags**: List of strings (e.g., "convex optimization", "nonsmooth", "complexity", "variational analysis").

## Problem pages with LaTeX

- Each problem can have a webpage at `docs/problems/<number>.html`.
- Problem numbers in the tables can link to these pages (for example, `problems/1.html` on GitHub Pages).
- LaTeX is supported via MathJax on these pages.
- To create a new page, copy `docs/problems/template.html` to `docs/problems/<number>.html` and edit:
  - Problem title and status/tags line
  - Problem statement
  - References
  - Notes
