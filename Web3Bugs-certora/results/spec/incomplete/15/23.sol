// Original Solidity: contracts/15/facilitators/flashMinter/GhoFlashMinter.sol lines 108-112; updateGhoTreasury
  function updateGhoTreasury(address newGhoTreasury) external override onlyPoolAdmin {
    address oldGhoTreasury = _ghoTreasury;
    _ghoTreasury = newGhoTreasury;
    emit GhoTreasuryUpdated(oldGhoTreasury, newGhoTreasury);
  }
