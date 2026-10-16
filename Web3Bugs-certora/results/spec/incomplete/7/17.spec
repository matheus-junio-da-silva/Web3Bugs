// Historical extract: contracts/7/specs/ReserveConfiguration.spec:85-88
// Source preamble: contracts/7/specs/ReserveConfiguration.spec:1-60
// Dependency status: incomplete; CVL2 migration intentionally not attempted.
methods {
    setLtv(uint256) envfree
    getLtv() returns (uint256) envfree
    setLiquidationThreshold(uint256) envfree
    getLiquidationThreshold() returns (uint256) envfree
    setLiquidationBonus(uint256) envfree
    getLiquidationBonus() returns (uint256) envfree
    setDecimals(uint256) envfree
    getDecimals() returns (uint256) envfree
    setActive(bool) envfree
    getActive() returns (bool) envfree
    setFrozen(bool) envfree
    getFrozen() returns (bool) envfree
    setPaused(bool) envfree
    getPaused() returns (bool) envfree
    setBorrowableInIsolation(bool) envfree
    getBorrowableInIsolation() returns (bool) envfree
    setSiloedBorrowing(bool) envfree
    getSiloedBorrowing() envfree
    setBorrowingEnabled(bool) envfree
    getBorrowingEnabled() returns (bool) envfree
    setStableRateBorrowingEnabled(bool) envfree
    getStableRateBorrowingEnabled() returns (bool) envfree
    setReserveFactor(uint256) envfree
    getReserveFactor() returns (uint256) envfree
    setBorrowCap(uint256) envfree
    getBorrowCap() returns (uint256) envfree
    setSupplyCap(uint256) envfree
    getSupplyCap() returns (uint256) envfree
    setDebtCeiling(uint256) envfree
    getDebtCeiling() returns (uint256) envfree
    setLiquidationProtocolFee(uint256) envfree
    getLiquidationProtocolFee() returns (uint256) envfree
    setUnbackedMintCap(uint256) envfree
    getUnbackedMintCap() returns (uint256) envfree
    setEModeCategory(uint256) envfree
    getEModeCategory() returns (uint256) envfree
    setFlashLoanEnabled(bool) envfree
    getFlashLoanEnabled() returns (bool) envfree
    getFlags() returns (bool, bool, bool, bool, bool) envfree
    getParams() returns (uint256, uint256, uint256, uint256, uint256, uint256) envfree
    getCaps() returns (uint256, uint256) envfree

    init_state() envfree
    getData() returns uint256 envfree
    xorWithReserve(uint256) returns uint256 envfree 
    initMaps() envfree
    
    getIntSetterLowerBound(uint256) returns uint256 envfree
    getIntSetterUpperBound(uint256) returns uint256 envfree
    executeIntSetterById(uint256, uint256) envfree
    executeIntGetterById(uint256) returns uint256 envfree

    getBoolSetterCompare(uint256) returns uint256 envfree
    executeBoolSetterById(uint256, bool) envfree
    executeBoolGetterById(uint256) returns bool envfree
}


// checks the integrity of set LTV function and correct retrieval of the corresponding getter.

rule setActiveIntegrity(bool active) {
    setActive(active);
    assert getActive() == active;
}
