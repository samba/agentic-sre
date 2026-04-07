---
name: learn-code-style
description: Learn and maintain language-specific coding style preferences from user-authored files, functions, commit ranges, and external style guides; apply those preferences during later feature, bugfix, and refactor work in matching languages.
---

# Learn Code Style

## Workflow

1. Determine target language(s) from the user request and evidence source.
2. Ingest style evidence from one or more sources:
- user-authored file/function samples
- commit history ranges or tags
- explicit style guides (local or internet)
3. Extract concrete, language-scoped patterns and anti-patterns.
4. Update the persistent style ledger in `references/style-ledger.md`.
5. On future authoring tasks, load only the matching language section from the ledger and apply it.

## Source-Specific Ingestion

### File or function sample

1. Read the exact file/function and nearby context.
2. Extract recurring signals:
- naming style
- control-flow shape
- error handling style
- comments/docstring density and tone
- test style and validation habits
- preferred library/runtime idioms
3. Record only repeated patterns, not one-off anomalies.

### Commit-range sample

1. Inspect a bounded range (for example `tag..HEAD`, `A^..B`).
2. Sample representative diffs across the range, not just commit subjects.
3. Separate style observations by language.
4. Record confidence and any uncertainty in the ledger.

### Internet style guides

1. Use primary sources when possible (official language/project docs, well-known style guides).
2. Record guide name, URL, and extraction date.
3. Convert guidance into actionable rules for authoring.
4. Prefer user-authored project style over generic guide defaults when conflicts occur, unless user says otherwise.

## Preference Precedence

Apply style preferences in this order:
1. Task-specific user instruction in current conversation.
2. Language-specific patterns learned from the user's own codebase/history.
3. User-approved external style guides for that language.
4. Default language conventions.

## Authoring-Time Behavior

When asked to implement, fix, or refactor:

1. Identify implementation language(s).
2. Load matching language style section(s) from `references/style-ledger.md`.
3. Apply preferred patterns directly in code edits.
4. Before writing code, call out risks from style choices that may affect behavior, performance, security, readability, or maintenance.
5. If a preferred style conflicts with correctness/safety constraints, surface the conflict and propose the smallest safe adjustment.

## Side-Effect Risk Callouts (Required)

Before initiating substantial code authoring in a language with style preferences, explicitly note likely side effects such as:
- deeper chaining reducing debuggability
- terse idioms reducing readability for mixed-skill teams
- heavy abstraction increasing indirection and test burden
- strict minimalism reducing guardrails around unsafe inputs
- strict verbosity increasing churn and review noise

Keep these callouts concise and specific to the task scope.

## Language Separation

Never merge styles across languages by default.
Maintain separate sections for each language and ecosystem (for example Bash, Python, Go, TypeScript).
When tasks span languages, apply each language's profile only to its own files.

## Ledger Maintenance

Use `references/style-ledger.md` as the persistent source of truth.
For each language entry, keep:
- preferred patterns
- discouraged patterns
- examples or evidence references
- source provenance (file/function/commit-range/style-guide URL)
- confidence level and last-updated date

Update instead of duplicating entries. Keep entries concise and operational.

## Quick Commands

Use `scripts/style_signals.sh` to collect basic style signals from a language-specific path.
Use it as a helper, not as the only source of truth.

## Output Contract

When the user asks to "learn my style":
1. Summarize extracted style by language.
2. State what was written/updated in the ledger.
3. Note any unresolved ambiguity.

When the user asks to author code later:
1. State which language profile was applied.
2. State key style choices used.
3. Include side-effect risk callouts before implementation.
