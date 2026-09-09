---
name: py4e-outline
description: Show the headings, code files, and exercises of a Python for Everybody chapter without reading the whole file. Use before deciding what to reuse from a chapter.
argument-hint: <chapter number or path, e.g. 05>
allowed-tools: Bash(python3 yr-materials/tools/outline.py:*)
---

Run, from the repo root:

    python3 yr-materials/tools/outline.py $ARGUMENTS

Report the outline as printed. Do not open the chapter file itself unless the
user asks about a specific section; then read only the line range the outline
gives for that section (Read with offset/limit).
