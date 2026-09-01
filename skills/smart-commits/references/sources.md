# Source History

Last substantive review: 2026-08-31.

- [Git commit documentation](https://git-scm.com/docs/git-commit#_discussion)
  supports a title and optional separated explanatory body. The
  rationale/impact/proof labels are this skill's local auditability policy.
- [Git status](https://git-scm.com/docs/git-status) distinguishes the index,
  working tree, and untracked paths; porcelain formats provide stable
  inspection output.
- [Git add](https://git-scm.com/docs/git-add) defines the index as the next
  commit snapshot and supports partial-file staging. Its warnings about edited
  patches support verifying index/worktree divergence before committing.
- [Git stash](https://git-scm.com/docs/git-stash) documents a staged/keep-index
  workflow for testing separated changes. This skill treats stash mutation as
  a separate, explicitly authorized side effect rather than a default step.

For consequential changes to the convention, retain publisher, canonical URL,
version/date, retrieval date, interpretation, and limits. Preserve superseded
entries and explain the change rather than rewriting history.
