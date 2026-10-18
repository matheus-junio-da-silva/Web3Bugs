// Project 10 example 212; handler HFurucomboStaking, property noOverwrite. Historical source excerpts only, NOT compilable assembly.
// Source: contracts/10/contracts/handlers/furucombo/HFurucomboStaking.sol original lines 16-41
    }

    function stake(address pool, uint256 amount) external payable {
        IStaking staking = IStaking(pool);
        address stakeToken = staking.stakingToken();
        amount = _getBalance(stakeToken, amount);
        require(amount > 0, "HFurucombo: stake amount = 0");

        _tokenApprove(stakeToken, pool, amount);
        staking.stakeFor(_getSender(), amount);
        _tokenApproveZero(stakeToken, pool);
    }

    function unstake(address pool, uint256 amount) external payable {
        require(amount > 0, "HFurucombo: unstake amount = 0");
        IStaking staking = IStaking(pool);
        staking.unstakeFor(_getSender(), amount);

        // Update involved token
        _updateToken(staking.stakingToken());
    }

    function claimAll(
        address user,
        address[] calldata pools,
        IMerkleRedeem.Claim[][] calldata claims

// Source: contracts/10/contracts/handlers/furucombo/HFurucomboStaking.sol original lines 27-52
    }

    function unstake(address pool, uint256 amount) external payable {
        require(amount > 0, "HFurucombo: unstake amount = 0");
        IStaking staking = IStaking(pool);
        staking.unstakeFor(_getSender(), amount);

        // Update involved token
        _updateToken(staking.stakingToken());
    }

    function claimAll(
        address user,
        address[] calldata pools,
        IMerkleRedeem.Claim[][] calldata claims
    ) external payable {
        require(claims.length > 0, "HFurucombo: claims length = 0");
        require(
            pools.length == claims.length,
            "HFurucombo: pools length != claims length"
        );

        for (uint256 i = 0; i < claims.length; i++) {
            IMerkleRedeem redeem = IMerkleRedeem(pools[i]);
            redeem.claimWeeks(user, claims[i]);
        }

// Source: contracts/10/specs/harnesses/ProxyHarness.sol original lines 7-25 (literal excerpt)

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
        return stack.length;
    }

    function ethBalance(address who) external view returns (uint256) {
        return who.balance;
