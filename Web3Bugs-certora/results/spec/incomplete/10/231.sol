// Project 10 example 231; handler HStakingRewardsAdapter, property stackLengthIncreaseIsBounded. Historical source excerpts only, NOT compilable assembly.
// Source: contracts/10/contracts/handlers/staking/HStakingRewardsAdapter.sol original lines 24-49

    // Stake for msg.sender
    function stake(
        address adapterAddr,
        uint256 amount
    ) external payable whenAdapterIsValid(adapterAddr) {
        IStakingRewardsAdapter adapter = IStakingRewardsAdapter(adapterAddr);
        IERC20 token = adapter.stakingToken();

        _tokenApprove(address(token), address(adapter), amount);

        try adapter.stakeFor(_getSender(), amount) {} catch Error(
            string memory reason
        ) {
            _revertMsg("stake", reason);
        } catch {
            _revertMsg("stake");
        }
        _tokenApproveZero(address(token), address(adapter));
    }

    // Stake for account
    function stakeFor(
        address adapterAddr,
        address account,
        uint256 amount

// Source: contracts/10/contracts/handlers/staking/HStakingRewardsAdapter.sol original lines 44-69

    // Stake for account
    function stakeFor(
        address adapterAddr,
        address account,
        uint256 amount
    ) external payable whenAdapterIsValid(adapterAddr) {
        IStakingRewardsAdapter adapter = IStakingRewardsAdapter(adapterAddr);
        IERC20 token = adapter.stakingToken();

        _tokenApprove(address(token), address(adapter), amount);

        try adapter.stakeFor(account, amount) {} catch Error(
            string memory reason
        ) {
            _revertMsg("stakeFor", reason);
        } catch {
            _revertMsg("stakeFor");
        }
        _tokenApproveZero(address(token), address(adapter));
    }

    // Only withdraw for msg.sender
    function withdraw(
        address adapterAddr,
        uint256 amount

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
