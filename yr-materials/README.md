# yr-materials

Everything in this folder is *mine* (Yitz Rosenthal); the rest of the repo is
an unmodified fork of <https://github.com/csev/py4e> (Python for Everybody,
by Charles Severance). Keeping my work in one folder means I can pull
upstream updates at any time without merge conflicts.

## Layout

| Path | What it is |
|------|------------|
| `tools/mkd2qmd.py` | Converts `book3/*.mkd` (Pandoc markdown + LaTeX macros) into clean Quarto `.qmd` |
| `py4e-quarto/` | Generated Quarto book: one `.qmd` per chapter, images copied in, `_quarto.yml` |
| `my-content/` | My own chapters, notebooks, exercises |

## Where the reusable py4e content lives in the upstream repo

| Upstream path | Contents |
|---------------|----------|
| `book3/*.mkd` | The book text, one file per chapter (the master source) |
| `code3/` | Every example program and data file referenced by the book |
| `images/`, `book3/figs2/` | Figures (svg/png/eps) |
| `html3/` | Pre-built HTML of each chapter, if you just want to read |
| `lectures3/` | Lecture slides (pptx/pdf) |
| `assn/` | Assignment descriptions |
| `lessons.json` | Mapping of chapters to videos/assignments used by py4e.com |

## Daily workflow

```bash
# refresh the converted Quarto chapters
python3 yr-materials/tools/mkd2qmd.py            # all chapters
python3 yr-materials/tools/mkd2qmd.py 04 05      # just some

# preview / build the Quarto edition of the book
cd yr-materials/py4e-quarto && quarto preview    # or: quarto render

# pull updates from Dr. Chuck's repo
git fetch upstream
git merge upstream/master
python3 yr-materials/tools/mkd2qmd.py            # regenerate after upstream edits

# save my work to my fork on GitHub
git push origin master
```

## Copy/paste into another book or site

The `.qmd` files in `py4e-quarto/` are plain Quarto/Pandoc markdown with
standard triple-backtick code fences and ATX (`#`) headings, so any section
can be copied straight into another Quarto project, a Jupyter Book, a Hugo
or MkDocs site, or a notebook markdown cell. Referenced images are in
`py4e-quarto/images/`; copy those alongside.

## License reminder

The book is CC BY-NC-SA 3.0. Reuse and remix is fine for teaching as long as
the result (a) credits Charles Severance / py4e.com, (b) is non-commercial
or fits the in-advance permissions in the *Copyright Detail* appendix, and
(c) is shared under the same license. Each generated `.qmd` carries an
attribution comment at the top; keep it (or an equivalent note) in anything
you publish.
