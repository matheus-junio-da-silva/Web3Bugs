# Project 2 — AAVE Proof of Reserve Spec Catalog

This document records the completion state of the Certora property catalog for Project 2.

## Coverage

- aggregator.spec: 2 active rules
- executorV2.spec: 4 active rules + 2 active invariants = 6
- executorV3.spec: 4 active rules + 3 active invariants = 7
- Total active property instances: **15**
- Complete examples: **1**
- Incomplete examples: **14**
- Bug Label relationship rows added to spec_buglabel.csv: **16**

The two integrityOfExecuteEmergencyAction rules are commented out in the supplied source specs and are not counted as active, even though the report discusses verified Executor V2/V3 emergency-action properties.

## Dependency status

Complete:
- PoRFeedChange

Known missing historical dependencies, with overlapping counts:
- areAllReservesBackedCorrelation: 1 example
- allBacked implementation/harness: 1 example
- enableAsset implementation/harness: 4 examples
- disableAsset implementation/harness: 4 examples
- getAssetState implementation/harness: 10 examples
- getAssetsLength implementation/harness: 13 examples
- getAsset implementation/harness: 3 examples

The production Solidity snapshot contains _assets and _assetsState plus bulk enableAssets/disableAssets behavior, but it does not contain the single-asset/getter harness declared in the CVL methods blocks. Those declarations were not treated as Solidity implementations.

## Formal results

Across the 15 active source property instances:
- VERIFIED: **10**
- VIOLATED: **0**
- NOT_STATED: **5**

Audit interpretation:
- NO_FINDING: **10**
- FINDING: **0**
- ACCEPTED_BEHAVIOR: **0**
- INCONCLUSIVE: **0**
- NOT_STATED: **5**

The four exact rule names shared by Executor V2/V3 are listed by the report under Common for Executor and are treated as VERIFIED for each concrete source instance. The two Aggregator rule names are also listed explicitly and are treated as VERIFIED.

The five active source invariants use names that do not map one-to-one to the report's descriptive entries Asset State Is Valid, Asset Is Not Zero, and Assets Uniqueness. Because the source contains five invariant instances while the report presents three descriptive aggregate concepts, no report result was automatically propagated to those source invariants; they remain NOT_STATED.

## Findings related

The report states that Certora also performed a manual audit, but the supplied six-page report does not attribute a reportable security finding to any of the 15 active source properties cataloged here. No property is therefore marked FINDING.

## Bug Label mapping and UNMAPPED

- S3-2: state/list/membership consistency and idempotent disable/enable-state transitions
- S2-1: non-zero feed and wrapper address validation in PoRFeedChange
- S2-3: duplicate asset identifier / array uniqueness checks
- S6-2: consistency of aggregate and per-asset reserve-backed return semantics
- UNMAPPED: **0**

All 15 properties encode normative consistency/uniqueness/return-value requirements rather than pure reachability or exploratory probes.

## Assumptions and important qualifiers

The report explicitly documents:
- PoolConfigurator and LendingPoolConfigurator actions are assumed to work as intended; only invocation was checked.
- In Executor V2/V3 verification, ProofOfReserveAggregator.areAllReservesBacked was summarized to arbitrary values.
- Loops are unrolled; violations requiring more than three iterations may not be detected.
- External calls may have arbitrary side effects outside the verified contract but are assumed not to affect the verified contract's state.
- The report defines ✔* for rules verified under simplified assumptions.

The active V2/V3 invariants in the source also filter executeEmergencyAction through tempOmittedFunc with comments stating the filter was temporary until a prover update.

Because PDF text extraction does not preserve every status glyph cleanly, the catalog records the report-wide simplifications explicitly rather than inventing a star qualifier for an individual row when the exact glyph is ambiguous. The original PDF is preserved at resources/2/Aave-Proof-of-Reserve-Formal-Verification-Report.pdf.

## Reproduction limitations

Dependency-complete means complete only with respect to the available snapshot. Exact reproduction remains limited by:
- missing historical harness implementations listed above;
- missing run/configuration material for the original Certora invocation;
- source-era CVL syntax and prover behavior;
- the report's loop-unrolling and external-call assumptions;
- the historical model/summarization choices described in the report.

CVL2 migration is intentionally not performed during cataloging.

## Semantic second review

| Source instance | What would make the assertion fail? | Bug Label review | Normative? | Report attribution review |
| --- | --- | --- | --- | --- |
| Aggregator PoRFeedChange | Wrong/nonzero feed-wrapper transition, failure to clear, or unrelated method mutates mappings | S3-2 for state transition; S2-1 for non-zero address validation | Yes | Exact report name: VERIFIED |
| Aggregator notAllReservesBacked_UnbackedArry_Correlation | Aggregate backed flag disagrees with per-asset correlation | S6-2 matches return-semantic disagreement | Yes | Exact report name: VERIFIED; source helper missing |
| V2 integrityOfDisableAssets | Flag remains active or length change disagrees with prior membership | S3-2 | Yes | Exact Common-for-Executor name: VERIFIED |
| V2 integrityOfEnableAssets | Flag remains inactive or length change disagrees with prior membership | S3-2 | Yes | Exact Common-for-Executor name: VERIFIED |
| V2 enableDuplicationsWithStorage | Two enables differ from one, including duplicate insertion | S2-3 | Yes | Exact Common-for-Executor name: VERIFIED |
| V2 disableDuplicationsWithStorage | Second disable causes extra state/list mutation | S3-2 | Yes | Exact Common-for-Executor name: VERIFIED |
| V2 flagConsistancy | Flag and mirrored array membership disagree | S3-2 | Yes | Descriptive report invariant is not exact: NOT_STATED |
| V2 uniqueArray | Two distinct in-range indices contain same address | S2-3 | Yes | Descriptive report invariant is not exact: NOT_STATED |
| V3 integrityOfDisableAssets | Flag remains active or length change disagrees with prior membership | S3-2 | Yes | Exact Common-for-Executor name: VERIFIED |
| V3 integrityOfEnableAssets | Flag remains inactive or length change disagrees with prior membership | S3-2 | Yes | Exact Common-for-Executor name: VERIFIED |
| V3 enableDuplicationsWithStorage | Two enables differ from one, including duplicate insertion | S2-3 | Yes | Exact Common-for-Executor name: VERIFIED |
| V3 disableDuplicationsWithStorage | Second disable causes extra state/list mutation | S3-2 | Yes | Exact Common-for-Executor name: VERIFIED |
| V3 flagConsistancy | In-range array asset is not marked active | S3-2 | Yes | Descriptive report invariant is not exact: NOT_STATED |
| V3 flagConsistancy2 | Active nonzero address does not round-trip through reverseMap/array | S3-2 | Yes | Descriptive report invariant is not exact: NOT_STATED |
| V3 uniqueArray | Two distinct in-range indices return same address | S2-3 | Yes | Descriptive report invariant is not exact: NOT_STATED |

This review intentionally separates property semantics, formal Result, Detection Outcome, target contract, and any report-level descriptive property.

## Source integrity

The original source specs were copied byte-for-byte into contracts/2/specs before extraction. SHA-256:
- aggregator.spec: f6787f5c0a14f0a7cb20115a3bdc1db6379f5301b405d93f610928814a854fb8
- executorV2.spec: 80c9afa753589467785cbcf634c067cecdf24f43c0a1ba18757e76fd68518640
- executorV3.spec: e213486c2268bdec03db68822e7a244343a32171706aea3104c4679eba1f0c06

## Validation

All required structural validators pass. This host does not provide a python alias, so the same scripts were executed with python3:

- python3 scripts/check_specs.py . — PASS: 85 spec examples and 88 Bug Label relationships are structurally consistent.
- python3 scripts/check_contests_csv.py . — PASS.
- python3 scripts/check_contracts.py . — PASS.

An additional catalog audit also passed:
- 15 active source properties exactly match the 15 Project 2 CSV instances;
- every extracted rule/invariant block is a literal substring of its source spec;
- copied source-spec SHA-256 hashes match the original PropertyGPT snapshot;
- the two commented integrityOfExecuteEmergencyAction rules remain excluded.

The structural validator does not rerun the Certora Prover or prove CVL semantics.

## Catalog locations

- Index: results/spec/spec_buglabel.csv
- Complete examples: results/spec/complete/2/
- Incomplete examples: results/spec/incomplete/2/
- Project report transcript: reports/2.md
- Preserved report PDF: resources/2/Aave-Proof-of-Reserve-Formal-Verification-Report.pdf

## Independent review findings

A second adversarial review was performed after initial catalog generation. It re-read the workflow and taxonomy, re-enumerated the active properties, compared source assertions with the original PDF report, expanded the dependency search to the full PropertyGPT repository, and rechecked the extracted artifacts.

Corrections made during review:

- Corrected inaccurate Original Spec Lines for PoRFeedChange and all Executor V2 examples. The earlier ranges incorrectly described omitted source lines as copied.
- Added the original latestRoundData() => NONDET summary to the PoRFeedChange extraction. Because the rule executes an arbitrary method f, a non-management branch can reach areAllReservesBacked, whose Solidity implementation calls the Chainlink feed.
- Added S2-1 as a second defensible relationship for PoRFeedChange. Its successful enable assertions require non-zero feed/wrapper address identifiers, while S3-2 still captures the mapping transition requirements.
- Added explicit source/report interpretation notes to affected examples rather than silently reconciling contradictory prose or formulas.
- Restored reports/2.md from direct PDF text extraction after detecting that an intermediate review edit had truncated it.

Material source/report differences preserved as uncertainty:

- The report's PoRFeedChange prose says unrelated functions should make feed/wrapper values change, while the executable source assertion requires them to remain unchanged. Classification follows the source assertion.
- For integrityOfDisableAssets, the report/source comment formula uses assetStateAfter in the length implications, but the executable source rules use assetStateBefore. Classification and methodology follow the executable rule.
- The report formulas for the two duplication rules contain additional postconditions not present in the supplied rule bodies. The report status is retained because the property names are explicit, but the formulas are not substituted for the source rules.
- The report contains three descriptive invariant concepts, while the supplied source has five active target-specific invariant instances. In particular, Asset Is Not Zero has no exact active invariant in the supplied snapshot. These source invariants remain NOT_STATED rather than inheriting an aggregate report result.
- The report discusses active V2/V3 integrityOfExecuteEmergencyAction properties, but both source rules are commented out in the supplied specs. They are correctly excluded from the active-property catalog.
- The report identifies latest reviewed commit 12296ce, but the local PropertyGPT snapshot does not provide evidence that its copied specs are byte-identical to that upstream commit. Exact historical run reproduction therefore remains unproven.

Expanded dependency search:

The full PropertyGPT repository was searched for the missing historical helpers/harnesses. No implementation of areAllReservesBackedCorrelation, allBacked, the single-asset enableAsset/disableAsset helpers, getAssetState, getAssetsLength, or the relevant historical getAsset harness was found for this project. Matches elsewhere were unrelated datasets or unrelated modern Aave code and were not imported as dependencies.

Label interpretation review:

- PoRFeedChange: S3-2 plus S2-1 is defensible because the rule combines exact mapping-transition assertions with non-zero address validation.
- enableDuplicationsWithStorage: S2-3 is retained because a second enable producing a larger list directly admits duplicate asset identity; SE-3 is a possible sequence-level description, but the taxonomy process prefers the more specific ID-related root cause when available.
- disableDuplicationsWithStorage: S3-2 is retained because a failure is an extra state/list mutation on the second disable; SE-3 is a possible sequence-level description but is less specific than the state-update oracle.
- uniqueArray: S2-3 remains direct.
- flagConsistancy/flagConsistancy2: S3-2 remains the conservative mapping because the assertions test disagreement between membership state representations rather than uniqueness itself.
- notAllReservesBacked_UnbackedArry_Correlation: S6-2 remains defensible from the equality assertion plus the report's stated return semantics, but the missing helper body is explicitly documented as a limitation.
- Replaced inferred contest metadata (type, high-count, and DefiLlama) with "-" because those fields are not established by the supplied report; only the project name and 2022-11 date are retained as report-supported metadata.
