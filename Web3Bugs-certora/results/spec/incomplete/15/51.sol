// Original Solidity: contracts/15/gho/GhoToken.sol lines 37-50; mint
  function mint(address account, uint256 amount) external override {
    Facilitator storage f = _facilitators[msg.sender];
    uint256 bucketCapacity = f.bucketCapacity;
    require(bucketCapacity > 0, 'INVALID_FACILITATOR');

    uint256 currentBucketLevel = f.bucketLevel;
    uint256 newBucketLevel = currentBucketLevel + amount;
    require(bucketCapacity >= newBucketLevel, 'FACILITATOR_BUCKET_CAPACITY_EXCEEDED');
    f.bucketLevel = uint128(newBucketLevel);

    _mint(account, amount);

    emit FacilitatorBucketLevelUpdated(msg.sender, currentBucketLevel, newBucketLevel);
  }
