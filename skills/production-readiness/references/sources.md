# Source History

Last substantive review: 2026-08-31.

- [Google SRE on SLOs](https://sre.google/sre-book/service-level-objectives/)
  and its [error-budget policy](https://sre.google/workbook/error-budget-policy/)
  support user-visible objectives and explicit reliability actions. Not every
  product needs a 24/7 SLO; only authorized owners may promise an SLA.
- [Canarying Releases](https://sre.google/workbook/canarying-releases/)
  supports representative exposure, evaluation, stop conditions, and rollback;
  it does not replace pre-production validation.
- [OpenTelemetry signals](https://opentelemetry.io/docs/concepts/signals/)
  supports correlated telemetry while leaving privacy, cardinality, retention,
  and cost controls to the implementation.

For consequential claims, retain publisher, URL, version/date, retrieval date,
finding, relevance, limits, and immutable identifier. Preserve superseded
entries and explain interpretation changes.
