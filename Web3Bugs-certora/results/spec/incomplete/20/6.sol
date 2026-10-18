// Historical source: contracts/20/contracts/BentoBox.sol:89-95
    mapping(IERC20 => mapping(address => uint256)) public balanceOf;

    // Rebase from amount to share
    mapping(IERC20 => Rebase) public totals;

    mapping(IERC20 => IStrategy) public strategy;
    mapping(IERC20 => IStrategy) public pendingStrategy;


// Historical source: contracts/20/contracts/BentoBox.sol:237-265
    function withdraw(
        IERC20 token_,
        address from,
        address to,
        uint256 amount,
        uint256 share
    ) public allowed(from) returns (uint256 amountOut, uint256 shareOut) {
        // Checks
        require(to != address(0), "BentoBox: to not set"); // To avoid a bad UI from burning funds

        // Effects
        IERC20 token = token_ == USE_ETHEREUM ? wethToken : token_;
        Rebase memory total = totals[token];
        if (share == 0) {
            // value of the share paid could be lower than the amount paid due to rounding, in that case, add a share (Always round up)
            share = total.toBase(amount, true);
        } else {
            // amount may be lower than the value of share due to rounding, that's ok
            amount = total.toElastic(share, false);
        }

        balanceOf[token][from] = balanceOf[token][from].sub(share);
        total.elastic = total.elastic.sub(amount.to128());
        total.base = total.base.sub(share.to128());
        // There have to be at least 1000 shares left to prevent reseting the share/amount ratio (unless it's fully emptied)
        require(total.base >= MINIMUM_SHARE_BALANCE || total.base == 0, "BentoBox: cannot empty");
        totals[token] = total;

        // Interactions


// Historical source: contracts/20/contracts/BentoBox.sol:289-335
    // F3: This isn't combined with transferMultiple for gas optimization
    function transfer(
        IERC20 token,
        address from,
        address to,
        uint256 share
    ) public allowed(from) {
        // Checks
        require(to != address(0), "BentoBox: to not set"); // To avoid a bad UI from burning funds

        // Effects
        balanceOf[token][from] = balanceOf[token][from].sub(share);
        balanceOf[token][to] = balanceOf[token][to].add(share);

        emit LogTransfer(token, from, to, share);
    }

    /// @notice Transfer shares from a user account to multiple other ones.
    /// @param token The ERC-20 token to transfer.
    /// @param from which user to pull the tokens.
    /// @param tos The receivers of the tokens.
    /// @param shares The amount of `token` in shares for each receiver in `tos`.
    // F3 - Can it be combined with another similar function?
    // F3: This isn't combined with transfer for gas optimization
    function transferMultiple(
        IERC20 token,
        address from,
        address[] calldata tos,
        uint256[] calldata shares
    ) public allowed(from) {
        // Checks
        require(tos[0] != address(0), "BentoBox: to[0] not set"); // To avoid a bad UI from burning funds

        // Effects
        uint256 totalAmount;
        uint256 len = tos.length;
        for (uint256 i = 0; i < len; i++) {
            address to = tos[i];
            balanceOf[token][to] = balanceOf[token][to].add(shares[i]);
            totalAmount = totalAmount.add(shares[i]);
            emit LogTransfer(token, from, to, shares[i]);
        }
        balanceOf[token][from] = balanceOf[token][from].sub(totalAmount);
    }

    /// @notice Flashloan ability.
    /// @param borrower The address of the contract that implements and conforms to `IFlashBorrower` and handles the flashloan.


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