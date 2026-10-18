// Historical source: contracts/20/contracts/BentoBox.sol:88-99
    // Balance per token per address/contract in shares
    mapping(IERC20 => mapping(address => uint256)) public balanceOf;

    // Rebase from amount to share
    mapping(IERC20 => Rebase) public totals;

    mapping(IERC20 => IStrategy) public strategy;
    mapping(IERC20 => IStrategy) public pendingStrategy;
    mapping(IERC20 => StrategyData) public strategyData;

    // ******************* //
    // *** CONSTRUCTOR *** //


// Historical source: contracts/20/contracts/BentoBox.sol:419-452
    function setStrategy(IERC20 token, IStrategy newStrategy) public onlyOwner {
        StrategyData memory data = strategyData[token];
        IStrategy pending = pendingStrategy[token];
        if (data.strategyStartDate == 0 || pending != newStrategy) {
            pendingStrategy[token] = newStrategy;
            // C1 - All math done through BoringMath (SWC-101)
            // C1: Our sun will swallow the earth well before this overflows
            data.strategyStartDate = (block.timestamp + STRATEGY_DELAY).to64();
            emit LogStrategyQueued(token, newStrategy);
        } else {
            require(data.strategyStartDate != 0 && block.timestamp >= data.strategyStartDate, "StrategyManager: Too early");
            if (address(strategy[token]) != address(0)) {
                int256 balanceChange = strategy[token].exit(data.balance);
                // Effects
                if (balanceChange > 0) {
                    uint256 add = uint256(balanceChange);
                    totals[token].addElastic(add);
                    emit LogStrategyProfit(token, add);
                } else if (balanceChange < 0) {
                    uint256 sub = uint256(-balanceChange);
                    totals[token].subElastic(sub);
                    emit LogStrategyLoss(token, sub);
                }

                emit LogStrategyDivest(token, data.balance);
            }
            strategy[token] = pending;
            data.strategyStartDate = 0;
            data.balance = 0;
            pendingStrategy[token] = IStrategy(0);
            emit LogStrategySet(token, newStrategy);
        }
        strategyData[token] = data;
    }


// Historical source: contracts/20/contracts/BentoBox.sol:463-518
    function harvest(
        IERC20 token,
        bool balance,
        uint256 maxChangeAmount
    ) public {
        StrategyData memory data = strategyData[token];
        IStrategy _strategy = strategy[token];
        int256 balanceChange = _strategy.harvest(data.balance, msg.sender);
        if (balanceChange == 0 && !balance) {
            return;
        }

        uint256 totalElastic = totals[token].elastic;

        if (balanceChange > 0) {
            uint256 add = uint256(balanceChange);
            totalElastic = totalElastic.add(add);
            totals[token].elastic = totalElastic.to128();
            emit LogStrategyProfit(token, add);
        } else if (balanceChange < 0) {
            // C1 - All math done through BoringMath (SWC-101)
            // C1: balanceChange could overflow if it's max negative int128.
            // But tokens with balances that large are not supported by the BentoBox.
            uint256 sub = uint256(-balanceChange);
            totalElastic = totalElastic.sub(sub);
            totals[token].elastic = totalElastic.to128();
            data.balance = data.balance.sub(sub.to128());
            emit LogStrategyLoss(token, sub);
        }

        if (balance) {
            uint256 targetBalance = totalElastic.mul(data.targetPercentage) / 100;
            // if data.balance == targetBalance there is nothing to update
            if (data.balance < targetBalance) {
                uint256 amountOut = targetBalance.sub(data.balance);
                if (maxChangeAmount != 0 && amountOut > maxChangeAmount) {
                    amountOut = maxChangeAmount;
                }
                token.safeTransfer(address(_strategy), amountOut);
                data.balance = data.balance.add(amountOut.to128());
                _strategy.skim(amountOut);
                emit LogStrategyInvest(token, amountOut);
            } else if (data.balance > targetBalance) {
                uint256 amountIn = data.balance.sub(targetBalance.to128());
                if (maxChangeAmount != 0 && amountIn > maxChangeAmount) {
                    amountIn = maxChangeAmount;
                }

                uint256 actualAmountIn = _strategy.withdraw(amountIn);

                data.balance = data.balance.sub(actualAmountIn.to128());
                emit LogStrategyDivest(token, actualAmountIn);
            }
        }

        strategyData[token] = data;


// Historical source: contracts/20/spec/harness/BentoBoxHarness.sol:1-82
pragma solidity 0.6.12;
pragma experimental ABIEncoderV2;

import "../../contracts/BentoBox.sol";

// Note: Rebasing tokens ARE NOT supported and WILL cause loss of funds
contract BentoBoxHarness is BentoBox {

	// getters to internal 
	function totalTokenAmount(address token) public returns (uint128) {
		return totals[IERC20(token)].elastic;
	}

	function totalTokenShare(address token) public returns (uint128) {
		return totals[IERC20(token)].base;
	}

	// wrap internal function
	function tokenBalanceOf(address token) public returns (uint256) {
		return _tokenBalanceOf(IERC20(token));
	}

	// wrap internal function
	function tokenBalanceOfUser(IERC20 token, address user) public returns (uint256) {
		return token.balanceOf(user);
	}

	function assumeTosNotOther(address[] calldata toParams, address other) private {
        for (uint256 i = 0; i < toParams.length; i++) {
            address to = toParams[i];
			require (to != other);
		}
	}
	
	// to constraint harnessOther == other (from the spec)
	address public harnessOther;
	address public harnessFrom;
	IFlashBorrower public harnessBorrower;
	IERC20 public harnessToken;

	// limit loops to bound of 3
	function transferMultiple(IERC20 token, address from, address[] calldata tos, uint256[] calldata shares) public override {
		require (tos.length <= 3);
	
		// this would not constraint tos for any other rule except noChangeToOthersBalances,
		// because harnessOther is only constraint in noChangeToOthersBalances
		assumeTosNotOther(tos, harnessOther);
		require(from == harnessFrom);

		super.transferMultiple(token, from, tos, shares);
	}

	function flashLoan(IFlashBorrower borrower, address receiver, IERC20 token, uint256 amount, bytes calldata data) override public
	{
		require(harnessToken == token);
		require(harnessBorrower == borrower);
		super.flashLoan(borrower, receiver, token, amount, data );
	}




	function getStrategyTokenBalance(IERC20 token) public returns (uint256) {
		return strategyData[token].balance;
	}

	//for invariants we need a function that simulate the constructor 
	function init_state() public { }

	constructor(IERC20 wethToken_) BentoBox(wethToken_) public { }


	function batch(bytes[] calldata calls, bool revertOnFail) external override payable returns(bool[] memory successes, bytes[] memory results) {
	}


	function deploy(address masterContract, bytes calldata data, bool useCreate2) public override  payable returns (address) {

	}

	function permitToken(IERC20 token, address from, uint256 amount, uint256 deadline, uint8 v, bytes32 r, bytes32 s) external {



// Historical source: contracts/20/spec/harness/SymbolicStrategy.sol:1-51
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
	}
}