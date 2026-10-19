# CVL2 required `rule` keyword — P17

A2 source: https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html — section `Rules must start with rule`.

The historical Compound source uses Specify. In CVL2 a rule requires the `rule` prefix, but adding it mechanically is NOT sufficient to make legacy `description`, `havoc`, static assertions, pre/action/post env or method summaries semantically equivalent. No code changed; candidate only.
