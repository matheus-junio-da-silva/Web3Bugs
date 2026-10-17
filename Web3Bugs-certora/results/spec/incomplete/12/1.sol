// Original: contracts/12/contracts/protocol/tokenization/StableDebtToken.sol:22-26

  uint256 internal _avgStableRate;
  mapping(address => uint40) internal _timestamps;
  mapping(address => uint256) internal _usersStableRate;
  uint40 internal _totalSupplyTimestamp;

// Original: contracts/12/contracts/protocol/tokenization/StableDebtToken.sol:89-91
  function getUserLastUpdated(address user) external view virtual override returns (uint40) {
    return _timestamps[user];
  }

// Original: contracts/12/contracts/protocol/tokenization/StableDebtToken.sol:165-165
    _totalSupplyTimestamp = _timestamps[onBehalfOf] = uint40(block.timestamp);

// Original: contracts/12/contracts/protocol/tokenization/StableDebtToken.sol:227-235
    if (amount == currentBalance) {
      _usersStableRate[user] = 0;
      _timestamps[user] = 0;
    } else {
      //solium-disable-next-line
      _timestamps[user] = uint40(block.timestamp);
    }
    //solium-disable-next-line
    _totalSupplyTimestamp = uint40(block.timestamp);

// Original: contracts/12/specs/harness/StableDebtTokenHarness.sol:26-28
  function getIncentivesController() public view returns (address) {
    return address(_incentivesController);
  }
