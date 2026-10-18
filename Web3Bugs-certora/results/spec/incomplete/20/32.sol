// Historical source: contracts/20/spec/harness/SymbolicStrategy.sol:1-49
pragma solidity 0.6.12;

import "./StrategyHarness.sol";
import "../../contracts/interfaces/IStrategy.sol";
import "@boringcrypto/boring-solidity/contracts/libraries/BoringERC20.sol";
import "@boringcrypto/boring-solidity/contracts/libraries/BoringMath.sol";

contract SymbolicStrategy is StrategyHarness, IStrategy {
	using BoringMath for uint256;
	using BoringERC20 for IERC20;

	IERC20 public token;
	address public receiver;

	//represent the current balance this strategy has
	//can be higher or lower by 50% than the amount believed to be in (balance)
	//uint256 symbolicCurrentBalance;
	function getCurrentBalance(uint256 balance) public  returns (uint256) {
		return token.balanceOf(address(this));
	}
  	
    function skim(uint256 balance) external override { }

    //Transfers to the receiver any profit made by the strategy on balance (from owner’s view). 
	//Returns the positive or negative profit 
    function harvest(uint256 balance, address sender) external override returns (int256 amountAdded) {
		uint256 b = getCurrentBalance(balance);
		int256 gain = safeSub(b, balance);
		if (gain > 0) {
			token.transfer(receiver, uint256(gain));
		}
		return gain;
	}

    // withdraw an amount and transfer to receiver
    function withdraw(uint256 amount) external override returns (uint256 actualAmount) {
		uint256 b = token.balanceOf(address(this));
		if( b < amount)
			amount = b;
		token.transfer(receiver, amount);
		return amount;
	}

    // Withdraw all assets in the safest way possible. This shouldn't fail.
	// returns the difference between the actual amount transferred and balance
    function exit(uint256 balance) external override returns (int256 amountAdded) {
		uint256 b = getCurrentBalance(balance);
		token.transfer(receiver, b);
		return safeSub(b, balance); 


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