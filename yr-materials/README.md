# yr-materials

Everything specific to this edition of *Python for Everybody* lives in this
folder; the rest of the repository is an unmodified fork of
<https://github.com/csev/py4e>.

Full documentation for editors and instructors (layout, build, upstream sync,
license, course design notes) is in [`for-editors.qmd`](for-editors.qmd),
which also renders as the last appendix of the book.

Quick start:

```bash
cd yr-materials
python3 tools/mkd2qmd.py     # regenerate chapters from upstream book3/
quarto preview               # view the book locally
```
