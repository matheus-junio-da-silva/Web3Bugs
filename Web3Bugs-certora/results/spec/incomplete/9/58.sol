// Original: contracts/9/contracts/governance/LockedGold.sol:18-42 (locked-gold state)
contract LockedGold is
  ILockedGold,
  ICeloVersionedContract,
  ReentrancyGuard,
  Initializable,
  UsingRegistry
{
  using SafeMath for uint256;
  using Address for address payable; // prettier-ignore
  using FixidityLib for FixidityLib.Fraction;
  using EnumerableSet for EnumerableSet.AddressSet;

  struct PendingWithdrawal {
    // The value of the pending withdrawal.
    uint256 value;
    // The timestamp at which the pending withdrawal becomes available.
    uint256 timestamp;
  }

  // NOTE: This contract does not store an account's locked gold that is being used in electing
  // validators.
  struct Balances {
    // The amount of locked gold that this account has that is not currently participating in
    // validator elections.
    uint256 nonvoting;
