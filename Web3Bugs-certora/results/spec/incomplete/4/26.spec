// Extracted from Project 4 — AAVE Staked Token v1.5
// Property: PersonalIndexLessOrEqualGlobalIndex
// Dependency status: incomplete
// CVL2 migration is intentionally out of scope.
// Included original CVL ranges: certora/specs/base.spec:4-4; certora/specs/base.spec:25-25; certora/specs/base.spec:26-26; certora/specs/base.spec:48-48; certora/specs/invariants.spec:117-118

methods {
    getAssetGlobalIndex(address) returns (uint256) envfree
    getUserPersonalIndex(address, address) returns (uint256) envfree
}
invariant PersonalIndexLessOrEqualGlobalIndex(address asset, address user)
    getUserPersonalIndex(asset, user) <= getAssetGlobalIndex(asset)
