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

// Original Solidity: contracts/15/gho/GhoToken.sol lines 111-121; setFacilitatorBucketCapacity
  function setFacilitatorBucketCapacity(
    address facilitator,
    uint128 newCapacity
  ) external onlyRole(BUCKET_MANAGER) {
    require(bytes(_facilitators[facilitator].label).length > 0, 'FACILITATOR_DOES_NOT_EXIST');

    uint256 oldCapacity = _facilitators[facilitator].bucketCapacity;
    _facilitators[facilitator].bucketCapacity = newCapacity;

    emit FacilitatorBucketCapacityUpdated(facilitator, oldCapacity, newCapacity);
  }
