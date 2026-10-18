// Extracted from: contracts/11/specs/harness/FullyBackedBondingHarness.sol
// Original source range: 30-45

    function balanceOf(address account) public view returns (uint256) {
        return account.balance;
    }

    function init_state() public {}

    function getDelegatedAuthority(address a) public view returns (address) {
        return delegatedAuthority[a];
    }

    function deposit(address operator) public payable {
        require(msg.sender != address(0));
        everDeposited[operator] = everDeposited[operator].add(msg.value);
        super.deposit(operator);
    }


// Extracted from: contracts/11/specs/harness/FullyBackedBondingHarness.sol
// Original source range: 109-111

    function _hasDelegationLockPassed(address operator) public returns (bool) {
        return hasDelegationLockPassed(operator);
    }

// Extracted from: contracts/11/contracts/AbstractBonding.sol
// Original source range: 81-94

    function deposit(address operator) public payable {
        address beneficiary = beneficiaryOf(operator);
        // Beneficiary has to be set (delegation exist) before an operator can
        // deposit wei. It protects from a situation when an operator wants
        // to withdraw funds which are transfered to beneficiary with zero
        // address.
        require(
            beneficiary != address(0),
            "Beneficiary not defined for the operator"
        );
        unbondedValue[operator] = unbondedValue[operator].add(msg.value);
        emit UnbondedValueDeposited(operator, beneficiary, msg.value);
    }


// Extracted from: contracts/11/contracts/AbstractBonding.sol
// Original source range: 329-342

    function withdrawBond(uint256 amount, address operator) internal {
        require(
            unbondedValue[operator] >= amount,
            "Insufficient unbonded value"
        );

        unbondedValue[operator] = unbondedValue[operator].sub(amount);

        address beneficiary = beneficiaryOf(operator);

        (bool success, ) = beneficiary.call.value(amount)("");
        require(success, "Transfer failed");

        emit UnbondedValueWithdrawn(operator, beneficiary, amount);

// Extracted from: contracts/11/contracts/fully-backed/FullyBackedBonding.sol
// Original source range: 156-173

    function withdraw(uint256 amount, address operator) public {
        require(
            msg.sender == operator || msg.sender == ownerOf(operator),
            "Only operator or the owner is allowed to withdraw bond"
        );

        require(
            hasDelegationLockPassed(operator),
            "Delegation lock period has not passed yet"
        );

        withdrawBond(amount, operator);
    }

    /// @notice Gets delegation info for the given operator.
    /// @param operator Address of the operator.
    /// @return createdAt The time when the delegation was created.
    /// @return undelegatedAt The time when undelegation has been requested.
