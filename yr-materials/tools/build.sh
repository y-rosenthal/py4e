#!/usr/bin/env bash
# Regenerate converted chapters, run sanity checks, render the book.
# Usage: tools/build.sh [--no-render]
set -euo pipefail
cd "$(dirname "$0")/.."             # yr-materials

python3 tools/mkd2qmd.py >/dev/null
echo "Regenerated $(ls py4e-quarto/*.qmd | wc -l) chapters."

problems=0
for f in py4e-quarto/*.qmd my-content/chapters/*.qmd; do
  [ -e "$f" ] || continue
  n=$(grep -c '^```' "$f" || true)
  if [ $((n % 2)) -eq 1 ]; then echo "UNBALANCED code fences: $f"; problems=1; fi
  h1=$(awk 'BEGIN{f=0} /^```/{f=!f; next} !f && /^# /{c++} END{print c+0}' "$f")
  if [ "$h1" -ne 1 ]; then echo "Expected 1 level-1 heading, found $h1: $f"; problems=1; fi
  if grep -qE '\\(index|VerbatimInput|begin|label|ref)\{' "$f"; then
    echo "Leftover LaTeX markup: $f"; problems=1
  fi
done
[ "$problems" -eq 0 ] && echo "Sanity checks passed."

if [ "${1:-}" != "--no-render" ]; then
  if quarto render >/tmp/quarto-render.log 2>&1; then
    echo "Rendered: $(find _book -name "*.html" | wc -l) pages -> $(pwd)/_book/index.html"
  else
    echo "quarto render FAILED; last lines of log:"; tail -20 /tmp/quarto-render.log; exit 1
  fi
fi
exit $problems
