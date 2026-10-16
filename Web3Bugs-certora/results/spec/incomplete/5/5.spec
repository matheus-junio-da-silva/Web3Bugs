// Extracted from Project 5 — Aave-StarkNet L1-L2 Bridge
// Property: dynamicToStaticInversible2
// Dependency status: incomplete
// CVL2 migration is intentionally out of scope.
// Included original CVL ranges: specs/setup.spec:16;22;33;52-53;78;114;136;143;265-268 | specs/bridge.spec:151-160

    using SymbolicLendingPoolL1 as LENDINGPOOL_L1
    using BridgeL2Harness as BRIDGE_L2
methods {
    _staticToDynamicAmount_Wrapper(uint256, address, address) envfree //(ILendingPool)
    _dynamicToStaticAmount_Wrapper(uint256, address, address) envfree //(ILendingPool)
    LENDINGPOOL_L1.liquidityIndexByAsset(address) returns (uint256) envfree
    BRIDGE_L2.l2RewardsIndex() returns (uint256) envfree
}
definition RAY() returns uint256 = 10^27;
function requireRayIndex(address asset) {
    require LENDINGPOOL_L1.liquidityIndexByAsset(asset) >= RAY();
    require BRIDGE_L2.l2RewardsIndex() >= RAY();
}
rule dynamicToStaticInversible2(uint256 amount)
{
    // We assume both indexes (L1,L2) are represented in Ray (1e27).
    address asset;
    requireRayIndex(asset);
    uint256 indexL1 = LENDINGPOOL_L1.liquidityIndexByAsset(asset);
    uint256 stat = _dynamicToStaticAmount_Wrapper(amount, asset, LENDINGPOOL_L1);
    uint256 dynm = _staticToDynamicAmount_Wrapper(stat, asset, LENDINGPOOL_L1);
     assert dynm == amount;  // Violated
}
