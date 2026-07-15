---
name: systems-engineer-diagnose
description: Use when a known-good manual baseline exists but runtime logs or a modified harness may be misleading; verify rendered artifacts first, trust the baseline over altered instrumentation, and recover by changing one variable at a time.
---

# Diagnostic Discovery Loop

## Overview

Use this skill when a working manual path exists, but the current harness, generated configuration, or probe logic may have distorted what you are seeing.

The workflow is baseline-first: trust the known-good path, inspect the rendered artifact that the runtime actually consumed, and only then expand the scope of probing or automation.

When a failure appears after a structural migration, suspect a stale contract assertion or a wrapper-induced mismatch before chasing component internals.

## When To Use

Use this skill when:
- a manual provisioning or runtime path has already succeeded
- generated artifacts may differ from source templates
- logs, thresholds, or probes may be influencing behavior
- a previous diagnosis may have been based on modified instrumentation
- you need to recover confidence before adding more changes

## Workflow

1. **Establish the witness baseline**
   - Anchor on the simplest known-good path and treat it as the current truth.
   - Freeze feature scope during recovery; do not remove useful capability to simplify diagnosis.

1.5. **Run an assumption audit before edits**
   - Record what is known, what is assumed, and which assumptions are currently unverified.
   - For high-risk or runtime-sensitive changes, verify critical assumptions before implementation.
   - If a critical assumption cannot be verified quickly, narrow scope or switch to signal-gathering first.

2. **Verify the runtime artifact, not source intent**
   - Inspect what was actually rendered and consumed at runtime.
   - Reject conclusions based only on templates, generator intent, or partial logs.
   - Compare the declared source, the rendered artifact, and the runtime consumer in that order.

3. **Classify the current signal quality**
   - Label current evidence as one of: not observed, observed late, observed failure, proven failure.
   - Treat harness-influenced output as provisional until confirmed against the baseline shape.
   - If the current path diverges from a known-good baseline after a contract shift, label the issue as a likely stale contract assertion until proven otherwise.

4. **Define the next narrow hypothesis**
   - Change one meaningful variable at a time, unless a coupled interaction is the explicit hypothesis.
   - Prefer reversible, low-blast-radius edits that can be cleanly rolled back.

5. **Run with a progress gate**
   - Define the earliest proof point before running an expensive test.
   - If proof does not appear by checkpoint, stop early and improve control/visibility rather than extending run time.

6. **Use independent calibration**
   - Compare the ambiguous path against a known-good comparator.
   - If the comparator is healthy and the current path is noisy, suspect harness/config drift first.

7. **Perform divergence analysis after witness**
   - Compare witness vs noisy path deltas (config, timing, environment, probe placement, defaults).
   - Rank deltas by failure type and stage relevance; allow multi-factor causes when evidence suggests coupling.
   - Give extra weight to differences introduced by retired wrapper layers or moved producer/consumer boundaries.

8. **Escalate to authoritative research when controls fail**
   - If added controls still do not produce clear evidence, stop guessing.
   - Use source/docs/help/proven examples to discover better built-in observability and control points.

9. **Repeat the loop with tighter scope**
   - Convert the top-ranked delta into the next smallest experiment.
   - Keep conclusions provisional until replicated under stable controls.

## Progress-Gated Testing

Expensive tests should continue only while they are still producing signals that increase confidence.

1. **Define the first proof point before running the test**
   - Name the earliest signal that would show the run is on track.
   - If you cannot name a clear first proof point, the run is too expensive to justify yet.

2. **Add or improve exit controls before extending a weak workflow**
   - If the workflow does not let you stop on unclear signals, make that control path first.
   - Isolate why the signal is unclear: wrong change, too-late change, probe in the wrong place, or harness interference.

3. **Continue only while the run is actively gaining confidence**
   - A run that is clearly progressing should continue.
   - A run that is quiet, ambiguous, or contradictory should stop early rather than consume more time.

4. **Use thresholds as checkpoints, not proof**
   - If a signal is missing at the expected threshold, record that as a warning or inconclusive state first.
   - If the signal still does not appear on rerun, reconsider the change instead of extending the timeout.

5. **Treat missing signal after a control fix as evidence**
   - If you added the missing control and the signal still does not appear, the absence now matters.
   - That usually means the change is wrong, incomplete, or arriving too late in the process.

## Research Fallback

If you have added or adjusted signal controls and the expensive test is still ambiguous, stop the run and research before trying again.

1. **Prefer authoritative sources for the tooling**
   - Review the component source code, official docs, and proven examples for the tools that control the workflow.
   - Learn what the tool already exposes before inventing new probes or assumptions.

2. **Use research to improve control and visibility**
   - Look for supported flags, debug modes, state files, logs, hooks, or protocol points that provide clearer evidence.
   - Favor controls already designed into the tool over bespoke guesswork layered on top.

3. **Return with a better hypothesis**
   - After research, rerun with the narrowest change that improves signal quality.
   - If the new control still does not produce clear evidence, stop again rather than extending the expensive run.

## Feature Preservation Under Recovery

Recovery work must not quietly trade away useful capabilities just to make the test path easier.

1. **Preserve valuable features by default**
   - If a capability already belongs to the system, treat it as part of the baseline unless the baseline itself proves it is broken.
   - Do not remove a useful feature simply because the current proof path is more convenient without it.

2. **Separate feature scope from recovery scope**
   - Keep debug instrumentation, proof logic, and recovery controls outside the core provisioning path whenever possible.
   - If a feature needs to be disabled temporarily, do so explicitly and locally, not by widening the blast radius into unrelated behavior.

3. **Treat feature loss as a design signal**
   - If restoring a working baseline requires removing a valuable feature, pause and reassess the boundaries.
   - That usually means the new complexity has entered the wrong layer or is entangled with core behavior.

4. **Keep the feature set frozen during recovery**
   - Recovery is for re-establishing correctness, not for expanding behavior.
   - Reintroduce valuable automation only after the baseline is stable again and the new boundary is clear.

## Independent Calibration Signals

When a known-good alternative path exists, use it as an external calibration signal for expensive or ambiguous runs.

1. **Use the calibration path as a comparator**
   - Treat the known-good path as a reference shape for early progress.
   - Compare the current run against that shape instead of relying on intuition alone.

2. **Use the signal to decide whether to continue**
   - If the current run is not producing signals that resemble the known-good path by the expected checkpoint, confidence should drop quickly.
   - That is a reason to stop and reassess, not to extend the run on hope.

3. **Separate system failure from harness drift**
   - If the calibration path is clean but the current path is noisy, the new complexity or instrumentation is the likely suspect.
   - If both paths are noisy in similar ways, the underlying system may have changed.

4. **Use the calibration signal to prevent overfitting**
   - A stable comparator keeps one noisy run from becoming the whole theory.
   - It also shows when a new probe has drifted too far from a known-good behavior pattern.

## Divergence Analysis After Witness

When a clear witness path succeeds, pause and compare the ambiguous path against that witness before continuing.

1. **Stop after the first proof point**
   - Do not immediately keep iterating once a known-good signal has appeared.
   - Use the witness as a reference point for the next judgment.

2. **Compare the delta, not just the outcome**
   - Identify what changed between the witness path and the noisy path:
     - configuration
     - environment
     - timing
     - frontend mode
     - probe placement
     - harness behavior
     - hidden defaults
   - The goal is to find the smallest meaningful difference set, not to guess.

3. **Rank the delta by failure type**
   - Different failure shapes imply different relevant changes.
   - A timeout, prompt, crash loop, or missing fetch does not point to the same causes.
   - Use the failure type to decide which differences matter most.

4. **Allow multi-factor causes**
   - Do not assume one variable explains the gap.
   - Sometimes the failure only appears when multiple conditions coincide.
   - Treat the distinguishing delta as a possible combination, not a single knob.

5. **Use research when the causal delta is not obvious**
   - If the relevant interaction is unclear, research the tooling, source code, or authoritative docs.
   - Let the tool’s documented behavior narrow the likely causes before the next expensive run.

6. **Turn the delta into the next narrow experiment**
   - The next run should test the top candidate difference(s), not reopen the whole problem.
   - Keep the follow-up experiment focused on the most likely causal delta.

## Delta Prioritization and Capability Discovery

After you identify a delta, decide which parts matter most and whether the tool exposes better ways to observe or control them.

1. **Ask which delta matters most**
   - Rank candidate differences by failure type and stage relevance.
   - Favor differences that plausibly affect the exact stage that failed.
   - Allow for interaction effects when the failure shape suggests more than one change is required.

2. **Ask how to discover more relevant capabilities**
   - Research the tool’s source, docs, help text, and proven examples for controls that sharpen the delta.
   - Look for built-in flags, hooks, logs, state checkpoints, or environment variables that make the relevant distinction clearer.

3. **Use discovery to tighten the next experiment**
   - Pick the narrowest follow-up that tests the highest-value delta with the best available controls.
   - Prefer an experiment that reduces ambiguity over one that merely repeats the same uncertainty.

## Complexity Budget and Boundary Discipline

Every additional probe, gate, or debug mode consumes complexity budget.

1. **Do not stack complexity into the core flow**
   - If a probe or gate is needed, prefer moving it to an optional overlay or companion path.
   - Avoid making observability or validation a prerequisite for basic correctness.

2. **Replace before adding**
   - If a new mechanism improves clarity, it should replace an older mechanism when possible instead of layering on top of it.

3. **Stop when complexity starts forcing feature removal**
   - If the only way to recover a working state is to remove useful behavior, the boundary is wrong.
   - Redesign the split between core behavior and inspection behavior before continuing.

## Operating Rules

- Prefer the simplest known-working path until a new hypothesis is validated.
- Keep debug instrumentation opt-in and isolated from the default flow.
- Treat brittle “tests of tests” as low-value unless they protect a durable contract.
- Label conclusions as provisional when they depend on modified instrumentation.
- Verify the rendered output before making claims about runtime behavior.
- For high-risk paths, run and record an assumption audit before implementation (known facts, assumptions, unverified assumptions).
- Preserve useful features unless the baseline proves they are the problem.
- Keep recovery changes from shrinking the system’s useful behavior.
- If a deployment contract changed, verify the producer, rendered artifact, and runtime consumer together before changing component internals.

## References

For detailed rationale, risks, mitigation strategies, and reporting guidance, read [references/recovery_principles.md](references/recovery_principles.md).

## Cross-Discipline Inspiration

This skill intentionally borrows from a few human disciplines that handle ambiguity, expensive iteration, and evidence-driven recovery well:

- **Experimental science**: use baselines, controls, and one-variable-at-a-time changes.
- **Differential diagnosis**: rank likely causes by symptom shape, timing, and interaction effects.
- **Reliability engineering**: use progress gates, early exits, and operational signal instead of hope.
- **Forensic analysis**: preserve evidence and compare working versus failing states.
- **Bayesian inference**: update confidence as evidence quality changes and stop when confidence is too weak to justify more cost.
- **Change control / safety engineering**: keep valuable capabilities intact while recovering the system.
