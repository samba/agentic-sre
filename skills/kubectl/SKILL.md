---
name: kubectl
description: Use when discovering kubeconfig files or contexts, or inspecting, validating, or troubleshooting Kubernetes clusters with kubectl, locally or over SSH, while avoiding accidental use of default kubeconfig, default context, or default SSH identity. Requires every non-discovery kubectl command to pass an explicit kubeconfig path and context, and every SSH-mediated command to pass an explicit SSH key path.
---

# Kubectl Explicit Context

Use this skill for read-only Kubernetes API inspection, diagnostic capture, and validation when command context must be deterministic.

## Required Inputs

Before running any non-discovery command, identify:

- kubeconfig path
- Kubernetes context name, unless the current step is context discovery
- local execution or SSH-mediated execution
- for SSH: target user, host, and SSH identity key path
- allowed command class: `get`, `list`, `describe`, `logs`, and `events` are permitted without approval when read-only and explicitly scoped; all mutating or potentially mutating operations require explicit user request or explicit approval

For discovery, identify the explicit local or remote search roots first. Do not
search the whole filesystem unless the user explicitly asks for that scope.

Do not infer required values from local defaults. If any required value is
missing, ask for it or stop with a clear blocker.

## Command Rules

Every non-discovery `kubectl` command must include:

```bash
kubectl --kubeconfig "$KUBECONFIG_PATH" --context "$KUBE_CONTEXT" ...
```

Never rely on:

- `$KUBECONFIG`
- current-context
- in-cluster defaults
- implicit local kubeconfig discovery
- shell aliases or wrapper functions

Every SSH-mediated command must include an explicit identity key:

```bash
ssh -i "$SSH_KEY_PATH" "$SSH_USER@$SSH_HOST" \
  kubectl --kubeconfig "$REMOTE_KUBECONFIG_PATH" --context "$KUBE_CONTEXT" ...
```

Never rely on:

- default SSH identities
- ssh-agent-only behavior
- remote shell aliases
- remote default kubeconfig
- remote current-context

Prefer `--` before the remote command when using additional SSH options and quote remote paths deliberately.

## Kubeconfig File Discovery

Kubeconfig file discovery is allowed before a kubeconfig path is known. It must
use explicit search roots and should stay bounded.

Prefer likely locations first:

- `$HOME/.kube`
- `/etc/kubernetes`
- project-provided artifact directories
- operator-supplied paths

Local discovery example:

```bash
find "$SEARCH_ROOT" -maxdepth 4 -type f \
  \( -name 'config' -o -name '*.kubeconfig' -o -name '*kubeconfig*' \) \
  -print
```

Remote discovery over SSH:

```bash
ssh -i "$SSH_KEY_PATH" "$SSH_USER@$SSH_HOST" \
  find "$REMOTE_SEARCH_ROOT" -maxdepth 4 -type f \
  \( -name 'config' -o -name '*.kubeconfig' -o -name '*kubeconfig*' \) \
  -print
```

For SSH-mediated discovery, always pass `ssh -i "$SSH_KEY_PATH"`. Do not rely on
default identities or remote shell aliases.

Discovery output is only a candidate list. Select one kubeconfig path explicitly
before running context discovery or cluster inspection.

## Context Discovery

Context discovery is the only allowed pre-context `kubectl` operation. It may
omit `--context` because the purpose is to discover valid context names, but it
must still pass an explicit kubeconfig path and must not rely on current-context
as the selected context for later operations.

Local context discovery:

```bash
kubectl --kubeconfig "$KUBECONFIG_PATH" config get-contexts -o name
```

Remote context discovery over SSH:

```bash
ssh -i "$SSH_KEY_PATH" "$SSH_USER@$SSH_HOST" \
  kubectl --kubeconfig "$REMOTE_KUBECONFIG_PATH" config get-contexts -o name
```

It is also permitted to inspect the kubeconfig's current context for reporting
or as a candidate, not as an implicit selection:

```bash
kubectl --kubeconfig "$KUBECONFIG_PATH" config current-context
```

After a context is selected, all normal `kubectl` calls must include both
`--kubeconfig` and `--context`.

## Operation Approval

Permitted without extra approval:

- `kubectl get`
- `kubectl describe`
- `kubectl logs` when explicitly scoped to a namespace, pod, controller, or label selector; prefer bounded output with `--tail`, `--since`, or equivalent when diagnosing failures
- `kubectl events` and `kubectl get events` when used only to inspect event history
- `kubectl api-resources` when used only to list resources
- `kubectl api-versions` when used only to list API versions
- bounded `find` commands used only to discover kubeconfig files under explicit search roots
- `kubectl config get-contexts -o name` when used only to discover contexts from an explicit kubeconfig
- `kubectl config current-context` when used only to report the kubeconfig's current context as a candidate

If a user asks for a generic inspection, status, inventory, or diagnostic pass,
prefer `get` and `describe` first, then use `events` and scoped `logs` when
resource status points to a concrete failing workload.

Prohibited unless the user explicitly requested the operation or explicitly
approves it after being asked:

- `apply`, `create`, `delete`, `edit`, `patch`, `replace`, `scale`, `rollout restart`
- `cordon`, `uncordon`, `drain`, `taint`, `label`, `annotate`
- `exec`, `cp`, `port-forward`, `proxy`
- `wait`, `auth can-i`, `version`, and `cluster-info` unless they are specifically included in the approved diagnostic scope
- any command that writes files, changes cluster state, opens a tunnel, or starts a long-lived process

When unsure whether a command is mutating, treat it as prohibited and ask for
approval.

Approval can come from either:

- the user's explicit request for that exact operation class, or
- an approval response after Codex asks whether to run the specific command or
  command class.

## Diagnostic Pattern

For cluster diagnostics, gather facts in a stable order:

1. API reachability and version
2. nodes and conditions
3. namespaces
4. pods by namespace
5. events sorted by time
6. services, endpoints, ingress, and gateway resources
7. storage classes, PVCs, PVs, CSI drivers, and storage-system resources
8. Flux sources, Kustomizations, HelmRepositories, and HelmReleases when Flux is installed
9. app-specific logs and status only after identifying namespaces and labels

Use explicit namespace flags. Do not assume `default` unless that is the intended namespace.

## Safety Checks

Before running a command, verify the rendered command includes:

- `--kubeconfig`, except for bounded kubeconfig file discovery
- `--context`, except for the context-discovery commands above
- for SSH: `ssh -i`

If a command is copied from documentation, rewrite it to include the explicit kubeconfig and context before running it.

If a diagnostic loop is needed, keep it bounded with a timeout or fixed iteration count.

## Reporting

When reporting results, include:

- kubeconfig path used, redacted only if path itself is sensitive
- context name used
- whether execution was local or SSH-mediated
- SSH host and key path for remote execution, redacted only if needed
- exact command class: read-only or mutating
- any commands skipped because they would mutate state

Do not include secret values, bearer tokens, kubeconfig contents, or private key material.
