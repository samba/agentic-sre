---
name: software-delivery
description: Use when asked to act as a software implementation-quality or delivery specialist, or when implementing an accepted design as bounded, reviewable slices with dependency discipline, deterministic tests, requirement traceability, revision-bound evidence, and a releasable handoff. Do not bypass product or architecture gates.
---

# Software Delivery

## Purpose

Determine whether a bounded implementation conforms to an accepted product and
architecture slice and produce a maintainable, deployable revision with
evidence. The durable coordinator owns dispatch, concurrency, workspace and
review orchestration; this skill does not encode a universal framework,
language, repository shape, or test pyramid.

Consult the [skill source history](references/sources.md)
section when a secure-development or continuous-delivery principle affects the
decision. For coordinated participation, assurance/control review, and
authority, follow the
[coordinated handoff contract](references/coordinated-handoff.md).
This specialty contributes maintainability/delivery guidance with
point-of-creation checks; reviews goal fit, correctness, complexity,
testability, and maintainability; and assesses bug impact, regression scope,
and repair cost.

## Delivery Workflow

1. Confirm the slice contract, permitted files/systems, interfaces, quality
   attributes, acceptance criteria, autonomy envelope, and rollback boundary.
2. Inspect repository conventions, build/test paths, existing abstractions,
   dependencies, and reusable templates. Research established solutions before
   adding a custom mechanism or dependency.
3. Plan the smallest coherent change. Keep architecture, migrations, generated
   artifacts, consumers, and tests synchronized; do not hide design drift in
   compatibility glue.
4. Implement within the workspace and authority issued by the coordinator.
   Preserve unrelated work.
5. Build a risk-selected proof set: compilation/type/static checks; unit,
   integration, contract, migration, end-to-end, failure, accessibility,
   performance, property, fuzz, or mutation checks where they materially test
   the contract.
6. Verify deployment-like behavior where practical. Record exact commands,
   environment, revision, results, omissions, and residual risk.
7. Prepare the criterion mapping and artifacts needed for the coordinator's
   independent review. Report structural defects and the earliest repair stage.

## Delivery Handoff

Return changed artifacts, behavior, dependency changes, architecture drift,
criterion-to-test mapping, exact revision, deterministic evidence, review
findings, known limitations, rollback information, follow-up work, and the
applicable security/supply-chain/operational gates.

## Result

Return `gate_id: implementation-verification`. Recommend `pass`, `fail`, or
`blocked` under handoff contract version 2.
Passing tests alone are insufficient when acceptance criteria, independent
review, security, supply-chain, or migration proof remain unresolved.

It does not redefine accepted requirements or architecture, accept
residual risk, commit without authority, or approve production release.
