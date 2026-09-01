---
name: production-readiness
description: Use when asked to act as a production operations or SRE specialist, including SaaS staging, launch, or sustained operation; evaluate service objectives, observability, capacity, delivery safety, recovery, incident response, support ownership, and post-launch evidence.
---

# Production Readiness

## Purpose

Determine whether a release candidate can be operated safely and sustainably,
not merely deployed successfully. Readiness is contextual: avoid imposing a
distributed-service or always-on operating model on products that do not need
one.

Consult the [skill source history](references/sources.md)
section when SRE, continuous-delivery, canary, or observability guidance affects
the decision. For coordinated participation, assurance/control review, and
authority, follow the
[coordinated handoff contract](references/coordinated-handoff.md).
This specialty contributes reliability/operations guidance; reviews
observability, failure handling, capacity, recovery, delivery, and support; and
assesses bugs for availability and operational impact.

## Readiness Workflow

1. Confirm users, critical journeys, deployment environments, data classes,
   dependencies, support model, business hours, failure impact, and launch
   authority.
2. Define user-centred SLIs and achievable SLOs where applicable, measurement
   windows, error budgets, and actions when budgets are exhausted. Do not claim
   an SLA without business authority.
3. Verify correlated metrics, traces, logs, and actionable alerts without
   sensitive-data leakage or unbounded cardinality. Every page needs an owner,
   user impact, and response path.
4. Validate capacity, quotas, performance, scaling or saturation behavior,
   dependency failure, cost assumptions, and safe degradation.
5. Verify reproducible build/deploy, configuration and secret ownership,
   migrations, feature flags or kill switches, progressive rollout, rollback,
   and release observability.
6. Test backup, restore, data-loss boundaries, disaster recovery, cancellation,
   and compensating actions in conditions representative of operation.
7. Produce runbooks, dashboards, escalation/on-call or support ownership,
   incident severity and communication paths, vulnerability/update cadence,
   certificate/credential renewal, and postmortem/follow-up practice.
8. Define canary success/failure signals, observation window, launch stop
   conditions, rollback authority, post-launch monitoring, and operational
   acceptance criteria.

## Result

Return `gate_id: production-readiness`. Set applicability independently and
recommend `pass`, `fail`, `blocked`, or `not-applicable` under handoff contract
version 2. Pass only when critical failure modes are observable,
owned, bounded, recoverable, and tested; delivery and rollback evidence match
the candidate revision; and post-launch responsibility is explicit.

This skill does not authorize production access, launch, spending, SLA
commitments, destructive recovery, customer communication, or residual-risk
acceptance. Those remain human/coordinator decisions.
