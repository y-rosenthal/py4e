# Repo notes for Claude

Fork of csev/py4e (Python for Everybody). Upstream layout is untouched; all
course-specific work lives in `yr-materials/`. Full editor documentation:
`yr-materials/for-editors.qmd`.

- Never edit upstream files (`book3/`, `code3/`, ...) or the generated
  `yr-materials/py4e-quarto/*.qmd`; copy into `yr-materials/my-content/` instead.
- Chapters are long (500+ lines). Use `/py4e-outline <nn>` before reading one,
  then read only the needed line range.
- Skills: `/py4e-outline`, `/py4e-extract`, `/py4e-new-chapter`,
  `/py4e-build`, `/py4e-sync`. They wrap scripts in `yr-materials/tools/`.
- Student-facing text must not mention "Quarto", "generated", or the repo.
  Editor-facing text goes in `for-editors.qmd`.
- Audience: business-school intro course. Examples about sales, invoices,
  customers, budgets. No geometry or turtle-angle exercises.
- Remotes: `origin` = y-rosenthal/py4e (push), `upstream` = csev/py4e (pull).
