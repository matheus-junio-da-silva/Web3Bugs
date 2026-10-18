// Original Solidity: contracts/15/facilitators/aave/tokens/GhoAToken.sol lines 104-111; burn
  function burn(
    address from,
    address receiverOfUnderlying,
    uint256 amount,
    uint256 index
  ) external virtual override onlyPool {
    revert(Errors.OPERATION_NOT_SUPPORTED);
  }

// Original Solidity: contracts/15/gho/GhoToken.sol lines 58-69; burn
  function burn(uint256 amount) external override {
    require(amount != 0, 'INVALID_BURN_AMOUNT');

    Facilitator storage f = _facilitators[msg.sender];
    uint256 currentBucketLevel = f.bucketLevel;
    uint256 newBucketLevel = currentBucketLevel - amount;
    f.bucketLevel = uint128(newBucketLevel);

    _burn(msg.sender, amount);

    emit FacilitatorBucketLevelUpdated(msg.sender, currentBucketLevel, newBucketLevel);
  }
