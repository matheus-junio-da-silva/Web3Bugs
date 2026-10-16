// Relevant excerpts for ATokenAssetPair.
// Target Contract: BridgeHarness
// NOTE: BridgeHarness was the historical verification target but is absent from the supplied snapshot; excerpts below are available production-code context and may be from a later source revision.

// Source: contracts/5/contracts/l1/Bridge.sol
// Original lines: 23-29

    IStarknetMessaging public _messagingContract;
    uint256 public _l2Bridge;
    address[] public _approvedL1Tokens;
    IERC20 public _rewardToken;
    IAaveIncentivesController public _incentivesController;
    mapping(address => ATokenData) public _aTokenData;
    uint256 public constant BRIDGE_REVISION = 0x1;

// Source: contracts/5/contracts/l1/Bridge.sol
// Original lines: 265-296

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
