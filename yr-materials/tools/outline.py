#!/usr/bin/env python3
"""
Print a compact outline of a converted py4e chapter (or one of our own),
without dumping its full text.

    python3 yr-materials/tools/outline.py 05
    python3 yr-materials/tools/outline.py my-content/chapters/invoices.qmd

Shows: headings with line numbers, number of code blocks, the upstream code
files inlined (# Code: ... lines), exercises, word count.
"""
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
YR = os.path.abspath(os.path.join(HERE, ".."))


def resolve(arg):
    if os.path.exists(arg):
        return arg
    hits = glob.glob(os.path.join(YR, "py4e-quarto", f"{arg}*.qmd"))
    if len(hits) == 1:
        return hits[0]
    sys.exit(f"cannot resolve chapter '{arg}' (matches: {[os.path.basename(h) for h in hits]})")


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    path = resolve(sys.argv[1])
    lines = open(path, encoding="utf-8").read().splitlines()
    in_fence = False
    fences = 0
    headings, code_files, exercises = [], [], []
    words = 0
    for n, line in enumerate(lines, 1):
        if line.startswith("```"):
            if not in_fence:
                fences += 1
            in_fence = not in_fence
            continue
        if in_fence:
            m = re.match(r"# Code: .*/([^/\s]+)$", line)
            if m:
                code_files.append(m.group(1))
            continue
        m = re.match(r"^(#{1,4}) (.*)", line)
        if m:
            headings.append((n, len(m.group(1)), m.group(2)))
        m = re.match(r"\*\*Exercise (\d+):\*\*\s*(.*)", line)
        if m:
            exercises.append((n, m.group(1), m.group(2)[:70]))
        words += len(line.split())

    print(f"{os.path.relpath(path, YR)}  ({len(lines)} lines, ~{words} words, {fences} code blocks)")
    print("\nHeadings (line: title):")
    for n, level, title in headings:
        print(f"  {n:5d}: {'  ' * (level - 1)}{title}")
    if code_files:
        print("\nUpstream code files inlined:", ", ".join(code_files))
    if exercises:
        print("\nExercises:")
        for n, num, text in exercises:
            print(f"  {n:5d}: Exercise {num}: {text}...")


if __name__ == "__main__":
    main()
