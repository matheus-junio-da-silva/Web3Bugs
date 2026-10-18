// Original Solidity: contracts/15/facilitators/aave/tokens/GhoAToken.sol lines 156-158; transferUnderlyingTo
  function transferUnderlyingTo(address target, uint256 amount) external virtual override onlyPool {
    IGhoToken(_underlyingAsset).mint(target, amount);
  }
