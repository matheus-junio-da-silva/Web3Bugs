// Project 10 example 232; handler HStakingRewardsAdapter, property senderIsAlwaysCleanedUp. Historical source excerpts only, NOT compilable assembly.
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
