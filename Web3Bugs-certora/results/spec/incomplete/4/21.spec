// Extracted from Project 4 — AAVE Staked Token v1.5
// Property: balanceOfZero
// Dependency status: incomplete
// CVL2 migration is intentionally out of scope.
// Included original CVL ranges: certora/specs/base.spec:4-4; certora/specs/base.spec:15-15; certora/specs/base.spec:48-48; certora/specs/invariants.spec:20-22

methods {
    balanceOf(address) returns (uint256) envfree
}
invariant balanceOfZero()
    balanceOf(0) == 0
