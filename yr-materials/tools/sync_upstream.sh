#!/usr/bin/env bash
# Pull Dr. Chuck's latest changes, regenerate the converted chapters, and
# print a short summary of what changed. Does NOT push.
set -euo pipefail
cd "$(dirname "$0")/../.."          # repo root

if [ -n "$(git status --porcelain)" ]; then
  echo "Working tree not clean; commit or stash first." >&2
  git status --short | head -20 >&2
  exit 1
fi

before=$(git rev-parse HEAD)
git fetch -q upstream
git merge -q --no-edit upstream/master
after=$(git rev-parse HEAD)

if [ "$before" = "$after" ]; then
  echo "Already up to date with upstream/master."
  exit 0
fi

echo "Merged upstream: $(git rev-list --count "$before".."$after") new commit(s)."
echo
echo "Upstream files changed (top-level summary):"
git diff --stat "$before" "$after" -- book3 code3 images | tail -1
git diff --name-only "$before" "$after" -- book3/*.mkd code3 images | sed 's/^/  /' | head -30

python3 yr-materials/tools/mkd2qmd.py >/dev/null
changed=$(git status --porcelain yr-materials/py4e-quarto | wc -l)
echo
if [ "$changed" -eq 0 ]; then
  echo "Regenerated chapters: no differences."
else
  echo "Regenerated chapters with differences ($changed files):"
  git status --porcelain yr-materials/py4e-quarto | sed 's/^/  /'
  echo
  echo "Review with: git diff yr-materials/py4e-quarto"
  echo "Then:        git add -A yr-materials && git commit -m 'Regenerate chapters after upstream sync' && git push origin master"
fi
