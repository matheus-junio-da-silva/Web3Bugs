// Original Solidity: contracts/15/facilitators/flashMinter/GhoFlashMinter.sol lines 127-130; flashFee
  function flashFee(address token, uint256 amount) external view override returns (uint256) {
    require(token == address(GHO_TOKEN), 'FlashMinter: Unsupported currency');
    return ACL_MANAGER.isFlashBorrower(msg.sender) ? 0 : _flashFee(amount);
  }
