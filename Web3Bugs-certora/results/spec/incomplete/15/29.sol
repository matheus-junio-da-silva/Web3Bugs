// Original Solidity: contracts/15/facilitators/aave/tokens/GhoAToken.sol lines 94-101; mint
  function mint(
    address caller,
    address onBehalfOf,
    uint256 amount,
    uint256 index
  ) external virtual override onlyPool returns (bool) {
    revert(Errors.OPERATION_NOT_SUPPORTED);
  }

// Original Solidity: contracts/15/facilitators/aave/tokens/GhoAToken.sol lines 104-111; burn
  function burn(
    address from,
    address receiverOfUnderlying,
    uint256 amount,
    uint256 index
  ) external virtual override onlyPool {
    revert(Errors.OPERATION_NOT_SUPPORTED);
  }

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
