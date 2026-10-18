// Historical LaunchEvent Solidity implementation excerpts — contracts/24/contracts/LaunchEvent.sol
// State line 51
    uint256 public auctionStart;
// Function getPenalty lines 573-627
    function getPenalty() public view returns (uint256) {
        if (block.timestamp < auctionStart) {
            return 0;
        }
        uint256 timeElapsed = block.timestamp - auctionStart;
        if (timeElapsed < phaseOneNoFeeDuration) {
            return 0;
        } else if (timeElapsed < phaseOneDuration) {
            return
                ((timeElapsed - phaseOneNoFeeDuration) * maxWithdrawPenalty) /
                (phaseOneDuration - phaseOneNoFeeDuration);
        }
        return fixedWithdrawPenalty;
    }

    /// @notice Returns the incentives for a given user
    /// @param _user The user to look up
    /// @return The amount of incentives `_user` can withdraw
    function getIncentives(address _user) public view returns (uint256) {
        UserInfo memory user = getUserInfo[_user];

        if (user.hasWithdrawnIncentives) {
            return 0;
        }

        if (_user == issuer) {
            if (address(pair) == address(0)) return 0;
            return tokenIncentiveIssuerRefund + tokenReserve;
        } else {
            if (avaxAllocated == 0) return 0;
            return (user.balance * tokenIncentivesForUsers) / avaxAllocated;
        }
    }

    /// @notice Returns the outstanding balance of the launch event contract
    /// @return The balances of AVAX and issued token held by the launch contract
    function getReserves() external view returns (uint256, uint256) {
        return (avaxReserve, tokenReserve + tokenIncentivesBalance);
    }

    /// @notice Get the rJOE amount needed to deposit AVAX
    /// @param _avaxAmount The amount of AVAX to deposit
    /// @return The amount of rJOE needed
    function getRJoeAmount(uint256 _avaxAmount) public view returns (uint256) {
        return (_avaxAmount * rJoePerAvax) / 1e18;
    }

    /// @notice The total amount of liquidity pool tokens the user can withdraw
    /// @param _user The address of the user to check
    /// @return The user's balance of liquidity pool token
    function pairBalance(address _user) public view returns (uint256) {
        UserInfo memory user = getUserInfo[_user];
        if (avaxAllocated == 0 || user.hasWithdrawnPair) {
            return 0;
        }
