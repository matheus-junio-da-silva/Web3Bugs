// Extracted from Project 5 — Aave-StarkNet L1-L2 Bridge
// Property: integrityApprovedTokensAndTokenData
// Dependency status: incomplete
// CVL2 migration is intentionally out of scope.
// Included original CVL ranges: specs/setup.spec:33;39;41;43;60;136;145;156-158;167-170 | specs/bridge.spec:324-333;336-342

methods {
    initialize(uint256, address, address, address[], uint256[], uint256[])
    withdraw(address, uint256, address, uint256, uint256, bool)
    receiveRewards(uint256, address, uint256)
    getApprovedL1TokensLength() returns (uint256) envfree
}
definition MAX_ARRAY_LENGTH() returns uint256 = max_uint;
definition excludeInitialize(method f) returns bool =
    f.selector != 
    initialize(uint256, address, address, address[], uint256[], uint256[]).selector; 
definition messageSentFilter(method f) returns bool = 
    f.selector != receiveRewards(uint256, address, uint256).selector
    &&
    f.selector != withdraw(address, uint256, address, uint256, uint256, bool).selector;
ghost mathint totalApprovedTokens {
    init_state axiom totalApprovedTokens == 0;
}

// Updates the ghost when change l2TokenAddress
hook Sstore _aTokenData[KEY address token].l2TokenAddress uint256 new_tokenAddress
    (uint256 old_tokenAddress) STORAGE {
        totalApprovedTokens = totalApprovedTokens + 1;
}

invariant integrityApprovedTokensAndTokenData()
    totalApprovedTokens == getApprovedL1TokensLength()
    filtered{f -> messageSentFilter(f) && excludeInitialize(f)}
    { preserved { 
        // Avoiding overflow
        require getApprovedL1TokensLength() < MAX_ARRAY_LENGTH(); 
    } }
