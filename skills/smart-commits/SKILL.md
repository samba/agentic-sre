---
name: smart-commits
description: Use when creating or rewriting commit messages so AI-generated commits are semantically meaningful, evidence-backed, and concise. Enforces a strong subject line and a bounded, context-rich body.
---

# Smart Commits

## Use This Skill When

Use this skill when:

- creating a new commit,
- amending a commit message,
- rewriting commit history for clarity,
- generating commit messages from AI-assisted changes.

## Goal

Produce commit messages that are clear, audit-friendly, and technically useful without being bloated.

The output must include:

1. a semantically significant descriptive subject line,
2. a short body with rationale, impact, and proof points,
3. complexity-aware detail only when justified.

## Required Structure

### Subject (first line)

- Imperative or direct descriptive form.
- Must state what changed at a meaningful semantic level (not generic wording like "update files").
- Keep concise, but specific.

### Body (default)

- At least a few sentences.
- Must briefly explain:
  - rationale (why this change was needed),
  - impact (bug fix, value-add, risk reduction, behavior change, etc.),
  - proof points (tests run, validation checks, observed outcomes, or explicit note if not run).

## Complex Commit Policy

For large/complex commits, the body may expand, but with strict limits:

- Maximum 4 paragraphs total.
- At most 2 bulleted lists total.
- Include, where relevant:
  - risks resolved and/or unmitigated,
  - failing test scopes,
  - newly integrated test scopes,
  - modules/components with changed behavior.

Prefer compact paragraphs over long bullet dumps.

## Quality Rules

- Do not use `WIP` unless explicitly requested.
- Do not leave proof status ambiguous; state what was validated and what was not.
- Avoid empty claims like "improves performance" without a proof point.
- Keep tone factual and accountable.
- Avoid excessive verbosity; include only information that helps future debugging, review, or rollback decisions.

## Workflow

1. Identify semantic intent of the change.
2. Draft a precise subject line.
3. Write a short body covering rationale, impact, and proof points.
4. If commit scope is complex, add bounded extra detail (within paragraph/list limits).
5. Run a final brevity and specificity check before committing.

## Output Template

Subject line

Rationale: <1-2 sentences>
Impact: <1-2 sentences>
Proof: <tests/checks/results or explicit "not run">

Optional complex section (only when needed):

- Risks: <resolved/unmitigated>
- Behavior changes: <modules/components>
- Testing scope: <new/failing/not run>
