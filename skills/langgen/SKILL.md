---
name: langgen
description: Use when debugging generated structured configs or deriving language tooling from authoritative corpora; compare against upstream examples, derive strict AST rules, optionally emit EBNF, build parsers, and generate interpreters with runtime-configurable operator and stdlib mappings.
---

# Langgen

## Short Command Mode

Support this shorthand invocation form:

`langgen [optional target language mapping] <research terms for internet corpus material acquisition>`

Rules:
- The optional target language mapping is a single word naming an existing language (for example: `Python`, `javascript`, `go`, `lua`, `c`).
- If omitted, derive target language mapping from languages already used in the current project.
- Treat remaining terms as corpus-acquisition search intent.
- Acquire authoritative sources first, then continue in standard workflow.

## Corpus Acquisition Heuristic (Gated)

Use sample-count ranges as heuristics, but decide readiness by coverage gates.

Sample-range guidance:
- Minimum viable: 30-50 authoritative samples.
- Usually solid: 100-200 samples.
- Complex or heterogeneous language surfaces: 300+ samples.

Coverage gates (all required before language production mode):
1. Core grammar coverage gate
- Observe every core production class at least once in corpus.
2. Operator coverage gate
- Observe all targeted operators and representative precedence/associativity interactions.
3. Declaration/function coverage gate
- Observe representative declaration forms and callable/function forms used in target usage.
4. Negative-shape coverage gate
- Include invalid/known-bad fixtures for rejection validation.
5. Holdout conformance gate
- On an unseen holdout slice, parser+validator conformance must meet target (default: >=99% parse+validate success for authoritative samples).

If sample count is high but one or more gates fail, continue corpus acquisition instead of forcing production.

If online research cannot produce enough samples to satisfy gates:
- Warn explicitly that corpus sufficiency is not met.
- Report which gates failed and which structures remain underrepresented.
- Restrict output to provisional artifacts (validator/grammar draft) unless user explicitly accepts higher risk.

## Overview

Use this skill when generated structured artifacts appear wrong, or when a corpus should drive language tooling. Start corpus-first: gather authoritative upstream examples, infer structure, and lock acceptance on corpus-backed rules.

## Modes

1. Validation mode (default)
- Derive strict AST validation rules from an authoritative corpus.
- Ensure upstream samples pass while known-bad generated variants fail.

2. Language production mode (optional)
- Emit an EBNF representation to a project-specific file.
- Build parser implementations in project-required languages.
- Build an interpreter that maps AST nodes to registered runtime functions.

3. Local EBNF mode (optional)
- Ingest a project-local EBNF spec as the primary grammar source.
- Generate parser/validator/interpreter artifacts directly from the local spec.
- Use corpus and runtime checks to refine ambiguities in the local grammar.

## Workflow

1. Collect authoritative corpus
- For new corpus-driven work, initialize a local scaffold first:
  - `python3 skills/langgen/scripts/scaffold.py init --root <parent> --name <language-or-domain> --target <target-language>`
- Download/mirror upstream samples from official sources.
- Treat these as the acceptance corpus.
- During collection, search for open-source EBNF/grammar specifications for the same language/version and record provenance.
- Register acquired samples as they are added:
  - authoritative samples: `python3 skills/langgen/scripts/scaffold.py add-sample --root <scaffold-root> --source <source-kind> --path <sample-file>`
  - holdout samples: add `--holdout`
  - invalid or generated-regression samples: add `--known-bad`

2. Derive structural model
- Infer token classes and grammar shape from corpus evidence.
- Build strict AST shape rules from observed structure.
- If authoritative EBNF exists, reconcile corpus-derived structure against it and document resolved differences.

3. Validate generated output
- Run parser/validator over generated artifacts.
- If upstream fails, fix rule/model first.
- If upstream passes and generated fails, fix generation path.

4. Record regression fixtures
- Keep failing generated shapes as regression fixtures.
- Refresh report skeletons after corpus or fixture changes:
  - `python3 skills/langgen/scripts/scaffold.py report --root <scaffold-root>`
- Use `reports/corpus-coverage.json`, `reports/holdout-conformance.json`, and `reports/rejection-conformance.json` to document gate status and unresolved gaps.

5. Optional: produce language artifacts
- If requested, emit grammar, parser(s), and interpreter runtime assets.

5a. Optional: local EBNF artifact production
- If a local EBNF spec is provided, treat it as primary grammar input.
- Generate parser/validator/interpreter outputs from local EBNF before corpus-derived synthesis.
- Validate local EBNF-driven outputs against corpus and runtime conformance gates.

6. Optional: external runtime execution loop
- If requested and safe in environment, execute generated expressions/program fragments with external compilers/interpreters.
- Compare runtime outcomes with parser/interpreter expectations to refine grammar and semantic mapping rules.
- Use smallest reproducible expression sets and keep failing cases as regression fixtures.

## EBNF Output Option

When requested, emit a project-local EBNF file representing the corpus-derived grammar.

Suggested output path pattern:
- `grammar/<language-name>.ebnf`
- In scaffolded projects, place generated grammar output under `<scaffold-root>/grammar/`.

Requirements:
- Keep EBNF aligned to accepted corpus structure.
- Include comments for intentionally constrained or corpus-specific productions.
- Prefer authoritative open-source EBNF as seed input when available, then patch with corpus-observed deltas.
- Record source URL/ref and version alignment for imported grammar material.

## Open-Source EBNF Research Option

When internet research is enabled, search for open-source grammar representations before deriving everything from corpus alone.

Source priority:
1. upstream project grammar/spec repositories,
2. official language/reference specs,
3. maintained parser-project grammars with clear version tags.

Use discovered grammars as bootstrap input, not unquestioned truth:
- corpus acceptance still governs final validator behavior,
- unresolved conflicts must be reported explicitly.

## Local EBNF Input Option

When a project already defines EBNF locally, support direct ingestion as an authoritative input candidate.

Suggested input path pattern:
- `grammar/*.ebnf`

Behavior:
- Parse local EBNF and generate parser/validator/interpreter scaffolding from it.
- Preserve local production names where possible to keep project terminology stable.
- Detect and report grammar ambiguities, left-recursion issues, or unsupported constructs in target parser backends.
- Reconcile local EBNF with corpus observations; when they diverge, report the mismatch and require an explicit selection policy.

Output expectation:
- Emit generated artifacts plus a reconciliation report documenting local-EBNF vs corpus/runtime deltas.

## Parser Generation Option

When requested, generate parser implementations in project-required languages.

Requirements:
- Keep parser behavior equivalent across target languages.
- Keep AST node schema stable across implementations.
- Validate each parser against:
  - authoritative corpus (must pass),
  - known-bad fixtures (must fail).

Suggested output path pattern:
- `parsers/<target-language>/...`
- In scaffolded projects, place generated parsers under `<scaffold-root>/generated/parsers/`.

## Interpreter Generation Option

When requested, generate an interpreter that:

1. Walks the AST,
2. maps AST functions/operators to registered runtime handlers,
3. resolves declared functions through runtime namespace mappings,
4. evaluates according to runtime configuration.

Suggested output path pattern:
- `interpreter/<target-language>/...`
- In scaffolded projects, place generated interpreters under `<scaffold-root>/generated/interpreters/`.

## Runtime Mapping Model

Interpreter runtime must support:

1. Operator mapping dictionary
- maps operator tokens to runtime handler IDs.

2. Function lexicon dictionary
- maps declared function names to runtime-callable handlers.

3. Namespace/stdlib mapping dictionary
- maps language-specific standard-library symbols into runtime namespace entries.

By default:
- use Lua-style operator execution with pre-registered default handlers (`lua-default`).

## Built-in Dictionary Profiles

Provide and support profile dictionaries for:

- `lua-default`
- `python-default`
- `javascript-default`
- `c-default`
- `go-default`

Use references:
- `references/operator-profiles.json`
- `references/stdlib-profiles.json`

Override behavior:
- start from selected profile,
- merge project overrides,
- fail fast on unknown operators/functions unless runtime explicitly allows unresolved symbols.

## Validation Rules for Generated Tooling

For parser/interpreter outputs, enforce:

1. Corpus conformance
- authoritative corpus parses and validates cleanly.

2. Rejection conformance
- known-bad fixtures fail with stable error classes.

3. Round-trip conformance (when serializer exists)
- parse -> AST -> serialize -> parse remains schema-equivalent.

4. Profile conformance
- operator and stdlib mapping behavior matches selected runtime profile.

5. External runtime conformance (when execution loop is enabled)
- generated expression fixtures evaluate consistently between:
  - generated interpreter semantics, and
  - selected external compiler/interpreter runtime.
- mismatches must produce actionable diffs and regression fixtures.

## External Compiler/Interpreter Execution Option

Allow optional invocation of external toolchains to refine parser/interpreter rules.

Requirements:
- tool/runtime version must be captured and tied to target language profile,
- execution must run in smallest safe sandbox available,
- test sets must include both expected-pass and expected-fail expressions,
- semantic mismatches feed back into grammar/rule refinement before widening scope.

If external execution is unavailable:
- warn user,
- continue with structural validation only,
- mark semantic confidence as reduced.

## Operating Rules

- Trust authoritative corpus over assumptions.
- Keep AST validator strict and local.
- Prefer one canonical parser/validator model with generated adapters over divergent logic.
- If rule rejects upstream, fix rule before widening scope.
- If runtime mapping changes semantics, capture it in explicit profile/override dictionaries.

## Useful Outputs

- Corpus snapshot from authoritative source.
- Minimal strict AST validator.
- Project EBNF grammar file (optional).
- Parser implementations for required languages (optional).
- Interpreter with runtime mapping dictionaries (optional).
- Regression fixture set for failing generated shapes.
