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
