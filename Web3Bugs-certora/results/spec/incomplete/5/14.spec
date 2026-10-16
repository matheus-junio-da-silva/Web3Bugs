// Extracted from Project 5 — Aave-StarkNet L1-L2 Bridge
// Property: alwaysUnSent
// Dependency status: incomplete
// CVL2 migration is intentionally out of scope.
// Included original CVL ranges: specs/setup.spec:33;41;43;136;167-170;202-204

methods {
    withdraw(address, uint256, address, uint256, uint256, bool)
    receiveRewards(uint256, address, uint256)
}
definition messageSentFilter(method f) returns bool = 
    f.selector != receiveRewards(uint256, address, uint256).selector
    &&
    f.selector != withdraw(address, uint256, address, uint256, uint256, bool).selector;
invariant alwaysUnSent(env e)
   !withdrawMessageStatus(e) && !bridgeRewardsMessageStatus(e)
    filtered{f -> messageSentFilter(f)}
