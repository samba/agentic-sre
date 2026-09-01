---
name: systems-engineer-diagnose
description: Use when a known-good baseline exists but runtime behavior, generated artifacts, a harness, instrumentation, or probes produce ambiguous or contradictory evidence. Recover confidence with controlled comparisons and discriminating experiments before proposing changes.
---

# Systems Diagnostic Loop

For coordinated participation, assurance/control review, and authority, follow
the [coordinated handoff contract](references/coordinated-handoff.md).
This specialty contributes diagnostic/experiment guidance when ambiguity
recurs; reviews hidden failure modes and weak signals; and assesses bugs through
plausible causal paths, affected environments, and discriminating probes.

Diagnose ambiguous systems failures without turning noisy instrumentation into
false certainty. Anchor on the simplest known-good witness, inspect the artifact
the runtime consumed, and choose the cheapest probe that can distinguish the
leading explanations.

The large [recovery principles](references/recovery_principles.md) reference is
a conditional rationale and pattern catalog. Read only the relevant topic when
the compact loop below does not resolve the case; it is not a second workflow.
Source foundations are in the
[skill source history](references/sources.md).

## Compact Loop

1. **Bound the incident.** Record the symptom, impact, current authority, time
   and probe budgets, stop condition, and valuable behavior that must not be
   removed merely to simplify diagnosis.
2. **Establish a witness.** Reproduce or identify the simplest known-good path,
   its environment, inputs, timing, and earliest progress signals. If no
   credible baseline exists, say so and switch to evidence discovery.
3. **Inspect consumed reality.** Compare declared source, generated/rendered
   artifact, runtime consumer, and observed state in that order. Treat logs or
   probes altered by the harness as provisional.
4. **Audit knowledge.** Separate observations, assumptions, and conclusions.
   Classify the current signal as `not-observed`, `observed-late`,
   `observed-failure`, or `proven-failure`.
5. **Rank hypotheses.** For each viable explanation record predicted
   observation, contrary evidence, discriminating probe, cost, mutation, and
   retry count. Attempt to falsify the leading hypothesis before recommending a
   consequential remedy.
6. **Run one bounded experiment.** Change one meaningful variable unless a
   coupled interaction is the explicit hypothesis. Define the earliest proof
   point and stop when the run is no longer increasing information.
7. **Compare and update.** Diff witness and failing paths across configuration,
   environment, timing, defaults, producer/consumer contract, instrumentation,
   and dependencies. Allow multi-factor causes when evidence requires them.
8. **Escalate intelligently.** When built-in controls or documented behavior
   are unclear, research source, official documentation, help, and proven
   examples before adding probes. Prefer supported diagnostics over bespoke
   instrumentation.
9. **Conclude or repeat.** Replicate a causal result under stable controls, or
   run the next cheapest discriminating experiment. Do not repeat an unchanged
   inconclusive probe after its budget is exhausted.

## Safety And Complexity

- Keep diagnosis and instrumentation opt-in, reversible, and outside the core
  production path where practical.
- Freeze feature scope during recovery. Temporary feature disablement must be
  explicit and local; permanent feature loss is a design signal, not a normal
  diagnostic shortcut.
- Replace obsolete probes when a clearer one is introduced instead of stacking
  permanent complexity.
- Preserve evidence and exact commands while redacting secrets and sensitive
  data.
- Diagnosis recommends a mutation; it does not authorize it. A destructive,
  privileged, externally consequential, or broader-scope test requires the
  caller's authority.

## Handoff

Return handoff contract version 2 with `gate_id: diagnosis`, applicability,
scope, witness, artifacts actually examined, confirmed and rejected
hypotheses, contrary evidence, experiments and results, residual uncertainty,
budget state, recommended next action, and earliest rework stage. Use canonical
recommendations only; a diagnosis normally reports `pass` when its stated
diagnostic criterion is established, `fail` for a falsified candidate or unmet
criterion, and `blocked` when no safe informative probe remains.
