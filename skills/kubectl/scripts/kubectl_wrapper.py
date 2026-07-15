#!/usr/bin/env python3
"""Run kubectl commands only after explicit-context controls pass."""

from __future__ import annotations

import argparse
import shlex
import subprocess
import sys
from dataclasses import dataclass


READ_ONLY_VERBS = {
    "api-resources",
    "api-versions",
    "describe",
    "events",
    "get",
    "logs",
}
CONTEXT_DISCOVERY = (
    ("config", "get-contexts"),
    ("config", "current-context"),
)
MUTATING_OR_SENSITIVE_VERBS = {
    "annotate",
    "apply",
    "auth",
    "cluster-info",
    "cordon",
    "cp",
    "create",
    "delete",
    "drain",
    "edit",
    "exec",
    "label",
    "patch",
    "port-forward",
    "proxy",
    "replace",
    "rollout",
    "scale",
    "taint",
    "uncordon",
    "version",
    "wait",
}


@dataclass
class Result:
    ok: bool
    messages: list[str]


def fail(message: str, code: int = 2) -> None:
    print(f"FAIL {message}", file=sys.stderr)
    raise SystemExit(code)


def has_option(tokens: list[str], option: str) -> bool:
    prefix = f"{option}="
    return option in tokens or any(token.startswith(prefix) for token in tokens)


def option_value(tokens: list[str], option: str) -> str | None:
    prefix = f"{option}="
    for index, token in enumerate(tokens):
        if token.startswith(prefix):
            return token[len(prefix) :]
        if token == option and index + 1 < len(tokens):
            return tokens[index + 1]
    return None


def kubectl_index(tokens: list[str]) -> int | None:
    for index, token in enumerate(tokens):
        if token == "kubectl" or token.endswith("/kubectl"):
            return index
    return None


def kubectl_verb(args: list[str]) -> tuple[str | None, list[str]]:
    skip_next = False
    filtered: list[str] = []
    for token in args:
        if skip_next:
            skip_next = False
            continue
        if token in {"--kubeconfig", "--context", "-n", "--namespace", "-o"}:
            skip_next = True
            continue
        if token.startswith("-"):
            continue
        filtered.append(token)
    if not filtered:
        return None, []
    return filtered[0], filtered[1:]


def context_discovery(args: list[str]) -> bool:
    verb, rest = kubectl_verb(args)
    if verb is None or not rest:
        return False
    return (verb, rest[0]) in CONTEXT_DISCOVERY


def validate(tokens: list[str]) -> Result:
    messages: list[str] = []
    if not tokens:
        return Result(False, ["empty command"])

    is_ssh = tokens[0] == "ssh"
    if is_ssh and not has_option(tokens, "-i"):
        messages.append("SSH-mediated commands must include an explicit identity with -i")

    kube_index = kubectl_index(tokens)
    if kube_index is None:
        messages.append("command must contain kubectl")
        return Result(False, messages)

    kubectl_args = tokens[kube_index + 1 :]
    if not has_option(kubectl_args, "--kubeconfig"):
        messages.append("kubectl command must include --kubeconfig")
    if not context_discovery(kubectl_args) and not has_option(kubectl_args, "--context"):
        messages.append("kubectl command must include --context outside context discovery")

    kubeconfig = option_value(kubectl_args, "--kubeconfig")
    if kubeconfig in {None, ""}:
        messages.append("--kubeconfig must have a non-empty value")
    context = option_value(kubectl_args, "--context")
    if not context_discovery(kubectl_args) and context in {None, ""}:
        messages.append("--context must have a non-empty value")

    verb, rest = kubectl_verb(kubectl_args)
    if verb is None:
        messages.append("kubectl verb is required")
    elif verb in MUTATING_OR_SENSITIVE_VERBS:
        messages.append(f"kubectl {verb} is not allowed through this read-only wrapper")
    elif verb not in READ_ONLY_VERBS and not context_discovery(kubectl_args):
        messages.append(f"kubectl {verb} is not in the read-only allowlist")

    if verb == "logs":
        scoped = has_option(kubectl_args, "-n") or has_option(kubectl_args, "--namespace")
        bounded = (
            has_option(kubectl_args, "--tail")
            or has_option(kubectl_args, "--since")
            or has_option(kubectl_args, "--since-time")
        )
        selector_or_target = bool(rest) or has_option(kubectl_args, "-l") or has_option(kubectl_args, "--selector")
        if not scoped:
            messages.append("kubectl logs should include an explicit namespace")
        if not selector_or_target:
            messages.append("kubectl logs should target a pod/controller or selector")
        if not bounded:
            messages.append("kubectl logs should be bounded with --tail, --since, or --since-time")

    return Result(not messages, messages or ["command passed kubectl explicit-context controls"])


def command_from_stdin() -> list[str]:
    command = sys.stdin.read().strip()
    if not command:
        return []
    try:
        return shlex.split(command)
    except ValueError as exc:
        fail(f"could not parse stdin command: {exc}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", nargs="*", help="Rendered command to run. Use -- before commands with flags.")
    parser.add_argument("--dry-run", action="store_true", help="Enforce controls and print the command without executing it.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    tokens = args.command or command_from_stdin()
    result = validate(tokens)
    for message in result.messages:
        print(("PASS " if result.ok else "FAIL ") + message)
    if not result.ok:
        return 1
    if args.dry_run:
        print("DRY-RUN " + shlex.join(tokens))
        return 0
    return subprocess.run(tokens, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
