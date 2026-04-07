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

## Recovery examples across systems contexts

The patterns below map common hard-to-diagnose failures to the recovery loop used by `systems-engineer-assist` and `systems-engineer-diagnose`.

### Networking

#### Kubernetes Service exists but traffic times out
Common hidden cause:
- Service has no usable endpoints (selector mismatch, unready pods, or manual Service without matching EndpointSlice).

Why it is misdiagnosed:
- DNS lookup works and Service object looks valid, so teams assume kube-proxy or CNI is broken.

Recovery sequence:
1. Witness baseline: run a direct Pod IP curl from a debug pod in the same namespace.
2. Runtime artifact: inspect live `EndpointSlice` objects and pod readiness, not just Service YAML.
3. Narrow experiment: fix only selector/readiness mismatch and re-check one request path.

#### Pod-to-pod DNS intermittently fails
Common hidden cause:
- CoreDNS healthy at deployment level, but upstream resolver, policy, or node-local path causes selective failures.

Why it is misdiagnosed:
- Operators jump to app retries because failures are intermittent.

Recovery sequence:
1. Witness baseline: resolve the same name from a known-good node and from an affected node.
2. Runtime artifact: inspect CoreDNS logs, pod `/etc/resolv.conf`, and NetworkPolicy/CNI constraints for DNS flows.
3. Narrow experiment: change one variable (policy rule, resolver config, or node path) and rerun `nslookup` at a fixed interval.

#### Sudden widespread `NotReady` and noisy evictions
Common hidden cause:
- Node condition taints (`node.kubernetes.io/not-ready` or `.../unreachable`) are driving scheduling/eviction behavior.

Why it is misdiagnosed:
- Looks like workload instability rather than control-plane reaction to node health.

Recovery sequence:
1. Witness baseline: compare a healthy node and an affected node condition timeline.
2. Runtime artifact: inspect node taints and pod tolerations together.
3. Narrow experiment: restore one node-path dependency (network route, kubelet reachability) before changing workload specs.

### iptables configuration, debugging, and recovery

#### Rules exist but traffic behavior does not change
Common hidden cause:
- Rules are added to the wrong table/chain for the actual packet path (for example, `INPUT` vs `FORWARD`, or `filter` vs `nat`).

Why it is misdiagnosed:
- Teams verify rule presence only, not packet traversal path.

Recovery sequence:
1. Witness baseline: reproduce with one known source/destination/port flow and confirm current behavior.
2. Runtime artifact: inspect packet path assumptions against chain purpose (`PREROUTING`, `INPUT`, `FORWARD`, `OUTPUT`, `POSTROUTING`) and current ruleset.
3. Narrow experiment: move one rule to the correct table/chain and verify counter changes for the test flow.

#### Correct rule is present but shadowed
Common hidden cause:
- Earlier broad `ACCEPT`/`DROP` rule, jump chain, or default policy prevents intended rule from ever matching.

Why it is misdiagnosed:
- Operators scan for rule text but ignore evaluation order and hit counters.

Recovery sequence:
1. Witness baseline: reset to the smallest reproducer ruleset for the affected chain path.
2. Runtime artifact: inspect ordered rules with packet/byte counters and identify first-match behavior.
3. Narrow experiment: reorder one rule (or narrow one broad matcher) and retest a single flow.

#### Firewall changes appear applied but host behavior is unchanged
Common hidden cause:
- Backend mismatch between `iptables-legacy` and `iptables-nft` (rules written to one frontend, datapath driven by another).

Why it is misdiagnosed:
- Command output looks correct from one CLI while active dataplane follows a different backend.

Recovery sequence:
1. Witness baseline: capture current backend/tooling mode and confirm which ruleset is active.
2. Runtime artifact: inspect saved rules and backend-specific listing consistently from the same toolchain.
3. Narrow experiment: apply one test rule through the confirmed active backend and verify packet counters.

#### Intermittent connectivity after rule updates
Common hidden cause:
- Stale conntrack state keeps old flow decisions after policy/NAT change.

Why it is misdiagnosed:
- New rules are correct, but existing sessions continue with pre-change state.

Recovery sequence:
1. Witness baseline: validate behavior on a brand-new connection tuple first.
2. Runtime artifact: inspect conntrack state and distinguish existing from new flows.
3. Narrow experiment: clear only relevant conntrack entries or rotate the test tuple, then recheck.

#### Outbound works, return path fails (asymmetric routing symptoms)
Common hidden cause:
- Missing or incorrect SNAT/MASQUERADE in `POSTROUTING`, or overly strict reverse-path assumptions.

Why it is misdiagnosed:
- Initial SYN path appears healthy, but responses cannot route back through expected state.

Recovery sequence:
1. Witness baseline: verify forward and return direction separately for one tuple.
2. Runtime artifact: inspect `nat` table postrouting rules and relevant route/interface selection.
3. Narrow experiment: add or correct one SNAT/MASQUERADE rule and retest the same tuple.

#### Kubernetes Service traffic breaks after manual node firewall edits
Common hidden cause:
- Manual edits collide with kube-proxy managed chains/rules and are later overwritten or bypassed.

Why it is misdiagnosed:
- Appears as random cluster networking instability across reconciliations.

Recovery sequence:
1. Witness baseline: compare affected node behavior to a node without manual firewall edits.
2. Runtime artifact: inspect kube-proxy-managed chains and node-local custom chains separation.
3. Narrow experiment: move custom filtering to an isolated chain with explicit jump point outside managed rule ownership, then validate after kube-proxy sync.

#### Remote host lockout during firewall rollout
Common hidden cause:
- Flush-first deployment or default-drop transition without guaranteed management-plane allow rules.

Why it is misdiagnosed:
- Rule set may be logically correct, but rollout order creates a brief self-deny window.

Recovery sequence:
1. Witness baseline: test rollout procedure on a console-attached canary host first.
2. Runtime artifact: inspect restore/apply ordering and confirm management access rules are loaded before restrictive policy.
3. Narrow experiment: stage one ordering-safe rollout change and verify uninterrupted control-plane access.

### nftables configuration, debugging, and recovery

#### Ruleset loads successfully but traffic is still dropped
Common hidden cause:
- Base chain hook/type/priority is wrong for the intended traffic stage, so packets never traverse the expected rule path.

Why it is misdiagnosed:
- Syntax validation passes, so teams assume semantic correctness.

Recovery sequence:
1. Witness baseline: reproduce with one explicit tuple (src/dst/proto/port) and known expected verdict.
2. Runtime artifact: inspect base chain `type`, `hook`, and `priority`, and confirm packet stage alignment.
3. Narrow experiment: change one chain registration attribute (usually `hook` or `priority`) and retest only that tuple.

#### `accept` appears to work but later chain still drops traffic
Common hidden cause:
- Multiple base chains share a hook with different priorities; an early `accept` is not final if later chains still evaluate.

Why it is misdiagnosed:
- Teams carry over iptables mental model where first accept often ends evaluation in that table path.

Recovery sequence:
1. Witness baseline: list all base chains for the same hook and rank by priority.
2. Runtime artifact: inspect downstream chain policies/rules after the accepting chain.
3. Narrow experiment: adjust one chain priority or final-policy location to make acceptance terminal for the target flow.

#### Intermittent behavior after incremental updates
Common hidden cause:
- Partial/stepwise command updates leave transient states or duplicate rules when ruleset replacement is not atomic.

Why it is misdiagnosed:
- Failures appear random and timing-dependent across deployments.

Recovery sequence:
1. Witness baseline: compare behavior using full-file atomic load vs interactive incremental edits.
2. Runtime artifact: inspect complete effective ruleset and duplicate/stale objects (chains, sets, maps).
3. Narrow experiment: switch one update path to atomic `nft -f` ruleset replacement and revalidate.

#### Rule matches are unclear in complex chain graphs
Common hidden cause:
- Packet path crosses jumps/verdict maps/sets where assumed control flow differs from actual evaluation.

Why it is misdiagnosed:
- Counter snapshots show activity but not exact decision points per packet.

Recovery sequence:
1. Witness baseline: isolate one packet class and enable tracing only for that class.
2. Runtime artifact: inspect `nft monitor trace` output to follow real chain traversal and verdict.
3. Narrow experiment: modify one decision edge (single rule/jump/verdict map entry) and retrace.

#### NAT rule compiles but has no effect
Common hidden cause:
- NAT statement placed in incompatible chain family/type/hook or attached at wrong stage.

Why it is misdiagnosed:
- Rule syntax is valid in some contexts, but runtime hook semantics prevent intended translation.

Recovery sequence:
1. Witness baseline: verify translation requirement on first packet of a new flow only.
2. Runtime artifact: inspect NAT chain family/type/hook placement and related counters.
3. Narrow experiment: move one NAT rule into a correctly typed/hooked chain and retest with a new connection tuple.

#### Mixed xtables-nft and native nft ownership causes drift
Common hidden cause:
- Legacy tooling (`iptables-nft*`) and native `nft` both mutate policy, creating ownership ambiguity and non-obvious ordering effects.

Why it is misdiagnosed:
- Teams inspect one interface and assume complete ruleset ownership.

Recovery sequence:
1. Witness baseline: inventory all active firewall writers in boot/runtime path (systemd units, scripts, orchestration agents).
2. Runtime artifact: capture full nft ruleset and identify chain/table naming ownership boundaries.
3. Narrow experiment: enforce single-writer ownership for one host class, then compare stability across reboots and reconciliations.

#### Performance collapse with large dynamic block lists
Common hidden cause:
- Linear rule expansion instead of set/map-based matching increases evaluation cost and update churn.

Why it is misdiagnosed:
- Functional correctness is preserved while latency/CPU regress gradually under scale.

Recovery sequence:
1. Witness baseline: benchmark one representative traffic profile before and after list growth.
2. Runtime artifact: inspect whether high-cardinality matches are encoded as rule chains vs sets/maps.
3. Narrow experiment: migrate one hot-path list to a set/map and measure packet path cost again.

### Orchestration

#### Pods stay Pending with vague scheduling messages
Common hidden cause:
- Taint/toleration mismatch or strict affinity interacting with scarce resources.

Why it is misdiagnosed:
- Teams only inspect pod spec and miss node-level constraints.

Recovery sequence:
1. Witness baseline: schedule the same pod template with affinity disabled in a test namespace.
2. Runtime artifact: inspect scheduler events, node taints, and allocatable resources at the same time.
3. Narrow experiment: change one scheduling constraint and observe a single reconciliation cycle.

#### Continuous CrashLoopBackOff after rollout
Common hidden cause:
- Liveness probe starts before app is ready; startup/liveness/readiness semantics are misaligned.

Why it is misdiagnosed:
- Restart noise looks like app defect instead of probe contract mismatch.

Recovery sequence:
1. Witness baseline: run container without liveness probe in an isolated env and confirm steady state.
2. Runtime artifact: inspect probe failures and container exit reasons, not only deployment health.
3. Narrow experiment: adjust one probe dimension (`startupProbe`, delay, threshold, or endpoint behavior) and rerun.

#### Admission or policy webhooks block unrelated deploys
Common hidden cause:
- Webhook timeout/scope causes API-path coupling; failure policy turns transient webhook outage into cluster-wide write failures.

Why it is misdiagnosed:
- Appears as random deployment flakiness across teams.

Recovery sequence:
1. Witness baseline: apply the same object in a namespace excluded from webhook scope.
2. Runtime artifact: inspect webhook configuration (`timeoutSeconds`, selectors, `failurePolicy`) and API server events.
3. Narrow experiment: reduce scope or timeout first, then validate final-state policy with a validating control path.

### Deployment and GitOps

#### Helm upgrades fail and roll back with little signal
Common hidden cause:
- Hook jobs exceed timeout, or readiness never converges under `--wait`/`--atomic`.

Why it is misdiagnosed:
- Rollback obscures first failing resource and teams diff only values files.

Recovery sequence:
1. Witness baseline: run the chart once without rollback in a disposable namespace to preserve failing state.
2. Runtime artifact: inspect hook job logs/events and the first resource that missed readiness.
3. Narrow experiment: adjust one timeout/readiness assumption, not the whole values set.

#### Flux appears stalled on dependent workloads
Common hidden cause:
- `dependsOn` or health checks gate reconciliation waiting for upstream CRDs/controllers that are not ready.

Why it is misdiagnosed:
- Seen as source-controller drift instead of dependency ordering.

Recovery sequence:
1. Witness baseline: reconcile dependency Kustomization/HelmRelease alone and confirm `Ready=True`.
2. Runtime artifact: inspect dependency graph, condition reasons, and controller events.
3. Narrow experiment: fix one dependency edge or health check target and observe one interval.

#### Chart/source fetch failures in GitOps
Common hidden cause:
- Auth secret mismatch, repository URL errors, or storage-operation failures in source-controller.

Why it is misdiagnosed:
- Workload manifests look correct, so teams keep changing app charts.

Recovery sequence:
1. Witness baseline: fetch chart/index with the same credentials outside reconciliation path.
2. Runtime artifact: inspect `HelmRepository`/`HelmChart` conditions (`FetchFailed`, `AuthenticationFailed`, `StorageOperationFailed`).
3. Narrow experiment: correct one credential or URL field and re-reconcile.

### Installation and node bootstrap

#### kubelet starts but pods fail repeatedly on new nodes
Common hidden cause:
- cgroup driver mismatch between kubelet and container runtime on kubeadm-based installs.

Why it is misdiagnosed:
- Node may initially appear joined while workloads fail later under pressure.

Recovery sequence:
1. Witness baseline: compare kubelet/runtime cgroup driver configuration on a known-good node.
2. Runtime artifact: inspect effective kubelet config and runtime config, not provisioning templates alone.
3. Narrow experiment: align one node's driver settings and validate with a single test workload.

#### Control plane intermittently inaccessible after otherwise stable period
Common hidden cause:
- Certificate expiry or near-expiry in kubeadm-managed PKI.

Why it is misdiagnosed:
- Symptoms mimic network instability or etcd issues.

Recovery sequence:
1. Witness baseline: run cert-expiration checks on healthy and failing control-plane nodes.
2. Runtime artifact: inspect actual certificate residual times and cert files in use.
3. Narrow experiment: renew one certificate set and verify API server stability before broader changes.

### Systemd unit configuration and startup recovery

#### Service repeatedly fails with `active (auto-restart)` and `start-limit-hit`
Common hidden cause:
- Unit `Restart=` policy plus low `StartLimitBurst`/`StartLimitIntervalSec` turns a transient error into a persistent lockout.

Why it is misdiagnosed:
- Teams focus on the final `start-limit-hit` state and miss the first failing process exit cause.

Recovery sequence:
1. Witness baseline: start the underlying `ExecStart` command manually with the same user, env, and working directory.
2. Runtime artifact: inspect `systemctl status` and `journalctl -u <unit>` for the first failure, not only the latest retry.
3. Narrow experiment: adjust one restart/rate-limit setting or one startup precondition, then retest from a clean failure counter.

#### Unit works manually but fails under systemd
Common hidden cause:
- Environment, path, permissions, or working directory differ from interactive shell assumptions.

Why it is misdiagnosed:
- Manual execution succeeds, leading to incorrect conclusion that binary/config is healthy in service context.

Recovery sequence:
1. Witness baseline: run with `systemd-run` or equivalent context to reproduce unit-like execution conditions.
2. Runtime artifact: inspect effective unit settings (`systemctl cat`, drop-ins, `Environment=`, `User=`, `WorkingDirectory=`, `ExecStart=`).
3. Narrow experiment: fix one mismatch (env var, path, user/group, directory) and validate one clean restart.

#### Service fails before main process due to `ExecStartPre`/`ExecCondition`
Common hidden cause:
- Pre-flight checks are brittle (timing, missing files, network dependency) and block startup path.

Why it is misdiagnosed:
- Operators inspect only main binary logs and miss pre-start gate failures.

Recovery sequence:
1. Witness baseline: execute each pre-start command independently in order with unit user/context.
2. Runtime artifact: inspect unit journal lines for failed pre-step exit code and command.
3. Narrow experiment: relax or harden one precondition (ordering, timeout, dependency) and rerun.

#### Service starts at boot ordering but fails reliably after reboot
Common hidden cause:
- Incorrect `After=`/`Wants=`/`Requires=` relationships with network, mounts, or dependent services.

Why it is misdiagnosed:
- Manual post-boot restarts succeed, hiding boot-time dependency race.

Recovery sequence:
1. Witness baseline: compare manual post-boot start success with early-boot failure timeline.
2. Runtime artifact: inspect unit dependency graph and boot journals for ordering edges and missing readiness.
3. Narrow experiment: change one dependency/order directive and validate on next reboot.

#### Drop-in overrides unexpectedly change production behavior
Common hidden cause:
- Additional unit fragments in `/etc/systemd/system/*.d/` override packaged defaults silently.

Why it is misdiagnosed:
- Teams read only packaged unit file and miss effective merged configuration.

Recovery sequence:
1. Witness baseline: compare effective unit content on known-good host vs failing host.
2. Runtime artifact: inspect merged unit (`systemctl cat <unit>`) and source of each override.
3. Narrow experiment: remove or adjust one override fragment and re-test service start.

#### Long startup gets killed despite healthy eventual readiness
Common hidden cause:
- `TimeoutStartSec` too short for migrations, cache warmup, or dependency convergence.

Why it is misdiagnosed:
- Appears as random startup instability when service would have succeeded with correct timeout contract.

Recovery sequence:
1. Witness baseline: measure actual startup-to-ready duration under representative load.
2. Runtime artifact: inspect timeout termination signal and timing in journal.
3. Narrow experiment: tune one timeout or readiness gate and rerun under same conditions.

### Podman configuration, debugging, and recovery

#### Container runs with `podman run` but fails as a systemd service
Common hidden cause:
- Quadlet/systemd execution context differs from interactive shell (env, user scope, paths, mounts, network timing).

Why it is misdiagnosed:
- Teams assume runtime behavior is identical between CLI and generated service units.

Recovery sequence:
1. Witness baseline: run the exact image/command interactively and capture expected ready signal.
2. Runtime artifact: inspect generated/effective unit, Quadlet source, and service journal for context differences.
3. Narrow experiment: fix one context mismatch (env var, mount, user scope, dependency) and rerun one start cycle.

#### Auto-update pulls image but service health regresses after restart
Common hidden cause:
- Unit restarts on image update without reliable readiness signaling (`sdnotify`) or with weak rollback assumptions.

Why it is misdiagnosed:
- Update workflow reports success while application fails shortly after restart.

Recovery sequence:
1. Witness baseline: run update in dry-run mode and record pre-update health probes.
2. Runtime artifact: inspect auto-update policy, unit restart behavior, and readiness signaling path.
3. Narrow experiment: enable one explicit readiness contract (notify + timeout alignment) and retest one update.

#### Rootless Podman service fails only after reboot or user logout
Common hidden cause:
- User-session lifecycle, runtime directory, or lingering settings do not match service expectations.

Why it is misdiagnosed:
- Works during active login sessions but fails in unattended boot lifecycle.

Recovery sequence:
1. Witness baseline: compare behavior with active session vs boot-time unattended start.
2. Runtime artifact: inspect user unit placement, runtime dir expectations, and service manager scope.
3. Narrow experiment: adjust one lifecycle control (unit scope/placement/lingering) and validate across reboot.

#### Generated unit behavior drifts over time
Common hidden cause:
- Mixed use of deprecated generated units and newer Quadlet-managed units creates ownership ambiguity.

Why it is misdiagnosed:
- Service definitions look similar while effective behavior differs by generation path.

Recovery sequence:
1. Witness baseline: identify one canonical management path for the target service.
2. Runtime artifact: inspect whether service is sourced from Quadlet generator or static generated unit files.
3. Narrow experiment: migrate one service to the canonical path and compare restart/update behavior.

### containerd configuration, debugging, and recovery

#### Pods fail with image pull errors despite valid credentials
Common hidden cause:
- Registry endpoint/TLS configuration mismatch in containerd CRI registry settings or host-level cert trust.

Why it is misdiagnosed:
- Application manifests are repeatedly changed while runtime registry config is the actual fault line.

Recovery sequence:
1. Witness baseline: pull one target image through the same CRI path used by workloads.
2. Runtime artifact: inspect containerd CRI registry configuration and containerd logs for resolver/TLS errors.
3. Narrow experiment: fix one registry trust or endpoint setting and retest one image pull.

#### Runtime appears healthy but kubelet pods stay in sandbox creation failures
Common hidden cause:
- CRI plugin disabled/misconfigured, wrong socket endpoint, or incompatible runtime stanza.

Why it is misdiagnosed:
- `containerd` process is running, masking CRI-layer failures.

Recovery sequence:
1. Witness baseline: verify CRI endpoint readiness independently of kubelet scheduling.
2. Runtime artifact: inspect containerd config/plugin status and kubelet runtime endpoint wiring.
3. Narrow experiment: correct one CRI endpoint/plugin setting and re-check sandbox creation for one pod.

#### Node instability under pressure after runtime migration
Common hidden cause:
- cgroup driver mismatch between kubelet and containerd (`cgroupfs` vs `systemd`), especially on systemd hosts.

Why it is misdiagnosed:
- Symptoms surface as sporadic eviction/restart noise rather than explicit config errors.

Recovery sequence:
1. Witness baseline: compare cgroup driver config on stable node vs unstable node.
2. Runtime artifact: inspect effective kubelet and containerd runtime cgroup settings.
3. Narrow experiment: align one node’s cgroup driver pair and validate under representative load.

#### Network setup failures for new pods while existing pods keep running
Common hidden cause:
- CNI configuration/version drift relative to containerd CRI expectations.

Why it is misdiagnosed:
- Existing workloads hide bootstrap-path failures for new sandboxes.

Recovery sequence:
1. Witness baseline: create one minimal new pod sandbox and capture exact failure stage.
2. Runtime artifact: inspect CNI config/plugins plus containerd CRI network error logs.
3. Narrow experiment: adjust one CNI config artifact/version and retest new sandbox creation.

### Container execution through systemd (cross-runtime)

#### Service reports `active` while containerized app is not actually ready
Common hidden cause:
- Unit `Type` and readiness semantics do not reflect container startup reality (missing notify/health contract).

Why it is misdiagnosed:
- Orchestrators and operators trust unit state rather than application readiness.

Recovery sequence:
1. Witness baseline: define one concrete app-level ready signal for the service.
2. Runtime artifact: inspect `Type=`, readiness signaling (`sd_notify` or equivalent), and timeout settings.
3. Narrow experiment: align one readiness mechanism and verify unit state transitions against real app readiness.

#### Stop/restart operations intermittently hang
Common hidden cause:
- Inconsistent stop command, signal handling, and timeout policy between systemd and container runtime.

Why it is misdiagnosed:
- Blamed on runtime instability instead of lifecycle contract mismatch.

Recovery sequence:
1. Witness baseline: measure normal stop latency for one healthy instance.
2. Runtime artifact: inspect unit stop directives, runtime stop timeout, and journal signal sequence.
3. Narrow experiment: tune one termination parameter (signal or timeout) and repeat controlled restart.

#### Dependency races with network, storage, or sidecar services
Common hidden cause:
- Unit ordering (`After=`/`Wants=`/`Requires=`) does not match real external dependency readiness.

Why it is misdiagnosed:
- Manual starts succeed after dependencies settle, hiding boot-time race conditions.

Recovery sequence:
1. Witness baseline: compare manual delayed start to boot-time automatic start.
2. Runtime artifact: inspect dependency graph and first-failure timestamps across involved units.
3. Narrow experiment: change one dependency edge or readiness gate and validate on reboot.

### Integration across complex stacks

#### Ingress resource applies but no traffic reaches backend
Common hidden cause:
- IngressClass/controller mismatch or multiple controllers with no clear default class behavior.

Why it is misdiagnosed:
- Backend service and pods are healthy, so attention shifts to app code.

Recovery sequence:
1. Witness baseline: port-forward directly to Service and verify backend behavior first.
2. Runtime artifact: inspect IngressClass defaults, controller ownership, and generated LB/controller events.
3. Narrow experiment: set explicit `ingressClassName` on one ingress and verify route.

#### PVC stays Pending even though storage platform looks up
Common hidden cause:
- No matching PV/storage class semantics for requested size/access mode or delayed provisioning path.

Why it is misdiagnosed:
- Teams inspect CSI pod health but skip claim-to-volume matching rules.

Recovery sequence:
1. Witness baseline: create a minimal PVC known to match an existing class/capacity.
2. Runtime artifact: inspect PVC events, storage class behavior, and provisioner logs for that claim.
3. Narrow experiment: adjust one claim constraint (class, size, access mode) and re-evaluate binding.

#### API migration breakage after cluster upgrade
Common hidden cause:
- Manifests still use deprecated/removed API versions.

Why it is misdiagnosed:
- Errors are interpreted as RBAC or controller outages.

Recovery sequence:
1. Witness baseline: apply one minimal object with the target stable API version.
2. Runtime artifact: inspect admission/apply errors for removed API groups and conversion details.
3. Narrow experiment: migrate one resource kind end-to-end and validate before bulk conversion.

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

## Research anchors for examples

Use these primary sources to keep examples version-aligned:

- Kubernetes API deprecations and removals: https://kubernetes.io/docs/reference/using-api/deprecation-guide
- Kubernetes admission webhook reliability guidance: https://kubernetes.io/docs/concepts/cluster-administration/admission-webhooks-good-practices/
- Kubernetes ingress controller and class behavior: https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/
- kubeadm certificate lifecycle and expiration checks: https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-certs/
- Helm upgrade wait/atomic semantics: https://helm.sh/docs/helm/helm_upgrade/
- Flux Helm chart source failure conditions: https://fluxcd.io/flux/components/source/helmcharts/
- systemd unit and service semantics: https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html
- iptables core command semantics: https://man7.org/linux/man-pages/man8/iptables.8.html
- iptables persistence and reproducible dumps: https://man7.org/linux/man-pages/man8/iptables-save.8.html
- iptables match/target extension behavior: https://man7.org/linux/man-pages/man8/iptables-extensions.8.html
- nftables command and ruleset semantics: https://netfilter.org/projects/nftables/manpage.html
- nftables chain configuration, hooks, and priorities: https://wiki.nftables.org/wiki-nftables/index.php/Configuring_chains
- nftables packet tracing and diagnostics (`nftrace`/monitor): https://wiki.nftables.org/wiki-nftables/index.php/Ruleset_debug/tracing
- Podman Quadlet and systemd integration: https://docs.podman.io/en/latest/markdown/podman-quadlet.1.html
- Podman auto-update and rollback/readiness behavior: https://docs.podman.io/en/v4.6.1/markdown/podman-auto-update.1.html
- containerd CRI configuration reference: https://github.com/containerd/containerd/blob/main/docs/cri/config.md

## Cross-discipline framing

The recovery workflow maps cleanly onto a handful of human disciplines:

- **Experimental science**: baseline, control, and one-variable changes.
- **Differential diagnosis**: symptom shape, timing, and interacting causes.
- **Reliability engineering**: progress gates, early exit, and operational signal.
- **Forensic analysis**: preserve evidence and compare working versus failing states.
- **Bayesian inference**: update confidence as evidence quality changes.
- **Change control / safety engineering**: keep valuable features intact while recovering the system.

These disciplines reinforce the same practical rule: reduce ambiguity cheaply, preserve useful behavior, and only spend more on expensive tests when the current signals still justify it.
