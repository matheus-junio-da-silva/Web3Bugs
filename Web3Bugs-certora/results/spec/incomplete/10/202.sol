// Project 10 example 202; handler HCurveDao, property senderIsAlwaysCleanedUp. Historical source excerpts only, NOT compilable assembly.
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
