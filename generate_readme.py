#!/usr/bin/env python3

import json
from collections import defaultdict
from pathlib import Path

DATA_FILE = Path(__file__).parent / "articles.json"
README_FILE = Path(__file__).parent / "README.md"

HEADER = """# Tech Articles

A categorized index of my technical writing on Twitter/X: system design (HLD/LLD), backend engineering, distributed systems, databases, and DevOps.

Each entry links straight to the original thread.

"""

FOOTER = """
---

### Adding a new article

1. Add an entry to `articles.json`:
```json
{
  "title": "...",
  "url": "https://twitter.com/...",
  "category": "HLD",
  "date": "YYYY-MM-DD",
  "description": "One line on what it covers."
}
```
2. Run `python3 generate_readme.py`
3. Commit both files.
"""


def main():
    data = json.loads(DATA_FILE.read_text())
    categories = data["categories"]
    articles = data["articles"]

    by_category = defaultdict(list)
    for a in articles:
        by_category[a["category"]].append(a)

    for cat_articles in by_category.values():
        cat_articles.sort(key=lambda a: a["date"], reverse=True)

    lines = [HEADER]

    # Table of contents
    lines.append("## Contents\n")
    for cat in categories:
        if by_category.get(cat):
            anchor = cat.lower().replace(" ", "-")
            lines.append(f"- [{cat}](#{anchor}) ({len(by_category[cat])})")
    lines.append("")

    for cat in categories:
        cat_articles = by_category.get(cat)
        if not cat_articles:
            continue
        lines.append(f"## {cat}\n")
        lines.append("| Article | Description | Date |")
        lines.append("|---|---|---|")
        for a in cat_articles:
            lines.append(
                f"| [{a['title']}]({a['url']}) | {a['description']} | {a['date']} |"
            )
        lines.append("")

    lines.append(FOOTER)

    README_FILE.write_text("\n".join(lines))
    print(f"Wrote {README_FILE} with {len(articles)} articles across {len(by_category)} categories.")


if __name__ == "__main__":
    main()
