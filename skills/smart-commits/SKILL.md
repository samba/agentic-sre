---
name: smart-commits
description: Use when arranging a working draft into topical, reviewable commits or when creating or rewriting commit messages. Uses task and thread context plus the actual diff to preserve intent, ownership, dependency order, revision-bound proof, and concise rationale/impact/proof messages.
---

# Smart Commits

For coordinated participation and authority, follow the
[coordinated handoff contract](references/coordinated-handoff.md).
This specialty contributes goal-traceability guidance; reviews history for
hidden scope, untraceable behavior, or missing proof without treating message
style as correctness; and assesses bugs for provenance and change-isolation
risk.

## Use This Skill When

Use this skill when:

- a request to commit encounters changes spanning more than one semantic topic,
- arranging tracked or untracked working-draft changes into atomic commits,
- creating a new commit,
- amending a commit message,
- rewriting commit history for clarity,
- generating commit messages from AI-assisted changes.

## Goal

Produce commit messages that are clear, audit-friendly, and technically useful without being bloated.

When a working draft contains multiple topics, produce the smallest coherent
commit series whose members are independently understandable, reviewable, and
revertible. Read
[working-draft partitioning](references/working-draft-partitioning.md) before
planning, staging, or executing that series.

The Git title/body behavior supporting this convention is linked in the
[skill source history](references/sources.md); rationale/impact/proof
labels are a local auditability policy.

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

1. Inspect the index, unstaged changes, untracked paths, and relevant task and
   thread context. If more than one semantic topic is present, apply the
   partitioning workflow before message generation.
2. Identify the semantic intent and exact content of the next proposed commit.
3. Draft a precise subject line.
4. Write a short body covering rationale, impact, and proof points.
5. If commit scope is complex, add bounded extra detail within the limits.
6. Run a final topical-cohesion, brevity, and specificity check.
7. For orchestrated work, consume the coordinator's revision-bound evidence
   summary. Verify that the tested revision matches the proposed commit tree;
   stale or partial evidence cannot support broader claims. This leaf text
   transformation does not require a specialist gate handoff.
8. Treat partition planning, index mutation, message generation, commit
   execution, and history rewriting as separate capabilities.
   Execute a commit only when the caller's autonomy envelope authorizes that
   side effect. Do not infer permission to rewrite existing history from
   permission to create new commits. A commit never implies release approval.

## Output Template

Subject line

Rationale: <1-2 sentences>
Impact: <1-2 sentences>
Proof: <tests/checks/results or explicit "not run">

Optional complex section (only when needed):

- Risks: <resolved/unmitigated>
- Behavior changes: <modules/components>
- Testing scope: <new/failing/not run>

For orchestrated work also include intent/task identifiers, tests actually
run, exact results, security-gate status, known exceptions, and
generated-artifact provenance when applicable. Derive these from evidence,
not agent memory.

For a partitioned draft, first return the ordered topic plan, affected paths or
hunks, dependency rationale, proposed validation, ambiguity/ownership notes,
and whether execution is authorized. After execution, return each commit id,
subject, included scope, exact validation result, and remaining working-tree
state.
