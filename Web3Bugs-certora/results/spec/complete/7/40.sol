// Original: contracts/7/contracts/protocol/tokenization/StableDebtToken.sol, lines 124-175
function mint(
    address user,
    address onBehalfOf,
    uint256 amount,
    uint256 rate
  ) external virtual override onlyPool returns (bool, uint256, uint256) {
    MintLocalVars memory vars;

    if (user != onBehalfOf) {
      _decreaseBorrowAllowance(onBehalfOf, user, amount);
    }

    (, uint256 currentBalance, uint256 balanceIncrease) = _calculateBalanceIncrease(onBehalfOf);

    vars.previousSupply = totalSupply();
    vars.currentAvgStableRate = _avgStableRate;
    vars.nextSupply = _totalSupply = vars.previousSupply + amount;

    vars.amountInRay = amount.wadToRay();

    vars.currentStableRate = _userState[onBehalfOf].additionalData;
    vars.nextStableRate = (vars.currentStableRate.rayMul(currentBalance.wadToRay()) +
      vars.amountInRay.rayMul(rate)).rayDiv((currentBalance + amount).wadToRay());

    _userState[onBehalfOf].additionalData = vars.nextStableRate.toUint128();

    //solium-disable-next-line
    _totalSupplyTimestamp = _timestamps[onBehalfOf] = uint40(block.timestamp);

    // Calculates the updated average stable rate
    vars.currentAvgStableRate = _avgStableRate = (
      (vars.currentAvgStableRate.rayMul(vars.previousSupply.wadToRay()) +
        rate.rayMul(vars.amountInRay)).rayDiv(vars.nextSupply.wadToRay())
    ).toUint128();

    uint256 amountToMint = amount + balanceIncrease;
    _mint(onBehalfOf, amountToMint, vars.previousSupply);

    emit Transfer(address(0), onBehalfOf, amountToMint);
    emit Mint(
      user,
      onBehalfOf,
      amountToMint,
      currentBalance,
      balanceIncrease,
      vars.nextStableRate,
      vars.currentAvgStableRate,
      vars.nextSupply
    );

    return (currentBalance == 0, vars.nextSupply, vars.currentAvgStableRate);
  }

// Original: contracts/7/contracts/protocol/tokenization/StableDebtToken.sol, lines 178-245
function burn(
    address from,
    uint256 amount
  ) external virtual override onlyPool returns (uint256, uint256) {
    (, uint256 currentBalance, uint256 balanceIncrease) = _calculateBalanceIncrease(from);

    uint256 previousSupply = totalSupply();
    uint256 nextAvgStableRate = 0;
    uint256 nextSupply = 0;
    uint256 userStableRate = _userState[from].additionalData;

    // Since the total supply and each single user debt accrue separately,
    // there might be accumulation errors so that the last borrower repaying
    // might actually try to repay more than the available debt supply.
    // In this case we simply set the total supply and the avg stable rate to 0
    if (previousSupply <= amount) {
      _avgStableRate = 0;
      _totalSupply = 0;
    } else {
      nextSupply = _totalSupply = previousSupply - amount;
      uint256 firstTerm = uint256(_avgStableRate).rayMul(previousSupply.wadToRay());
      uint256 secondTerm = userStableRate.rayMul(amount.wadToRay());

      // For the same reason described above, when the last user is repaying it might
      // happen that user rate * user balance > avg rate * total supply. In that case,
      // we simply set the avg rate to 0
      if (secondTerm >= firstTerm) {
        nextAvgStableRate = _totalSupply = _avgStableRate = 0;
      } else {
        nextAvgStableRate = _avgStableRate = (
          (firstTerm - secondTerm).rayDiv(nextSupply.wadToRay())
        ).toUint128();
      }
    }

    if (amount == currentBalance) {
      _userState[from].additionalData = 0;
      _timestamps[from] = 0;
    } else {
      //solium-disable-next-line
      _timestamps[from] = uint40(block.timestamp);
    }
    //solium-disable-next-line
    _totalSupplyTimestamp = uint40(block.timestamp);

    if (balanceIncrease > amount) {
      uint256 amountToMint = balanceIncrease - amount;
      _mint(from, amountToMint, previousSupply);
      emit Transfer(address(0), from, amountToMint);
      emit Mint(
        from,
        from,
        amountToMint,
        currentBalance,
        balanceIncrease,
        userStableRate,
        nextAvgStableRate,
        nextSupply
      );
    } else {
      uint256 amountToBurn = amount - balanceIncrease;
      _burn(from, amountToBurn, previousSupply);
      emit Transfer(from, address(0), amountToBurn);
      emit Burn(from, amountToBurn, currentBalance, balanceIncrease, nextAvgStableRate, nextSupply);
    }

    return (nextSupply, nextAvgStableRate);
  }

// Original: contracts/7/contracts/protocol/tokenization/StableDebtToken.sol, lines 285-287
function totalSupply() public view virtual override returns (uint256) {
    return _calcTotalSupply(_avgStableRate);
  }
