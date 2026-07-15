#!/usr/bin/env python3
"""Create and maintain langgen corpus scaffolds."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Any


SCHEMA_VERSION = 1
SAFE_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,79}$")
SAFE_SOURCE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:-]{0,79}$")

DIRECTORIES = (
    "corpus/authoritative/samples",
    "corpus/holdout",
    "corpus/known-bad",
    "grammar",
    "fixtures/valid",
    "fixtures/invalid",
    "reports",
    "generated/parsers",
    "generated/validators",
    "generated/interpreters",
)

METADATA_FILE = "langgen.json"
PROVENANCE_FILE = "corpus/provenance.json"


class ScaffoldError(Exception):
    """User-facing scaffold failure."""


def fail(message: str) -> None:
    raise ScaffoldError(message)


def validate_name(value: str, label: str) -> str:
    if not SAFE_NAME.fullmatch(value):
        fail(
            f"invalid {label} {value!r}: use 1-80 letters, digits, dots, "
            "underscores, or hyphens; start with a letter or digit"
        )
    if value in {".", ".."} or value.startswith("."):
        fail(f"invalid {label} {value!r}: hidden or traversal-like names are not allowed")
    return value


def validate_source_kind(value: str) -> str:
    if not SAFE_SOURCE.fullmatch(value):
        fail(
            f"invalid source kind {value!r}: use 1-80 letters, digits, dots, "
            "underscores, hyphens, or colons; start with a letter or digit"
        )
    return value


def resolve_existing_dir(path: Path, label: str) -> Path:
    resolved = path.expanduser().resolve()
    if not resolved.is_dir():
        fail(f"{label} does not exist or is not a directory: {path}")
    return resolved


def resolve_existing_file(path: Path, label: str) -> Path:
    resolved = path.expanduser().resolve()
    if not resolved.is_file():
        fail(f"{label} does not exist or is not a file: {path}")
    return resolved


def ensure_within(path: Path, root: Path, label: str) -> Path:
    try:
        path.relative_to(root)
    except ValueError:
        fail(f"refusing unsafe write outside scaffold root for {label}: {path}")
    return path


def read_json(path: Path, default: dict[str, Any]) -> dict[str, Any]:
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        fail(f"expected JSON object in {path}")
    return data


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, sort_keys=True)
        handle.write("\n")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def relative_posix(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def load_scaffold_root(path: Path) -> tuple[Path, dict[str, Any]]:
    root = resolve_existing_dir(path, "scaffold root")
    metadata_path = root / METADATA_FILE
    if not metadata_path.is_file():
        fail(f"missing {METADATA_FILE}; run init first: {root}")
    metadata = read_json(metadata_path, {})
    if metadata.get("schema_version") != SCHEMA_VERSION:
        fail(f"unsupported scaffold schema in {metadata_path}")
    return root, metadata


def ensure_scaffold_dirs(root: Path) -> None:
    for directory in DIRECTORIES:
        target = ensure_within(root / directory, root, directory)
        target.mkdir(parents=True, exist_ok=True)


def command_init(args: argparse.Namespace) -> int:
    name = validate_name(args.name, "name")
    target_language = validate_name(args.target, "target language")
    parent = Path(args.root).expanduser().resolve()
    parent.mkdir(parents=True, exist_ok=True)
    if not parent.is_dir():
        fail(f"root parent is not a directory: {args.root}")

    scaffold_root = ensure_within(parent / name, parent, "scaffold root")
    scaffold_root.mkdir(parents=True, exist_ok=True)
    ensure_scaffold_dirs(scaffold_root)

    metadata_path = scaffold_root / METADATA_FILE
    metadata = {
        "name": name,
        "schema_version": SCHEMA_VERSION,
        "target_language": target_language,
    }
    if metadata_path.exists():
        existing = read_json(metadata_path, {})
        if existing != metadata:
            fail(
                f"existing scaffold metadata differs in {metadata_path}; "
                "choose a new name or reconcile it manually"
            )
    else:
        write_json(metadata_path, metadata)

    provenance_path = scaffold_root / PROVENANCE_FILE
    if not provenance_path.exists():
        write_json(
            provenance_path,
            {
                "samples": [],
                "schema_version": SCHEMA_VERSION,
            },
        )

    print(scaffold_root)
    return 0


def sample_destination(root: Path, sample_path: Path, holdout: bool, known_bad: bool) -> Path:
    if holdout and known_bad:
        fail("--holdout and --known-bad are mutually exclusive")
    filename = validate_name(sample_path.name, "sample file name")
    if known_bad:
        directory = root / "corpus/known-bad"
    elif holdout:
        directory = root / "corpus/holdout"
    else:
        directory = root / "corpus/authoritative/samples"
    return ensure_within(directory / filename, root, "sample")


def sample_role(holdout: bool, known_bad: bool) -> str:
    if known_bad:
        return "known-bad"
    if holdout:
        return "holdout"
    return "authoritative"


def update_provenance(root: Path, entry: dict[str, Any]) -> None:
    provenance_path = root / PROVENANCE_FILE
    provenance = read_json(
        provenance_path,
        {
            "samples": [],
            "schema_version": SCHEMA_VERSION,
        },
    )
    samples = provenance.get("samples")
    if not isinstance(samples, list):
        fail(f"expected samples list in {provenance_path}")

    kept = [
        item
        for item in samples
        if not isinstance(item, dict) or item.get("path") != entry["path"]
    ]
    kept.append(entry)
    kept.sort(key=lambda item: (item.get("role", ""), item.get("path", "")))
    provenance["samples"] = kept
    provenance["schema_version"] = SCHEMA_VERSION
    write_json(provenance_path, provenance)


def command_add_sample(args: argparse.Namespace) -> int:
    root, _metadata = load_scaffold_root(Path(args.root))
    ensure_scaffold_dirs(root)
    source_kind = validate_source_kind(args.source)
    source_path = resolve_existing_file(Path(args.path), "sample file")
    destination = sample_destination(root, source_path, args.holdout, args.known_bad)
    destination.parent.mkdir(parents=True, exist_ok=True)

    source_hash = sha256_file(source_path)
    if destination.exists():
        if not destination.is_file():
            fail(f"destination exists and is not a file: {destination}")
        if sha256_file(destination) != source_hash:
            fail(f"destination already exists with different content: {destination}")
    else:
        shutil.copyfile(source_path, destination)

    entry = {
        "path": relative_posix(destination, root),
        "role": sample_role(args.holdout, args.known_bad),
        "sha256": source_hash,
        "size_bytes": source_path.stat().st_size,
        "source_kind": source_kind,
        "source_path": str(source_path),
    }
    update_provenance(root, entry)
    print(entry["path"])
    return 0


def count_files(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for item in path.rglob("*") if item.is_file())


def command_report(args: argparse.Namespace) -> int:
    root, metadata = load_scaffold_root(Path(args.root))
    ensure_scaffold_dirs(root)
    provenance = read_json(
        root / PROVENANCE_FILE,
        {
            "samples": [],
            "schema_version": SCHEMA_VERSION,
        },
    )
    samples = provenance.get("samples", [])
    if not isinstance(samples, list):
        fail(f"expected samples list in {root / PROVENANCE_FILE}")

    counts_by_role: dict[str, int] = {
        "authoritative": 0,
        "holdout": 0,
        "known-bad": 0,
    }
    for item in samples:
        if isinstance(item, dict) and item.get("role") in counts_by_role:
            counts_by_role[item["role"]] += 1

    coverage = {
        "counts": {
            "authoritative_samples": count_files(root / "corpus/authoritative/samples"),
            "fixture_invalid": count_files(root / "fixtures/invalid"),
            "fixture_valid": count_files(root / "fixtures/valid"),
            "holdout": count_files(root / "corpus/holdout"),
            "known_bad": count_files(root / "corpus/known-bad"),
            "provenance_authoritative": counts_by_role["authoritative"],
            "provenance_holdout": counts_by_role["holdout"],
            "provenance_known_bad": counts_by_role["known-bad"],
        },
        "gates": {
            "core_grammar_coverage": "pending",
            "declaration_function_coverage": "pending",
            "negative_shape_coverage": "pending",
            "operator_coverage": "pending",
        },
        "name": metadata["name"],
        "schema_version": SCHEMA_VERSION,
        "status": "pending",
        "target_language": metadata["target_language"],
    }
    holdout = {
        "name": metadata["name"],
        "schema_version": SCHEMA_VERSION,
        "status": "pending",
        "target_language": metadata["target_language"],
        "totals": {
            "failed": 0,
            "passed": 0,
            "registered": counts_by_role["holdout"],
        },
    }
    rejection = {
        "name": metadata["name"],
        "schema_version": SCHEMA_VERSION,
        "status": "pending",
        "target_language": metadata["target_language"],
        "totals": {
            "accepted_unexpectedly": 0,
            "rejected": 0,
            "registered": counts_by_role["known-bad"],
        },
    }

    write_json(root / "reports/corpus-coverage.json", coverage)
    write_json(root / "reports/holdout-conformance.json", holdout)
    write_json(root / "reports/rejection-conformance.json", rejection)

    print(root / "reports")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create and maintain deterministic langgen corpus scaffolds."
    )
    subcommands = parser.add_subparsers(dest="command", required=True)

    init_parser = subcommands.add_parser("init", help="create a scaffold")
    init_parser.add_argument("--root", required=True, help="parent directory for the scaffold")
    init_parser.add_argument("--name", required=True, help="language or domain scaffold name")
    init_parser.add_argument("--target", required=True, help="target implementation language")
    init_parser.set_defaults(func=command_init)

    add_parser = subcommands.add_parser("add-sample", help="copy and register a sample")
    add_parser.add_argument("--root", required=True, help="existing scaffold root")
    add_parser.add_argument("--source", required=True, help="source kind or provenance class")
    add_parser.add_argument("--path", required=True, help="sample file to copy")
    add_parser.add_argument("--holdout", action="store_true", help="register as holdout corpus")
    add_parser.add_argument("--known-bad", action="store_true", help="register as known-bad corpus")
    add_parser.set_defaults(func=command_add_sample)

    report_parser = subcommands.add_parser("report", help="refresh JSON report skeletons")
    report_parser.add_argument("--root", required=True, help="existing scaffold root")
    report_parser.set_defaults(func=command_report)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except ScaffoldError as exc:
        parser.exit(2, f"error: {exc}\n")
    except json.JSONDecodeError as exc:
        parser.exit(2, f"error: invalid JSON: {exc}\n")


if __name__ == "__main__":
    sys.exit(main())
