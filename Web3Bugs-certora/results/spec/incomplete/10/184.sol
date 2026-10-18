// Project 10 example 184; handler HCToken, property senderIsAlwaysCleanedUp. Historical source excerpts only, NOT compilable assembly.
// Source: contracts/10/contracts/handlers/compound/HCToken.sol original lines 14-39
    }

    function mint(
        address cToken,
        uint256 mintAmount
    ) external payable returns (uint256) {
        // Get ctoken balance of proxy before mint
        ICToken compound = ICToken(cToken);
        uint256 beforeCTokenAmount = compound.balanceOf(address(this));

        address token = _getToken(cToken);
        // if amount == type(uint256).max return balance of Proxy
        mintAmount = _getBalance(token, mintAmount);
        _tokenApprove(token, cToken, mintAmount);
        try compound.mint(mintAmount) returns (uint256 errorCode) {
            _requireMsg(
                errorCode == 0,
                "mint",
                string(abi.encodePacked("error ", _uint2String(errorCode)))
            );
        } catch Error(string memory reason) {
            _revertMsg("mint", reason);
        } catch {
            _revertMsg("mint");
        }
        _tokenApproveZero(token, cToken);

// Source: contracts/10/contracts/handlers/compound/HCToken.sol original lines 47-72
    }

    function redeem(
        address cToken,
        uint256 redeemTokens
    ) external payable returns (uint256) {
        // Get token balance of proxy before redeem
        address token = _getToken(cToken);
        uint256 beforeTokenAmount = IERC20(token).balanceOf(address(this));

        ICToken compound = ICToken(cToken);
        // if amount == type(uint256).max return balance of Proxy
        redeemTokens = _getBalance(cToken, redeemTokens);
        try compound.redeem(redeemTokens) returns (uint256 errorCode) {
            _requireMsg(
                errorCode == 0,
                "redeem",
                string(abi.encodePacked("error ", _uint2String(errorCode)))
            );
        } catch Error(string memory reason) {
            _revertMsg("redeem", reason);
        } catch {
            _revertMsg("redeem");
        }

        // Get token balance of proxy after redeem

// Source: contracts/10/contracts/Storage.sol original lines 30-45 (literal excerpt)
    modifier isNotInitialized() {
        require(_getSender() == address(0), "Sender is initialized");
        _;
    }

    function _setSender() internal isNotInitialized {
        cache.setAddress(MSG_SENDER_KEY, msg.sender);
    }

    function _resetSender() internal {
        cache.setAddress(MSG_SENDER_KEY, address(0));
    }

    function _getSender() internal view returns (address) {
        return cache.getAddress(MSG_SENDER_KEY);
    }
