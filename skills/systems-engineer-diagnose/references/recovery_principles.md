# Recovery Principles

This reference expands the diagnostic discovery loop workflow into practical guidance for debugging systems that have already demonstrated a working manual path.

## Why the baseline matters

A known-good manual baseline is the strongest available truth because it demonstrates the system can work without the extra machinery of automation, instrumentation, or threshold logic. Once a harness is added, the harness can change timing, shell mode, network exposure, or prompt behavior. That means the harness is no longer neutral evidence.

When a failure appears after the harness changes, the first question should be whether the harness itself has altered the behavior enough to invalidate the observed signal.

## Why rendered artifacts matter

Source templates, generator intent, and runtime artifacts are not the same thing.

Examples:
- a preseed template may render differently after env substitution or stripping rules
- a generated bundle may omit profile values even when the source env file looks correct
- a probe may inspect a stage marker in the wrong file or at the wrong time

The runtime only sees the rendered artifact. Debugging begins by checking what actually got consumed.

## Why modified harnesses are provisional

A harness can become a participant in the failure:
- a new console mode can change whether prompts appear
- a new SSH probe can change whether timing looks healthy
- a timeout can kill a process before it would have completed
- extra logging can hide or reveal the very event being measured

Because of that, conclusions drawn from a modified harness should be labeled provisional until the same behavior is verified by a simpler or known-good path.

## Why progress gates matter

Expensive tests should only continue when observed signals still increase confidence. If a run is silent, ambiguous, or contradictory, the right answer is usually to stop early, improve the controls, and rerun a narrower hypothesis rather than spend more time waiting.

The first priority is often to add the control that lets you exit when the signal is unclear. If the workflow cannot stop cleanly on a missing signal, the test path itself needs correction before more runtime is spent.

When a control has been added and the signal still does not appear, that absence becomes evidence:
- the change may be wrong
- the change may be too late in the flow
- the probe may still be looking in the wrong place
- the harness may still be masking the real behavior

The practical rule is to keep the expensive path alive only while it is producing concrete proof that it is progressing correctly.

## Why research belongs after a failed signal-control attempt

If a test remains ambiguous after you have added or adjusted the controls meant to make it legible, the next step is research, not more guessing. At that point, the workflow itself may be missing an existing capability already supported by the underlying tools.

The most useful research targets are:
- official documentation for the tooling
- the tool's own source code or help text
- proven examples from authoritative or upstream sources
- existing flags, hooks, environment variables, or log outputs that can be enabled

That research can reveal controls that improve both signal quality and failure isolation. It may also show that the ambiguity is caused by using the tool in a way that hides the relevant evidence.

The rule is simple:
- if the control fix works, continue with the run
- if the control fix does not produce clear signal, stop and research
- then return with a stronger hypothesis and a narrower, more authoritative control path

## Why feature preservation matters during recovery

Recovery should restore confidence without silently deleting capabilities that the system already provides. A useful automation feature, such as topology detection or RAID setup, should not be sacrificed simply because the new debugging or validation machinery made the path harder to reason about.

The risk is not only that a feature disappears temporarily. The bigger risk is that diagnostic complexity gets pushed into the core path until the only practical way back is to remove valuable behavior. Once that happens, the recovery process has already crossed a boundary it should not have crossed.

Mitigation:
- freeze the feature set while recovering the baseline
- keep debug and proof layers optional and outside the core provisioning path
- if a useful feature must be removed to regain confidence, stop and redesign the boundary instead of normalizing the loss
- reintroduce the feature only after the baseline is stable and the split is clear

This is especially important for features that improve automation value, because they are easy to lose when the test path becomes too tangled to support them safely.

## Why independent calibration signals matter

An alternative known-good path is not just another test. It is a calibration signal for the recovery process. It gives you a stable reference shape for what healthy progress looks like when the current run is expensive and ambiguous.

Use it to decide:
- whether the current run is still worth continuing
- whether the new control path is making the signal clearer or noisier
- whether the observed behavior looks like system regression or harness drift

The key advantage is speed. If the current run stops resembling the known-good shape by the checkpoint where it should, the right move is to stop and reconsider, not to let the expensive test keep running in the hope that clarity will appear later.

## Why divergence analysis comes next

Once a witness path proves that success is possible, the next useful question is not just “did this other run fail?” It is “what is the delta between the witness and the noisy path, and which part of that delta is most relevant to the failure type?”

The important idea is that a failure is often explained by the interaction of several changes, not just one. For example, a failure may depend on both a frontend choice and a timing change, or on a probe change and a missing environment value. The skill should encourage the search for the smallest meaningful difference set, while still allowing for multi-factor causes.

Failure type matters because it changes which deltas are worth investigating:
- a timeout points at progress gates, late-stage stalls, or missing signals
- a prompt points at frontend, preseeding, or ordering issues
- a crash loop points at restart behavior, unit state, or repeated failure conditions
- a missing fetch points at network, URL, or boot-time readiness issues

If the causal delta is not obvious, the next step is research. The goal is to learn which controls the tool actually exposes, which defaults may have shifted, and which interactions are documented or visible in source code. Then the next experiment can target the most plausible difference instead of guessing broadly.

## How to prioritize the delta

Not every change matters equally. After a witness path succeeds, the next question is which differences are most likely to explain the failure shape.

Use these filters:
- stage relevance: does the difference affect the step that actually failed?
- failure shape: does the difference map to a timeout, prompt, crash loop, or missing fetch?
- interaction likelihood: does the failure need several conditions to coincide?
- control leverage: can the difference be adjusted or observed with the tools already available?

This keeps the analysis from becoming a flat list of differences with no ordering.

## How to discover additional capabilities

Once the likely delta is identified, the next question is whether the underlying tools already expose a better way to inspect or control it.

Useful sources:
- official documentation
- the component’s source code
- help text and flags
- upstream examples
- runtime logs, hooks, or state files already emitted by the tool

The goal is to find built-in capabilities that sharpen the distinction between success and failure, not to invent a bespoke theory around the delta.

If discovery reveals a better control path, rerun the smallest experiment that uses it. If it does not, keep the focus on the highest-value delta and stop if the run remains ambiguous.

## Why complexity needs a budget

Every extra probe, gate, summary, or debug mode consumes attention and can change behavior. That complexity is not free. If the added machinery begins to force feature removal or make the system harder to reason about, it is being added in the wrong place.

Mitigation:
- prefer replacing an older mechanism over layering a new one on top
- keep observability optional when it is not part of the core contract
- stop adding controls when they begin to crowd out useful behavior
- redesign the boundary when the cheapest recovery step is to delete capability

## Common failure modes in recovery work

### Overweighting a false model
A false model often feels useful because it explains a lot of symptoms at once. The danger is that it can send the work in the wrong direction for hours.

Signals that the model may be wrong:
- manual success contradicts the harness result
- the instrumentation changed at the same time as the failure
- several configuration layers changed together
- the failure description depends on a timeout more than on actual evidence

### Changing too many variables
Multiple simultaneous changes make the cause of success or failure impossible to isolate. Even when the end result is good, the path is too ambiguous to be trusted.

Mitigation:
- freeze the baseline
- isolate one change
- validate immediately
- only then move to the next change

### Treating “not observed” as “failed”
A missing event may simply mean the probe did not run long enough, the log source was wrong, or the event happened later than expected.

Mitigation:
- record threshold misses as warnings first
- distinguish missing, late, and failed states
- only fail when the evidence supports the failure classification

### Continuing expensive runs without confidence
Long-running tests can become a way to delay uncertainty instead of resolve it. If the early signals do not show the run is still healthy, the run should stop and the workflow should be improved before trying again.

Mitigation:
- define the earliest confidence signal before the run starts
- add an early-exit control if the workflow lacks one
- rerun only after the signal is legible
- if the rerun still lacks signal, reconsider the change rather than extending the timeout

### Building brittle tests of tests
If a test mostly proves the test harness rather than the system contract, it can distort design choices. Such tests often overreact to harmless redesigns and can become more important than the behavior they were meant to protect.

Mitigation:
- test durable contracts
- avoid exact-render assertions unless the layout itself is the contract
- prefer checks that survive reasonable refactors

## Mitigation approach

1. Start from the working manual baseline.
2. Verify the exact rendered artifact.
3. Reproduce with the smallest possible change.
4. Keep debug instrumentation separate from the default flow.
5. Treat thresholds and timers as checkpoints, not proof.
6. Revert or quarantine any change that turns observation into interference.
7. Prefer a short recovery loop over a broad rewrite.
8. Add or fix exit controls before spending more time on an unclear expensive run.
9. Preserve useful features unless the baseline proves they are the defect.
10. Treat feature loss during recovery as a signal that the boundary is wrong.
11. Use an independent calibration signal when a known-good alternative path exists.
12. After a witness succeeds, compare the delta against the noisy path and rank it by failure type before the next experiment.
13. Ask which deltas matter most and which built-in capabilities can sharpen them before the next run.

## Recommended reporting shape

When applying this skill, report:
- the baseline you are trusting
- the artifact you inspected
- the smallest change under test
- what was observed
- what remains provisional
- the next smallest safe step

That reporting shape helps keep conclusions precise and prevents the recovery process from becoming another source of confusion.

## Cross-discipline framing

The recovery workflow maps cleanly onto a handful of human disciplines:

- **Experimental science**: baseline, control, and one-variable changes.
- **Differential diagnosis**: symptom shape, timing, and interacting causes.
- **Reliability engineering**: progress gates, early exit, and operational signal.
- **Forensic analysis**: preserve evidence and compare working versus failing states.
- **Bayesian inference**: update confidence as evidence quality changes.
- **Change control / safety engineering**: keep valuable features intact while recovering the system.

These disciplines reinforce the same practical rule: reduce ambiguity cheaply, preserve useful behavior, and only spend more on expensive tests when the current signals still justify it.
