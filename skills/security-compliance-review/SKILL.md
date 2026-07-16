---
name: security-compliance-review
description: Use when reviewing design or implementation work before committing, especially for new projects, security-sensitive changes, customer-facing systems, cloud services, data handling, access control, auditability, compliance certification readiness, ISO/IEC 27001, ISO/IEC 27017, SOC 2, Capability Maturity Model/CMMI-style process maturity, or adjacent security governance concerns.
---

# Security Compliance Review

Use this skill before committing design or implementation work that could affect security, compliance posture, audit evidence, customer trust, or certification readiness.

This is a proactive review skill. It does not certify compliance, replace counsel, or claim conformity to any standard. It helps identify design gaps, implementation risks, missing evidence, and work that should be tracked before release.

## Use This Skill When

Use this skill for:

- new projects, services, APIs, integrations, deployment workflows, or data stores
- changes touching authentication, authorization, secrets, encryption, logging, monitoring, backup, recovery, tenancy, data lifecycle, vendor integrations, or CI/CD
- design reviews where ISO/IEC 27001, ISO/IEC 27017, SOC 2, CMMI-style maturity, customer security questionnaires, or audit readiness may matter
- pre-commit review when security or compliance risks should be surfaced before code lands

Do not use this skill as a generic code review replacement. Pair it with normal tests, implementation review, and domain-specific security testing.

## Review Inputs

Before reviewing, identify:

- business purpose and users
- assets and data classes affected
- trust boundaries and external dependencies
- deployment/runtime environment
- operators and support model
- evidence already produced by tests, logs, docs, CI, or design artifacts
- relevant compliance drivers: ISO/IEC 27001, ISO/IEC 27017, SOC 2 trust service criteria, customer contract, regulatory expectation, or internal maturity goal

If the project is new, require a short security/compliance assumptions section before commit.

## Review Workflow

1. **Scope the change**
   - Identify what changed, what data or services it affects, and which users/operators can reach it.
   - State whether the change is security-sensitive, compliance-relevant, or operationally material.

2. **Map risks to control themes**
   - Use the checklist in [references/review-checklist.md](references/review-checklist.md).
   - Cover information security management, cloud shared responsibility, SOC 2 control evidence, process maturity, and adjacent security subjects as relevant.

3. **Inspect implementation evidence**
   - Prefer concrete artifacts: code paths, config, tests, CI logs, runbooks, threat notes, audit logs, monitoring dashboards, backup/restore proof, access-control tests.
   - Do not accept policy assertions without implementation evidence when code/config changed.

4. **Classify findings**
   - `blocker`: release or commit would create unacceptable security/compliance risk.
   - `required-follow-up`: commit can proceed only if a tracked follow-up exists with owner and due condition.
   - `advisory`: improvement worth recording, not required for this change.
   - `not-applicable`: state why the control theme does not apply.

5. **Recommend the smallest safe action**
   - Prefer concrete fixes, evidence additions, tests, or follow-up cards over broad policy prose.
   - Avoid claiming compliance unless an accredited audit/certification process supports that claim.

## Minimum Pre-Commit Gate

Before approving a commit, ensure:

- affected assets and data classes are known
- secrets and credentials are not introduced or exposed
- authentication and authorization paths are explicit
- audit/logging evidence exists for security-relevant actions, or the absence is justified
- cloud/provider/customer responsibilities are clear when cloud services are involved
- tests or validation cover the security-relevant behavior touched by the change
- residual risks are documented with owner, follow-up, and acceptance rationale

If any item is unknown for a new project, treat it as `required-follow-up` at minimum.

## Output Contract

Return:

```text
Security/compliance review: <blocker|required-follow-up|advisory|clear>

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
```

## Source Awareness

Use official sources when the exact standard framing matters. As of this skill revision:

- ISO/IEC 27001:2022 defines ISMS requirements and has a 2024 amendment.
- ISO/IEC 27017:2015 provides cloud-service control guidance and is expected by ISO to be replaced soon; verify current status before making version-specific claims.
- SOC 2 is governed through AICPA SOC reporting and Trust Services Criteria.
- CMMI is a capability and performance improvement model, not a security control catalog.

When a standards detail would affect a commitment, certification claim, contract response, or customer-facing statement, verify it against the current official source before relying on it.
