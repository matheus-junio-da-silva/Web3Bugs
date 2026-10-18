// Historical source: contracts/20/contracts/strategies/SushiStrategy.sol:1-30
// SPDX-License-Identifier: MIT
pragma solidity 0.6.12;
import "../interfaces/IStrategy.sol";
import "@boringcrypto/boring-solidity/contracts/BoringOwnable.sol";
import "@boringcrypto/boring-solidity/contracts/libraries/BoringMath.sol";
import "@boringcrypto/boring-solidity/contracts/libraries/BoringERC20.sol";

// solhint-disable not-rely-on-time

interface ISushiBar is IERC20 {
    function enter(uint256 _amount) external;

    function leave(uint256 _share) external;
}

contract SushiStrategy is IStrategy, BoringOwnable {
    using BoringMath for uint256;
    using BoringERC20 for IERC20;

    IERC20 private immutable sushi;
    ISushiBar private immutable bar;

    constructor(ISushiBar bar_, IERC20 sushi_) public {
        bar = bar_;
        sushi = sushi_;
    }

    // Send the assets to the Strategy and call skim to invest them
    /// @inheritdoc IStrategy
    function skim(uint256 amount) external override {


// Historical source: contracts/20/contracts/strategies/SushiStrategy.sol:65-73
    function exit(uint256 balance) external override onlyOwner returns (int256 amountAdded) {
        uint256 share = bar.balanceOf(address(this));
        bar.leave(share);

        uint256 amount = sushi.balanceOf(address(this));
        amountAdded = int256(amount) - int256(balance);
        sushi.safeTransfer(owner, amount);
    }
}


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

// Historical source: contracts/20/spec/harness/SushiStrategyHarness.sol:1-12
pragma solidity 0.6.12;

import "./StrategyHarness.sol";
import "../../contracts/strategies/SushiStrategy.sol";

contract SushiStrategyHarness is StrategyHarness, SushiStrategy {
    constructor(ISushiBar bar_, IERC20 sushi_) SushiStrategy(bar_, sushi_) public { }

    function receiver() public returns (address) {
		return owner;
	}
}