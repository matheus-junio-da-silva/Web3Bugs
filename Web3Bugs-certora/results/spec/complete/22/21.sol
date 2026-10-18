// Literal Solidity excerpt: contracts/22/contracts/popsicle-v3-optimizer/PopsicleV3Optimizer.sol:123-158
    address public immutable override token0;
    /// @inheritdoc IPopsicleV3Optimizer
    address public immutable override token1;
    // WETH address
    address public constant weth = 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2;
    // @inheritdoc IPopsicleV3Optimizer
    int24 public immutable override tickSpacing;

    uint24 constant GLOBAL_DIVISIONER = 1e6; // for basis point (0.0001%)
    //The protocol's fee in hundredths of a bip, i.e. 1e-6
    uint24 constant protocolFee = 2 * 1e5; //20%

    mapping (address => bool) private _operatorApproved;

    // @inheritdoc IPopsicleV3Optimizer
    IUniswapV3Pool public override pool;
    // Accrued protocol fees in terms of token0
    uint256 public protocolFees0;
    // Accrued protocol fees in terms of token1
    uint256 public protocolFees1;
    // Total lifetime accrued fees in terms of token0
    uint256 public totalFees0;
    // Total lifetime accrued fees in terms of token1
    uint256 public totalFees1;
    
    // Address of the Optimizer's owner
    address public governance;
    // Pending to claim ownership address
    address public pendingGovernance;
    //PopsicleV3 Optimizer settings address
    address public strategy;
    // Current tick lower of Optimizer pool position
    int24 public override tickLower;
    // Current tick higher of Optimizer pool position
    int24 public override tickUpper;
    // Checks if Optimizer is initialized

// Literal Solidity excerpt: contracts/22/contracts/popsicle-v3-optimizer/token/ERC20.sol:1-115
// SPDX-License-Identifier: MIT

pragma solidity ^0.7.0;

import "../utils/Context.sol";
import "./IERC20.sol";
import "../libraries/LowGasSafeMath.sol";

/**
 * @dev Implementation of the {IERC20} interface.
 *
 * This implementation is agnostic to the way tokens are created. This means
 * that a supply mechanism has to be added in a derived contract using {_mint}.
 * For a generic mechanism see {ERC20PresetMinterPauser}.
 *
 * TIP: For a detailed writeup see our guide
 * https://forum.zeppelin.solutions/t/how-to-implement-erc20-supply-mechanisms/226[How
 * to implement supply mechanisms].
 *
 * We have followed general OpenZeppelin guidelines: functions revert instead
 * of returning `false` on failure. This behavior is nonetheless conventional
 * and does not conflict with the expectations of ERC20 applications.
 *
 * Additionally, an {Approval} event is emitted on calls to {transferFrom}.
 * This allows applications to reconstruct the allowance for all accounts just
 * by listening to said events. Other implementations of the EIP may not emit
 * these events, as it isn't required by the specification.
 *
 * Finally, the non-standard {decreaseAllowance} and {increaseAllowance}
 * functions have been added to mitigate the well-known issues around setting
 * allowances. See {IERC20-approve}.
 */
contract ERC20 is Context, IERC20 {
    using LowGasSafeMath for uint256;

    mapping (address => uint256) private _balances;

    mapping (address => mapping (address => uint256)) private _allowances;

    uint256 private _totalSupply;

    string private _name;
    string private _symbol;
    uint8 private _decimals;

    /**
     * @dev Sets the values for {name} and {symbol}, initializes {decimals} with
     * a default value of 18.
     *
     * To select a different value for {decimals}, use {_setupDecimals}.
     *
     * All three of these values are immutable: they can only be set once during
     * construction.
     */
    constructor (string memory name_, string memory symbol_) {
        _name = name_;
        _symbol = symbol_;
        _decimals = 18;
    }

    /**
     * @dev Returns the name of the token.
     */
    function name() public view virtual returns (string memory) {
        return _name;
    }

    /**
     * @dev Returns the symbol of the token, usually a shorter version of the
     * name.
     */
    function symbol() public view virtual returns (string memory) {
        return _symbol;
    }

    /**
     * @dev Returns the number of decimals used to get its user representation.
     * For example, if `decimals` equals `2`, a balance of `505` tokens should
     * be displayed to a user as `5,05` (`505 / 10 ** 2`).
     *
     * Tokens usually opt for a value of 18, imitating the relationship between
     * Ether and Wei. This is the value {ERC20} uses, unless {_setupDecimals} is
     * called.
     *
     * NOTE: This information is only used for _display_ purposes: it in
     * no way affects any of the arithmetic of the contract, including
     * {IERC20-balanceOf} and {IERC20-transfer}.
     */
    function decimals() public view virtual returns (uint8) {
        return _decimals;
    }

    /**
     * @dev See {IERC20-totalSupply}.
     */
    function totalSupply() public view virtual override returns (uint256) {
        return _totalSupply;
    }

    /**
     * @dev See {IERC20-balanceOf}.
     */
    function balanceOf(address account) public view virtual override returns (uint256) {
        return _balances[account];
    }

    /**
     * @dev See {IERC20-transfer}.
     *
     * Requirements:
     *
     * - `recipient` cannot be the zero address.
     * - the caller must have a balance of at least `amount`.
     */
    function transfer(address recipient, uint256 amount) public virtual override returns (bool) {
