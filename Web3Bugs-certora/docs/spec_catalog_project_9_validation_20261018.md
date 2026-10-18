# Project 9 — final local source audit / verification log (2026-10-18)

**Source:** `Web3Bugs.zip` from the user-provided Project files. This ZIP includes real Git history (`.git`, pack objects, refs). The extracted top-level checkout was `main` at `4a1bea89d88aa3b6aa165e8d81b8dd523c7afb82` and had unrelated working-tree changes. No reset/pull/push was performed on that working tree. A new clean Git worktree was checked out from the existing PR #7 commit `a2bf80bc4dd74d1c0bf6de6add456b0adf31a8ed` on branch `catalog/p09-farol-celo-governance`. GitHub confirmed the same PR head and base at the start. All mutations below were isolated to this worktree and Project 9 paths.

## Whitespace: baseline failure and verified resolution

The **original** exact check `git -c core.whitespace=cr-at-eol diff --check origin/main...HEAD` had exit **2** with 490 diagnostics across 139 paths: 456 trailing whitespace, 7 space-before-tab, and 27 blank EOF lines. Breakdown:

| Class | Trailing | Space/tab | EOF | Total | Change |
| --- | ---: | ---: | ---: | ---: | --- |
| Historical immutable `contracts/9/**` | 220 | 4 | 1 | **225** | No byte changes; narrow exception |
| Original historical CVL literal excerpts `results/spec/{complete,incomplete}/9/*.spec` | 192 | 3 | 1 | **196** | No byte changes; narrow exception |
| Generated Project 9 example `.md` | 44 | 0 | 0 | **44** | Trim trailing spaces in authored prose |
| Generated Project 9 example `.sol` | 0 | 0 | 25 | **25** | Trim empty separator lines at EOF only |
| **Total** | **456** | **7** | **27** | **490** | No repository-wide relaxation |

Only `Web3Bugs-certora/.gitattributes` adds these Project 9 root-relative patterns, with `-whitespace`: `/contracts/9/**`, `/results/spec/complete/9/*.spec`, `/results/spec/incomplete/9/*.spec`. `git check-attr whitespace` confirmed **unset** only for the historical paths and **unspecified** for generated `.sol`, `.md` and other projects. The exception does not apply to CSVs or all `.spec` files. The uncommitted working tree's complete comparison against `origin/main` returned exit **0**, and the exact triple-dot command was repeated against the **committed PR HEAD** before delivery (exit **0**, no diagnostics).

## Reproducible commands and observed outputs

`python` is Python 3.13.5 in this VM. `origin/main` was `4a1bea89d88aa3b6aa165e8d81b8dd523c7afb82` and the pre-fix parent was `a2bf80bc4dd74d1c0bf6de6add456b0adf31a8ed`.

```text
working directory: Web3Bugs-certora
$ python scripts/check_specs.py .
exit: 0
Check passed! 225 spec examples and 230 Bug Label relationships are structurally consistent.

$ python scripts/check_contests_csv.py .
exit: 0
Check passed!
`./results/contests.csv` is consistant with `./reports`

$ python scripts/check_contracts.py .
exit: 0
Check passed!
`./contracts` is consistant with `./reports`

working directory: Git repository root
$ git -c core.whitespace=cr-at-eol diff --check origin/main...HEAD
exit: 0
stdout: empty
stderr: empty
```

## Independent source verification and result attribution

- **61/61** active rules/invariants in ten original source files, independently enumerated with comments masked; 61/61 original source-line property bodies are literal in the extracted `.spec` artifacts; **50 complete, 11 incomplete**; **151/151** Solidity source-excerpt spans match the referenced historical contract/harness text. The 195 historical source files under `contracts/9` are unchanged.
- Incomplete instances #27, #30, #36, #37, #48, #49, #50, #58, #59, #60 and #61 retain `.txt` evidence. #36 and #37 intentionally remain incomplete: `getVoteRecord(address,uint256)` has three CVL return values versus six in the supplied Solidity; no historical adapter is invented. #61 lacks the referenced original `Reserve.sol`.
- #50 `constitution_change_legal` ends with the sole active assertion `assert true`: this is tautological, **UNMAPPED**, and not evidence of constitutional legality. Four diagnostic examples remain UNMAPPED (#11, #20, #27, #50). All 61 formal `Result` and `Detection Outcome` entries remain **NOT_STATED**; aggregate PDF check marks are not assigned to source-specific rules.
- All non-Project-9 rows in `results/spec/spec_buglabel.csv`, `results/contests.csv` and `results/bugs.csv` are identical, in the original order, to the `origin/main` versions (no shared-index overwrite).
- The preserved 14-page `resources/9/CeloMay2020.pdf` was re-read and relevant tables/inequalities visually checked. Git blob SHA-1: `9801e32b8a0e59fe7dc7a0a11d736d1750c282e0`; SHA-256: `38181d04c6363e4896abb18804544d31ac132be57bb75f267b81e1a0c59fde49`. The report companion is a **paraphrase**, not a transcript of independently named Prover rule results.

**Historical restrictions not removed:** `--optimistic_loop`, Accounts `--loop_iter 2`, empty `GovernanceHarness.dequeueProposalsIfReady`, `LockedGoldHarness.ercBalanceOf` returning native address balance, and `applyHarness.sh` alterations to visibility, arithmetic, approval conditions and external-call behavior. Missing original transitive packages/runner environments and unresolved linked APIs mean `complete` is snapshot dependency closure, **not** a claim of an executed formal proof. **PR remains draft; no merge.**
