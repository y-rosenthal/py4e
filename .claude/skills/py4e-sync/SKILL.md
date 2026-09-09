---
name: py4e-sync
description: Merge the latest changes from Dr. Chuck's upstream py4e repository and regenerate the converted chapters. Reports what changed; does not push.
disable-model-invocation: true
allowed-tools: Bash(bash yr-materials/tools/sync_upstream.sh), Bash(git diff --stat:*), Bash(git status:*)
---

Run from the repo root:

    bash yr-materials/tools/sync_upstream.sh

Relay the script's summary. If it reports regenerated chapters with
differences, show `git diff --stat yr-materials/py4e-quarto` and ask whether
to commit and push; do not push without confirmation. If the working tree was
not clean, tell the user what is uncommitted and stop.
