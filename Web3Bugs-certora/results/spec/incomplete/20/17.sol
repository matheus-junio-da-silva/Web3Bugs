// Historical source: contracts/20/contracts/strategies/CompoundStrategy.sol:53-88
contract CompoundStrategy is IStrategy, BoringOwnable {
    using BoringMath for uint256;
    using BoringERC20 for IERC20;
    using BoringERC20 for IcToken;

    address public immutable bentobox;
    IERC20 public immutable token;
    IcToken public immutable cToken;
    IERC20 public immutable compToken;
    IERC20 public immutable weth;
    IFactory public immutable factory;
    bool public exited;

    constructor(
        address bentobox_,
        IFactory factory_,
        IERC20 token_,
        IcToken cToken_,
        IERC20 compToken_,
        IERC20 weth_
    ) public {
        bentobox = bentobox_;
        factory = factory_;
        token = token_;
        cToken = cToken_;
        compToken = compToken_;
        weth = weth_;

        token_.approve(address(cToken_), type(uint256).max);
    }

    modifier onlyBentobox {
        // Only the bentobox can call harvest on this strategy
        require(msg.sender == bentobox, "CompoundStrategy: only bento");
        require(!exited, "CompoundStrategy: exited");
        _;


// Historical source: contracts/20/contracts/strategies/CompoundStrategy.sol:110-135
    }

    // Send the assets to the Strategy and call skim to invest them
    /// @inheritdoc IStrategy
    function skim(uint256 amount) external override onlyBentobox {
        require(cToken.mint(amount) == 0, "CompoundStrategy: mint error");
    }

    // Harvest any profits made converted to the asset and pass them to the caller
    /// @inheritdoc IStrategy
    function harvest(uint256 balance, address sender) external override onlyBentobox returns (int256 amountAdded) {
        // To prevent anyone from using flash loans to 'steal' part of the profits, only EOA is allowed to call harvest
        require(sender == tx.origin, "CompoundStrategy: EOA only");
        // Get the amount of tokens that the cTokens currently represent
        uint256 tokenBalance = cToken.balanceOfUnderlying(address(this));
        // Convert enough cToken to take out the profit
        // If the amount is negative due to rounding (near impossible), just revert. Should be positive soon enough.
        require(cToken.redeemUnderlying(tokenBalance.sub(balance)) == 0, "CompoundStrategy: profit fail");

        // Find out how much has been added (+ sitting on the contract from harvestCOMP)
        uint256 amountAdded_ = token.balanceOf(address(this));
        // Transfer the profit to the bentobox, the amountAdded at this point matches the amount transferred
        token.safeTransfer(bentobox, amountAdded_);

        return int256(amountAdded_);
    }


// Historical source: contracts/20/contracts/strategies/CompoundStrategy.sol:147-165
    function withdraw(uint256 amount) external override onlyBentobox returns (uint256 actualAmount) {
        // Convert enough cToken to take out 'amount' tokens
        require(cToken.redeemUnderlying(amount) == 0, "CompoundStrategy: redeem fail");

        // Make sure we send and report the exact same amount of tokens by using balanceOf
        actualAmount = token.balanceOf(address(this));
        token.safeTransfer(bentobox, actualAmount);
    }

    // Withdraw all assets in the safest way possible. This shouldn't fail.
    /// @inheritdoc IStrategy
    function exit(uint256 balance) external override onlyBentobox returns (int256 amountAdded) {
        // Get the amount of tokens that the cTokens currently represent
        uint256 tokenBalance = cToken.balanceOfUnderlying(address(this));
        // Get the actual token balance of the cToken contract
        uint256 available = token.balanceOf(address(cToken));

        // Check that the cToken contract has enough balance to pay out in full
        if (tokenBalance <= available) {


// Historical source: contracts/20/spec/harness/CompoundStrategyHarness.sol:1-15
pragma solidity 0.6.12;

import "./StrategyHarness.sol";
import "../../contracts/strategies/CompoundStrategy.sol";

contract CompoundStrategyHarness is StrategyHarness, CompoundStrategy {
    constructor(address bentobox_, IFactory factory_, IERC20 token_, IcToken cToken_,
                IERC20 compToken_, IERC20 weth_) CompoundStrategy(bentobox_, factory_, token_, cToken_, compToken_, weth_) public { }

    function receiver() public returns (address) {
		return bentobox;
	}

	function tokenBalanceOf(address token, 
			address account) public returns (uint256)  {


// Historical source: contracts/20/spec/harness/StrategyHarness.sol:1-47
pragma solidity 0.6.12;

import "@boringcrypto/boring-solidity/contracts/libraries/BoringMath.sol";

contract StrategyHarness {
    using BoringMath for uint256;

	function compareLEzero(int256 x) external returns (bool) {
		return x <= 0;
	}

	function compareLTzero(int256 x) external returns (bool) {
		return x < 0;
	}

	function compareGEzero(int256 x) external returns (bool) {
		return x >= 0;
	}

	function compareGTzero(int256 x) external returns (bool) {
		return x > 0;
	}

	function compareLEmaxUint255(int256 x) external returns (bool) {
		return x < (2^255 -1);
	}

	function checkAplusBeqC(uint256 a, int256 b, uint256 c) public returns (bool) {
		if (b >= 0) {
            uint256 b_ = uint256(b);
            return a.add(b_) == c;
        } else if (b < 0) {
            uint256 b_ = uint256(-b);
            return a.sub(b_) == c;
        }
	}

	function subToInt(uint256 a, uint256 b) public returns (int256) {
		return int256(a - b);
	}

	function safeSub(uint256 a, uint256 b) public returns (int256) {
		int256 c = int256(a - b);
		require((a > b && c > 0) || ( a <= b && c <= 0), "underflow");
		return c;
	}
}