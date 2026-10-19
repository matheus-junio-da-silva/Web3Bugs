# P01 — methods declarations and visibility

**Authority:** A1-METHODS, A2-METHODS, A2-CVL-METHODS. Historical CVL1 entries of `methods` lack compulsory `function`, `internal/external` and `;`. **Candidate only:** e.g. `grantRole(bytes32,address)` → `function grantRole(bytes32,address) external;` **iff** contract ABI exposes matching external method, without unretained harness; `_checkRole(bytes32)` may instead be internal and not ABI callable. Inspect source-line and concrete method. Never presume the example alone demonstrates a valid translation.

Review each property's `SRC18-###`, target, ABI, inherited definition and any envfree getter. The extra annotation can alter which calls are summarized. No CVL2 compilation; alternative is to leave unresolved, not guess visibility.
