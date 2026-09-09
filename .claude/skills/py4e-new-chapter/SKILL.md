---
name: py4e-new-chapter
description: Scaffold a new course-written chapter in my-content/chapters and register it in the book's _quarto.yml.
argument-hint: <slug> "<Title>"
allowed-tools: Bash(python3 yr-materials/tools/new_chapter.py:*)
---

Run from the repo root:

    python3 yr-materials/tools/new_chapter.py $ARGUMENTS

The slug must be lowercase letters, digits, and hyphens. The chapter is added
at the end of the `my-content chapters` block in `yr-materials/_quarto.yml`;
tell the user to move that line if they want a different position.

When writing content into the new chapter, follow the audience note inside
the template: business-school students, business-flavoured examples, no
geometry or turtle-angle exercises.
