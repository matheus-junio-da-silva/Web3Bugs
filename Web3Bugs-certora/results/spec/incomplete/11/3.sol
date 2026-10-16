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
// Original source range: 222-267

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
    /// @param amount Amount to be seized.
    /// @param destination Address to send the amount to.
    function seizeBond(
        address operator,
        uint256 referenceID,
        uint256 amount,
        address payable destination
    ) public {
        require(amount > 0, "Requested amount should be greater than zero");

        address payable holder = msg.sender;
        bytes32 bondID = getBondID(operator, holder, referenceID);

        require(
            lockedBonds[bondID] >= amount,
            "Requested amount is greater than the bond"
        );

        lockedBonds[bondID] = lockedBonds[bondID].sub(amount);

        (bool success, ) = destination.call.value(amount)("");
        require(success, "Transfer failed");

        emit BondSeized(operator, referenceID, destination, amount);
    }

    /// @notice Authorizes sortition pool for the provided operator.
    /// Operator's authorizers need to authorize individual sortition pools

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

// Extracted from: contracts/11/specs/harness/FullyBackedBondingHarness.sol
// Original source range: 7-27

    mapping(address => uint256) public everDeposited;
    // mapping from operator,holder,referenceId to BondID
    mapping(address => mapping(address => mapping(uint256 => bytes32)))
        public operatorHolderRefToBondID;

    address payable public otherBeneficiary;

    constructor(KeepRegistry _keepRegistry, uint256 _initializationPeriod)
        public
        FullyBackedBonding(_keepRegistry, _initializationPeriod)
    {}

    function getBondID(
        address operator,
        address holder,
        uint256 referenceID
    ) internal view returns (bytes32) {

            bytes32 bondID
         = operatorHolderRefToBondID[operator][holder][referenceID];
        return bondID;

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

