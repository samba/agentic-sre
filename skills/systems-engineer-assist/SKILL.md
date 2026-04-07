---
name: systems-engineer-assist
description: Use when authoring or validating systems code/scripts/configuration where distro/version compatibility, service semantics, policy composition, and deployment-environment variance can cause generated artifacts to fail.
---

# Systems Engineering Diagnostics

## Use This Skill When

Use this skill as a prerequisite for authoring and validating systems-facing artifacts, especially:

- Bash scripts that are generated or deployed as part of release workflows,
- packaging/release work for Debian, CentOS, Rocky Linux, or Arch Linux,
- Helm charts,
- Flux configuration,
- Kubernetes command workflows,
- Kubernetes API-convention YAML manifests (`apiVersion`/`kind` resources),
- service and host configuration for Linux systems.

This skill is authoring-first: invoke before writing substantive code/config and again during validation.

## Primary Goal

Ensure generated code/scripts/configuration are correct for target environments before broad rollout, and detect/resolve mismatches during validation against distro/version/runtime realities.

## Required Lifecycle

### 1) Pre-Authoring Research (mandatory)

Before generating or changing implementation artifacts:

1. Identify target environment matrix:
- distribution(s), version(s), kernel/runtime family,
- orchestration/deployment substrate,
- policy/auth boundaries.
2. Run the research domains below.
3. Convert findings into explicit authoring constraints.
4. Author only against those constraints.

### 2) Post-Generation Validation (mandatory)

After generating or editing artifacts:

1. Validate generated output against target environment matrix.
2. Identify mismatches (syntax, directives, APIs, package names, module assumptions, orchestration behavior).
3. Resolve mismatches with smallest safe delta.
4. Re-validate until aligned.

### 3) Validation-Failure Recovery Loop (mandatory on failure)

If validation fails, remains noisy, or is ambiguous, invoke `systems-engineer-diagnose` as the required recovery workflow:

1. Anchor on the simplest known-good baseline path.
2. Verify the rendered/runtime-consumed artifact, not source intent alone.
3. Classify signal quality and define one narrow next hypothesis.
4. Change one meaningful variable at a time with early progress gates.
5. Use independent calibration where a known-good comparator exists.
6. If signals remain ambiguous, pause further expensive runs and research authoritative sources before the next change.
7. Iterate until mismatch cause is explicit and validation outcome is decisive.

## Research Domains (Authoring Drivers)

Run these domains whenever they are relevant to the target artifact.

1. Distribution package database research
- Verify package names, splits/transitions, availability, and version lineage in official package indexes.
- Prioritize Debian, CentOS, Rocky Linux, and Arch Linux when relevant.

2. Official container image provenance research
- Verify official publisher/delegated publisher status.
- Record registry source, tag/version policy, and support posture before selecting an image.

3. Distribution-specific manpage research
- Use distro/version-aligned manpages for behavior-sensitive tools and directives.
- Apply especially to tools like `iptables`, `awk`, `find`.

4. Kernel module availability research
- Verify module presence, naming, packaging, and load constraints per distro/kernel stream.
- Distinguish built-in vs loadable expectations.

5. Version-aligned working configuration sample research
- Find known-good, version-matched samples for the target package/service.
- Prefer upstream, distro-maintained, or vendor-maintained canonical samples.
- Apply especially to services like PostgreSQL, Samba, rsync, Squid.

6. Kubernetes and ecosystem capability research
- Map target Kubernetes version to supported API versions/resource kinds and deprecations.
- Verify version-aligned config options for control-plane and workload settings.
- Evaluate CNI/CRI/CSI options for compatibility and operational tradeoffs.
- Search Artifact Hub for deployable components and check maintenance/compatibility/trust signals.
- Validate Flux/Helm/Kustomize capabilities and limits for install/upgrade/drift strategy.

## Integrated Skills Policy

### Default-on (invoke unless disqualified)

- `security-best-practices`
- `security-ownership-map`
- `security-threat-model`

Disqualify only when explicitly out of scope for the current task (for example strictly non-security, user-excluded, or insufficient repo metadata for ownership mapping).

### Conditional-on (invoke only when triggered)

- `gh-fix-ci`: only when GitHub Actions/PR checks are active blockers.
- `sentry`: only when Sentry telemetry is available/relevant or explicitly requested.

## Authoring Constraints Derivation

Translate research into explicit constraints before implementation, for example:

- allowed package names per distro/version,
- allowed directives/flags per tool version,
- required API kinds/versions,
- required modules/services/features,
- unsupported combinations and required fallbacks.

If constraints are unknown, pause authoring and research first.

## Validation Expectations

1. Validate generated artifacts against each target environment in scope.
2. Confirm assumptions tied to distro/version/runtime.
3. Report concrete mismatches and corrective action.
4. Prefer one change-class at a time when environment validation is expensive.

## Exit Criteria

- Pre-authoring research completed for relevant domains.
- Constraints are explicit and traceable to sources.
- Generated artifacts validate against target environment matrix.
- Mismatches are resolved or clearly documented with bounded risk.

## Out of Scope

- Standalone domain-agnostic diagnostics that are unrelated to authoring/validation correctness.
- Project policy decisions unrelated to implementation correctness.
