---
name: py4e-extract
description: Copy one section of a Python for Everybody chapter into my-content as the start of a course chapter, with license attribution. Use when the user wants to reuse or adapt part of a py4e chapter.
argument-hint: <chapter> "<heading>" [my-content/chapters/<slug>.qmd]
allowed-tools: Bash(python3 yr-materials/tools/extract_section.py:*), Bash(python3 yr-materials/tools/outline.py:*)
---

Arguments: chapter number, a section heading (case-insensitive, backticks
ignored), and optionally an output path under `yr-materials/`.

1. If the heading is uncertain, run `python3 yr-materials/tools/outline.py <chapter>` to list headings.
2. Run from the repo root:

       python3 yr-materials/tools/extract_section.py <chapter> "<heading>" --out <path>

   Omit `--out` only if the user wants the text shown rather than saved.
3. If a file was written, remind the user to add it to `_quarto.yml` (or use
   `/py4e-new-chapter` first and paste into that file), and that any
   `images/...` references need the image copied from `py4e-quarto/images/`.

Do not read the source chapter or the output file back; the script already
reports what it wrote.
