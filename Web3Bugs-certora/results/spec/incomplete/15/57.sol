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

// Original Solidity: contracts/15/gho/GhoToken.sol lines 94-108; removeFacilitator
  function removeFacilitator(address facilitatorAddress) external onlyRole(FACILITATOR_MANAGER) {
    require(
      bytes(_facilitators[facilitatorAddress].label).length > 0,
      'FACILITATOR_DOES_NOT_EXIST'
    );
    require(
      _facilitators[facilitatorAddress].bucketLevel == 0,
      'FACILITATOR_BUCKET_LEVEL_NOT_ZERO'
    );

    delete _facilitators[facilitatorAddress];
    _facilitatorsList.remove(facilitatorAddress);

    emit FacilitatorRemoved(facilitatorAddress);
  }

// Original Solidity: contracts/15/gho/ERC20.sol lines 29-29; storage
  mapping(address => uint256) public balanceOf;
