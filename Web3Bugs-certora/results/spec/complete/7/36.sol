// Original: contracts/7/contracts/protocol/tokenization/StableDebtToken.sol, lines 91-93
function getUserLastUpdated(address user) external view virtual override returns (uint40) {
    return _timestamps[user];
  }
