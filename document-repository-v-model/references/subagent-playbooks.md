# Subagent Playbooks

Use this reference only when the environment and repository instructions permit
delegation. Keep one coordinator responsible for developer intent, shared contracts,
integration, durable docs, and V-model deletion.

## Isolation

- Give each agent a concrete, bounded lane with explicit inputs, outputs, dependencies,
  and verification.
- Provide the skill path, repository path, pinned commit, and a normal user-style task.
- Use a separate worktree or disposable clone per writing agent. Never share a worktree.
- For discovery and evaluation, prohibit source changes and pushes.
- Require exact file, symbol, and test anchors with confidence and conflicts.
- Keep one concurrency slot for the coordinator.

## Initial implementation swarm

Do not delegate implementation until the developer has confirmed stakeholder outcomes,
observable behavior, subsystem boundaries, shared interfaces, error semantics, and
acceptance criteria.

Split work along stable `SUB` boundaries rather than arbitrary file counts. For each
agent, provide:

1. Owned requirements and component contracts.
2. Inputs, outputs, state transitions, errors, and prohibited changes.
3. Dependencies and integration order.
4. Required tests or other evidence and objective pass criteria.
5. The persistent context topics and local router that apply.

Assign separate integration work when several agents touch one contract. Have the
coordinator reconcile interface changes before dependents proceed. Update durable
context as code, commands, and architecture become concrete.

After integration, independently inspect trace coverage and try boundary cases. Transfer
unfinished items to concise context gaps or issues, remove V-model links and IDs, delete
`.agents/v-model/`, and lint in `absent` mode.

## Holistic codebase review

Use nonoverlapping discovery lanes:

- **Public contract:** docs, examples, manifests, releases, compatibility promises.
- **Code architecture:** entry points, state and error boundaries, APIs, subsystems.
- **Verification:** tests, CI, fixtures, environments, skips, evidence durability.
- **Agent context:** router scope, selective loading, commands, duplication, anchors.

The coordinator merges evidence, then interviews the developer only about intent that
inspection cannot establish. Build the temporary V-model from confirmed goals.

Assign independent comparisons for stakeholder outcomes, system behavior, subsystem
contracts, component invariants, and verification. Every finding must include:

1. Classification: matched, design defect, missing implementation, unintended behavior,
   verification gap, accepted decision, or unresolved.
2. Affected goal, code, and evidence anchors.
3. Impact and confidence.
4. Smallest safe correction or follow-up.
5. Whether developer intent is still required.

For sampled passing actions, compare every phrase in the procedure and criterion with
the cited evidence. Search for counterexamples to universal claims. Mechanical reverse
links are not semantic coverage.

The coordinator deduplicates findings, applies agreed corrections, improves durable
docs, and deletes the V-model at review completion.

## Documentation review

Keep the V-model absent. Assign independent passes for router/link integrity,
source/test drift, context retrieval quality, and duplication. Start from representative
repository tasks and follow only the links an agent is told to open. Report missing
routes, unnecessary hops, unrelated material, stale commands, and mixed context needs.

## Forward-test this skill

Skill maintainers should use disposable clones pinned to exact commits. Test at least:

- A rough new-project prompt that must become a precise, parallelizable design before
  any code is written.
- A brownfield codebase whose implementation conflicts with developer-stated goals.
- An established repository receiving routine docs maintenance with no V-model.
- Final cleanup of both bounded workflows, including successful `--v-model absent`
  linting.

Keep prompts, raw diffs, linter output, and scores outside the shipped skill. Retain them
only until findings are incorporated, then remove temporary artifacts.
