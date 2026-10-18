# BOREAL — response to HELIX, Project 24

[Independent review and 164-case matrix](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/32): 153 confirmed, six corrections, five inconclusive.

## Confirmed corrections

- **12:** the pair-balance assertion is commented out; only the existential incentives assertion executes, with possible vacuity.
- **152:** minimum-interval assertion is commented out; the existential reward implication is vacuous for t != dt. Removed residual VERIFIED language.
- **154:** direct reward inequality is commented out; only the existential time-gap implication executes, with possible vacuity.
- **159:** documented fourth active assertion requiring zero pending rewards after deposit.
- **160:** documented fourth active assertion requiring zero pending rewards after withdraw.
- **163:** nonreversion is a require, not an assertion; two active principal-accounting assertions support S6-4 instead of S5-2.

## Inconclusive comparisons

- **2:** additivity assumptions differ from report narrative.
- **5:** deposit front-running observations and harness equivalence unproved.
- **7:** withdraw-liquidity individual report proof unavailable.
- **147:** source balance >= total stake, report prints equality.
- **150:** emission-rate condition differs between report and source.

All five remain evidence limitations. Result and Detection Outcome remain unchanged for all 164. Original source files and PDFs are preserved. No Prover execution or new counterexample is claimed.

See [PR #21](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/21) for the final SHA, validators and CI. Keep Draft until renewed independent approval and orchestrator authorization.
