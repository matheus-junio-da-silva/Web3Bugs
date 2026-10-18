// Project 10 example 201; handler HCurveDao, property stackLengthIncreaseIsBounded. Historical source excerpts only, NOT compilable assembly.
// Source: contracts/10/contracts/handlers/curve/HCurveDao.sol original lines 20-45
    }

    function mint(address gaugeAddr) external payable returns (uint256) {
        IMinter minter = IMinter(CURVE_MINTER);
        address user = _getSender();
        uint256 beforeCRVBalance = IERC20(CRV_TOKEN).balanceOf(user);
        _requireMsg(
            minter.allowed_to_mint_for(address(this), user),
            "mint",
            "not allowed to mint"
        );

        try minter.mint_for(gaugeAddr, user) {} catch Error(
            string memory reason
        ) {
            _revertMsg("mint", reason);
        } catch {
            _revertMsg("mint");
        }
        uint256 afterCRVBalance = IERC20(CRV_TOKEN).balanceOf(user);

        _updateToken(CRV_TOKEN);
        return afterCRVBalance - beforeCRVBalance;
    }

    function mintMany(

// Source: contracts/10/contracts/handlers/curve/HCurveDao.sol original lines 43-68
    }

    function mintMany(
        address[] calldata gaugeAddrs
    ) external payable returns (uint256) {
        IMinter minter = IMinter(CURVE_MINTER);
        address user = _getSender();
        uint256 beforeCRVBalance = IERC20(CRV_TOKEN).balanceOf(user);
        _requireMsg(
            minter.allowed_to_mint_for(address(this), user),
            "mintMany",
            "not allowed to mint"
        );

        for (uint256 i = 0; i < gaugeAddrs.length; i++) {
            try minter.mint_for(gaugeAddrs[i], user) {} catch Error(
                string memory reason
            ) {
                _revertMsg(
                    "mintMany",
                    string(abi.encodePacked(reason, " on ", _uint2String(i)))
                );
            } catch {
                _revertMsg(
                    "mintMany",
                    string(abi.encodePacked("Unspecified on ", _uint2String(i)))

// Source: contracts/10/contracts/Storage.sol original lines 8-18 (literal excerpt)
/// @notice A cache structure composed by a bytes32 array
contract Storage {
    using LibCache for mapping(bytes32 => bytes32);
    using LibStack for bytes32[];

    bytes32[] public stack;
    mapping(bytes32 => bytes32) public cache;

    // keccak256 hash of "msg.sender"
    // prettier-ignore
    bytes32 public constant MSG_SENDER_KEY = 0xb2f2618cecbbb6e7468cc0f2aa43858ad8d153e0280b22285e28e853bb9d453a;

// Source: contracts/10/contracts/handlers/HandlerBase.sol original lines 30-53 (literal excerpt)

    function _updateToken(address token) internal {
        stack.setAddress(token);
        // Ignore token type to fit old handlers
        // stack.setHandlerType(uint256(HandlerType.Token));
    }

    function _updatePostProcess(bytes32[] memory params) internal {
        for (uint256 i = params.length; i > 0; i--) {
            stack.set(params[i - 1]);
        }
        stack.set(msg.sig);
        stack.setHandlerType(HandlerType.Custom);
    }

    function getContractName() public pure virtual returns (string memory);

    function _revertMsg(
        string memory functionName,
        string memory reason
    ) internal pure {
        revert(
            string(
                abi.encodePacked(
