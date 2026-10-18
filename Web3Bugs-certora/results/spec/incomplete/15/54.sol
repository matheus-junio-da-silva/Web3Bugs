// Original Solidity: contracts/15/gho/GhoToken.sol lines 72-91; addFacilitator
  function addFacilitator(
    address facilitatorAddress,
    string calldata facilitatorLabel,
    uint128 bucketCapacity
  ) external onlyRole(FACILITATOR_MANAGER) {
    Facilitator storage facilitator = _facilitators[facilitatorAddress];
    require(bytes(facilitator.label).length == 0, 'FACILITATOR_ALREADY_EXISTS');
    require(bytes(facilitatorLabel).length > 0, 'INVALID_LABEL');

    facilitator.label = facilitatorLabel;
    facilitator.bucketCapacity = bucketCapacity;

    _facilitatorsList.add(facilitatorAddress);

    emit FacilitatorAdded(
      facilitatorAddress,
      keccak256(abi.encodePacked(facilitatorLabel)),
      bucketCapacity
    );
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
