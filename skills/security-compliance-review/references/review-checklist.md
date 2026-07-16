# Security Compliance Review Checklist

Use this checklist to review designs and implementation changes before commit. Apply only the sections relevant to the change, but record why omitted sections are not applicable when the work is a new project or a security-sensitive change.

## ISO/IEC 27001-Style ISMS Themes

- Scope: affected systems, data, teams, suppliers, and locations are identifiable.
- Risk assessment: threats, vulnerabilities, impacts, and likelihood are considered for the change.
- Risk treatment: mitigation, transfer, acceptance, or avoidance is explicit for material risks.
- Control ownership: every required control has an owner and operational path.
- Asset handling: information assets and data classes are identified and protected.
- Access control: authentication, authorization, least privilege, and privileged operations are explicit.
- Cryptography and secrets: key ownership, storage, rotation, and secret exposure risks are addressed.
- Logging and monitoring: security-relevant events are observable without leaking sensitive data.
- Incident response: failure modes and escalation paths are known for material risks.
- Business continuity: backup, restore, availability, and dependency-failure behavior are covered when relevant.
- Evidence: tests, reviews, configuration, logs, runbooks, or tickets support the security claim.
- Continual improvement: repeated misses create backlog work or skill/process updates.

## ISO/IEC 27017 Cloud Themes

- Cloud role clarity: provider, customer, and shared responsibilities are explicit.
- Tenant isolation: data, compute, network, and identity boundaries are understood.
- Cloud asset lifecycle: provisioning, configuration, backup, return, deletion, and decommissioning are covered.
- Administrative operations: privileged cloud operations are logged, reviewed, and recoverable.
- Provider dependencies: regions, managed services, sub-processors, and SLAs are documented when material.
- Monitoring: cloud activity, control-plane changes, and customer-visible health are observable.
- Portability and exit: data export, deletion proof, and provider lock-in risks are considered when relevant.

## SOC 2 Themes

Map findings to the relevant Trust Services Criteria category:

- Security: protection against unauthorized access, disclosure, and system damage.
- Availability: system operation and recovery meet commitments.
- Processing integrity: processing is complete, valid, accurate, timely, and authorized.
- Confidentiality: confidential information is protected according to commitments.
- Privacy: personal information handling aligns with commitments and notice/choice/retention expectations.

For each applicable category, ask:

- What control is intended?
- Where is it implemented?
- How is it tested?
- What evidence would an auditor or customer accept?
- What exception or residual risk remains?

## CMMI-Style Process Maturity Themes

- Repeatability: the control does not depend on one person remembering an unwritten step.
- Ownership: responsible roles are explicit for operation and review.
- Measurement: success/failure signals are visible and can be trended.
- Verification: checks happen before release, not only after incidents.
- Supplier management: vendor or dependency risks have review and escalation paths.
- Improvement loop: defects, incidents, and audit findings become durable process changes.

## Adjacent Security Subjects

- Threat modeling: trust boundaries, abuse cases, and attacker paths are considered.
- Secure SDLC: security requirements, code review, dependency review, and CI gates are present when relevant.
- Supply chain: dependencies, base images, packages, provenance, and update strategy are known.
- Data governance: classification, minimization, retention, deletion, and cross-border concerns are considered.
- Vulnerability management: detection, triage, remediation, and exception handling are defined.
- Change management: risky changes are reviewable, reversible, and observable.
- Customer commitments: public claims, contracts, questionnaires, and documentation match actual implementation.

## Review Decision

- `blocker`: unacceptable risk or missing evidence for a material control.
- `required-follow-up`: acceptable only with owner, scope, and due condition.
- `advisory`: useful improvement that does not block this commit.
- `not-applicable`: explicitly out of scope with reason.

Prefer one precise finding with evidence over broad compliance language.
