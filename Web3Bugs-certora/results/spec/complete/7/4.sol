// Original: contracts/7/contracts/protocol/tokenization/AToken.sol, lines 128-132
function balanceOf(
    address user
  ) public view virtual override(IncentivizedERC20, IERC20) returns (uint256) {
    return super.balanceOf(user).rayMul(POOL.getReserveNormalizedIncome(_underlyingAsset));
  }

// Original: contracts/7/contracts/protocol/tokenization/base/ScaledBalanceTokenBase.sol, lines 130-155
function _transfer(address sender, address recipient, uint256 amount, uint256 index) internal {
    uint256 senderScaledBalance = super.balanceOf(sender);
    uint256 senderBalanceIncrease = senderScaledBalance.rayMul(index) -
      senderScaledBalance.rayMul(_userState[sender].additionalData);

    uint256 recipientScaledBalance = super.balanceOf(recipient);
    uint256 recipientBalanceIncrease = recipientScaledBalance.rayMul(index) -
      recipientScaledBalance.rayMul(_userState[recipient].additionalData);

    _userState[sender].additionalData = index.toUint128();
    _userState[recipient].additionalData = index.toUint128();

    super._transfer(sender, recipient, amount.rayDiv(index).toUint128());

    if (senderBalanceIncrease > 0) {
      emit Transfer(address(0), sender, senderBalanceIncrease);
      emit Mint(_msgSender(), sender, senderBalanceIncrease, senderBalanceIncrease, index);
    }

    if (sender != recipient && recipientBalanceIncrease > 0) {
      emit Transfer(address(0), recipient, recipientBalanceIncrease);
      emit Mint(_msgSender(), recipient, recipientBalanceIncrease, recipientBalanceIncrease, index);
    }

    emit Transfer(sender, recipient, amount);
  }

// Original: contracts/7/contracts/protocol/tokenization/base/ScaledBalanceTokenBase.sol, lines 66-88
function _mintScaled(
    address caller,
    address onBehalfOf,
    uint256 amount,
    uint256 index
  ) internal returns (bool) {
    uint256 amountScaled = amount.rayDiv(index);
    require(amountScaled != 0, Errors.INVALID_MINT_AMOUNT);

    uint256 scaledBalance = super.balanceOf(onBehalfOf);
    uint256 balanceIncrease = scaledBalance.rayMul(index) -
      scaledBalance.rayMul(_userState[onBehalfOf].additionalData);

    _userState[onBehalfOf].additionalData = index.toUint128();

    _mint(onBehalfOf, amountScaled.toUint128());

    uint256 amountToMint = amount + balanceIncrease;
    emit Transfer(address(0), onBehalfOf, amountToMint);
    emit Mint(caller, onBehalfOf, amountToMint, balanceIncrease, index);

    return (scaledBalance == 0);
  }

// Original: contracts/7/contracts/protocol/tokenization/base/ScaledBalanceTokenBase.sol, lines 99-120
function _burnScaled(address user, address target, uint256 amount, uint256 index) internal {
    uint256 amountScaled = amount.rayDiv(index);
    require(amountScaled != 0, Errors.INVALID_BURN_AMOUNT);

    uint256 scaledBalance = super.balanceOf(user);
    uint256 balanceIncrease = scaledBalance.rayMul(index) -
      scaledBalance.rayMul(_userState[user].additionalData);

    _userState[user].additionalData = index.toUint128();

    _burn(user, amountScaled.toUint128());

    if (balanceIncrease > amount) {
      uint256 amountToMint = balanceIncrease - amount;
      emit Transfer(address(0), user, amountToMint);
      emit Mint(user, user, amountToMint, balanceIncrease, index);
    } else {
      uint256 amountToBurn = amount - balanceIncrease;
      emit Transfer(user, address(0), amountToBurn);
      emit Burn(user, target, amountToBurn, balanceIncrease, index);
    }
  }
