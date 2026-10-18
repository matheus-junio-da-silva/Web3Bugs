// Source: contracts/10/specs/harnesses/ProxyHarness.sol, original lines 4-20

contract ProxyHarness is Proxy {
    constructor(address registry) public Proxy(registry) {}

    function getSlot(uint256 s) external view returns (uint256 x) {
        assembly {
            x := sload(s)
        }
    }

    function getStackLengthSlot() external view returns (uint256 x) {
        assembly {
            x := stack_slot
        }
    }

    function getStackLength() external view returns (uint256) {

// Source: contracts/10/contracts/Proxy.sol, original lines 97-120
    function batchExec(
        address[] calldata tos,
        bytes32[] calldata configs,
        bytes[] memory datas,
        uint256[] calldata ruleIndexes
    ) external payable override isNotHalted isNotBanned {
        _preProcess(ruleIndexes);
        _execs(tos, configs, datas);
        _postProcess();
    }

    /**
     * @notice The execution interface for callback function to be executed.
     * @dev This function can only be called through the handler, which makes
     * the caller become proxy itself.
     */
    function execs(
        address[] calldata tos,
        bytes32[] calldata configs,
        bytes[] memory datas
    ) external payable override isNotHalted isNotBanned isInitialized {
        require(msg.sender == address(this), "Does not allow external calls");
        _execs(tos, configs, datas);
    }
