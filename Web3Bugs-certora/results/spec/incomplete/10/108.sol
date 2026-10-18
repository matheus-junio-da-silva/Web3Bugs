// Exact Solidity excerpt for HStakingRewardsAdapter
// Source: contracts/10/contracts/handlers/staking/HStakingRewardsAdapter.sol original lines 1-70
// SPDX-License-Identifier: MIT

pragma solidity 0.8.10;

import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "../HandlerBase.sol";
import "../../staking/IStakingRewardsAdapter.sol";
import "../../staking/IStakingRewardsAdapterRegistry.sol";

contract HStakingRewardsAdapter is HandlerBase {
    using SafeERC20 for IERC20;

    // prettier-ignore
    IStakingRewardsAdapterRegistry constant public registry = IStakingRewardsAdapterRegistry(0xCa591346A311A372a20ed69e08bBE5107979e243);

    modifier whenAdapterIsValid(address adapter) {
        _requireMsg(registry.isValid(adapter), "General", "Invalid adapter");
        _;
    }

    function getContractName() public pure override returns (string memory) {
        return "HStakingRewardsAdapter";
    }

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
    ) external payable whenAdapterIsValid(adapterAddr) {
