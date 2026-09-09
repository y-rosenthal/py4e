#!/usr/bin/env python3
"""
Convert the Python for Everybody book chapters (book3/*.mkd, Pandoc markdown
with LaTeX-isms) into clean Quarto markdown (.qmd) that can be rendered as a
Quarto book or copy/pasted into other material.

Usage (from the repo root):
    python3 yr-materials/tools/mkd2qmd.py            # convert all chapters
    python3 yr-materials/tools/mkd2qmd.py 05 06      # only chapters 05 and 06

What it does:
  * strips \\index{...} entries
  * converts `~~~~ {.python .trinket}` fences to ```python fences
  * inlines \\VerbatimInput{../code3/foo.py} as a ```python block and adds a
    comment with the URL of the original file on py4e.com
  * replaces \\begin{trinketfiles}...\\end{trinketfiles} with a note that lists
    the data files the example needs (links to py4e.com)
  * converts figures `![Cap](height=1.5in@../images/foo)` into
    `![Cap](images/foo.svg){height=1.5in}` and copies the image file
  * turns figure \\label{x} / \\ref{x} into Quarto cross references (@fig-x)
  * converts setext headings (===== / -----) to ATX headings (# / ##)
  * drops leftover LaTeX page commands
  * adds an HTML comment with source + license attribution at the top
"""
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
BOOK3 = os.path.join(REPO, "book3")
OUT = os.path.join(REPO, "yr-materials", "py4e-quarto")
OUT_IMAGES = os.path.join(OUT, "images")
PY4E_CODE_URL = "https://www.py4e.com/code3/"

CHAPTERS = [
    "A0-preface", "01-intro", "02-variables", "03-conditional", "04-functions",
    "05-iterations", "06-strings", "07-files", "08-lists", "09-dictionaries",
    "10-tuples", "11-regex", "12-network", "13-web", "14-objects",
    "15-database", "16-viz", "AA-contrib", "AB-copyright",
]

FENCE_OPEN = re.compile(r"^~~~~\s*(\{(?P<attrs>[^}]*)\})?\s*$")
INDEX_RE = re.compile(r"\\index\{[^}]*\}")
VERBATIM_RE = re.compile(r"^\\VerbatimInput\{([^}]*)\}\s*$")
FIGURE_RE = re.compile(r"^!\[(?P<cap>.*)\]\((?:(?P<attrs>[^@)]*)@)?(?P<path>[^)]*)\)\s*$")
LABEL_RE = re.compile(r"\\label\{([^}]*)\}")
REF_RE = re.compile(r"Figure\s+\\ref\{([^}]*)\}")
DROP_RE = re.compile(r"^\\(thispagestyle|cleardoublepage|newpage)")

LANG_MAP = {"python": "python", "bash": "bash", "sql": "sql", "html": "html",
            "js": "javascript", "json": "json", "xml": "xml"}


def fence_lang(attrs):
    """Map pandoc fence attributes like '.python .trinket height="120"' to a language."""
    if not attrs:
        return ""
    for token in attrs.split():
        if token.startswith("."):
            lang = token[1:]
            if lang in LANG_MAP:
                return LANG_MAP[lang]
    return ""


def resolve_image(rel_path):
    """book3-relative path without extension -> (abs source path, basename with ext)."""
    base = os.path.normpath(os.path.join(BOOK3, rel_path))
    for ext in (".svg", ".png", ".jpg"):
        if os.path.exists(base + ext):
            return base + ext, os.path.basename(base) + ext
    return None, os.path.basename(base)


def verbatim_block(rel_path):
    src = os.path.normpath(os.path.join(BOOK3, rel_path))
    name = os.path.basename(src)
    lang = "python" if name.endswith(".py") else ""
    out = ["```" + lang]
    try:
        with open(src, encoding="utf-8") as fh:
            body = fh.read().rstrip("\n")
        out.append(body)
    except OSError:
        out.append(f"# (could not read {rel_path})")
    out.append("")
    out.append(f"# Code: {PY4E_CODE_URL}{name}")
    out.append("```")
    return out


def convert_lines(lines):
    out = []
    in_fence = False
    in_trinketfiles = False
    trinket_files = []
    prev = ""  # previous *output* line, used for setext headings

    def emit(line):
        nonlocal prev
        out.append(line)
        prev = line

    i = 0
    while i < len(lines):
        raw = lines[i].rstrip("\n")
        i += 1

        # ---- inside a code fence: only look for the closing fence ----
        if in_fence:
            if raw.strip() == "~~~~":
                in_fence = False
                emit("```")
            else:
                emit(raw)
            continue

        # ---- trinketfiles block ----
        if raw.strip() == r"\begin{trinketfiles}":
            in_trinketfiles = True
            trinket_files = []
            continue
        if in_trinketfiles:
            if raw.strip() == r"\end{trinketfiles}":
                in_trinketfiles = False
                links = ", ".join(
                    f"[{os.path.basename(f)}]({PY4E_CODE_URL}{os.path.basename(f)})"
                    for f in trinket_files)
                emit("")
                emit(f"::: {{.callout-note collapse=\"false\"}}")
                emit(f"Data file(s) used by this example: {links}")
                emit(":::")
                emit("")
            elif raw.strip():
                trinket_files.append(raw.strip())
            continue

        # ---- opening code fence ----
        m = FENCE_OPEN.match(raw)
        if m:
            in_fence = True
            emit("```" + fence_lang(m.group("attrs")))
            continue

        # ---- \VerbatimInput ----
        m = VERBATIM_RE.match(raw)
        if m:
            for l in verbatim_block(m.group(1)):
                emit(l)
            continue

        # ---- drop LaTeX page commands ----
        if DROP_RE.match(raw):
            continue

        # ---- figures ----
        m = FIGURE_RE.match(raw)
        if m and "/" in m.group("path"):
            cap = m.group("cap")
            fig_id = ""
            lm = LABEL_RE.search(cap)
            if lm:
                fig_id = lm.group(1)
                cap = LABEL_RE.sub("", cap).strip()
            attrs = {}
            for piece in (m.group("attrs") or "").split(","):
                if "=" in piece:
                    k, v = piece.split("=", 1)
                    attrs[k.strip()] = v.strip()
            src, fname = resolve_image(m.group("path"))
            if src:
                os.makedirs(OUT_IMAGES, exist_ok=True)
                shutil.copy2(src, os.path.join(OUT_IMAGES, fname))
            attr_parts = []
            if fig_id:
                attr_parts.append(f"#fig-{fig_id}")
            if "height" in attrs:
                attr_parts.append(f"height={attrs['height']}")
            attr_str = "{" + " ".join(attr_parts) + "}" if attr_parts else ""
            emit(f"![{cap}](images/{fname}){attr_str}")
            continue

        # ---- setext headings -> ATX ----
        if re.fullmatch(r"=+", raw.strip()) and prev.strip():
            out[-1] = "# " + prev.strip()
            prev = out[-1]
            continue
        if re.fullmatch(r"-{3,}", raw.strip()) and prev.strip() and not prev.startswith("#"):
            out[-1] = "## " + prev.strip()
            prev = out[-1]
            continue

        # ---- inline cleanups ----
        line = INDEX_RE.sub("", raw)
        line = REF_RE.sub(lambda mm: f"@fig-{mm.group(1)}", line)
        # a line that was only \index{...} entries becomes blank; skip it
        if raw.strip() and not line.strip():
            continue
        emit(line)

    # collapse runs of blank lines
    cleaned = []
    for l in out:
        if l.strip() == "" and cleaned and cleaned[-1].strip() == "":
            continue
        cleaned.append(l)
    return cleaned


def convert_chapter(name):
    src = os.path.join(BOOK3, name + ".mkd")
    dst = os.path.join(OUT, name + ".qmd")
    with open(src, encoding="utf-8") as fh:
        lines = fh.readlines()
    body = convert_lines(lines)
    header = [
        f"<!-- Source: book3/{name}.mkd from https://github.com/csev/py4e",
        "     \"Python for Everybody\" by Charles Severance,",
        "     licensed CC BY-NC-SA 3.0 (https://creativecommons.org/licenses/by-nc-sa/3.0/).",
        "     Generated by yr-materials/tools/mkd2qmd.py -- edit the .mkd or the",
        "     converter, not this file, unless you intend to fork the chapter. -->",
        "",
    ]
    os.makedirs(OUT, exist_ok=True)
    with open(dst, "w", encoding="utf-8") as fh:
        fh.write("\n".join(header + body).rstrip("\n") + "\n")
    return dst


def main(argv):
    wanted = CHAPTERS
    if argv:
        wanted = [c for c in CHAPTERS if any(c.startswith(a) for a in argv)]
    for name in wanted:
        dst = convert_chapter(name)
        print("wrote", os.path.relpath(dst, REPO))


if __name__ == "__main__":
    main(sys.argv[1:])
