// Extracted from: contracts/11/contracts/AbstractBonding.sol
// Original source range: 29-40

    KeepRegistry internal registry;

    // Unassigned value in wei deposited by operators.
    mapping(address => uint256) public unbondedValue;

    // References to created bonds. Bond identifier is built from operator's
    // address, holder's address and reference ID assigned on bond creation.
    mapping(bytes32 => uint256) internal lockedBonds;

    // Sortition pools authorized by operator's authorizer.
    // operator -> pool -> boolean
    mapping(address => mapping(address => bool)) internal authorizedPools;

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
// Original source range: 136-170

    function createBond(
        address operator,
        address holder,
        uint256 referenceID,
        uint256 amount,
        address authorizedSortitionPool
    ) public {
        require(
            availableUnbondedValue(
                operator,
                msg.sender,
                authorizedSortitionPool
            ) >= amount,
            "Insufficient unbonded value"
        );

        bytes32 bondID = getBondID(operator, holder, referenceID);

        require(
            lockedBonds[bondID] == 0,
            "Reference ID not unique for holder and operator"
        );

        unbondedValue[operator] = unbondedValue[operator].sub(amount);
        lockedBonds[bondID] = lockedBonds[bondID].add(amount);

        emit BondCreated(
            operator,
            holder,
            authorizedSortitionPool,
            referenceID,
            amount
        );
    }


// Extracted from: contracts/11/contracts/AbstractBonding.sol
// Original source range: 222-239

    function freeBond(address operator, uint256 referenceID) public {
        address holder = msg.sender;
        bytes32 bondID = getBondID(operator, holder, referenceID);
        require(lockedBonds[bondID] > 0, "Bond not found");

        uint256 amount = lockedBonds[bondID];
        lockedBonds[bondID] = 0;
        unbondedValue[operator] = unbondedValue[operator].add(amount);

        emit BondReleased(operator, referenceID);
    }

    /// @notice Seizes the bond by moving some or all of the locked bond to the
    /// provided destination address.
    /// @dev Function requires that a caller is the holder of the bond which is
    /// being seized.
    /// @param operator Address of the bonded operator.
    /// @param referenceID Reference ID of the bond.

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
// Original source range: 79-112

    function delegate(
        address operator,
        address payable beneficiary,
        address authorizer
    ) external payable {
        address owner = msg.sender;

        require(operator != address(0), "Invalid operator address");
        require(authorizer != address(0), "Invalid authorizer address");

        require(
            operators[operator].owner == address(0),
            "Operator already in use"
        );

        require(
            msg.value >= MINIMUM_DELEGATION_DEPOSIT,
            "Insufficient delegation value"
        );

        operators[operator] = Operator(
            OperatorParams.pack(0, block.timestamp, 0),
            owner,
            beneficiary,
            authorizer
        );

        deposit(operator);

        emit Delegated(owner, operator);
        emit OperatorDelegated(operator, beneficiary, authorizer, msg.value);
    }

    /// @notice Top-ups operator's unbonded value.

// Extracted from: contracts/11/contracts/fully-backed/FullyBackedBonding.sol
// Original source range: 123-127

    function topUp(address operator) public payable {
        deposit(operator);

        emit OperatorToppedUp(operator, msg.value);
    }

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
