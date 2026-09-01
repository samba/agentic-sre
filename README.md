# Agentic SRE

Agentic SRE is an independently installable suite of software-product and
systems specialist skills. It supplies domain judgment from product discovery
through sustained production operation, with proactive assurance during work
and independent control review before acceptance.

The suite is designed to participate in a durable coordinator such as
[Agentic Delta](https://github.com/samba/agentic-delta), but each skill can also
serve a direct, bounded request. SRE skills do not own backlog priority,
workflow state, permission expansion, risk acceptance, spending, launch, or
release authority.

## Intended Use

Use these skills to:

- turn product goals into evidence-backed product and architecture contracts;
- research standards, platform capabilities, open-source solutions, and
  templates before creating custom mechanisms;
- build and validate bounded implementation slices;
- evaluate security, privacy, compliance, dependencies, provenance, and
  operational readiness;
- author or diagnose version-sensitive system artifacts and runtime behavior;
- learn project coding conventions and produce evidence-backed change records;
- review an existing codebase from every relevant specialist perspective;
- contribute project principles and tenets early enough to guide production;
- assess discovered bugs for goal-relative impact before prioritization.

Use the smallest relevant set for a direct task. Under a durable project
workflow, enroll all available specialist classes early and let each specialist
determine applicability rather than assuming silence means approval.

## How the Suites Compose

Agentic Delta coordinates; Agentic SRE specializes.

1. The coordinator supplies the goal, project context, assigned specialist
   class and version, engagement role, frozen tenets, review-plan item,
   autonomy envelope, artifact revision, and required output.
2. The matching SRE skill activates from that role and task context without the
   coordinator hard-coding a repository-specific skill name.
3. The specialist produces domain work or an advisory handoff with findings,
   evidence, risks, obligations, applicability, and gate recommendation.
4. The coordinator validates and atomically ingests the handoff, routes rework,
   and retains all state-transition and authority decisions.

Every participating skill packages its coordinated-handoff contract and source
history locally. A copied skill must not depend on the repository checkout.

## Product-to-Production Workflow

The lifecycle has a normal causal order, but independent research and read-only
review may overlap when dependencies permit.

1. **Product discovery — `software-product-discovery`.** Establish users,
   problems, workflows, outcomes, constraints, quality attributes,
   accessibility, hypotheses, open-source alternatives, and the smallest
   useful validation slices. Do not select architecture before the product
   contract is sufficiently clear.
2. **Architecture — `software-architecture`.** Compare proven solutions,
   define boundaries and contracts, model data and failure behavior, evaluate
   quality-attribute tradeoffs, record decisions, and define fitness checks and
   incremental slices.
3. **Design assurance — cross-cutting specialists.** Security, supply-chain,
   production, compatibility, delivery, convention, and other enrolled
   specialists contribute sourced constraints and verifiable obligations before
   implementation hardens. Each may opt out with evidence and rationale.
4. **Delivery — `software-delivery`.** Implement bounded accepted slices,
   preserve unrelated work, keep interfaces and generated artifacts aligned,
   and produce risk-selected, revision-bound validation evidence.
5. **Control review — applicable specialists.** Independently verify the exact
   candidate against accepted requirements, frozen tenets, assurance
   obligations, and gate-specific evidence. Route defects to the earliest stage
   capable of correcting them.
6. **Supply-chain acceptance — `software-supply-chain`.** Verify source,
   provenance, license posture, vulnerabilities, pinning, SBOM coverage,
   maintenance, update ownership, and replacement path for affected inputs and
   artifacts.
7. **Production readiness — `production-readiness`.** Verify user-centred
   objectives, observability, capacity, delivery safety, recovery, rollback,
   incident/support ownership, launch controls, and post-launch evidence.
8. **Change record — `smart-commits`.** Derive concise rationale, impact, and
   proof from the exact revision and accepted evidence. Message generation does
   not authorize commit execution or release.
9. **Operate and learn.** Feed observed outcomes, incidents, defects, recovery,
   and operational evidence back to the coordinating learning system.

Passing tests alone does not imply security, supply-chain, architecture,
product, or production acceptance. Conversely, no specialist recommendation
can grant authority reserved for the coordinator or human owner.

## Assurance, Control, and Applicability

- **Assurance** is proactive contribution to a good result. Material advice is
  converted into an obligation tied to frozen project guidance, an owner, a
  lifecycle stage, an affected artifact, and a verification method.
- **Control** is independent evaluation of completed work and its evidence.
  Control reviewers verify assurance obligations and identify gaps; they do not
  retroactively substitute for omitted design-time assurance.
- **Applicability** belongs to the assigned specialist. `not-applicable` is a
  valid reviewed result only when it records examined scope and rationale.

This pattern builds quality into production while retaining independent checks
for omissions, drift, and incorrect assumptions.

## Existing Codebase Review and Bug Triage

For an existing-codebase review, every enrolled specialist compares observed
artifacts with the project goal and effective principles and tenets. Each
returns evidence, risks, deficiencies, and the earliest repair stage, or an
evidenced `not-applicable` disposition.

For a bug, each specialist reports applicability, goal impact, urgency, risk,
and rationale without setting backlog rank or authorizing corrective work. The
coordinator combines these assessments with the remaining product backlog and
creates a governed repair task when prioritized.

## Specialist Skills

Lifecycle and cross-cutting engineering:

- `software-product-discovery`: users, value, requirements, accessibility,
  outcomes, reuse opportunities, and validation slices.
- `software-architecture`: boundaries, contracts, alternatives, tradeoffs,
  failure design, ADRs, and fitness checks.
- `software-delivery`: implementation quality, maintainability, traceable
  verification, and releasable engineering evidence.
- `security-compliance-review`: design-time and pre-release security, privacy,
  control, audit, and compliance review.
- `software-supply-chain`: dependency and artifact provenance, license,
  vulnerability, pinning, SBOM, maintenance, and replacement risk.
- `production-readiness`: service objectives, telemetry, capacity, deployment,
  recovery, incident response, support, and launch readiness.

Focused production support:

- `systems-engineer-assist`: target-version compatibility research, authoring
  constraints, and rendered/runtime artifact validation.
- `systems-engineer-diagnose`: baseline-first diagnosis with discriminating,
  bounded experiments and explicit uncertainty.
- `learn-code-style`: project-local, language-specific convention learning and
  application without confusing preference with correctness.
- `smart-commits`: thread- and task-informed working-draft partitioning plus
  concise, evidence-backed commits and change-record text.
- `langgen`: specification- and corpus-grounded structured-language tooling.
- `kubectl`: explicit-context, least-privilege Kubernetes inspection and
  troubleshooting.

## Improvement Strategy

Each specialist improves project quality without self-authorizing reusable
policy changes:

- propose principles only for durable domain outcomes;
- propose tenets as scoped, actionable standard work with verification;
- cite authoritative sources and preserve superseded interpretations;
- research established libraries, templates, platform primitives, and
  maintained open source before recommending custom construction;
- prefer prevention and point-of-creation feedback over late defect discovery;
- return recurring gaps, escaped defects, rework causes, and weak evidence to
  the learning system;
- separate project-specific guidance from portable method proposals;
- evaluate reusable changes against evidence, compatibility, overlap,
  regression limits, and rollback before promotion.

An SRE specialist may recommend improvement. It cannot change its governing
workflow, adopt residual risk, or promote its own recommendation.

## Example Prompts

Product discovery before architecture:

> Act as a software product-discovery specialist. Turn this idea into an
> evidence-backed product contract, distinguish facts from hypotheses, research
> comparable and open-source solutions, identify product-owner decisions, and
> define the smallest slices that test the highest-risk assumptions.

Architecture with reuse-first research:

> Act as a software architecture specialist for the accepted product contract.
> Research maintained libraries, platforms, reference architectures, and
> templates before proposing custom components. Compare the viable options,
> record tradeoffs and decisions, and define independently testable slices and
> fitness checks.

Design-time security assurance:

> You are the systems security and privacy specialist. Review this design before
> implementation hardens. Identify trust boundaries, sensitive data, abuse
> cases, privileges, deterministic controls, and evidence needs. Convert
> material guidance into verifiable assurance obligations; do not accept risk
> or authorize release.

Bounded implementation and verification:

> Act as the software delivery specialist for this accepted slice. Inspect
> existing conventions and reusable components, implement only the bounded
> scope, and return criterion-to-test mapping and exact revision-bound evidence.
> Report architecture drift instead of hiding it in compatibility glue.

Production-readiness control review:

> You are the production operations specialist. Evaluate this release candidate
> for user-centred objectives, observability, capacity, dependency failure,
> rollout, rollback, recovery, incident response, and support ownership. Return
> an advisory gate recommendation with exact evidence and unresolved risks.

Ambiguous runtime diagnosis:

> Act as a systems diagnostic specialist. A manual path works but the automated
> harness times out. Establish the known-good witness, inspect what the runtime
> consumed, separate observations from assumptions, rank falsifiable
> hypotheses, and run only bounded discriminating probes within current access.

Existing-codebase specialist review:

> Review this existing codebase as a software supply-chain specialist. Compare
> it with the project goal and effective guidance, identify unmanaged or stale
> dependencies, provenance and license uncertainty, SBOM gaps, and replacement
> risk, and state the earliest repair stage for each finding.

Project-specific improvement guidance:

> Based on this project's goal and evidence, propose security principles and
> actionable tenets that should guide future work. Cite authoritative sources,
> include applicability and verification methods, and leave adoption to the
> coordinator.

## Independent Packaging Invariant

Every directory under [`skills/`](skills/) is an independently installable
package. Functionally important instructions, contracts, source history,
templates, and helpers must be inside that skill directory and discoverable
from `SKILL.md`.

A runtime dependency on repository-level `docs/`, a sibling skill, a
machine-local path, or an uninstalled checkout is an anti-pattern. Top-level
documents may be non-normative maintainer notes only. Do not use synchronization
scripts to make a skill complete after installation; validate the copied skill
in isolation instead.

## Repository Scope

This repository owns software-product, software-delivery, supply-chain,
production, systems, security, convention, and change-record specialist
behavior. Durable backlog coordination, workflow state, evidence ingestion,
priority, closure, and method-promotion authority belong to Agentic Delta or
another compatible coordinator.
