// Original Solidity: contracts/15/facilitators/aave/tokens/GhoAToken.sol lines 156-158; transferUnderlyingTo
  function transferUnderlyingTo(address target, uint256 amount) external virtual override onlyPool {
    IGhoToken(_underlyingAsset).mint(target, amount);
  }

// Original Solidity: contracts/15/facilitators/aave/tokens/GhoAToken.sol lines 161-173; handleRepayment
  function handleRepayment(
    address user,
    address onBehalfOf,
    uint256 amount
  ) external virtual override onlyPool {
    uint256 balanceFromInterest = _ghoVariableDebtToken.getBalanceFromInterest(onBehalfOf);
    if (amount <= balanceFromInterest) {
      _ghoVariableDebtToken.decreaseBalanceFromInterest(onBehalfOf, amount);
    } else {
      _ghoVariableDebtToken.decreaseBalanceFromInterest(onBehalfOf, balanceFromInterest);
      IGhoToken(_underlyingAsset).burn(amount - balanceFromInterest);
    }
  }
