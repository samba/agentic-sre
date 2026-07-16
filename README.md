# agentic-sre

A curated skill set for agentic software and systems work.

This repository exists to improve day-to-day agent output quality through reusable, high-leverage skills. The primary value is not automation glue; it is the operational behavior encoded in each skill.

## Intent

These skills are designed to make agent work:

- more evidence-based,
- more consistent with your coding style,
- safer in high-risk systems tasks,
- easier to audit and maintain over time.

## Core Capabilities

### `systems-engineer-assist`

Use this before and during systems-facing changes (scripts, packaging, Kubernetes, Linux config).

What it adds:

- mandatory pre-authoring research against target distro/runtime constraints,
- explicit compatibility checks before rollout,
- structured post-generation validation,
- disciplined failure handling with smallest-safe-delta iteration.

Best for:

- cross-distro packaging/deployment work,
- service configuration changes,
- infra code where environment drift can break generated artifacts.

### `systems-engineer-diagnose`

Use when a manual path is known-good but automated/harnessed runs are noisy or contradictory.

What it adds:

- baseline-first diagnostics,
- inspection of runtime-consumed artifacts (not template intent),
- one-variable-at-a-time hypothesis testing,
- progress-gated expensive test runs.

Best for:

- flaky provisioning,
- misleading logs,
- harness-induced false negatives.

### `security-compliance-review`

Use before committing design or implementation work that could affect security, compliance posture, audit evidence, customer trust, or certification readiness.

What it adds:

- proactive security and compliance review gates,
- ISO/IEC 27001 and ISO/IEC 27017 risk/control framing,
- SOC 2 evidence and Trust Services Criteria awareness,
- CMMI-style process maturity checks,
- concrete blocker/follow-up/advisory output for pre-commit review.

Best for:

- new projects and services,
- cloud services and customer-facing systems,
- changes touching data handling, access control, auditability, supplier dependencies, secrets, logging, monitoring, backup, or CI/CD.

### `langgen`

Use for generated structured config or custom language/tooling work driven by authoritative corpora.

What it adds:

- corpus-first grammar/AST derivation,
- strict validation gates before broad generation,
- optional EBNF/parser/interpreter production,
- configurable runtime mapping for operators/stdlib behavior.

Best for:

- DSL/config parser generation,
- hardening generated config correctness,
- validating language rules against real upstream examples.

### `learn-code-style`

Use to infer and persist coding preferences from real user-authored examples.

What it adds:

- language-specific style extraction,
- persistent style ledger updates,
- downstream reuse during feature, bugfix, and refactor tasks.

Best for:

- reducing stylistic churn in AI-authored diffs,
- improving reviewability,
- preserving team conventions across languages.

### `smart-commits`

Use when writing or rewriting commit messages.

What it adds:

- stronger semantic subject lines,
- concise rationale/impact/proof body structure,
- bounded detail for larger commits without commit-message sprawl.

Best for:

- auditability,
- faster PR/review context loading,
- clearer rollback/debug history.

## Recommended Usage Pattern

Treat skills as task triggers:

1. identify the risk profile of the task,
2. invoke the matching skill(s) explicitly,
3. execute with the skill’s workflow and gates,
4. keep results and revisions in git.

A practical default mapping:

- systems change planned: `systems-engineer-assist`
- noisy/ambiguous failure: `systems-engineer-diagnose`
- generated grammar/config pipeline: `langgen`
- style consistency needed: `learn-code-style`
- commit quality pass: `smart-commits`

## Repository Structure

```text
.
├── Makefile
└── skills/
    └── <skill-name>/
        ├── SKILL.md
        ├── references/   (optional)
        ├── scripts/      (optional)
        └── assets/       (optional)
```

## Skill Domain Boundary

This repository should only version skills that improve software engineering, systems engineering, infrastructure troubleshooting, language/config generation, code style alignment, or commit quality.

Before adding or syncing a skill into this repo, verify that it belongs to this domain. Planning, reflection-loop, product workflow, OpenAI API, plugin authoring, document rendering, image generation, and general marketplace/installer skills belong in a different skill stack unless they directly support the SRE/software systems domain here.

`make import` is intentionally broad: it copies every discovered `SKILL.md` directory from supported local agent homes into `./skills`, replacing same-named directories. Treat imported untracked skill directories as review candidates, not automatically accepted repo content. Remove irrelevant imported directories before staging changes.

## Minimal Operations

This repo includes sync helpers, but they are operational support, not the core product:

- `make import`: pull discovered skills from supported local agent homes into `./skills`
- `make install`: publish `./skills` to supported local agent homes

Supported homes:

- `~/.codex`
- `~/.claude`
- `~/.cursor`
