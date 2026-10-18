// Original Solidity: contracts/15/facilitators/flashMinter/GhoFlashMinter.sol lines 115-124; maxFlashLoan
  function maxFlashLoan(address token) external view override returns (uint256) {
    if (token != address(GHO_TOKEN)) {
      return 0;
    } else {
      IGhoToken.Facilitator memory flashMinterFacilitator = GHO_TOKEN.getFacilitator(address(this));
      uint256 capacity = flashMinterFacilitator.bucketCapacity;
      uint256 level = flashMinterFacilitator.bucketLevel;
      return capacity > level ? capacity - level : 0;
    }
  }
