// Historical source: contracts/20/contracts/BentoBox.sol:89-95
    mapping(IERC20 => mapping(address => uint256)) public balanceOf;

    // Rebase from amount to share
    mapping(IERC20 => Rebase) public totals;

    mapping(IERC20 => IStrategy) public strategy;
    mapping(IERC20 => IStrategy) public pendingStrategy;


// Historical source: contracts/20/contracts/BentoBox.sol:140-163
    /// @dev Helper function to represent an `amount` of `token` in shares.
    /// @param token The ERC-20 token.
    /// @param amount The `token` amount.
    /// @param roundUp If the result `share` should be rounded up.
    /// @return share The token amount represented in shares.
    function toShare(
        IERC20 token,
        uint256 amount,
        bool roundUp
    ) external view returns (uint256 share) {
        share = totals[token].toBase(amount, roundUp);
    }

    /// @dev Helper function represent shares back into the `token` amount.
    /// @param token The ERC-20 token.
    /// @param share The amount of shares.
    /// @param roundUp If the result should be rounded up.
    /// @return amount The share amount back into native representation.
    function toAmount(
        IERC20 token,
        uint256 share,
        bool roundUp
    ) external view returns (uint256 amount) {
        amount = totals[token].toElastic(share, roundUp);


// Historical source: contracts/20/contracts/BentoBox.sol:174-218
    function deposit(
        IERC20 token_,
        address from,
        address to,
        uint256 amount,
        uint256 share
    ) public payable allowed(from) returns (uint256 amountOut, uint256 shareOut) {
        // Checks
        require(to != address(0), "BentoBox: to not set"); // To avoid a bad UI from burning funds

        // Effects
        IERC20 token = token_ == USE_ETHEREUM ? wethToken : token_;
        Rebase memory total = totals[token];

        // If a new token gets added, the tokenSupply call checks that this is a deployed contract. Needed for security.
        require(total.elastic != 0 || token.totalSupply() > 0, "BentoBox: No tokens");
        if (share == 0) {
            // value of the share may be lower than the amount due to rounding, that's ok
            share = total.toBase(amount, false);
            // Any deposit should lead to at least the minimum share balance, otherwise it's ignored (no amount taken)
            if (total.base.add(share.to128()) < MINIMUM_SHARE_BALANCE) {
                return (0, 0);
            }
        } else {
            // amount may be lower than the value of share due to rounding, in that case, add 1 to amount (Always round up)
            amount = total.toElastic(share, true);
        }

        // In case of skimming, check that only the skimmable amount is taken.
        // For ETH, the full balance is available, so no need to check.
        // During flashloans the _tokenBalanceOf is lower than 'reality', so skimming deposits will mostly fail during a flashloan.
        require(
            from != address(this) || token_ == USE_ETHEREUM || amount <= _tokenBalanceOf(token).sub(total.elastic),
            "BentoBox: Skim too much"
        );

        balanceOf[token][to] = balanceOf[token][to].add(share);
        total.base = total.base.add(share.to128());
        total.elastic = total.elastic.add(amount.to128());
        totals[token] = total;

        // Interactions
        // During the first deposit, we check that this token is 'real'
        if (token_ == USE_ETHEREUM) {
            // X2 - If there is an error, could it cause a DoS. Like balanceOf causing revert. (SWC-113)


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



// Historical source: contracts/20/spec/harness/CompoundStrategyHarness.sol:1-18
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
				return (IERC20(token)).balanceOf(account);
	}
}

// Historical source: contracts/20/contracts/strategies/CompoundStrategy.sol:53-91
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
    }

    function _swapAll(


// Historical source: contracts/20/contracts/strategies/CompoundStrategy.sol:110-190
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

    function harvestCOMP(uint256 minAmount) public onlyOwner {
        // To prevent flash loan sandwich attacks to 'steal' the profit, only the owner can harvest the COMP
        // Swap all COMP to WETH
        _swapAll(compToken, weth, address(this));
        // Swap all WETH to token and leave it on the contract to be swept up in the next harvest
        require(_swapAll(weth, token, address(this)) >= minAmount, "CompoundStrategy: not enough");
    }

    // Withdraw assets.
    /// @inheritdoc IStrategy
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
            // If there are more tokens available than our full position, take all based on cToken balance (continue if unsuccesful)
            try cToken.redeem(cToken.balanceOf(address(this))) {} catch {}
        } else {
            // Otherwise redeem all available and take a loss on the missing amount (continue if unsuccesful)
            try cToken.redeemUnderlying(available) {} catch {}
        }

        // Check balance of token on the contract
        uint256 amount = token.balanceOf(address(this));
        // Calculate tokens added (or lost)
        amountAdded = int256(amount) - int256(balance);
        // Transfer all tokens to bentobox
        token.safeTransfer(bentobox, amount);
        // Flag as exited, allowing the owner to manually deal with any amounts available later
        exited = true;
    }

    function afterExit(
        address to,
        uint256 value,
        bytes memory data
    ) public onlyOwner returns (bool success) {
        // After exited, the owner can perform ANY call. This is to rescue any funds that didn't get released during exit or
        // got earned afterwards due to vesting or airdrops, etc.
        require(exited, "CompoundStrategy: Not exited");
