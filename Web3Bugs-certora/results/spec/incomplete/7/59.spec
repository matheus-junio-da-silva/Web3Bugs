// Historical extract: contracts/7/specs/UserConfiguration.spec:154-159
// Source preamble: contracts/7/specs/UserConfiguration.spec:1-19
// Dependency status: incomplete; CVL2 migration intentionally not attempted.
methods {
    setBorrowing(uint256, bool) envfree
    setUsingAsCollateral(uint256, bool) envfree
    isUsingAsCollateralOrBorrowing(uint256) returns bool envfree
    isBorrowing(uint256) returns bool envfree
    isUsingAsCollateral(uint256) returns bool envfree
	isUsingAsCollateralOne() returns bool envfree
    isUsingAsCollateralAny() returns bool envfree
    isBorrowingOne() returns (bool) envfree
    isBorrowingAny() returns bool envfree
    isEmpty() returns bool envfree    
    getIsolationModeState() returns (bool, address, uint256) envfree
    getSiloedBorrowingState() returns (bool, address) envfree
	isIsolated() returns bool envfree

}


// checks the integrity of set Borrowing function and correct retrieval of the corresponding getter

rule integrityOfSiloedBorrowingState(){
    bool existExactlyOneBorrow = isBorrowingOne();
    bool answer; address asset;
    answer, asset = getSiloedBorrowingState();
    assert answer => existExactlyOneBorrow;
}
