#!/usr/bin/env python3
"""
Copy one section (heading through to the next heading of the same or higher
level) out of a converted py4e chapter, ready to paste or save as our own file.

    python3 yr-materials/tools/extract_section.py 05 "The while statement"
    python3 yr-materials/tools/extract_section.py 05 "The while statement" \
            --out my-content/chapters/while-loops.qmd

Heading matching is case-insensitive and ignores backticks, so "the while
statement" matches "## The `while` statement". Without --out the section is
printed to stdout. With --out a file is written with an attribution comment
(and the heading promoted to level 1 so it can be its own chapter).
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from outline import resolve, YR  # noqa: E402

ATTRIB = (
    "<!-- Adapted from \"Python for Everybody\" by Charles R. Severance\n"
    "     (https://www.py4e.com/), chapter source book3/{src}.mkd,\n"
    "     CC BY-NC-SA 3.0 (https://creativecommons.org/licenses/by-nc-sa/3.0/).\n"
    "     Edited for this course. -->\n"
)


def norm(s):
    return re.sub(r"[`*_]", "", s).strip().lower()


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    out = None
    if "--out" in sys.argv:
        out = sys.argv[sys.argv.index("--out") + 1]
        args = [a for a in args if a != out]
    if len(args) != 2:
        sys.exit(__doc__)
    path = resolve(args[0])
    want = norm(args[1])
    lines = open(path, encoding="utf-8").read().splitlines()

    in_fence = False
    start = level = None
    end = len(lines)
    for i, line in enumerate(lines):
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = re.match(r"^(#{1,4}) (.*)", line)
        if not m:
            continue
        if start is None:
            if norm(m.group(2)) == want:
                start, level = i, len(m.group(1))
        elif len(m.group(1)) <= level:
            end = i
            break
    if start is None:
        sys.exit(f"heading '{args[1]}' not found in {os.path.relpath(path, YR)}; "
                 f"run outline.py to list headings")

    section = lines[start:end]
    while section and not section[-1].strip():
        section.pop()
    body = "\n".join(section) + "\n"

    if out:
        shift = level - 1
        if shift:
            body = re.sub(r"^(#{1,4}) ", lambda m: "#" * max(1, len(m.group(1)) - shift) + " ",
                          body, flags=re.M)
        src = os.path.basename(path).replace(".qmd", "")
        out_path = out if os.path.isabs(out) else os.path.join(YR, out)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as fh:
            fh.write(ATTRIB.format(src=src) + "\n" + body)
        print(f"wrote {os.path.relpath(out_path, YR)} ({len(section)} lines). "
              f"Images are referenced as images/...; copy from py4e-quarto/images if needed.")
    else:
        sys.stdout.write(body)


if __name__ == "__main__":
    main()
