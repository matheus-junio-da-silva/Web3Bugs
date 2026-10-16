// Relevant excerpts for shouldRevertInitializeTokens.
// Target Contract: BridgeHarness
// NOTE: BridgeHarness was the historical verification target but is absent from the supplied snapshot; excerpts below are available production-code context and may be from a later source revision.

// Source: contracts/5/contracts/l1/Bridge.sol
// Original lines: 53-71

    function initialize(
        uint256 l2Bridge,
        address messagingContract,
        address incentivesController,
        address[] calldata l1Tokens,
        uint256[] calldata l2Tokens,
        uint256[] calldata ceilings
    ) external virtual onlyValidL2Address(l2Bridge) initializer {
        require(
            address(incentivesController) != address(0),
            Errors.B_INVALID_INCENTIVES_CONTROLLER_ADDRESS
        );
        _messagingContract = IStarknetMessaging(messagingContract);
        _l2Bridge = l2Bridge;
        _incentivesController = IAaveIncentivesController(incentivesController);
        _rewardToken = IERC20(_incentivesController.REWARD_TOKEN());

        _approveBridgeTokens(l1Tokens, l2Tokens, ceilings);
    }

// Source: contracts/5/contracts/l1/Bridge.sol
// Original lines: 244-296

    function _approveBridgeTokens(
        address[] calldata l1Tokens,
        uint256[] calldata l2Tokens,
        uint256[] calldata ceilings
    ) internal {
        require(
            l1Tokens.length == l2Tokens.length &&
                l1Tokens.length == ceilings.length,
            Errors.B_MISMATCHING_ARRAYS_LENGTH
        );
        for (uint256 i = 0; i < l1Tokens.length; i++) {
            _approveToken(l1Tokens[i], l2Tokens[i], ceilings[i]);
        }
    }

    /**
     * @notice Approves a new L1<->L2 token bridge.
     * @dev Function is invoked only by bridge admin
     * @param l1AToken token address
     * @param l2Token token address
     **/
    function _approveToken(
        address l1AToken,
        uint256 l2Token,
        uint256 ceiling
    ) internal onlyValidL2Address(l2Token) {
        require(l1AToken != address(0), Errors.B_INVALID_ADDRESS);

        require(
            _aTokenData[l1AToken].l2TokenAddress == 0,
            Errors.B_TOKEN_ALREADY_APPROVED
        );

        require(
            IATokenWithPool(l1AToken).getIncentivesController() ==
                _incentivesController,
            Errors.B_INVALID_INCENTIVES_CONTROLLER_ADDRESS
        );

        IERC20 underlyingAsset = IERC20(
            IATokenWithPool(l1AToken).UNDERLYING_ASSET_ADDRESS()
        );
        ILendingPool lendingPool = IATokenWithPool(l1AToken).POOL();
        underlyingAsset.safeApprove(address(lendingPool), type(uint256).max);

        _aTokenData[l1AToken] = ATokenData(
            l2Token,
            underlyingAsset,
            lendingPool,
            ceiling
        );
        _approvedL1Tokens.push(l1AToken);
        emit ApprovedBridge(l1AToken, l2Token, ceiling);
