// Project 10: relevant preserved Solidity excerpts; line annotations retain original provenance.

// Exact source excerpt: contracts/10/contracts/handlers/maker/HMaker.sol:39-47
        override
        returns (string memory)
    {
        return "HMaker";
    }

    function getProxyActions() public pure virtual returns (address) {
        return 0x82ecD135Dce65Fbc6DbdD0e4237E0AF93FFD5038;
    }

// Exact source excerpt: contracts/10/contracts/handlers/maker/HMaker.sol:104-120
        address token = IMakerGemJoin(gemJoin).gem();

        // if amount == type(uint256).max return balance of Proxy
        wadC = _getBalance(token, wadC);

        _tokenApprove(token, address(proxy), wadC);
        try
            proxy.execute(
                getProxyActions(),
                abi.encodeWithSelector(
                    // selector of "openLockGemAndDraw(address,address,address,address,bytes32,uint256,uint256,bool)"
                    0xdb802a32,
                    getCdpManager(),
                    getMcdJug(),
                    gemJoin,
                    daiJoin,
                    ilk,

// Exact source excerpt: contracts/10/specs/harnesses/Summary.sol:77-94
    // for HMaker, HSCompound
    address[] delegated;
    function lenDelegated() external returns (uint256) { return delegated.length; }
    function checkDelegated(address allowed) external returns (bool) {
        for (uint i = 0 ; i < delegated.length; i++) {
            if (delegated[i] != allowed) {
                return false;
            }
        }

        return true;
    }

    function execute(address a, bytes calldata b) external payable returns (bytes32) {
        delegated.push(a);
        havocDummyToken();
        return executeRet;
    }
