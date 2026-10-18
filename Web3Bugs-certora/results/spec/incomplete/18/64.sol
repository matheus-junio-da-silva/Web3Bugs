// ORIGINAL HISTORICAL SOLIDITY excerpts; content copied literally from contracts/18
// CVL property: ERC20FlashMint.spec:18-28 letsWatchItBurns

// Original: contracts/18/contracts/token/ERC20/extensions/ERC20FlashMint.sol lines 39-44 function/modifier flashFee
    function flashFee(address token, uint256 amount) public view virtual override returns (uint256) {
        require(token == address(this), "ERC20FlashMint: wrong token");
        // silence warning about unused variable without the addition of bytecode.
        amount;
        return 0;
    }

// Original: contracts/18/contracts/token/ERC20/extensions/ERC20FlashMint.sol lines 73-95 function/modifier flashLoan
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

// Original: contracts/18/contracts/mocks/ERC20FlashMintMock.sol lines 28-31 function/modifier flashFee
    function flashFee(address token, uint256 amount) public view virtual override returns (uint256) {
        super.flashFee(token, amount);
        return _flashFeeAmount;
    }

// Original: contracts/18/contracts/token/ERC20/ERC20.sol lines 36-36 state declaration
    mapping(address => uint256) private _balances;

// Original: contracts/18/contracts/token/ERC20/ERC20.sol lines 40-40 state declaration
    uint256 private _totalSupply;
