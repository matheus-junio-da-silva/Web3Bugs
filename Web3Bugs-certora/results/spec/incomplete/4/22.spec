// Extracted from Project 4 — AAVE Staked Token v1.5
// Property: lowerBoundNotZero
// Dependency status: incomplete
// CVL2 migration is intentionally out of scope.
// Included original CVL ranges: certora/specs/base.spec:4-4; certora/specs/base.spec:11-11; certora/specs/base.spec:48-48; certora/specs/invariants.spec:27-29

methods {
    LOWER_BOUND() returns (uint256) envfree
}
invariant lowerBoundNotZero()
    LOWER_BOUND() > 0
