# PAT-01 — Methods, visibility and receiver discipline

Evidence: EV-A1-METHODS, EV-A1-VISIBILITY, EV-A1-RECEIVER, EV-A1-LOCATION, EV-A1-OPTIONAL. Originals: `contracts/10/specs/{proxy,registry,libParam,hmaker,hbalancer,hscompound}.spec`.

**Text-only candidate, conditional**: a line such as `getStackLength() returns (uint256) envfree` could be expressed as `function Target.getStackLength() external returns (uint256) envfree;` only **after** checking which contract actually implements that getter in the post-script ABI. Every signature in `methods` needs this same case-specific proof, not a mechanical blanket `external`.

The receiver omission is not neutral for `DISPATCHER`, `NONDET`, or any summary: a summary that reached many contracts in CVL1 may stop reaching them in CVL2. Evaluate owner and target; choose explicit `Target.method` or wildcard `_.method` only when the original reach is demonstrated. An injected getter may not exist in the preserved unmodified source; `optional` could silently skip a rule and is **not** a safe repair without proof. Record signature changes, inherited public wrapper/internal entrypoints, and referenced parameter locations.

**Risco:** vacuity, method resolution, external/internal dispatcher coverage, envfree semantics. **Not run.**