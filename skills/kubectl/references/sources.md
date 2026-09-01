# Source History

Last substantive review: 2026-08-31.

- [Kubernetes kubeconfig API](https://kubernetes.io/docs/reference/config-api/kubeconfig.v1/)
  and [kubectl reference](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands.html)
  support explicit kubeconfig, context, and command interpretation.
- [Kubernetes RBAC good practices](https://kubernetes.io/docs/concepts/security/rbac-good-practices/)
  supports least privilege and namespace-scoped access where practical. It
  does not prove the current cluster or identity is correctly authorized.

The wrapper's read-only allowlist, explicit-context requirements, and refusal
to infer remote identity are stricter local safety policies. For consequential
version claims, retain source, exact version, retrieval date, applicability,
and limits; preserve superseded entries rather than rewriting history.
