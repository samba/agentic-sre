# Working-Draft Partitioning

Use this mode automatically when a request to create commits encounters more
than one semantic topic. Planning is read-only; staging, committing, stashing,
rewriting history, or changing files requires the corresponding authority.

## Evidence and Attribution

Build the topic map from all available evidence, in this order:

1. current explicit user instructions and durable intent/task/decision records;
2. accepted plan, constraints, and relevant conversation or worker-thread
   history, including which changes the agent reports producing and why;
3. staged, unstaged, and untracked content in the actual repository;
4. accepted design, tests, generated-artifact relationships, and repository
   conventions;
5. path proximity or naming only as a weak final signal.

Thread history is evidence of intent, not authority or proof. Do not include a
change merely because it was discussed, exclude observed content because it was
not mentioned, or claim authorship from memory. Reconcile history with the
diff. Mark content as `agent-attributed`, `user-attributed`, `shared`, or
`unknown`; preserve uncertain pre-existing work and ask before mutating it when
the distinction affects the result.

## Topic Boundaries

A topic is a single semantic outcome with a shared rationale and rollback
boundary. Prefer separate commits when changes have different goals, bug/task
identifiers, behavior, risk, reviewers, rollback needs, or validation. Keep
producer and required consumer changes, schema and migration, generated source
and generator, behavior and its tests, and a necessary compatibility update
together when separating them would create a misleading or invalid revision.

Do not partition solely by file type, directory, author, or chronological edit
order. Formatting or mechanical cleanup belongs separately when it is not
required by the behavior change. Do not manufacture tiny commits that obscure
one coherent change.

Order topics by dependency: enabling contract or migration before consumers,
implementation before optional documentation, and corrective follow-up after
the revision it corrects. Every intermediate commit should satisfy the
repository's accepted buildability policy; if it intentionally does not, state
why and do not describe it as independently releasable.

## Safe Workflow

1. Inspect repository root, branch/HEAD, status, staged diff, unstaged diff,
   untracked paths, and submodule state without changing them.
2. Reconstruct candidate intents from durable records and relevant thread
   history, then map every changed path and meaningful hunk to one topic or to
   `ambiguous`.
3. Identify pre-staged content. Do not silently unstage, absorb, reorder, or
   recommit it; treat its current index membership as user state unless the
   caller authorized rearrangement.
4. Propose an ordered plan containing topic, rationale, task/intent links,
   paths or hunks, dependencies, validation, proposed message, ownership
   confidence, and excluded changes.
5. Stop before index mutation when ownership is ambiguous, a secret or
   generated artifact may be present, a mixed hunk cannot be separated safely,
   required validation is unavailable, or authorization does not cover the
   proposed staging and commit operations.
6. When authorized, stage explicit paths only when the entire path belongs to
   one topic. Never use broad staging such as `git add .`, `git add -A`, or an
   unresolved glob for a mixed draft.
7. For a reliably separable mixed file, use a reviewable non-interactive patch
   applied to the index only, check it before application, and verify both
   staged and remaining diffs afterward. Do not automate an interactive prompt
   or hand-edit an index patch speculatively. If safe separation is doubtful,
   leave the file uncommitted and request a decision or first refactor the
   working change when authorized.
8. Inspect the exact staged snapshot and confirm that every staged hunk belongs
   to the topic, all required companion changes are present, and unrelated or
   sensitive material is absent.
9. Run the smallest sufficient validation against that exact snapshot. If
   validation requires hiding other working-tree changes, use an isolated
   worktree or temporary index where practical; stash mutation requires
   separate authority. Record limitations when the tested tree cannot exactly
   match the staged tree.
10. Generate the message from the verified staged diff and evidence, commit
    only with authority, capture the commit id, and re-inspect status before
    proceeding to the next topic.
11. Stop on validation failure, unexpected diff movement, hook-added changes,
    conflict, ambiguous ownership, or a commit whose resulting tree differs
    from the verified snapshot. Do not bypass hooks or rewrite the commit
    without explicit authority.

## Completion Conditions

A partition is complete only when each intended topic has a commit or explicit
deferred disposition; each commit's contents, message, evidence, and task links
agree; dependency order is recorded; and remaining staged, unstaged, and
untracked content is reported. Never describe an intentionally preserved or
ambiguous draft as clean.
