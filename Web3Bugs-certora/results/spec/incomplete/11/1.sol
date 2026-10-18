// Extracted from: contracts/11/contracts/fully-backed/FullyBackedBonding.sol
// Original source range: 78-112

    /// @param authorizer Address of the authorizer.
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

// Extracted from: contracts/11/contracts/AbstractBonding.sol
// Original source range: 310-326

        address _operatorContract
    ) public view returns (bool);

    /// @notice Gets the authorizer for the specified operator address.
    /// @param _operator Operator address.
    /// @return Authorizer address.
    function authorizerOf(address _operator) public view returns (address);

    /// @notice Gets the beneficiary for the specified operator address.
    /// @param _operator Operator address.
    /// @return Beneficiary address.
    function beneficiaryOf(address _operator)
        public
        view
        returns (address payable);

    /// @notice Withdraws the provided amount from unbonded value of the
