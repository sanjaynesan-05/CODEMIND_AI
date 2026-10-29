# Contributing and team workflow

## Branches

- `main` is the protected, releasable branch. Do not push feature work directly to it.
- Create a short-lived branch from the latest `main` for each change.
- Use `feature/<short-description>` for features, `fix/<short-description>` for bug fixes, and `docs/<short-description>` for documentation.
- Keep each branch focused. Rebase or merge the latest `main` before requesting final review when needed.

## Commits

- Use clear, imperative commit messages, such as `Add API health check` or `Fix runner timeout handling`.
- Keep unrelated changes in separate commits where practical.
- Never commit credentials, `.env`, local databases, generated build output, or learner submissions.

## Pull requests

1. Push your branch and open a pull request targeting `main`.
2. Explain the problem and solution, list notable implementation choices, and link related issues.
3. Include screenshots for user-interface changes and deployment/configuration notes where relevant.
4. Complete the pull request checklist and state the verification you performed. Do not claim tests passed unless they were run.
5. Wait for the required GitHub Actions checks to pass and request at least one review from another team member.
6. Resolve review comments and push updates. Re-request review when the change materially changes.
7. Merge only after required checks pass, at least one approving review is recorded, and there are no unresolved review threads. Prefer squash merge for focused changes.

## Required checks

The `CI` workflow runs frontend build and dependency audit, backend compile/import and dependency audit, and API/frontend container builds. Repository administrators should configure `main` branch protection to require the `frontend`, `backend`, and `containers` status checks, one approving review, dismissal of stale approvals, and conversation resolution. Block force pushes and branch deletion on `main`.

## Pull request checklist

- [ ] Change is scoped and documented.
- [ ] Relevant frontend/backend checks were run, or limitations are stated.
- [ ] No secrets or generated local data are included.
- [ ] UI changes include screenshots when appropriate.
- [ ] Deployment/configuration impact is described.
- [ ] CI passes and review feedback is addressed.
