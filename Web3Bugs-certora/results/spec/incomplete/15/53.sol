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
