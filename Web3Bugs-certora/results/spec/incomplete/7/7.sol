// Original: contracts/7/contracts/protocol/tokenization/AToken.sol, lines 203-218
function _transfer(address from, address to, uint256 amount, bool validate) internal virtual {
    address underlyingAsset = _underlyingAsset;

    uint256 index = POOL.getReserveNormalizedIncome(underlyingAsset);

    uint256 fromBalanceBefore = super.balanceOf(from).rayMul(index);
    uint256 toBalanceBefore = super.balanceOf(to).rayMul(index);

    super._transfer(from, to, amount, index);

    if (validate) {
      POOL.finalizeTransfer(underlyingAsset, from, to, amount, fromBalanceBefore, toBalanceBefore);
    }

    emit BalanceTransfer(from, to, amount.rayDiv(index), index);
  }

// Original: contracts/7/contracts/protocol/tokenization/AToken.sol, lines 226-228
function _transfer(address from, address to, uint128 amount) internal virtual override {
    _transfer(from, to, amount, true);
  }

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

// Original: contracts/7/contracts/protocol/tokenization/base/IncentivizedERC20.sol, lines 185-199
function _transfer(address sender, address recipient, uint128 amount) internal virtual {
    uint128 oldSenderBalance = _userState[sender].balance;
    _userState[sender].balance = oldSenderBalance - amount;
    uint128 oldRecipientBalance = _userState[recipient].balance;
    _userState[recipient].balance = oldRecipientBalance + amount;

    IAaveIncentivesController incentivesControllerLocal = _incentivesController;
    if (address(incentivesControllerLocal) != address(0)) {
      uint256 currentTotalSupply = _totalSupply;
      incentivesControllerLocal.handleAction(sender, currentTotalSupply, oldSenderBalance);
      if (sender != recipient) {
        incentivesControllerLocal.handleAction(recipient, currentTotalSupply, oldRecipientBalance);
      }
    }
  }
