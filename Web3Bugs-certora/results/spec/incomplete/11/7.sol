// Extracted from: contracts/11/contracts/AbstractBonding.sol
// Original source range: 242-267

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
// Original source range: 96-107

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
    }

// Extracted from: contracts/11/specs/harness/FullyBackedBondingHarness.sol
// Original source range: 30-34

    function balanceOf(address account) public view returns (uint256) {
        return account.balance;
    }

    function init_state() public {}
