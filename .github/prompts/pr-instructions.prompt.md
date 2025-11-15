---
agent: agent
---

Read the changes introduced on the current branch, including BOTH:

1. Uncommitted workspace modifications (staged and unstaged)
2. Committed changes that are on the current HEAD but not yet in the default upstream branch (e.g. `origin/main`)

Guidance:

- First, capture uncommitted diffs (equivalent of `git diff` and `git diff --cached`).
- Then, determine the merge base with the default branch (assume `origin/main` unless configured otherwise) using `git merge-base HEAD origin/main` and diff (`git diff <merge-base>...HEAD`) to include committed-but-unpushed work.

After understanding all of these changes:

- Check current branch with `git branch --show-current`. If on `main` or `master`, create a new branch with a descriptive name based on the changes (format: `feature/brief-desc` or `fix/brief-desc`) using `git checkout -b <branch-name>`.
- Read every instruction file under `.github/instructions` and assess whether any instruction is invalidated. If so, propose minimal, necessary wording updates. If no updates are needed, respond exactly with: `No updates needed`.
- If uncommitted changes exist, stage them (`git add .`), commit with a conventional message (`feat:`, `fix:`, `refactor:`, `docs:`, `chore:`), and push to origin (`git push -u origin <branch-name>`).
- After successful push, create a PR against the default branch with descriptive title and body. Provide the command: `gh pr create --base main --head <branch> --title "<title>" --body "<description>"`.

Be concise and conservative: only suggest changes that are absolutely necessary.