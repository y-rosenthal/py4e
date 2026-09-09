---
name: py4e-build
description: Regenerate the converted chapters, run sanity checks, and render the book with Quarto. Use after editing chapters or the converter.
argument-hint: [--no-render]
allowed-tools: Bash(bash yr-materials/tools/build.sh:*), Bash(xdg-open:*)
---

Run from the repo root:

    bash yr-materials/tools/build.sh $ARGUMENTS

Report the last lines only: chapter count, sanity-check result, and the
rendered page count or the error tail. If the user asks to see it, open
`yr-materials/_book/index.html` with `xdg-open`, or suggest
`cd yr-materials && quarto preview` for live reload.
