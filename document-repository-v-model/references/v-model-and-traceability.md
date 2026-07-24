# V-Model and Traceability

Use this reference whenever writing, changing, or reviewing normative specification and
verification records.

## Contents

- [Profile and source basis](#profile-and-source-basis)
- [Incremental V-model](#incremental-v-model)
- [Four specification layers](#four-specification-layers)
- [Specification record format](#specification-record-format)
- [Verification action format](#verification-action-format)
- [Traceability rules](#traceability-rules)
- [Specification versus decisions](#specification-versus-decisions)
- [Risk tailoring](#risk-tailoring)

## Profile and source basis

This is a repository-neutral V-profile. It borrows useful distinctions and traceability
practices; it does not establish compliance with NASA, FDA, ECSS, V-Modell XT, or any
regulated lifecycle.

- [NASA Systems Engineering Handbook §2.4](https://www.nasa.gov/reference/2-4-distinctions-between-product-verification-and-product-validation/)
  distinguishes verification of compliance with requirements from validation of the
  intended purpose in the intended environment. Preserve that distinction: `ACC`
  actions validate stakeholder outcomes; the other right-side records verify specified
  behavior or contracts.
- [FDA General Principles of Software Validation](https://www.fda.gov/media/73141/download)
  maps unit evidence to detailed design, integration evidence to high-level design, and
  system evidence to software requirements; it also calls for objective pass/fail
  records and traceability in both directions. Use the mapping without implying that
  ordinary repositories are medical-device submissions.
- [ECSS-E-ST-40C Rev.1](https://ecss.nl/standard/ecss-e-st-40c-rev-1-software-30-april-2025/)
  emphasizes tailoring, early verification/validation planning, requirements-to-design
  traceability, controlled evidence, and risk-scaled independence. Use only these
  selected practices.

## Incremental V-model

Do not run the profile as a single-pass waterfall. For each feature, defect correction,
compatibility change, or release:

1. Identify affected stakeholder outcomes and system requirements.
2. Update logical contracts without encoding chosen file/package topology.
3. Plan or revise right-side actions while writing the left-side records.
4. Implement at the bottom of the V.
5. Execute unit/inspection, integration, system, and acceptance evidence as applicable.
6. Update current status, durable evidence, nonconformance, and regression impact.

Baseline records incrementally after developer confirmation. A change to a baselined
product gets its own mini-V and regression analysis.

## Four specification layers

| Layer | Include | Exclude | Right side |
| --- | --- | --- | --- |
| `STK-###` stakeholder outcomes | Actors, operational scenarios, intended outcomes, success measures, explicit exclusions | Package names, file layout, algorithms | `ACC-###` operational validation and acceptance |
| `SYS-###` system requirements | Observable capabilities, quality attributes, constraints, external boundaries, objective acceptance criteria | Internal architecture unless externally observable | `SYSV-###` black-box system verification |
| `SUB-###` subsystem/interface contracts | Logical responsibilities, data/state/error semantics, boundary contracts | Chosen package and file topology | `INTV-###` integration, contract, and failure-path verification |
| `CMP-###` component contracts | Non-obvious behavior, invariants, pre/postconditions, resource budgets needed to implement or verify | Exhaustive function documentation and obvious behavior | `UNITV-###` unit, property, static-analysis, or inspection evidence |

Parent layers are strict: `STK` has no parent; `SYS` points to `STK`; `SUB` points to
`SYS`; `CMP` points to `SUB`. Use multiple parents when one record refines several
concerns. Keep IDs stable when wording changes; retire rather than reuse an ID.

## Specification record format

Use a level-two or deeper heading and the exact required fields:

```markdown
## SYS-014 — Export results without data loss

- **Normative statement:** The product shall ...
- **Parents:** STK-003
- **Acceptance criterion:** Given ..., when ..., then ...
- **Verification:** SYSV-008 (test), SYSV-011 (analysis)
- **Origin / risk:** Customer interview; medium data-loss risk
- **Context:** [Persistence decision](../context/persistence.md)
```

Required fields are `Normative statement`, `Parents`, `Acceptance criterion`, and
`Verification`. `Origin / risk` and `Context` are optional. Put `None` in `Parents` only
for `STK` records. Every verification mapping includes an action ID and one method in
parentheses: `test`, `analysis`, `inspection`, or `demonstration`.

Write one independently testable normative statement per record. Make the acceptance
criterion objective enough for a future agent to decide pass or fail. Avoid vague terms
such as “fast,” “robust,” or “user-friendly” unless a measurable threshold or scenario
defines them.

## Verification action format

Store all right-side actions in `verification.md` or its shards:

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

Every action requires all eight fields. Use statuses consistently:

| Status | Meaning |
| --- | --- |
| `planned` | The full action is designed but its durable test, analysis, inspection, or demonstration is not yet implemented. |
| `implemented` | A durable action artifact exists, but current full-criterion execution evidence is absent or incomplete. |
| `passing` | Current durable evidence demonstrates every pass-criterion clause in the named environment. |
| `failing` | Current evidence violates at least one pass-criterion clause. |
| `blocked` | Execution cannot proceed; name the blocker and owner or trigger. |
| `waived` | Authorized rationale accepts the missing or failing evidence; link the approval. |

A `passing` action must name durable evidence: a committed test or report, stable
CI/release record, analysis file, or inspection record. Do not use pasted logs or a claim
such as “tested manually” as the only evidence.
For an `implemented` inspection action, cite a durable checklist, review record, or
automated check; the source file being inspected is not itself the inspection artifact.

Record a failing or blocked action honestly and link its nonconformance. A waiver needs
an explicit rationale and approval anchor. One action may cover several specifications,
and one specification may require several actions.

Match the action’s procedure and pass criterion to the cited evidence clause by clause.
If a specification contains several conditions, either exercise every condition or split
the evidence into separate actions. Never mark an action `passing` because adjacent
behavior is tested, because source inspection suggests it should work, or because only
one direction or entry point is covered. Use a separate `analysis` or `inspection`
action for source evidence and record unexercised cases as nonconformance or planned
work.
Choose fixtures that can distinguish the claimed outcomes. Symmetric or identical
inputs cannot establish ordering, direction, field identity, or correct branch routing
when a swapped implementation would produce the same result.

## Traceability rules

Maintain bidirectional many-to-many links:

- Every specification lists at least one matching right-side action.
- Every action lists at least one covered specification.
- The action ID appears on both sides, and the method in the specification matches the
  action’s `Method`.
- `ACC` covers only `STK`; `SYSV` only `SYS`; `INTV` only `SUB`; `UNITV` only `CMP`.
- Parent references point to existing records in the immediately higher layer.
- Regular context documents link back to related specification IDs.
- Plan verification while specifying the behavior; do not postpone all right-side
  design until implementation is complete.

Traceability demonstrates coverage, not truth. Review whether a test actually exercises
the criterion and whether the criterion represents developer intent.

## Specification versus decisions

The V-model must stand alone as a behavioral contract. Keep these outside it:

- Chosen language, framework, package, file, class, or database layout.
- Current source-file locations and named CI jobs when the normative need is an API or
  compatibility outcome.
- Trade studies and rejected alternatives.
- Build-tool choices and local development conventions.
- Rationale that explains why one implementation was selected.

Link to one relevant topic per subsystem section when background helps. If an
implementation decision becomes an externally observable invariant, promote only that
invariant into a `SYS`, `SUB`, or `CMP` statement. Leave the decision and rationale in
`.agents/context/`. State a compatibility result independently of the workflow or tool
currently used to demonstrate it.

## Risk tailoring

Record origin and risk when it changes assurance. Increase specialist review,
environment fidelity, failure injection, evidence durability, and reviewer independence
for safety, security, privacy, destructive operations, financial impact, hard real-time
budgets, broad compatibility promises, or externally consumed interfaces.

Keep low-risk tiny libraries proportional: a small number of precise records is better
than one record per function. Tailoring may reduce ceremony, never the objective
pass/fail meaning of a retained requirement.
