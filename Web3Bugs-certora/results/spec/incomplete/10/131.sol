// Project 10 example 131; handler HMaker, property cubeCounterIsAlwaysCleanedUp. Historical source excerpts only, NOT compilable assembly.
// Source: contracts/10/contracts/handlers/maker/HMaker.sol original lines 43-68
    }

    function getProxyActions() public pure virtual returns (address) {
        return 0x82ecD135Dce65Fbc6DbdD0e4237E0AF93FFD5038;
    }

    function getCdpManager() public pure virtual returns (address) {
        return 0x5ef30b9986345249bc32d8928B7ee64DE9435E39;
    }

    function getMcdJug() public view returns (address) {
        return IMakerChainLog(CHAIN_LOG).getAddress("MCD_JUG");
    }

    function openLockETHAndDraw(
        uint256 value,
        address ethJoin,
        address daiJoin,
        bytes32 ilk,
        uint256 wadD
    ) external payable returns (uint256 cdp) {
        IDSProxy proxy = IDSProxy(_getProxy(address(this)));
        // if amount == type(uint256).max return balance of Proxy
        value = _getBalance(address(0), value);

        try

// Source: contracts/10/contracts/handlers/maker/HMaker.sol original lines 47-72
    }

    function getCdpManager() public pure virtual returns (address) {
        return 0x5ef30b9986345249bc32d8928B7ee64DE9435E39;
    }

    function getMcdJug() public view returns (address) {
        return IMakerChainLog(CHAIN_LOG).getAddress("MCD_JUG");
    }

    function openLockETHAndDraw(
        uint256 value,
        address ethJoin,
        address daiJoin,
        bytes32 ilk,
        uint256 wadD
    ) external payable returns (uint256 cdp) {
        IDSProxy proxy = IDSProxy(_getProxy(address(this)));
        // if amount == type(uint256).max return balance of Proxy
        value = _getBalance(address(0), value);

        try
            proxy.execute{value: value}(
                getProxyActions(),
                abi.encodeWithSelector(
                    // selector of "openLockETHAndDraw(address,address,address,address,bytes32,uint256)"

// Source: contracts/10/specs/harnesses/ProxyHarness.sol original lines 30-36 (literal excerpt)
        return _getSender();
    }

    function getCubeCounter() public view returns (uint256) {
        return _getCubeCounter();
    }
