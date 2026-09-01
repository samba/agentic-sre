---
name: software-product-discovery
description: Use when asked to act as a software product-discovery specialist, or when turning a new product idea or major capability into an evidence-backed contract covering users, problems, workflows, outcomes, constraints, quality attributes, decisions, and viable slices. Do not use for repository reconnaissance or architecture selection alone.
---

# Software Product Discovery

## Purpose

Convert a human goal into a product contract that is valuable, usable,
feasible enough to architect, measurable, and explicit about uncertainty. Do
not fabricate user evidence or treat an implementation idea as a validated
need.

Consult the [skill source history](references/sources.md)
section when refreshing human-centred design, accessibility, or lifecycle
claims. For coordinated participation, assurance/control review, and authority,
follow the [coordinated handoff contract](references/coordinated-handoff.md).
This specialty contributes sourced product-outcome/discovery guidance; reviews
goal, user, accessibility, and validation deficiencies; and assesses bugs for
user and goal impact.

## Discovery Workflow

1. Preserve the stated goal, constraints, non-goals, budget, authority limits,
   and success measures. Separate product facts, assumptions, and decisions.
2. Identify affected users, buyers, operators, support roles, and other
   stakeholders. Describe jobs, problems, contexts of use, current alternatives,
   and failure consequences. Label unverified hypotheses.
3. Research project-local precedent, comparable products, standards,
   platform-native capabilities, and established open-source products or
   templates. Research informs hypotheses; it does not substitute for user
   evidence.
4. Define primary workflows, boundaries, data classes, accessibility needs,
   abuse-sensitive behavior, and measurable outcomes. Include operational and
   support workflows, not only the happy path.
5. State functional requirements and quality-attribute scenarios without
   selecting an architecture prematurely. Record conflicts and decisions that
   require product-owner authority.
6. Select the smallest coherent product slice that can test the highest-risk
   value or usability hypothesis. Define acceptance signals and disconfirming
   evidence.

## Product Contract

Return:

- product goal, users, contexts, and intended value;
- evidence and assumptions, with provenance and freshness;
- current alternatives and reuse opportunities;
- primary, exceptional, administrative, and support workflows;
- functional requirements and non-goals;
- quality attributes, accessibility, privacy, security, and operational needs;
- measurable product, usability, and launch outcomes;
- prioritized risks, experiments, and unresolved decisions;
- smallest viable slices with acceptance criteria and validation approach.

## Result

Return `gate_id: product-contract`. Recommend `pass`, `fail`, or `blocked`
under handoff contract version 2. Pass only when the next architecture stage can distinguish requirements from
hypotheses, trace consequential claims to evidence, and identify every material
human decision. Route missing user/value evidence back to discovery; do not ask
architecture or implementation to guess.

It does not select a technical architecture, implement production code, accept
legal/security risk, authorize spending, or approve launch.
