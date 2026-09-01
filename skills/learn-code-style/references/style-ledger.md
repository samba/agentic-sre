# Project Style Ledger Template

This packaged file defines the schema only. Never write project observations
here. Instantiate it as `.agentic/style-ledger.md` in the active project.

```markdown
# Project Style Ledger

Project: <project identifier>
Visibility: project-versioned|project-local-ignored
Last updated: <ISO date>

## Language: <language/ecosystem>

Confidence: low|medium|high
Last observed: <ISO date>

Sources:
- <project-relative file/symbol, commit range, or authoritative guide URL>

Preferred patterns:
- <actionable repeated pattern>

Discouraged patterns:
- <actionable repeated anti-pattern>

Constraints and exceptions:
- <correctness, safety, generated-code, public-API, or team exception>

Promotion history:
- <date, target profile, approved-by, portable rule, removal condition; or none>
```

Do not include raw proprietary snippets, secrets, personal data, or paths
outside the project. Add language sections only when evidence exists.
