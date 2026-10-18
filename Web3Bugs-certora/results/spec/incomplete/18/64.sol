// Historical Solidity excerpts; not a compilable harness.
// Original: contracts/18/contracts/token/ERC20/extensions/ERC20FlashMint.sol lines 39-62 (callable)
    function flashFee(address token, uint256 amount) public view virtual override returns (uint256) {
        require(token == address(this), "ERC20FlashMint: wrong token");
        // silence warning about unused variable without the addition of bytecode.
        amount;
        return 0;
    }

    /**
     * @dev Returns the receiver address of the flash fee. By default this
     * implementation returns the address(0) which means the fee amount will be burnt.
     * This function can be overloaded to change the fee receiver.
     * @return The address for which the flash fee will be sent to.
     */
    function _flashFeeReceiver() internal view virtual returns (address) {
        return address(0);
    }

    /**
     * @dev Performs a flash loan. New tokens are minted and sent to the
     * `receiver`, who is required to implement the {IERC3156FlashBorrower}
     * interface. By the end of the flash loan, the receiver is expected to own
     * amount + fee tokens and have them approved back to the token contract itself so
     * they can be burned.
     * @param receiver The receiver of the flash loan. Should implement the

// Original: contracts/18/contracts/token/ERC20/extensions/ERC20FlashMint.sol lines 70-93 (callable)
    // This function can reenter, but it doesn't pose a risk because it always preserves the property that the amount
    // minted at the beginning is always recovered and burned at the end, or else the entire function will revert.
    // slither-disable-next-line reentrancy-no-eth
    function flashLoan(
        IERC3156FlashBorrower receiver,
        address token,
        uint256 amount,
        bytes calldata data
    ) public virtual override returns (bool) {
        require(amount <= maxFlashLoan(token), "ERC20FlashMint: amount exceeds maxFlashLoan");
        uint256 fee = flashFee(token, amount);
        _mint(address(receiver), amount);
        require(
            receiver.onFlashLoan(msg.sender, token, amount, fee, data) == _RETURN_VALUE,
            "ERC20FlashMint: invalid return value"
        );
        address flashFeeReceiver = _flashFeeReceiver();
        _spendAllowance(address(receiver), address(this), amount + fee);
        if (fee == 0 || flashFeeReceiver == address(0)) {
            _burn(address(receiver), amount + fee);
        } else {
            _burn(address(receiver), amount);
            _transfer(address(receiver), flashFeeReceiver, fee);
        }

// Original: contracts/18/contracts/token/ERC20/extensions/ERC20FlashMint.sol lines 71-94 (callable)
    // minted at the beginning is always recovered and burned at the end, or else the entire function will revert.
    // slither-disable-next-line reentrancy-no-eth
    function flashLoan(
        IERC3156FlashBorrower receiver,
        address token,
        uint256 amount,
        bytes calldata data
    ) public virtual override returns (bool) {
        require(amount <= maxFlashLoan(token), "ERC20FlashMint: amount exceeds maxFlashLoan");
        uint256 fee = flashFee(token, amount);
        _mint(address(receiver), amount);
        require(
            receiver.onFlashLoan(msg.sender, token, amount, fee, data) == _RETURN_VALUE,
            "ERC20FlashMint: invalid return value"
        );
        address flashFeeReceiver = _flashFeeReceiver();
        _spendAllowance(address(receiver), address(this), amount + fee);
        if (fee == 0 || flashFeeReceiver == address(0)) {
            _burn(address(receiver), amount + fee);
        } else {
            _burn(address(receiver), amount);
            _transfer(address(receiver), flashFeeReceiver, fee);
        }
        return true;

// Original: contracts/18/contracts/token/ERC20/extensions/ERC20FlashMint.sol lines 73-96 (callable)
    function flashLoan(
        IERC3156FlashBorrower receiver,
        address token,
        uint256 amount,
        bytes calldata data
    ) public virtual override returns (bool) {
        require(amount <= maxFlashLoan(token), "ERC20FlashMint: amount exceeds maxFlashLoan");
        uint256 fee = flashFee(token, amount);
        _mint(address(receiver), amount);
        require(
            receiver.onFlashLoan(msg.sender, token, amount, fee, data) == _RETURN_VALUE,
            "ERC20FlashMint: invalid return value"
        );
        address flashFeeReceiver = _flashFeeReceiver();
        _spendAllowance(address(receiver), address(this), amount + fee);
        if (fee == 0 || flashFeeReceiver == address(0)) {
            _burn(address(receiver), amount + fee);
        } else {
            _burn(address(receiver), amount);
            _transfer(address(receiver), flashFeeReceiver, fee);
        }
        return true;
    }
}

// Original: contracts/18/contracts/mocks/ERC20FlashMintMock.sol lines 24-44 (callable)
    function setFlashFee(uint256 amount) public {
        _flashFeeAmount = amount;
    }

    function flashFee(address token, uint256 amount) public view virtual override returns (uint256) {
        super.flashFee(token, amount);
        return _flashFeeAmount;
    }

    function setFlashFeeReceiver(address receiver) public {
        _flashFeeReceiverAddress = receiver;
    }

    function flashFeeReceiver() public view returns (address) {
        return _flashFeeReceiver();
    }

    function _flashFeeReceiver() internal view override returns (address) {
        return _flashFeeReceiverAddress;
    }
}

// Original: contracts/18/contracts/mocks/ERC20FlashMintMock.sol lines 28-44 (callable)
    function flashFee(address token, uint256 amount) public view virtual override returns (uint256) {
        super.flashFee(token, amount);
        return _flashFeeAmount;
    }

    function setFlashFeeReceiver(address receiver) public {
        _flashFeeReceiverAddress = receiver;
    }

    function flashFeeReceiver() public view returns (address) {
        return _flashFeeReceiver();
    }

    function _flashFeeReceiver() internal view override returns (address) {
        return _flashFeeReceiverAddress;
    }
}
