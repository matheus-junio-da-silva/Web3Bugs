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
// Original source range: 192-267

    function reassignBond(
        address operator,
        uint256 referenceID,
        address newHolder,
        uint256 newReferenceID
    ) public {
        address holder = msg.sender;
        bytes32 bondID = getBondID(operator, holder, referenceID);

        require(lockedBonds[bondID] > 0, "Bond not found");

        bytes32 newBondID = getBondID(operator, newHolder, newReferenceID);

        require(
            lockedBonds[newBondID] == 0,
            "Reference ID not unique for holder and operator"
        );

        lockedBonds[newBondID] = lockedBonds[bondID];
        lockedBonds[bondID] = 0;

        emit BondReassigned(operator, referenceID, newHolder, newReferenceID);
    }

    /// @notice Releases the bond and moves the bond value to the operator's
    /// unbounded value pool.
    /// @dev Function requires that caller is the holder of the bond which is
    /// being released.
    /// @param operator Address of the bonded operator.
    /// @param referenceID Reference ID of the bond.
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

// Extracted from: contracts/11/specs/harness/FullyBackedBondingHarness.sol
// Original source range: 9-27

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
// Original source range: 48-106

    function registerBondID(
        address operator,
        address holder,
        uint256 referenceID
    ) private {
        /*  bytes32 bondID = keccak256(
            abi.encodePacked(operator, holder, referenceID)
        );
        operatorHolderRefToBondID[operator][holder][referenceID] = bondID;
        */
    }

    function createBond(
        address operator,
        address holder,
        uint256 referenceID,
        uint256 amount,
        address authorizedSortitionPool
    ) public {
        require(msg.sender != address(0));
        registerBondID(operator, holder, referenceID);
        super.createBond(
            operator,
            holder,
            referenceID,
            amount,
            authorizedSortitionPool
        );
    }

    function reassignBond(
        address operator,
        uint256 referenceID,
        address newHolder,
        uint256 newReferenceID
    ) public {
        require(msg.sender != address(0));
        registerBondID(operator, msg.sender, referenceID);
        registerBondID(operator, newHolder, newReferenceID);
        super.reassignBond(operator, referenceID, newHolder, newReferenceID);
    }

    function freeBond(address operator, uint256 referenceID) public {
        require(msg.sender != address(0));
        registerBondID(operator, msg.sender, referenceID);
        super.freeBond(operator, referenceID);
    }

    function seizeBond(
        address operator,
        uint256 referenceID,
        uint256 amount,
        address payable destination
    ) public {
        require(msg.sender != address(0));
        // so transfer will not fail
        require(destination == otherBeneficiary);
        registerBondID(operator, msg.sender, referenceID);
        super.seizeBond(operator, referenceID, amount, otherBeneficiary);
