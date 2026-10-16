// Extracted from Project 4 — AAVE Staked Token v1.5
// Property: indexesMonotonicallyIncrease
// Dependency status: incomplete
// CVL2 migration is intentionally out of scope.
// Included original CVL ranges: certora/specs/base.spec:4-4; certora/specs/base.spec:25-25; certora/specs/base.spec:26-26; certora/specs/base.spec:48-48; certora/specs/invariants.spec:117-118; certora/specs/allProps.spec:440-453

methods {
    getAssetGlobalIndex(address) returns (uint256) envfree
    getUserPersonalIndex(address, address) returns (uint256) envfree
}
invariant PersonalIndexLessOrEqualGlobalIndex(address asset, address user)
    getUserPersonalIndex(asset, user) <= getAssetGlobalIndex(asset)
rule indexesMonotonicallyIncrease(method f, address asset, address user) {
    requireInvariant PersonalIndexLessOrEqualGlobalIndex(asset, user);
    uint256 _globalIndex = getAssetGlobalIndex(asset);
    uint256 _personalIndex = getUserPersonalIndex(asset, user);

    env e; calldataarg args;
    f(e, args);

    uint256 globalIndex_ = getAssetGlobalIndex(asset);
    uint256 personalIndex_ = getUserPersonalIndex(asset, user);

    assert(globalIndex_ >= _globalIndex);
    assert(personalIndex_ >= _personalIndex);
}
