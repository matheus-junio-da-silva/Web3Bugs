// Original Solidity: contracts/15/gho/GhoToken.sol lines 16-16; storage
  mapping(address => Facilitator) internal _facilitators;

// Original Solidity: contracts/15/gho/GhoToken.sol lines 17-17; storage
  EnumerableSet.AddressSet internal _facilitatorsList;

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

// Original Solidity: contracts/15/gho/GhoToken.sol lines 134-136; getFacilitatorsList
  function getFacilitatorsList() external view returns (address[] memory) {
    return _facilitatorsList.values();
  }

// Original Solidity: contracts/15/gho/ERC20.sol lines 29-29; storage
  mapping(address => uint256) public balanceOf;
