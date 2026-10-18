// Original Solidity: contracts/15/facilitators/flashMinter/GhoFlashMinter.sol lines 100-105; updateFee
  function updateFee(uint256 newFee) external override onlyPoolAdmin {
    require(newFee <= MAX_FEE, 'FlashMinter: Fee out of range');
    uint256 oldFee = _fee;
    _fee = newFee;
    emit FeeUpdated(oldFee, newFee);
  }

// Original Solidity: contracts/15/facilitators/flashMinter/GhoFlashMinter.sol lines 108-112; updateGhoTreasury
  function updateGhoTreasury(address newGhoTreasury) external override onlyPoolAdmin {
    address oldGhoTreasury = _ghoTreasury;
    _ghoTreasury = newGhoTreasury;
    emit GhoTreasuryUpdated(oldGhoTreasury, newGhoTreasury);
  }
