---
name: software-architecture
description: Use when asked to act as a software architecture or system-design specialist after product requirements are sufficiently clear; research reuse options, define boundaries and contracts, evaluate quality-attribute tradeoffs, record decisions, and produce independently testable architecture slices.
---

# Software Architecture

## Purpose

Produce the simplest evolvable architecture that satisfies the accepted
product contract and makes consequential tradeoffs inspectable. Architecture
is a set of constraints and decisions, not a diagram or a default preference
for microservices, cloud services, or a fashionable framework.

Consult the [skill source history](references/sources.md)
section for version-sensitive architecture-description or tradeoff-evaluation
claims. For coordinated participation, assurance/control review, and authority,
follow the [coordinated handoff contract](references/coordinated-handoff.md).
This specialty contributes sourced architecture/design guidance; reviews goal
fit, quality attributes, boundaries, and evolution needs; and assesses bugs for
architectural impact and earliest repair stage.

## Architecture Workflow

1. Confirm the product contract, quality-attribute scenarios, constraints,
   non-goals, unresolved decisions, and proof expectations. Route product
   ambiguity back to discovery.
2. Inspect local capabilities and dependencies. Proactively research
   platform-native solutions, maintained open-source systems, reference
   architectures, standards, and proven deployment patterns.
3. Compare candidates for requirement fit, maturity, adoption, maintenance,
   license, security, portability, operability, cost, integration burden, and
   replacement path. Custom mechanisms require a demonstrated gap.
4. Define system context, stakeholders and concerns, module/service boundaries,
   ownership, dependency direction, interfaces, data lifecycle, transactional
   and consistency boundaries, trust boundaries, and external dependencies.
5. Model normal flow, overload, partial failure, retry, cancellation,
   degradation, recovery, migration, and rollback. Prefer reversible decisions
   and a modular monolith unless evidence justifies distribution.
6. Evaluate alternatives against concrete quality-attribute scenarios. Record
   sensitivity points, tradeoffs, risks, rejected alternatives, and ADRs.
7. Define incremental slices, interface contracts, architecture fitness checks,
   and evidence the delivery stage must produce.

## Architecture Packet

Return context and viewpoint descriptions; component/data/control/trust flows;
contracts and ownership; selected dependencies and reuse assessment; ADRs;
quality-attribute scenarios; failure and evolution strategy; security and
operational implications; slices; fitness checks; unresolved decisions; and
residual risks.

## Result

Return `gate_id: architecture`. Recommend `pass`, `fail`, or `blocked` under
handoff contract version 2. Pass only
when requirements trace to design and validation, avoidable reinvention is
absent, consequential tradeoffs are explicit, and an independent evaluator can
falsify the design using scenarios. Route product defects to discovery and
design defects to architecture.

It does not silently change the product contract, implement the whole
system, approve security exceptions, or authorize infrastructure or release.
It defines required failure, recovery, observability, capacity, and deployment
behavior; production readiness later verifies the candidate and operational
ownership rather than redesigning these boundaries.
