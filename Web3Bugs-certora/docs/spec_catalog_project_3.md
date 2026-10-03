# Project 3 — AAVE Rescue Mission Phase 1 Spec Catalog

This document records the completion state of the Certora property catalog for Project 3.

## Coverage

- rescueLendMigrator.spec: 1 active invariant + 1 active rule = 2 active properties
- rescueSTKAAVE.spec: 1 active invariant
- Total active property instances: **3**
- Complete examples: **0**
- Incomplete examples: **3**
- Bug Label relationship rows added to spec_buglabel.csv: **3**

The commented-out rule named LendIsBackedByAave at source lines 29-39 is not active and is not counted separately from the active invariant of the same name.

## Dependency status

All three examples are incomplete because the source specs depend on historical linked dummy-token contracts that are absent from the Rescue Mission snapshot.

Known missing dependencies:

- DummyERC20Impl as LEND1: affects LendIsBackedByAave
- DummyERC20Impl2 as AAVE1: affects LendIsBackedByAave
- DummyERC20Impl as LEND1: affects LendIsBackedByAaveIncInitialize
- DummyERC20Impl2 as AAVE1: affects LendIsBackedByAaveIncInitialize
- DummyERC20Impl as STAKED_TOKEN1: affects StkAaveIsBackedByAave

A full-tree PropertyGPT search found generic DummyERC20Impl contracts in unrelated projects, but no applicable Rescue Mission harness and no DummyERC20Impl2 implementation inside the supplied project snapshot.

An independent upstream check identified the exact historical missing artifacts in bgd-labs/rescue-mission-phase-1: certora/harness/ERC20Dummy.sol, certora/harness/ERC20Dummy2.sol, certora/harness/SafeMath.sol, verifyRescueLendMigrator.sh, and verifyRescueStkAAVE.sh. The upstream scripts confirm the target/link mappings used by the specs. The PropertyGPT specs are byte-identical to the upstream Certora Review copies. These upstream files are deliberately not copied into Project 3 because complete/incomplete is defined against the supplied PropertyGPT snapshot, not against artifacts recovered later from the internet.

AaveTokenV2, LEND_AAVE_RATIO(), totalSupply(), and REWARDS_VAULT() are resolved from concrete code in the Project 3 snapshot where applicable. A declaration in methods {} was not treated as a Solidity/harness implementation. For the Lend target, the snapshot also lacks the external solidity-utils IERC20 package imported by LendToAaveMigrator.sol; the upstream historical run script supplied it with a package mapping.

## Formal results

Across the 3 active source property instances:

- VERIFIED: **2**
- VIOLATED: **1**
- NOT_STATED: **0**

Audit interpretation:

- FINDING: **2**
- NO_FINDING: **1**
- ACCEPTED_BEHAVIOR: **0**
- INCONCLUSIVE: **0**
- NOT_STATED: **0**

LendIsBackedByAave is marked ❌ in the Formal Properties section and is explicitly named as broken for two report issues. The report also states that the issues were fixed and their fixes verified. The catalog preserves the explicit property status as VIOLATED rather than inferring a different individual result from that report-wide statement.

LendIsBackedByAaveIncInitialize is explicitly marked ✔ and is not specifically named as the broken property for a report issue, so it is VERIFIED / NO_FINDING.

The VIOLATED simple invariant and VERIFIED extension are semantically compatible. The simple invariant demands the backing relation in the immediate post-state of preserved calls. The extension rule instead executes the migrator initializer and AAVE token initializer back-to-back with the same lendToAaveAmount before asserting the relation. It is therefore an end-state sequence proof, not a proof that the intermediate state between the two real asynchronous governance upgrades is always backed or that arbitrary interleavings are safe.

StkAaveIsBackedByAave is explicitly marked ✔ on the fixed code, but the Main Issues section says this property caught the undercollateralizing rescue behavior before mitigation. It is therefore VERIFIED / FINDING.

## Findings related

The report lists three main issues:

1. Rescue of underlying AAVE from StakedTokenV2Rev4 could undercollateralize stkAAVE. The broken property named by the report is StkAaveIsBackedByAave.
2. Rescue of AAVE/LEND from LendToAaveMigrator could leave remaining LEND insufficiently collateralized. The broken property named by the report is LendIsBackedByAave.
3. A burnt-LEND miscount introduced in commit 759275c could understate circulating LEND and therefore the AAVE backing requirement. The report again names LendIsBackedByAave.

The findings are recorded in results/bugs.csv separately from the property labels. The rescue execution is performed through Aave governance proposal payloads that call proxy upgradeToAndCall, so the primary finding label is O1 for this dataset. The technical property relationship remains S6-4. The third finding has an S6-3-like narrower arithmetic mechanism, but the final finding label remains separate from the detector-property label.

The report's Main Issues section uses labels such as Property #1 for StkAaveIsBackedByAave and Property #2 for LendIsBackedByAave, while the later Formal Properties section numbers those entries differently. Linkage is therefore based on the exact property names, not the inconsistent numeric references.

RM-01, RM-02, and RM-03 in results/bugs.csv are catalog-local identifiers because the report does not provide stable issue IDs or severities for these three Potential Issue entries. Severity remains - rather than being inferred.

## Bug Label mapping and UNMAPPED

- LendIsBackedByAave: S6-4
- LendIsBackedByAaveIncInitialize: S6-4
- StkAaveIsBackedByAave: S6-4
- UNMAPPED: **0**

All three active properties encode normative backing/accounting requirements. None is merely a reachability, sanity, or generic mutation probe.

## Assumptions and important qualifiers

The report explicitly documents:

- loop unrolling limited so violations requiring more than one loop iteration are not detected;
- onTransfer is assumed not to change any contract state;
- for the LEND backing property, msg.sender is assumed to be neither the LEND token contract nor the AAVE V2 token contract;
- ✔* denotes proofs under simplification/assumptions, but the extracted report text does not support assigning an individual star to any of the three source instances without speculation.

The source specs also contain preserved/precondition restrictions that are retained literally.

A source quirk is preserved in LendIsBackedByAaveIncInitialize: it declares env e2 but invokes AAVE_ORIG.initialize with e. No correction is made during cataloging.

The report prose for LendIsBackedByAaveIncInitialize also contains a reqs2 footnote marker, but the supplied PDF's final page defines only reqs. The missing reqs2 text is treated as unresolved report metadata; no assumption is invented for it.

## Reproduction limitations

Dependency-complete reproduction is not possible from the supplied PropertyGPT snapshot. The independent review established the following limitations:

- the exact historical ERC20 dummy harnesses and their SafeMath dependency are absent from the snapshot;
- the original verifyRescueLendMigrator.sh and verifyRescueStkAAVE.sh run scripts are absent, although the upstream copies show the target/link mappings, solc map, package map, and --optimistic_loop flag;
- LendToAaveMigrator.sol imports the external solidity-utils IERC20 package, which is not included in Project 3;
- source-era CVL syntax and prover behavior remain historical and CVL2 migration is intentionally out of scope;
- the report's bounded loop and onTransfer assumptions still limit what a verification result establishes;
- the paired LendIsBackedByAaveIncInitialize rule checks the end state after two back-to-back modeled initializers and does not prove arbitrary intermediate interleavings between the real short- and long-executor governance steps.

There is also source-version drift. The two PropertyGPT specs are byte-identical to the upstream Certora Review commit 33c1aeca, while the PropertyGPT Solidity files are byte-identical to a later upstream master snapshot. Relative to the Certora Review Solidity, the later master changes relevant to these files are constructor-side lastInitializedRevision assignments; however, the report's stated latest reviewed commit 4c59da8d is older and materially differs in the Lend/AAVE initializer signatures. The report also refers to later mitigation commit c905eaf. Therefore no single commit in the supplied evidence can safely be asserted as the exact code snapshot for every report status. The extracted .sol files are explicitly context from the supplied PropertyGPT snapshot.

For project metadata, the PDF body says the work was undertaken January 6-12 but omits the year. Certora's official report page identifies the report as January 2023, and the PropertyGPT paper independently lists the project as 2023/January. results/contests.csv therefore uses 2023-01. The preserved PDF itself has a later file-generation timestamp, which is not treated as the audit month.

## Semantic second review

| Source instance | What would make the assertion fail? | Bug Label review | Normative? | Report attribution review |
| --- | --- | --- | --- | --- |
| LendIsBackedByAave | Required AAVE backing computed from circulating LEND exceeds the migrator's AAVE balance after an allowed preserved execution | S6-4 directly matches a broken collateral/accounting relation | Yes | Exact property is marked ❌ and named for two issues |
| LendIsBackedByAaveIncInitialize | A state starts backed but the selected arbitrary call, or the migrator initialize + AAVE initialize sequence, ends underbacked | S6-4; the executable assertion is the backing inequality | Yes | Exact property is ✔; report does not name this exact rule as broken |
| StkAaveIsBackedByAave | stkAAVE totalSupply() exceeds the target's underlying AAVE balance | S6-4 directly matches liability-versus-asset backing | Yes | Exact property is ✔ on fixed code and explicitly named as detector of an earlier issue |

This review intentionally separates property semantics, formal Result, Detection Outcome, finding classification, and Target Contract.

## Source integrity

The source specs were copied byte-for-byte from the PropertyGPT project into contracts/3/specs/ before extraction.

SHA-256 of the original source specs:

- rescueLendMigrator.spec: ffac5f5dcf6c99ad25a18eef2929b1a4d6c31d156970f227ac7c10c7ef8661aa
- rescueSTKAAVE.spec: ecc7ef67d01904b40a8e049a7bd783a9d919c59de1debf3ea8909424ea41d304

Independent upstream comparison found both hashes identical to the specs added in upstream Certora Review commit 33c1aeca. The copied Solidity snapshot, by contrast, matches the later upstream master files rather than that exact Certora Review tree. This distinction is recorded so that source-spec identity is not confused with exact historical prover-code identity.

## Validation

The three exact commands requested by the workflow were attempted initially. This host does not provide a python executable, so those invocations return exit 127 before reaching validator logic. The equivalent python3 commands were rerun after the independent review and all pass:

- python3 scripts/check_specs.py . — PASS: 88 spec examples and 91 Bug Label relationships are structurally consistent.
- python3 scripts/check_contests_csv.py . — PASS: results/contests.csv is consistent with reports/.
- python3 scripts/check_contracts.py . — PASS: contracts/ is consistent with reports/.

A separate adversarial Project 3 review also passes after the corrections documented below. It independently checks:

- exactly 3 active source properties and exactly 3 Project 3 catalog examples;
- exact Property, Bug Label, Result, Detection Outcome, Target Contract, and Status values;
- literal preservation of every extracted CVL source range and active property block;
- literal presence of every Solidity range declared in each .sol;
- byte identity of contracts/3/contracts and contracts/3/specs with the supplied PropertyGPT snapshot;
- no complete/3 artifacts;
- exact report-name/status glyph evidence and finding linkage;
- 3 report-linked finding rows with O1, catalog-local IDs, and no inferred severity;
- local absence of the historical dummy harnesses together with independent upstream corroboration of the exact missing harness/link configuration;
- source-spec hashes and preserved report-PDF hash;
- 2023-01 contest metadata;
- explicit recording of the unresolved reqs2, source-version drift, paired-rule/intermediate-state limitation, and external solidity-utils dependency.

The adversarial review found and corrected several catalog-quality issues:

1. 3.sol had truncated totalSupply() at source lines 489-490 and omitted its closing brace at line 491. The excerpt now includes 489-491.
2. 3.sol did not include claimRewards or the concrete _beforeTokenTransfer hook. Those excerpts were added because they explain the REWARDS_VAULT preservation restriction and the report's onTransfer assumption.
3. 2.sol previously copied a broad AaveTokenV2 region while omitting the concrete safeTransfer and onTransfer paths. It now uses smaller, behavior-specific ranges.
4. The incomplete reasons originally knew only that dummy contracts were absent. Independent upstream review identified the exact missing historical harnesses, SafeMath helper, link mappings, run scripts, package mapping, and --optimistic_loop; the examples remain incomplete because those artifacts are absent from the supplied PropertyGPT snapshot.
5. Source-version drift was made explicit: the specs match the upstream Certora Review copy, the supplied Solidity matches a later upstream master snapshot, and the report's stated commit does not line up with all later source/formula evidence.
6. The paired nature of LendIsBackedByAaveIncInitialize is now documented so VERIFIED is not overstated as proving the intermediate asynchronous governance state.
7. The unresolved reqs2 report marker and inconsistent report property numbering are now recorded rather than silently interpreted.
8. Project time was updated from - to 2023-01 using external official corroboration of the year/month; no exact day is inferred into the dataset.

A targeted git diff --check over the Project 3 artifacts and results/bugs.csv passes. Running it directly on the shared CSVs flags their carriage-return line endings as trailing whitespace because those files historically use CRLF; their original newline convention was deliberately preserved rather than normalized. git diff --numstat confirms the shared CSV diffs remain additive only: 19 added property rows total for the existing Project 2 plus Project 3 work, 2 added contest rows, and 3 added Project 3 bug rows.

The structural validator does not rerun the Certora Prover or prove CVL semantics.

## Catalog locations

- Index: results/spec/spec_buglabel.csv
- Incomplete examples: results/spec/incomplete/3/
- Project report transcript: reports/3.md
- Preserved report PDF: resources/3/Rescue-Mission-Phase-1.pdf
