// Extracted from: contracts/11/specs/harness/FullyBackedBondingHarness.sol
// Original source range: 7-8

    mapping(address => uint256) public everDeposited;
    // mapping from operator,holder,referenceId to BondID

// Extracted from: contracts/11/specs/harness/FullyBackedBondingHarness.sol
// Original source range: 40-46

    function deposit(address operator) public payable {
        require(msg.sender != address(0));
        everDeposited[operator] = everDeposited[operator].add(msg.value);
        super.deposit(operator);
    }

    /* to track totalLockedBond we add a map (operator, holder, referenceID) to BondID */

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

