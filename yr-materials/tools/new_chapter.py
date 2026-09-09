#!/usr/bin/env python3
"""
Scaffold a new chapter of our own and register it in the book.

    python3 yr-materials/tools/new_chapter.py invoices "Working with invoice data"

Creates my-content/chapters/<slug>.qmd and inserts it into _quarto.yml between
the '# --- my-content chapters' markers. Reorder the line by hand if needed.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
YR = os.path.abspath(os.path.join(HERE, ".."))
TEMPLATE = """<!-- Original material for this course. CC BY-NC-SA 4.0. -->

# {title}

<!-- Audience: business-school students in an intro Python course.
     Prefer examples about sales, invoices, customers, budgets, spreadsheets.
     Avoid geometry / turtle-angle / number-theory examples. -->

## Introduction

## Worked example

```python
```

## Exercises

**Exercise 1:** 
"""


def main():
    if len(sys.argv) != 3 or not re.fullmatch(r"[a-z0-9][a-z0-9-]*", sys.argv[1]):
        sys.exit(__doc__)
    slug, title = sys.argv[1], sys.argv[2]
    rel = f"my-content/chapters/{slug}.qmd"
    path = os.path.join(YR, rel)
    if os.path.exists(path):
        sys.exit(f"{rel} already exists")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(TEMPLATE.format(title=title))

    qy = os.path.join(YR, "_quarto.yml")
    text = open(qy, encoding="utf-8").read()
    marker = "    # --- end my-content chapters ---"
    if marker not in text:
        sys.exit(f"wrote {rel}, but marker not found in _quarto.yml; add it by hand")
    text = text.replace(marker, f"    - {rel}\n{marker}")
    open(qy, "w", encoding="utf-8").write(text)
    print(f"wrote {rel} and added it to _quarto.yml")


if __name__ == "__main__":
    main()
