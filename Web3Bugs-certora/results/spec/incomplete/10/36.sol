// Original Project 10 source excerpts; HBProtocol uses a different Maker actions target than HMaker.

// contracts/10/contracts/handlers/bprotocol/HBProtocol.sol:7-20
contract HBProtocol is HMaker {
    using SafeERC20 for IERC20;

    function getContractName() public pure override returns (string memory) {
        return "HBProtocol";
    }

    function getProxyActions() public pure override returns (address) {
        return 0x351626387B5bb5408f97F8fD6B2EC415Efc9E6a1;
    }

    function getCdpManager() public pure override returns (address) {
        return 0x3f30c2381CD8B917Dd96EB2f1A4F96D91324BBed;
    }

// contracts/10/contracts/handlers/maker/HMaker.sol:39-47
        override
        returns (string memory)
    {
        return "HMaker";
    }

    function getProxyActions() public pure virtual returns (address) {
        return 0x82ecD135Dce65Fbc6DbdD0e4237E0AF93FFD5038;
    }

// contracts/10/specs/harnesses/Summary.sol:77-94
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
