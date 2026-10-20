# AGENTE-05 — Authorized CVL2 compilation-only pilot, Project 19

**Authorization:** second independent review of [research PR #40](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/40#pullrequestreview-5577011717), 2026-10-19. Scope is exactly the two separate complete P19 examples against `contracts/19/spec/harnesses/Dummy.sol`. The PR #40 itself is untouched and remains draft.

## Results

| Example | Original rule | Immutable source SHA-256 | Status | Exit code | Duration |
| --- | --- | --- | --- | ---: | ---: |
| [1](example-1.md) | `mathOfChangeSupply`, assertion `T2 <= MAX_SUPPLY()` | `279c6c956d9084cb576f9e3f99dba63936d27b6e07401f9878751ac22808016a` | COMPILE_ERROR | 1 | 3.224s |
| [2](example-2.md) | `mathOfChangeSupply`, assertion `T2 <= T || T2 == NR` | `132af5147a37652fe4318fc3fda8b6148fe6da0cc3195397c86d1527677c3df7` | COMPILE_ERROR | 1 | 3.419s |

Both preserved the original bytes and used target SHA-256 `11f334db4012673cfb05cd9d1aca8904e9f3a822080a4d3c1c52ed474665c875`. No target/spec source files are in this commit.

## Diagnosis

The Certora CVL2 local checker, invoked via `certora-cli 8.19.0 --compilation_steps_only` with native `solc 0.8.7`, found identical type errors in both individually tested specs:

- `property.spec:18:34`: arithmetic `T - NR` is `mathint` but a `uint256` argument is required.
- `property.spec:21:32`: value `RCPT` is `mathint` but a `uint256` argument is required.

There was no timeout, Prover run, CVL1 run or trial-and-error modification. A separate example 1 preflight attempt ended with an **environment-only** missing Python `solc_select` module (2.320s, exit 1); retry used a pre-installed native compiler binary and led to the authentic CVL2 type-check errors. The preflight diagnostic is preserved in [the safe log](logs/example-1-environment-preflight.stdout.log).

## Reproduction

- OS: WSL/Linux, isolated clone from `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`.
- CLI: `/home/mat/certora-ac-audit/certora_venv/bin/certoraRun`, version `8.19.0`.
- Target compiler: `/home/mat/.solc-select/artifacts/solc-0.8.7/solc-0.8.7`, version `0.8.7+commit.e28d00a7.Linux.g++`.
- For each example `N`, **separately** copy `results/spec/complete/19/N.spec` to isolated `property.spec`, `contracts/19/spec/harnesses/Dummy.sol` to isolated `Dummy.sol`, verify SHA-256 and `cmp`, and in that directory run:

```bash
env -u CERTORAKEY -u CERTORA_KEY -u CERTORA_API_KEY -u CERTORA_TOKEN -u CERTORA_CREDENTIALS -u ETHERSCAN_API_KEY \
  HOME="$PWD/home" XDG_CONFIG_HOME="$PWD/home/config" \
  PATH="/home/mat/certora-ac-audit/certora_venv/bin:/usr/local/bin:/usr/bin:/bin" \
  timeout --signal=TERM --kill-after=5s 60s \
  /home/mat/certora-ac-audit/certora_venv/bin/certoraRun \
  Dummy.sol:Dummy --verify Dummy:property.spec \
  --compilation_steps_only \
  --solc /home/mat/.solc-select/artifacts/solc-0.8.7/solc-0.8.7
```

The executed commands additionally used a fresh isolated `HOME` and `XDG_CONFIG_HOME` to prevent reading shared credentials. The separate [JSON manifest](results.json) and safe stdout/stderr logs record durations, exit codes and byte identities. No API keys or environment files were read, copied or committed.

## Next phase / restrictions

This run only establishes **COMPILE_ERROR**, not verified/violated/semantically incorrect contract behavior. The official [CVL2 integer changes](https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html#changes-to-integer-types) and [migration guide](https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html#type-errors-in-arithmetic-and-casts) describe possible type-compatibility edits, but a change would need separately authorized semantic review (especially avoiding `require_` casts that may hide counterexamples). **No edits are performed or proposed as final patches.**

**SEM ALTERAÇÕES EM SPECS; SEM COMPILAÇÃO CVL1; SEM PROVER; SEM EXPANSÃO DO ESCOPO.**
