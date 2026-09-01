---
name: software-supply-chain
description: Use when asked to act as a software supply-chain or dependency-risk specialist, or when selecting, adding, updating, packaging, or releasing third-party libraries, images, build actions, generated artifacts, or models; evaluate provenance, licensing, maintenance, security, pinning, SBOM coverage, and replacement risk.
---

# Software Supply Chain

## Purpose

Enable reuse without importing unmanaged legal, security, availability, or
maintenance risk. A dependency scanner score is evidence, not an acceptance
decision.

Consult the [skill source history](references/sources.md)
section for SLSA, SPDX, OpenSSF, or secure-development claims. For coordinated
participation, assurance/control review, and authority, follow the
[coordinated handoff contract](references/coordinated-handoff.md).
This specialty contributes dependency/provenance/update guidance; reviews
unmanaged dependencies, licensing uncertainty, provenance gaps, and maintenance
risk; and assesses bugs for supply-chain contribution or exposure.

## Assessment Workflow

1. Inventory direct, transitive, build-time, runtime, generated, container,
   action/plugin, model, and service dependencies affected by the change.
2. Establish the canonical source, publisher/maintainer identity, version,
   digest, release channel, license expression, provenance, support posture,
   and known vulnerabilities.
3. Consume product/architecture fit as an input and compare eligible candidates for maintenance activity,
   adoption, security practices, release quality, update cadence, ecosystem
   health, portability, operational burden, and viable replacement.
4. Verify artifacts and provenance against explicit expectations. Pin immutable
   revisions or digests where the ecosystem supports them; document unavoidable
   floating inputs.
5. Produce or update an SBOM in a standard supported format. Record licenses,
   notices, redistribution obligations, exceptions, vulnerability disposition,
   and update ownership. Escalate legal interpretation rather than claiming it.
6. Define automated monitoring, update policy, emergency replacement path, and
   evidence freshness. Reassess on material version, maintainer, license,
   provenance, or threat changes.

## Result

Return `gate_id: supply-chain`. Set applicability independently and recommend
`pass`, `fail`, `blocked`, or `not-applicable` under handoff contract version 2.
A pass requires an attributable and verified artifact,
acceptable license/security/maintenance posture, recorded transitive exposure,
SBOM coverage where applicable, and an owned update/replacement path.

This skill advises dependency acceptability. It does not provide legal advice,
accept business risk, authorize purchase, change architecture, or release an
artifact. Unknown or disputed license obligations require human/legal review.
