// Extracted from: contracts/3/specs/rescueLendMigrator.spec
// Property: LendIsBackedByAave
// Dependency status: incomplete
// Original source ranges included: 1-2;5-12;19-27
// CVL2 migration is intentionally out of scope for this catalog stage.

using DummyERC20Impl as LEND1
using DummyERC20Impl2 as AAVE1
methods{
    LEND1.balanceOf(address) returns (uint256) envfree
    AAVE1.balanceOf(address) returns (uint256) envfree
    LEND1.totalSupply() returns (uint256) envfree
    LEND_AAVE_RATIO() returns (uint256) envfree
    transfer(address, uint256) returns (bool) => DISPATCHER(true)
    onTransfer(address, address, uint256) => NONDET
}
// All the LEND that wasn’t sent for swap in the migrator must be fully collateralised with AAVE
invariant LendIsBackedByAave()
    ( (LEND1.totalSupply() - LEND1.balanceOf(LEND1)) ) / LEND_AAVE_RATIO() <= AAVE1.balanceOf(currentContract)
    {
        preserved with (env e){
            require e.msg.sender != LEND1;
            require e.msg.sender != AAVE1;
        }
    }
