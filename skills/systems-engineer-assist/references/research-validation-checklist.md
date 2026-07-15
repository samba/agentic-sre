# Research and Validation Checklist

Use this checklist during pre-authoring research and again after generation.
Record only the rows relevant to the target artifact, but make each recorded
answer traceable to a source, command, rendered artifact, or test result.

## Pre-Authoring Research

1. Target matrix
- Distribution, release, architecture, kernel/runtime family, and deployment
  substrate are named.
- Ownership boundary, privilege boundary, network exposure, persistence path,
  and rollout/rollback path are known or explicitly uncertain.
- Unsupported combinations and required fallbacks are written down before
  implementation.

2. Distro and packages
- Package names, virtual packages, splits, transitions, versions, and repository
  components are verified in official distro indexes.
- Install commands and service names match the target release, not a nearby
  release or upstream default.
- Security/update channel expectations are clear for pinned, backported, EPEL,
  AUR, vendor, or third-party packages.

3. Images and artifacts
- Container image publisher, delegated publisher status, registry, digest/tag
  policy, base image lineage, supported architectures, and update posture are
  verified.
- Trust path for archives, binaries, charts, manifests, and signatures/checksums
  is documented before use.
- Pull, mirror, or cache behavior does not bypass provenance or update policy.

4. Versions, manpages, kernels, and modules
- Behavior-sensitive flags, directives, defaults, and exit codes are checked
  against distro/version-aligned manpages or official reference docs.
- Kernel module names, packaging, built-in vs loadable state, parameters, and
  load-time constraints are verified for the target kernel stream.
- Runtime APIs, CLIs, libraries, and config formats are aligned to the version
  actually installed or deployed.

5. Services and config samples
- A version-matched working config sample exists from upstream, distro, vendor,
  or project-maintained examples.
- Unit files, environment files, config include paths, ownership, permissions,
  sockets, ports, state directories, and reload/restart semantics match the
  target service.
- Defaults that affect security, persistence, data migration, or compatibility
  are made explicit.

6. Kubernetes, Flux, Helm, and APIs
- Kubernetes version is mapped to supported `apiVersion`/`kind` values,
  deprecated or removed APIs, admission requirements, and feature gates.
- CRD versions, controller versions, Helm chart versions, values schema, and
  upgrade/drift behavior are verified against official or maintainer docs.
- CNI/CRI/CSI assumptions, RBAC, service accounts, namespaces, storage classes,
  ingress/load balancer behavior, and image pull policy are checked.
- Flux/Helm/Kustomize capabilities and limits are matched to the desired
  install, reconciliation, pruning, rollback, and secret-handling strategy.

7. Cross-cutting checks
- Security posture uses least privilege, explicit allowlists, safe defaults,
  verified provenance, secret redaction, and fail-closed behavior where policy
  is ambiguous.
- Ownership/review path is identified from repo metadata, CODEOWNERS, service
  names, deployment paths, or nearby docs.
- Lightweight threat model covers entry points, identities, permissions, data
  flows, dependency compromise, persistence, rollback, and audit coverage.
- CI/release assumptions cover runner platform, permissions, secrets, exact
  failing command or test harness, and syntax validation for release-path files.
- Telemetry or incident signals are used only when available or requested, and
  remain low-cardinality, non-sensitive, and tied to an actionable question.

## Post-Generation Validation

1. Rendered artifact check
- Validate the artifact consumed at runtime, not only source templates.
- Compare rendered packages, images, services, manifests, policies, ownership,
  permissions, paths, ports, and secrets handling against the target matrix.

2. Environment-specific validation
- Run the narrowest available syntax, dry-run, lint, unit, integration, package,
  container, Kubernetes, Helm, Flux, or service validation for each target in
  scope.
- Confirm producer, consumer, and validator moved together when the deployment
  contract changed.
- Recheck version-sensitive assumptions after generation instead of relying on
  pre-authoring notes alone.

3. Failure handling
- Classify each mismatch as syntax, package/version, API, module, service
  semantics, orchestration behavior, policy, ownership, security, CI, or
  telemetry evidence.
- Fix one meaningful change class at a time when validation is expensive or
  ambiguous.
- If the signal remains noisy or contradictory, invoke
  `systems-engineer-diagnose` before further broad changes.

4. Evidence to retain
- Target matrix and authoritative sources used.
- Commands, dry-runs, rendered files, logs, package/image/API versions, and test
  results that prove validation.
- Known limitations, unsupported combinations, unresolved risks, and why they
  are bounded.
