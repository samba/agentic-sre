---
name: security-compliance-review
description: Use when asked to act as a systems, application, privacy, or compliance security specialist, including design-time threat/control review or pre-release evidence review of customer-facing, cloud, data, identity, audit, ISO/IEC 27001/27017, SOC 2, or CMMI-related work. Does not replace ordinary code review, counsel, audit, or certification.
---

# Security Compliance Review

Use this skill at two distinct gates for work that could affect security,
compliance posture, audit evidence, customer trust, or certification readiness:

- `design-time`: before implementation commits to trust boundaries, data flows,
  identities, privileges, dependencies, or risk treatment;
- `pre-release`: after implementation evidence exists and before the change is
  accepted for release or merge.

This is a proactive review skill. It does not certify compliance, replace counsel, or claim conformity to any standard. It helps identify design gaps, implementation risks, missing evidence, and work that should be tracked before release.

## Use This Skill When

Use this skill for:

- new projects, services, APIs, integrations, deployment workflows, or data stores
- changes touching authentication, authorization, secrets, encryption, logging, monitoring, backup, recovery, tenancy, data lifecycle, vendor integrations, or CI/CD
- research datasets, source-plugin integrations, public-data pipelines, survey or microdata access, data licensing, redistribution, provenance, evidence manifests, credentialed APIs, and analytics outputs that could affect customer trust or compliance evidence
- design reviews where ISO/IEC 27001, ISO/IEC 27017, SOC 2, CMMI-style maturity, customer security questionnaires, or audit readiness may matter
- pre-commit review when security or compliance risks should be surfaced before code lands

Do not use this skill as a generic code review replacement. Pair it with normal tests, implementation review, and domain-specific security testing.

## Review Inputs

For coordinated participation, assurance/control review, and authority, follow
the [coordinated handoff contract](references/coordinated-handoff.md).
This specialty contributes sourced security/privacy/control guidance; reviews
trust boundaries, data obligations, abuse cases, and effective guidance; and
assesses bugs for security, privacy, compliance, and customer-trust impact.

Before reviewing, identify:

- business purpose and users
- assets and data classes affected
- trust boundaries and external dependencies
- deployment/runtime environment
- operators and support model
- evidence already produced by tests, logs, docs, CI, or design artifacts
- data sources, licenses, access conditions, provenance records, retention expectations, and whether personal, household, respondent-level, or sensitive data is involved
- relevant compliance drivers: ISO/IEC 27001, ISO/IEC 27017, SOC 2 trust service criteria, customer contract, regulatory expectation, or internal maturity goal

If the project is new, require a short security/compliance assumptions section
at design-time and reconcile it against evidence at pre-release.

## Product Lifecycle Integration

Apply this review across the lifecycle without taking ownership from the
specialist skill:

- product discovery: identify sensitive users and data, foreseeable misuse,
  privacy expectations, tenant boundaries, retention/deletion needs, and human
  decisions before requirements harden;
- architecture: validate identity, authentication and authorization, trust and
  data flows, tenant isolation, secrets, cryptography boundaries, abuse cases,
  failure containment, and the planned control evidence;
- delivery: verify that implementations, tests, scans, migrations, logs, and
  rendered artifacts satisfy the accepted controls rather than only the happy
  path;
- supply chain: consume provenance, vulnerability, SBOM, and update-ownership
  evidence from the supply-chain gate and evaluate its security implications;
  leave general license and maintenance acceptability to that specialist;
- production readiness: consume recovery and operational evidence, then verify
  security telemetry, incident/disclosure paths, backup protections,
  credential renewal, emergency revocation, and owned security risks; leave
  general capacity, release, and support readiness to that specialist.

Route a defect to the earliest lifecycle stage that can correct it. Never
convert an advisory review result into risk acceptance or release authority.

## Gate Selection

Record the gate in the review output. Run both gates for material
security/compliance work. A pre-release review cannot retroactively substitute
for design-time review when implementation has already embedded a consequential
security decision; route such a gap to design rework.

At `design-time`, review:

- assets, data classes, trust boundaries, identities, privileges, entry points,
  external dependencies, abuse cases, failure behavior, and risk owners;
- proposed controls and evidence strategy;
- alternatives, residual risk, human decisions, rollout, and rollback;
- requirement-to-design-to-validation traceability.

Return `gate_id: security-design`, the independently determined applicability,
and a version-2 recommendation of `pass`, `fail`, `blocked`, or
`not-applicable`, with evidence and the implementation constraints that follow.

At `pre-release`, review:

- the implemented paths and rendered/deployed artifacts;
- tests, scans, dependency/provenance evidence, access-control checks, logs,
  runbooks, backup/restore or rollback proof, and tracked exceptions;
- drift from the accepted design and whether the evidence proves each
  applicable security requirement.

Return `gate_id: security-release` and a version-2 recommendation of `pass`,
`fail`, `blocked`, or `not-applicable`. Classify individual findings as
`blocker`, `required-follow-up`, or `advisory`.

## Review Workflow

1. **Select and record the gate**
   - Apply the matching gate inputs and output statuses above.

2. **Scope the change**
   - Identify what changed, what data or services it affects, and which users/operators can reach it.
   - State whether the change is security-sensitive, compliance-relevant, or operationally material.

3. **Map risks to control themes**
   - Use the checklist in [references/review-checklist.md](references/review-checklist.md).
   - Cover information security management, cloud shared responsibility, SOC 2 control evidence, process maturity, and adjacent security subjects as relevant.
   - For agentic systems, explicitly assess goal hijacking and indirect prompt
     injection, tool misuse or confused-deputy behavior, identity/privilege
     abuse, secret-to-network flows, memory poisoning, agent/MCP supply-chain
     compromise, insecure inter-agent messages, unexpected code execution,
     retry amplification or cascading failure, and cancellation/kill-switch
     failure.
   - Classify each applicable safeguard as `deterministic-control`,
     `model-instruction-only`, `absent`, or `unknown`. Do not report a prompt or
     model instruction as an enforced security boundary.

4. **Inspect available evidence**
   - Prefer concrete artifacts: code paths, config, tests, CI logs, runbooks, threat notes, audit logs, monitoring dashboards, backup/restore proof, access-control tests.
   - Do not accept policy assertions without implementation evidence when code/config changed.

5. **Classify findings**
   - `blocker`: release or commit would create unacceptable security/compliance risk.
   - `required-follow-up`: commit can proceed only if a tracked follow-up exists with owner and due condition.
   - `advisory`: improvement worth recording, not required for this change.
   - `not-applicable`: state why the control theme does not apply.

6. **Recommend the smallest safe action**
   - Prefer concrete fixes, evidence additions, tests, or follow-up cards over broad policy prose.
   - Avoid claiming compliance unless an accredited audit/certification process supports that claim.

## Minimum Pre-Release Gate

Before approving a commit, ensure:

- affected assets and data classes are known
- secrets and credentials are not introduced or exposed
- authentication and authorization paths are explicit
- audit/logging evidence exists for security-relevant actions, or the absence is justified
- cloud/provider/customer responsibilities are clear when cloud services are involved
- tests or validation cover the security-relevant behavior touched by the change
- residual risks are documented with owner, follow-up, and acceptance rationale
- dataset licenses, redistribution limits, restricted-data access, and credential redaction are explicit when data sources are touched

If any item is unknown for a new project, treat it as `required-follow-up` at minimum.

## Output Contract

Return:

```text
Security/compliance review: <pass|fail|blocked|not-applicable>
Gate: <design-time|pre-release>
Gate id: <security-design|security-release>
Applicability: <applicable|not-applicable|undetermined>

Scope:
- <assets, data, trust boundaries, runtime>

Findings:
- <severity>: <issue> | evidence: <file/test/log/design ref> | action: <fix/follow-up>

Standards mapping:
- ISO/IEC 27001: <risk management / ISMS / control evidence relevance>
- ISO/IEC 27017: <cloud shared-responsibility relevance or not applicable>
- SOC 2: <security/availability/processing integrity/confidentiality/privacy relevance>
- CMMI/process maturity: <repeatability, ownership, measurement, or improvement relevance>

Residual risk:
- <accepted/deferred risks and owner>

Specialist handoff:
- <contract-versioned structured handoff; every blocker names evidence and its earliest rework stage>
```

## Source Awareness

Use official sources when the exact standard framing matters. As of this skill revision:

- ISO/IEC 27001:2022 defines ISMS requirements and has a 2024 amendment.
- ISO/IEC 27017:2026 is the current cloud-service control guidance; it
  superseded ISO/IEC 27017:2015 in July 2026.
- SOC 2 is governed through AICPA SOC reporting and Trust Services Criteria.
- CMMI is a capability and performance improvement model, not a security control catalog.

When a standards detail would affect a commitment, certification claim, contract response, or customer-facing statement, verify it against the current official source before relying on it.

Read the skill [source history](references/sources.md) before making
version-specific or conformity-adjacent claims. Link refreshed sources and
preserve superseded interpretations in the project evidence record.
