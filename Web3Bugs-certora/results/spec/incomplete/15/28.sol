// Original Solidity: contracts/15/facilitators/flashMinter/GhoFlashMinter.sol lines 68-90; flashLoan
  function flashLoan(
    IERC3156FlashBorrower receiver,
    address token,
    uint256 amount,
    bytes calldata data
  ) external override returns (bool) {
    require(token == address(GHO_TOKEN), 'FlashMinter: Unsupported currency');

    uint256 fee = ACL_MANAGER.isFlashBorrower(msg.sender) ? 0 : _flashFee(amount);
    GHO_TOKEN.mint(address(receiver), amount);

    require(
      receiver.onFlashLoan(msg.sender, address(GHO_TOKEN), amount, fee, data) == CALLBACK_SUCCESS,
      'FlashMinter: Callback failed'
    );

    GHO_TOKEN.transferFrom(address(receiver), address(this), amount + fee);
    GHO_TOKEN.burn(amount);

    emit FlashMint(address(receiver), msg.sender, address(GHO_TOKEN), amount, fee);

    return true;
  }

// Original Solidity: contracts/15/facilitators/flashMinter/GhoFlashMinter.sol lines 127-130; flashFee
  function flashFee(address token, uint256 amount) external view override returns (uint256) {
    require(token == address(GHO_TOKEN), 'FlashMinter: Unsupported currency');
    return ACL_MANAGER.isFlashBorrower(msg.sender) ? 0 : _flashFee(amount);
  }
