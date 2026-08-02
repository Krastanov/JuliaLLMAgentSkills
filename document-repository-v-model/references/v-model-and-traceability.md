# V-Model and Traceability

Use this reference only while designing a new project before code or conducting a
holistic review of an existing codebase.

## Contents

- [Purpose and lifetime](#purpose-and-lifetime)
- [Four specification layers](#four-specification-layers)
- [Specification records](#specification-records)
- [Verification actions](#verification-actions)
- [Traceability](#traceability)
- [Specification versus decisions](#specification-versus-decisions)
- [Risk tailoring](#risk-tailoring)
- [Close the V-model](#close-the-v-model)

## Purpose and lifetime

Use the V-model for exactly two bounded tasks:

- Turn a rough project prompt into a developer-confirmed design whose contracts and
  acceptance criteria let independent agents build a coherent first version.
- Compare a whole existing codebase with developer-confirmed goals to detect design
  defects, missing or unintended behavior, and verification gaps.

Store it under `.agents/v-model/` while the task is active. It may be committed on a task
branch for coordination. Delete it when the initial implementation or holistic review
is complete. Do not maintain it for routine feature work, releases, or later repository
changes; persistent parallel specifications create avoidable synchronization work and
eventually drift from the implementation.

This is a repository-neutral V-profile, not a claim of NASA, FDA, ECSS, V-Modell XT, or
regulated-lifecycle compliance. It uses the distinction between validating intended
outcomes and verifying specified behavior, objective pass/fail records, bidirectional
traceability, early evidence planning, tailoring, and risk-scaled independence.

## Four specification layers

| Layer | Include | Exclude | Right side |
| --- | --- | --- | --- |
| `STK-###` stakeholder outcomes | Actors, operational scenarios, intended outcomes, success measures, exclusions | Package names, file layout, algorithms | `ACC-###` operational validation and acceptance |
| `SYS-###` system requirements | Observable capabilities, quality attributes, constraints, external boundaries, objective criteria | Internal architecture unless externally observable | `SYSV-###` black-box system verification |
| `SUB-###` subsystem/interface contracts | Logical responsibilities, data, state, error, and boundary semantics | Chosen package and file topology | `INTV-###` integration and contract verification |
| `CMP-###` component contracts | Non-obvious invariants, preconditions, postconditions, and resource budgets | Exhaustive function documentation and obvious behavior | `UNITV-###` unit, property, analysis, or inspection evidence |

Parent layers are strict: `STK` has no parent; `SYS` points to `STK`; `SUB` points to
`SYS`; `CMP` points to `SUB`. Use multiple parents when one record refines several
concerns. Keep IDs stable during the active task and never reuse retired IDs.

For initial design, make `SUB` boundaries and shared contracts precise enough to assign
nonoverlapping implementation work. For holistic review, use every layer to compare
confirmed intent with actual behavior and evidence.

## Specification records

Use a level-two or deeper heading and these fields:

```markdown
## SYS-014 — Export results without data loss

- **Normative statement:** The product shall ...
- **Parents:** STK-003
- **Acceptance criterion:** Given ..., when ..., then ...
- **Verification:** SYSV-008 (test), SYSV-011 (analysis)
- **Origin / risk:** Developer interview; medium data-loss risk
- **Context:** [Persistence design](../context/persistence.md)
```

`Normative statement`, `Parents`, `Acceptance criterion`, and `Verification` are
required. `Origin / risk` and `Context` are optional. Use `None` in `Parents` only for
`STK`. Every verification mapping includes an action ID and one method in parentheses:
`test`, `analysis`, `inspection`, or `demonstration`.

Write one independently testable statement per record. Make its criterion objective
enough for an agent to decide pass or fail. Replace words such as "fast," "robust," or
"user-friendly" with thresholds or concrete scenarios.

## Verification actions

Store right-side actions in `verification.md` or its shards:

```markdown
## SYSV-008 — Verify lossless result export

- **Covers:** SYS-014
- **Method:** test
- **Procedure:** Run ...
- **Environment / configuration:** Supported release build on ...
- **Pass criterion:** The exported ...
- **Status:** passing
- **Evidence:** [`tests/export_roundtrip.py`](../../tests/export_roundtrip.py)
- **Nonconformance:** None
```

Every action requires all eight fields. Use these statuses:

| Status | Meaning |
| --- | --- |
| `planned` | The action is designed but its durable artifact is absent. |
| `implemented` | The artifact exists but current full-criterion evidence is incomplete. |
| `passing` | Current durable evidence demonstrates every criterion clause in the named environment. |
| `failing` | Current evidence violates at least one clause. |
| `blocked` | Execution cannot proceed; name the blocker and owner or trigger. |
| `waived` | An authorized rationale accepts missing or failing evidence; link approval. |

A `passing` action must cite durable evidence. Do not use pasted logs or "tested
manually" as the only evidence. Match procedures, criteria, and evidence clause by
clause. Split actions when one artifact does not exercise every condition. Use fixtures
that distinguish ordering, direction, field identity, and branch behavior.

## Traceability

Maintain bidirectional many-to-many links inside the temporary V-model:

- Every specification lists at least one matching action.
- Every action lists at least one covered specification.
- IDs appear on both sides and declared methods match.
- `ACC` covers only `STK`; `SYSV` only `SYS`; `INTV` only `SUB`; `UNITV` only `CMP`.
- Parent references point to the immediately higher layer.
- Plan verification while specifying behavior.

Traceability demonstrates coverage, not truth. Review whether evidence exercises the
criterion and whether the criterion represents developer intent. Persistent context may
be linked from V-model records, but must not depend on reverse links or IDs that become
meaningless after deletion.

## Specification versus decisions

Keep these outside the V-model and in persistent context when they remain useful:

- Chosen language, framework, package, file, class, or database layout.
- Current source paths, CI job names, build tools, and local conventions.
- Trade studies, rejected alternatives, architecture rationale, and workflows.

If an implementation choice becomes externally observable, specify only its invariant
and objective acceptance meaning. Keep the mechanism and rationale in context. In a
holistic review, preserve conflicts rather than rewriting goals to match code.

## Risk tailoring

Increase specialist review, environment fidelity, failure injection, evidence
durability, and reviewer independence for safety, security, privacy, destructive
operations, financial impact, hard real-time budgets, compatibility promises, or public
interfaces. Keep low-risk projects proportional: a few precise records are better than
one record per function.

## Close the V-model

Before completing the task:

1. Reconcile confirmed goals with implementation and evidence.
2. Put current usage, development workflows, architecture, and decisions in durable
   agent context.
3. Record remaining work as concise current gaps in context or the issue tracker,
   without V-model IDs or copied trace tables.
4. Remove every router link to `.agents/v-model/`.
5. Delete `.agents/v-model/` and run the linter with `--v-model absent`.
