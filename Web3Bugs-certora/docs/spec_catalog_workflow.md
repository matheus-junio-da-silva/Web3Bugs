# Spec Catalog Workflow

This document describes how to catalog Certora properties for additional projects in `Web3Bugs-certora`.

The goal is to preserve a small, auditable unit that connects a formal property to a Web3Bugs Bug Label and to the Solidity code that motivated the property.

## Core principles

1. Never modify the original project snapshot under `contracts/<project-id>/`.
2. Preserve the original CVL property text whenever possible.
3. Extract only the dependencies actually required by the selected property.
4. Preserve source file paths and original line ranges.
5. Do not silently reconstruct missing harnesses or helpers.
6. Do not migrate historical CVL syntax to CVL2 during this cataloging step.
7. Do not force a Web3Bugs label when the relationship is weak; use `UNMAPPED`.
8. Keep formal verification outcome (`Result`) separate from audit interpretation (`Detection Outcome`).
9. Separate documented facts from reconstructed methodology.

## Inputs for one project

Before cataloging a project, identify:

- the `Project ID` from `results/contests.csv`;
- the original `.spec` files under `contracts/<project-id>/`;
- the Solidity contracts under the same project snapshot;
- the corresponding report under `reports/<project-id>.md`;
- the Web3Bugs taxonomy in `docs/standard.md`.

## Output layout

Dependency-complete examples are stored under:

```text
results/spec/complete/<project-id>/
```

Dependency-incomplete examples are stored under:

```text
results/spec/incomplete/<project-id>/
```

For one example `N`, keep the related files together:

```text
N.spec   extracted CVL property and required available CVL dependencies
N.sol    relevant Solidity excerpts
N.md     explanation, provenance, Bug Label relationship, and methodology
N.txt    only for incomplete examples; explains the missing dependency
```

The catalog index is:

```text
results/spec/spec_buglabel.csv
```

`Project ID + Status + Example ID` identifies an example. Numeric IDs may restart for each project and status directory.

## Step 1 — Inventory the original verification material

List all `.spec` files for the project and inspect their top-level structure.

Record at least:

- imports such as `import "other.spec"`;
- `using` declarations;
- `methods { ... }` declarations;
- `definition` declarations;
- invariants;
- ghosts and hooks;
- rule names;
- helper or harness names that are not Solidity ABI methods.

Also search the project for configuration or harness files that may have been used during the original Certora run.

Useful searches include:

```bash
find contracts/<project-id> -type f
grep -RIn --include='*.spec' -E '^[[:space:]]*(import|using|methods|definition|invariant|ghost|hook|rule)' contracts/<project-id>
```

Do not assume that every dependency used by the original verification is present in the snapshot.

## Step 2 — Select one original property

Use the exact original `rule` or `invariant` name as the CSV `Property` value.

Example:

```cvl
rule independentQueuedActions(method f)
```

becomes:

```text
Property = independentQueuedActions
```

Record the exact source file and line range containing the property.

If the same property exists in multiple specs for different target contracts, treat each target-specific instance independently when its dependencies or execution context differ.

## Step 3 — Read the report before classifying anything

Search the project report for the property name and for any issue connected to it.

Determine:

- what security behavior the report says the property represents;
- whether the report states the property was verified or violated;
- whether the property produced or directly supported a reported finding;
- whether a counterexample was accepted by the project as intended/acceptable behavior;
- whether the report documents assumptions or simplifications;
- whether a reported issue explicitly references the property.

Set `Result` from the original report only:

- `VERIFIED` — the report states that the property was verified;
- `VIOLATED` — the report states that the property was violated;
- `NOT_STATED` — the final report does not state an outcome.

Then set `Detection Outcome` from the audit interpretation:

- `FINDING` — the property result produced or directly supported a reported security finding;
- `ACCEPTED_BEHAVIOR` — the property exposed a behavior/counterexample, but the project explicitly treated it as intended, acceptable, or not a bug;
- `NO_FINDING` — the property did not produce a reported issue, typically because it was verified;
- `INCONCLUSIVE` — the available material is insufficient to determine the security meaning;
- `NOT_STATED` — the report does not state enough information to determine the audit outcome.

`Result` is not the status of the extracted `.spec` file, and `Detection Outcome` is not the Web3Bugs label.

Do not infer `Detection Outcome` mechanically. A `VIOLATED` property can be `FINDING`, `ACCEPTED_BEHAVIOR`, or `INCONCLUSIVE` depending on the documented audit interpretation. Likewise, do not assume that every `O6` mapping is automatically `ACCEPTED_BEHAVIOR`; verify the report/project response.

Examples:

```text
Result = VIOLATED
Detection Outcome = FINDING
```

means that a formal counterexample was found and it was treated as a reportable issue.

```text
Result = VIOLATED
Detection Outcome = ACCEPTED_BEHAVIOR
```

means that a formal counterexample/behavior was observed but the project did not treat it as a vulnerability.

An example can also be `Status = incomplete` and `Result = VERIFIED` when the original report verified the property using a helper or harness that is missing from the available snapshot.

## Step 4 — Determine the Target Contract

`Target Contract` is the contract against which the property is intended to be interpreted or executed.

Do not infer the target only from the Solidity excerpt.

For example, a property may inspect logic implemented in `BridgeExecutorBase.sol` while its target contract is `PolygonBridgeExecutor`.

Use the concrete target contract when it can be established from the original spec/project context.

If the same formal property was intended for materially different targets, create separate examples or rows rather than hiding the distinction.

## Step 5 — Build the dependency closure

Starting from the selected property, inspect every non-built-in symbol it references.

For each symbol, determine whether it is:

1. a CVL built-in, such as `lastReverted`, `lastStorage`, `currentContract`, or `max_uint`;
2. a Solidity ABI method on the target contract;
3. a declaration from the original `methods {}` block;
4. a `definition` from the same spec;
5. an invariant required by the property;
6. a ghost, hook, or other CVL construct;
7. a symbol provided by an imported `.spec`;
8. a contract introduced by `using`;
9. a helper/harness supplied outside the visible Solidity ABI;
10. another unresolved external artifact.

Follow dependencies recursively until every required non-built-in symbol is accounted for.

Do not copy an entire imported spec merely because the original file imports it. Include it only when the selected property actually depends on symbols from that import.

### Dependency completeness rule

An example is `complete` when every non-built-in symbol required by the extracted property can be resolved from:

- CVL content included in the extracted `.spec`; or
- files present in the project snapshot.

An example is `incomplete` when an original dependency needed by the property cannot be resolved from the available snapshot.

Missing historical CVL syntax migration is not an `incomplete` dependency by itself. CVL2 migration is a separate future task.

### Typical complete case

A property calls `getDelay()` and uses `stateVariableUpdate(f)`. The original spec contains the required `methods` declaration and the `stateVariableUpdate` definition. Both are copied into the extracted `.spec`.

### Typical incomplete case

A property calls `queue2(...)`, the report says `queue2` was a simplified verification helper, but no declaration or implementation exists in the snapshot. The example belongs under `incomplete/`.

## Step 6 — Create the extracted `.spec`

Create:

```text
results/spec/<complete|incomplete>/<project-id>/<example-id>.spec
```

The extracted file should contain:

1. a short English provenance header;
2. the required original CVL declarations from `methods {}`;
3. required definitions, invariants, ghosts, hooks, or imported declarations;
4. the selected original property.

Keep original CVL syntax at this stage.

Do not rewrite the property to make it cleaner, newer, or more generic.

Do not add a replacement for a missing original helper merely to make the example look complete.

Record every copied source range in the header and in the CSV `Original Spec Lines` field.

## Step 7 — Create the relevant `.sol` excerpt

Create:

```text
results/spec/<complete|incomplete>/<project-id>/<example-id>.sol
```

The `.sol` file is evidence/context for the property. It is not required to be a standalone compilable contract.

Extract the smallest useful Solidity regions that explain the security behavior checked by the CVL property.

Examples of useful regions include:

- the state variable being checked;
- the state update that should occur;
- the authorization modifier;
- the hash or ID construction involved in a uniqueness property;
- the function entrypoint exercised by the rule;
- a base-contract implementation inherited by the target.

If relevant code spans multiple Solidity files, include multiple clearly separated excerpts in the same `N.sol` and record all original source files/ranges in the documentation and CSV.

## Step 8 — Map the property to a Web3Bugs Bug Label

Read `docs/standard.md` and map based on the detection intent of the property, not on severity and not only on the vulnerability found in one specific report.

Rules:

- use the most technically defensible Bug Label;
- the same example may have multiple CSV rows when more than one mapping is defensible;
- do not duplicate `.spec`, `.sol`, or `.md` files just because there are multiple labels;
- if no defensible relationship exists, set `Bug Label = UNMAPPED`.

`UNMAPPED` is a dataset sentinel. It is not part of the original Web3Bugs taxonomy.

Do not invent a weak mapping merely to avoid `UNMAPPED`.

### Semantic interpretation rules

The primary rule is:

> **Classify what the property actually asserts, not what its name or comment suggests.**

Read the complete `rule` or `invariant` body and reason from the encoded preconditions, calls, state observations, and final assertion. A property name may be suggestive but is not authoritative for Bug Label mapping.

Apply the following rules:

- Distinguish **normative properties** from **diagnostic or exploratory properties**. Reachability checks, sanity rules, generic mutation probes such as “who changed X?”, and rules intended to discover which functions can perform an operation may not encode a security requirement by themselves. If no clear security requirement exists, use `UNMAPPED` rather than forcing an `S` label.
- Do not confuse a **partial detector** with a **complete proof**. For example, a property showing that two distinct callers cannot both succeed does not necessarily prove that the one caller who can succeed is the correct authorized identity. Describe exactly what the property establishes.
- Keep the **Bug Label of the property** separate from the **Bug Label of a reported finding**. A property may have technical intent `S2-3` while the final finding is classified `O1` by the Web3Bugs process.
- Never infer `Result` from the property code. `VERIFIED`, `VIOLATED`, and `NOT_STATED` must come from the report or equivalent original verification evidence.
- Never infer `Detection Outcome` from `Result` alone. A `VIOLATED` result may correspond to `FINDING`, `ACCEPTED_BEHAVIOR`, or `INCONCLUSIVE` depending on the documented audit interpretation.
- Do not automatically propagate an aggregate report result to individual source rules. If a report states that aggregate property `X` is verified while the source contains `X1`, `X2`, and `X3`, keep the individual rules `NOT_STATED` unless the report explicitly supports each one.
- Preserve report qualifiers such as `✔*`, timeout status, assumptions, simplifications, bounded loop unrolling, special harnesses, or other proof restrictions. If the CSV representation is coarser, preserve the qualifier in the example `.md`.
- Do not assume that the same property name in multiple specs or targets has the same formal result. Verify that the report actually covers each source instance or target before copying a result.
- Treat multiple targets deliberately. A shared source spec may use a target set such as `OptimismBridgeExecutor;ArbitrumBridgeExecutor`, but if target-specific access controls, harnesses, or execution semantics materially change the meaning of the property, consider separate examples.
- `complete` does not mean historically reproducible. It means required property dependencies are resolved in the available snapshot. Missing `.conf` files, historical harnesses, CLI flags, prover settings, or report assumptions may still prevent exact reproduction of the original run.
- Explain the `.sol` excerpt specifically. State which variables, updates, hashes, modifiers, counters, branches, or state transitions correspond to the property observations and assertions. Avoid generic statements such as only “this code is relevant”.
- Do not repair or modernize a suspicious property during cataloging. Preserve historical logic as-is and document the interpretation. CVL2 migration, reconstruction, and semantic correction are separate tasks.
- When evidence is uncertain, be conservative. `UNMAPPED`, `NOT_STATED`, or `incomplete` are preferable to unsupported certainty.

## Step 9 — Write the example `.md`

Every example must have:

```text
results/spec/<complete|incomplete>/<project-id>/<example-id>.md
```

Use these sections:

```markdown
# Example N — `PropertyName`

## Status
## Bug Label relationship
## Original sources
## Motivation
## Reconstructed methodology
## Why the Solidity excerpt is relevant
## Dependencies included
```

For incomplete examples, replace or extend the final section with:

```markdown
## Missing dependency
```

### Writing the methodology section

`Reconstructed methodology` explains the observable reasoning encoded by the property.

It should describe the verification strategy step by step, for example:

1. read the relevant state before the operation;
2. execute a selected method or privileged entrypoint;
3. read the state after the operation;
4. compare the before/after values;
5. assert the intended security condition;
6. explain what a counterexample would demonstrate.

Use the property, Solidity code, and public report as evidence.

Do not claim access to private auditor thoughts or hidden reasoning.

Prefer language such as:

> The following reasoning is reconstructed from the property and the report.

rather than:

> The auditor thought that...

## Step 10 — Add `N.txt` for incomplete examples

Every incomplete example must contain:

```text
results/spec/incomplete/<project-id>/<example-id>.txt
```

The file must explain:

- the exact missing symbol or artifact;
- where it is referenced;
- where the developer searched for it;
- any explanation provided by the report;
- why the example cannot be treated as dependency-complete.

Example:

```text
INCOMPLETE DEPENDENCY

The property calls queue2(...), but no implementation or declaration
of queue2 is present in the available project snapshot.
```

Do not use `N.txt` for CVL1-to-CVL2 syntax differences alone.

## Step 11 — Add the CSV row

Append one row to `results/spec/spec_buglabel.csv` for each Bug Label relationship.

Current columns:

```text
Project ID
Status
Example ID
Bug Label
Property
Result
Detection Outcome
Target Contract
Spec
Code
Documentation
Incomplete Reason
Original Spec
Original Spec Lines
Original Contract
Original Contract Lines
Detection Intent
```

For a complete example, leave `Incomplete Reason` empty.

For an incomplete example, point `Incomplete Reason` to its `N.txt` file.

When one example maps to multiple labels, duplicate the CSV relationship row but reuse the same artifact paths.

## Semantic Review

Before accepting any Bug Label mapping or considering an example semantically reviewed, verify all of the following:

- [ ] I read the actual assertion and full property body, not only the property name or comment.
- [ ] I can explain what counterexample would make this property fail.
- [ ] The selected Bug Label describes that counterexample or its root cause.
- [ ] The property is normative, not merely diagnostic or exploratory; otherwise I used `UNMAPPED`.
- [ ] I did not infer `Result` from the spec itself.
- [ ] I did not infer `Detection Outcome` from `Result` alone.
- [ ] Report-level, aggregate-property, and individual source-rule results were not conflated.
- [ ] Any report assumptions, simplifications, `✔*` qualifiers, timeout status, or similar limitations are preserved.
- [ ] The `Target Contract` or target set attribution is defensible.
- [ ] The Solidity excerpt directly explains the state, control flow, authorization, hash/ID logic, or transition observed by the property.
- [ ] Any detector that proves only a partial condition is documented as partial rather than described as a complete security proof.
- [ ] Anything uncertain is marked conservatively with `UNMAPPED`, `NOT_STATED`, or `incomplete` when appropriate.

## Step 12 — Final review checklist

Before committing an example, verify all of the following:

- [ ] `Project ID` exists in `results/contests.csv`.
- [ ] `Property` exactly matches the original rule/invariant name.
- [ ] Original spec path exists.
- [ ] Original spec line ranges are exact.
- [ ] Report outcome was checked before setting `Result`.
- [ ] Audit interpretation was checked before setting `Detection Outcome`.
- [ ] `Result` and `Detection Outcome` are not being conflated.
- [ ] `Target Contract` is explicit.
- [ ] Every non-built-in CVL dependency was traced.
- [ ] Required available CVL dependencies were copied into `N.spec`.
- [ ] Missing dependencies cause `Status = incomplete`.
- [ ] Every incomplete example has `N.txt`.
- [ ] `N.sol` contains only relevant source context and preserves provenance.
- [ ] `N.md` separates documented facts from reconstructed methodology.
- [ ] Bug Label mapping is defensible or uses `UNMAPPED`.
- [ ] All CSV paths exist.
- [ ] `python scripts/check_specs.py .` passes from the repository root.
- [ ] Original files under `contracts/<project-id>/` remain unchanged.
- [ ] No CVL2 migration was silently mixed into the extraction step.

## Decision summary

```text
Select property
    |
    v
Read report and determine Result
    |
    v
Determine Detection Outcome
    |
    v
Identify Target Contract
    |
    v
Trace every required dependency
    |
    +--> all dependencies available --> complete/<project-id>/N.*
    |
    +--> dependency missing ----------> incomplete/<project-id>/N.* + N.txt
    |
    v
Map detection intent to Web3Bugs label
    |
    +--> defensible mapping --> label
    |
    +--> no defensible mapping --> UNMAPPED
    |
    v
Write N.md and append CSV row(s)
```

## Reference examples in Project 1

Current AAVE examples demonstrate the intended process:

- `results/spec/complete/1/1.*` — `whoChangedStateVariables`, with required getter declarations included;
- `results/spec/complete/1/2.*` — `queuedChangedCounter`, with its required methods included;
- `results/spec/complete/1/3.*` — `independentQueuedActions`, including its `stateVariableUpdate` definition; `Result = VIOLATED` and `Detection Outcome = FINDING`;
- `results/spec/complete/1/4.*` — Polygon `queuePriviliged`;
- `results/spec/incomplete/1/1.*` — Optimism/Arbitrum-style `queuePriviliged`, kept incomplete because the original `queue2` helper is missing.

These examples are templates for structure and auditability, not a requirement that future properties use the same Bug Labels or dependency patterns.
