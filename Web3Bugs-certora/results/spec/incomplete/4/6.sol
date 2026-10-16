// Relevant excerpts for noEntryUntilSlashingSettled.
// Target Contract: StakedAaveV3Harness

// Source: contracts/4/contracts/StakedTokenV3.sol
// Original lines: 50;172-178;442-447

  bool public inPostSlashingPeriod;
  function stake(address to, uint256 amount)
    external
    override(IStakedTokenV2, StakedTokenV2)
  {
    _stake(msg.sender, to, amount);
  }

  function _stake(
    address from,
    address to,
    uint256 amount
  ) internal {
    require(!inPostSlashingPeriod, 'SLASHING_ONGOING');
