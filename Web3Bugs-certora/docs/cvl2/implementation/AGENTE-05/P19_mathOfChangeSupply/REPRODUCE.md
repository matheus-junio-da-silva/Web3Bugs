# Reproduction runbook — AGENTE-05 / P19 experimental CVL2

## Prerequisites and scope

Use Linux/WSL with `certora-cli==8.19.0`, native `solc 0.8.7+commit.e28d00a7.Linux.g++`, GNU `timeout`, Python 3, and Git. The **only** specification inputs are `results/cvl2/02_unresolved/19/{1,2}.spec`, each compiled **individually** against the unchanged `contracts/19/spec/harnesses/Dummy.sol`. Run **no** CVL1 and **no** full Prover: `--compilation_steps_only` is mandatory. No authorization to modify any source beyond the existing two derived signatures.

Set `CERTORA_BIN` and `SOLC_BIN` to the installed native executables; examples below use the exact paths reported in PR #44. The paths are **illustrative on other machines**, and may need adjustment. Do not pass secrets through CLI arguments.

```bash
set -u
BASE=2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3
CERTORA_BIN=/home/mat/certora-ac-audit/certora_venv/bin/certoraRun
SOLC_BIN=/home/mat/.solc-select/artifacts/solc-0.8.7/solc-0.8.7
ROOT="$(git rev-parse --show-toplevel)"
DATA="$ROOT/Web3Bugs-certora"
TEST_ROOT="$(mktemp -d)"
printf 'Base=%s\n' "$BASE"
"$SOLC_BIN" --version
"$CERTORA_BIN" --version
```

Create **two isolated** working folders. All commands below are meant to run from the repo root. No API key should be copied into either folder. Every run uses a fresh `HOME` and sanitized credential environment.

```bash
for N in 1 2; do
  DIR="$TEST_ROOT/$N"
  mkdir -p "$DIR/home/config"
  cp "$DATA/results/cvl2/02_unresolved/19/$N.spec" "$DIR/property.spec"
  cp "$DATA/contracts/19/spec/harnesses/Dummy.sol" "$DIR/Dummy.sol"
  sha256sum "$DATA/results/spec/complete/19/$N.spec" "$DIR/property.spec" "$DIR/Dummy.sol"

  START_NS="$(date +%s%N)"
  (
    cd "$DIR" || exit 99
    env -u CERTORAKEY -u CERTORA_KEY -u CERTORA_API_KEY -u CERTORA_TOKEN \
        -u CERTORA_CREDENTIALS -u ETHERSCAN_API_KEY \
        HOME="$DIR/home" XDG_CONFIG_HOME="$DIR/home/config" \
        PATH="/home/mat/certora-ac-audit/certora_venv/bin:/usr/local/bin:/usr/bin:/bin" \
        timeout --signal=TERM --kill-after=5s 60s \
        "$CERTORA_BIN" Dummy.sol:Dummy --verify Dummy:property.spec \
          --compilation_steps_only --solc "$SOLC_BIN"
  ) > "$DIR/stdout.log" 2> "$DIR/stderr.log"
  EXIT_CODE=$?
  END_NS="$(date +%s%N)"
  printf 'example=%s exit=%s wall_ms=%s\n' "$N" "$EXIT_CODE" "$(( (END_NS-START_NS)/1000000 ))"
  if [ "$EXIT_CODE" -eq 124 ] || [ "$EXIT_CODE" -eq 137 ]; then
    printf 'TIMEOUT: example %s\n' "$N"
  fi
done
```

**Review logs locally for sensitive data before publication.** Never upload environment variables, config files, API keys, complete `HOME` folders, or raw logs without sanitizing them. Preserve actual stdout/stderr, duration, exit code, tool versions and input hashes when a run is performed. **Exit 0** from compilation-only is not a formal proof.

## Exact-byte scope guard and authorized transformation

This check uses Python standard library. It should print `OK` for each example and must reject any difference except the authorized signature:

```bash
python3 - <<'PY'
from pathlib import Path
from hashlib import sha256
root = Path("Web3Bugs-certora")
old = b"definition divPrecisely(uint x, uint y) returns mathint"
new = b"definition divPrecisely(mathint x, mathint y) returns mathint"
want = {
    1: ("279c6c956d9084cb576f9e3f99dba63936d27b6e07401f9878751ac22808016a",
        "6dff6a352b42887fbf8c8679a16cb35c20489fefd668ce960146e701fe4ff4af"),
    2: ("132af5147a37652fe4318fc3fda8b6148fe6da0cc3195397c86d1527677c3df7",
        "cffd0de64eef3d466acbd706967e4729fd8aa8ad12e2e3376ba241eafa9adac3"),
}
for n, (expected_original, expected_derived) in want.items():
    original = (root / f"results/spec/complete/19/{n}.spec").read_bytes()
    derived = (root / f"results/cvl2/02_unresolved/19/{n}.spec").read_bytes()
    assert original.count(old) == 1
    assert derived == original.replace(old, new)
    assert sha256(original).hexdigest() == expected_original
    assert sha256(derived).hexdigest() == expected_derived
    print(f"OK: P19/{n} signature-only + hashes")
PY
```

## Catalog and Git validation

```bash
cd Web3Bugs-certora
python3 scripts/check_specs.py .
python3 scripts/check_contests_csv.py .
python3 scripts/check_contracts.py .
./scripts/check_git.sh .
cd ..
git diff --check 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3...HEAD
```

**Historical whitespace limitation:** both original CVL snapshots contain literal trailing whitespace. Since a newly added, byte-faithful derived spec reproduces those bytes, the plain `git diff --check` may flag the new spec lines. Altering those whitespace bytes would violate the single-transformation authorization. If the strict check reports trailing whitespace, record its exact output and leave the bytes unchanged until the coordinator determines a policy. An optional *diagnostic*, not a substitute for reporting the strict check, is:

```bash
git -c core.whitespace=-blank-at-eol,-blank-at-eof,-space-before-tab,cr-at-eol \
    diff --check 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3...HEAD
```

The catalog validators only validate the historical catalog; they do **not** prove CVL2 equivalence.

## Recorded status of this session

The exact-byte checks were performed using the GitHub original contents and a standalone SHA-256 implementation; their two derived digests match the coordinator's independently recorded digests. **No Certora execution, shell validator, or literal `git diff --check` run occurred in this session** because the attached execution device is offline and the local execution backend was unavailable. The code blocks are reproducible commands, **not fabricated execution logs**.

**Restriction: do not run full Prover, CVL1, or merge; keep both examples in 02_unresolved.**
