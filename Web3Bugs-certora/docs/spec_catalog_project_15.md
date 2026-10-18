# Project 15 — AAVE Proof of Reserve / HELIX

## Source identity and existing Project 2
This is intentionally an independent *recatalog* of the same historic AAVE
Proof of Reserve material already covered by Project 2. No new distinct
verification engagement, finding or set of 15 extra original properties
is implied. The original Project 2 was not edited. P15 source contracts,
three specs and original PDF are byte-identical to P2; P15 uses a stricter
transitive Solidity dependency test. The supplied PropertyGPT specs have
SHA256 hashes:
- aggregator.spec: f6787f5c0a14f0a7cb20115a3bdc1db6379f5301b405d93f610928814a854fb8
- executorV2.spec: 80c9afa753589467785cbcf634c067cecdf24f43c0a1ba18757e76fd68518640
- executorV3.spec: e213486c2268bdec03db68822e7a244343a32171706aea3104c4679eba1f0c06
The preserved historic PDF is resources/15/Aave-Proof-of-Reserve-Formal-Verification-Report.pdf
(Git blob 383307e6076e87d549faa23817a17e79acfc4317).
The report identifies 6–22 Nov 2022 and reviewed commit 12296ce;
there is no proof that the supplied source snapshot matches the historical
upstream commit byte for byte. Reports/15.md is the PDF text-layer transcript
derived from reports/2.md; PDF visuals and status marks are authoritative.

## Coverage and dispositions
Aggregator 2 active rules; Executor V2 4 rules and 2 invariants;
Executor V3 4 rules and 3 invariants = **15 active source instances**.
Two integrityOfExecuteEmergencyAction rules remain commented out and
must not be indexed despite descriptions of proofs in the PDF.
Every CVL property body is copied literally; no migration to CVL2.

**Status: 0 complete / 15 incomplete.** Compared with P2 (1/14), the new
PoRFeedChange incomplete classification additionally requires closed
Solidity imports. The Solidity contracts depend on non-vendored
solidity-utils, chainlink-brownie-contracts, aave-address-book and/or
missing historical harnesses/helpers. N.txt documents concrete deficits.
Not having source dependencies is not evidence that the report's proof failed.

**Results: 10 VERIFIED, 5 NOT_STATED, 0 VIOLATED.**
**Detection Outcomes: 10 NO_FINDING, 5 NOT_STATED, 0 FINDING.**
16 CSV relationship rows (PoRFeedChange has labels S3-2 and S2-1).
The existing report does not attribute a new specific security finding
to one of these active instances; bugs.csv must remain unmodified.

## Individual second semantic review
| ID | Target | Property | Result / outcome | What falsifies the assertion |
| ---: | --- | --- | --- | --- |
| 1 | Aggregator | PoRFeedChange | VERIFIED / NO_FINDING | feed & wrapper transitions and zero-address checks |
| 2 | Aggregator | notAllReservesBacked_UnbackedArry_Correlation | VERIFIED / NO_FINDING | aggregate backing boolean disagrees with per-asset helper |
| 3 | Executor V2 | integrityOfDisableAssets | VERIFIED / NO_FINDING | disable leaves flag enabled or wrong list length |
| 4 | Executor V2 | integrityOfEnableAssets | VERIFIED / NO_FINDING | enable leaves flag disabled or wrong list length |
| 5 | Executor V2 | enableDuplicationsWithStorage | VERIFIED / NO_FINDING | enabling twice differs from once |
| 6 | Executor V2 | disableDuplicationsWithStorage | VERIFIED / NO_FINDING | disabling twice differs from once |
| 7 | Executor V2 | flagConsistancy | NOT_STATED / NOT_STATED | V2 mirrored flag/list mismatch |
| 8 | Executor V2 | uniqueArray | NOT_STATED / NOT_STATED | V2 duplicate asset indices |
| 9 | Executor V3 | integrityOfDisableAssets | VERIFIED / NO_FINDING | disable leaves flag enabled or wrong list length |
| 10 | Executor V3 | integrityOfEnableAssets | VERIFIED / NO_FINDING | enable leaves flag disabled or wrong list length |
| 11 | Executor V3 | enableDuplicationsWithStorage | VERIFIED / NO_FINDING | enabling twice differs from once |
| 12 | Executor V3 | disableDuplicationsWithStorage | VERIFIED / NO_FINDING | disabling twice differs from once |
| 13 | Executor V3 | flagConsistancy | NOT_STATED / NOT_STATED | V3 in-range list asset has disabled flag |
| 14 | Executor V3 | flagConsistancy2 | NOT_STATED / NOT_STATED | V3 active flag maps to different asset |
| 15 | Executor V3 | uniqueArray | NOT_STATED / NOT_STATED | V3 duplicate asset indices |

The report describes three aggregate invariant concepts, including
Asset Is Not Zero, but five active source invariants are present across
Executor V2/V3. No report glyph is assigned individually to those five
without one-to-one evidence. Four common Executor rules are reported
as verified for each version; aggregator rules are named explicitly.

## Semantic divergences and model caveats
- Aggregator PoRFeedChange prohibits mapping changes by unrelated
  functions, contrary to contradictory PDF prose saying "must change."
- Source disableAssets assertions use assetStateBefore where report
  formulas sometimes use assetStateAfter.
- Duplication-rule report formulas include conditions absent from active
  CVL. No assertions are fabricated.
- Executor V2 uses mirrorArray/mirrorFlag/reverseMap/_assetsLength ghosts,
  preserved invariants and Sload/Sstore hooks, and filters the emergency
  selector. Executor V3 uses distinct OneToOne_arrOfTokens/Consistant_flag
  ghosts, reverseMapInit, access-set hooks and an extra msg.value==0
  requirement in its duplication rules.
- V2 emergency logic disables borrowing across the pool and freezes
  affected assets. V3 freezes affected assets and sets their LTV to zero.
  Commented emergency properties are not revived.
- Missing original areAllReservesBackedCorrelation/allBacked, enableAsset,
  disableAsset, getAssetState, getAsset, getAssetsLength and Dummy/harness
  implementations cannot be inferred from methods declarations.
- The report assumes correct external configurator effects and checks
  only invoked functions; executor aggregator responses are nondeterministic;
  loops are unrolled to three iterations; external calls may affect other
  contracts but are assumed not to change the verified contract state.
  Historical VERIFIED is scoped to these assumptions and is not a new
  unrestricted formal proof.

## Validation and provenance
The original CVL and Solidity snapshot lives under contracts/15;
each results/spec/incomplete/15/N.spec, N.sol, N.md, N.txt describes
a property, actual source line excerpts, its report result, technical
Bug Label, target, specific missing dependencies, and counterexample.
CSV changes are additive only for Project 15; Project 2 records untouched.
Run scripts/check_specs.py, check_contests_csv.py and check_contracts.py
with python from Web3Bugs-certora; run git -c core.whitespace=cr-at-eol
diff --check origin/main...HEAD at Git root, and record exact exit codes.
Structural validation is not Certora re-verification.

The local ZIP was not inspected because local Python/container tooling
failed with infrastructure errors. GitHub checkout and versioned Git
blobs, not an unverified ZIP, are the source for this recatalog.
