# {{REPOSITORY_NAME}} Repository Guidance

## Scope

This file applies repository-wide. More specific `AGENTS.md` files add or override
guidance for their directory subtrees.

## Start here

- Open [the repository context index](.agents/index.md) to choose only the topic needed
  for the current task. Do not read `.agents/` recursively.
- Open [the V-model index](.agents/v-model/index.md) when changing observable behavior,
  interfaces, acceptance criteria, or verification evidence.
- Read the closest nested `AGENTS.md` before editing within a code root or subsystem.

## Code roots

- `{{CODE_ROOT}}/` — {{CODE_ROOT_PURPOSE}}. Follow
  [`{{CODE_ROOT}}/AGENTS.md`]({{CODE_ROOT}}/AGENTS.md).

## Commands

- Setup: `{{SETUP_COMMAND}}`
- Focused check: `{{FOCUSED_CHECK_COMMAND}}`
- Full validation: `{{FULL_VALIDATION_COMMAND}}`

## Repository rules

- {{REPOSITORY_WIDE_RULE}}
- Preserve unrelated user changes and follow the repository’s worktree policy.
- Update canonical specification or context before changing a router that links to it.

## Handoff

Report changed behavior and documentation, checks run, unresolved specification or
evidence gaps, and checks not run.
