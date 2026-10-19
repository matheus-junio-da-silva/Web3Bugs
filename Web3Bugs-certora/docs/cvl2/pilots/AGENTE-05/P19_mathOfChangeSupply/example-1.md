# Project 19 / complete/1.spec — CVL2 compilation-only pilot

## Immutable inputs

- GitHub: https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/results/spec/complete/19/1.spec
- Git commit base: `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`.
- Original spec SHA-256: `279c6c956d9084cb576f9e3f99dba63936d27b6e07401f9878751ac22808016a`.
- Copied spec SHA-256: `279c6c956d9084cb576f9e3f99dba63936d27b6e07401f9878751ac22808016a`; byte-for-byte identical (`cmp` exit 0).
- Target: `Web3Bugs-certora/contracts/19/spec/harnesses/Dummy.sol`; target SHA-256 `11f334db4012673cfb05cd9d1aca8904e9f3a822080a4d3c1c52ed474665c875`; copied target byte-for-byte identical (`cmp` exit 0).
- Spec and Dummy.sol were tested only from a temporary, isolated folder; they were **not** committed or edited.

## Compilation result

- **COMPILE_ERROR**; exit code **1** (not a timeout).
- Observed wall duration: **3.224 seconds**.
- Certora CLI `8.19.0`; solc `0.8.7+commit.e28d00a7.Linux.g++`; Python 3.14.4.
- Working directory: `/home/mat/cvl2-agent05-pilot-20261019/work/1`.
- Timeout: `timeout --signal=TERM --kill-after=5s 60s`.
- Invocation: `certoraRun Dummy.sol:Dummy --verify Dummy:property.spec --compilation_steps_only --solc /home/mat/.solc-select/artifacts/solc-0.8.7/solc-0.8.7`; credentials removed from the subprocess environment.
- Local typechecker reported `property.spec:18:34`: `(T - NR)` has type `mathint`, expected `uint256`.
- Local typechecker reported `property.spec:21:32`: `RCPT` has type `mathint`, expected `uint256`.
- No Prover verification job was requested; the tool's mention of 'Certora Prover typechecker locally' describes a **local typecheck**, not a proof.
- Safe logs: [stdout](logs/example-1.stdout.log), [stderr](logs/example-1.stderr.log).

## Separate rule and semantic limits

- Original CVL property name: `mathOfChangeSupply` (shared name, but **different assertion** between examples).
- Unmodified assertion for this example: `assert T2 <= MAX_SUPPLY();`.
- Root source cause: `definition divPrecisely(uint x, uint y) returns mathint` receives `T-NR` and later `RCPT` as the second `uint` parameter. CVL2 arithmetic yields `mathint`, and narrowing cannot happen implicitly.
- The source preconditions constrain `T`, `NR` and `RC`, but do not eliminate CVL2 typechecking requirements. The two errors occur before the assertion is verified or falsified.
- Official guide [Changes Introduced in CVL 2 / Changes to integer types](https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html#changes-to-integer-types) and [Migration / Type errors in arithmetic and casts](https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html#type-errors-in-arithmetic-and-casts) describe explicit bounds/casts. An `assert_uint256` candidate would add range proof obligations; a `require_uint256` candidate could suppress counterexamples. **Neither was applied or tried.**
- Whether the division denominator `RCPT` can be zero is a separate semantic question; this pilot does not resolve it.
- This is not a historical report reproduction and does not assert VERIFIED, VIOLATED or 00_unchanged.

**SEM ALTERAÇÕES EM SPECS; SEM CVL1; SEM PROVER; SEM REPAROS TENTATIVOS.**
