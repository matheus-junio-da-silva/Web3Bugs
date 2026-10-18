# Project 22 — ECHO independent audit and command log (2026-10-18)

Repository base main SHA: eba10cbb6a37ba5230bda307cdf9105ba72489dc.
PropertyGPT source main SHA: 687f654c679ed45ab127b7949e2a29c8f5e491b9.

## Source-level independent checks

- Comment-aware lexical scanner: PoolActions 3, sanity 2, FullMathWrapper 3, PopsicleV3Optimizer 13 = **21 active**.
- FullMathWrapper commented integrityOfSafeMulDiv; Popsicle optimizer commented more_shares_more_amounts_to_withdraw, withdraw_amount, zeroBalancesAfterRebalance and unterminated block comment covering totalSupplyIntegrity; sanity commented reentrency. Excluded as inactive.
- All 21 property bodies occur literally in their corresponding N.spec; 21 index rows, each with required files.
- 54 Solidity source files and 61 original non-PDF files preserved byte-identically; original PDF SHA-256 b11b2c428959dff60f5da03278868b804dcf844b1a23634dd725a09f37946298.
- Transitive Solidity imports rooted at FullMathWrapper, PoolActionsWrapper, PopsicleV3Optimizer, SymbolicUniswapV3Pool and DummyERC20A/B: **zero unresolved relative imports** among the preserved source trees. This check does not prove successful Prover execution.

## Development VM structural validation, before commit

Run from Web3Bugs-certora root, with Python 3 exposed as command python via a local noncommitted PATH shim (the VM installation does not provide an unqualified python executable by default).

~~~text
$ python scripts/check_specs.py .
Check passed! 576 spec examples and 581 Bug Label relationships are structurally consistent.
exit=0
$ python scripts/check_contests_csv.py .
Check passed!
./results/contests.csv is consistant with ./reports
exit=0
$ python scripts/check_contracts.py .
Check passed!
./contracts is consistant with ./reports
exit=0
$ git -c core.whitespace=cr-at-eol diff --cached --check
(no output)
exit=0
~~~

The exact mandatory post-commit command git -c core.whitespace=cr-at-eol diff --check origin/main...HEAD will be run after commit. The published PR description records its real exit code together with the exact final head SHA. No Certora prover run is claimed.
