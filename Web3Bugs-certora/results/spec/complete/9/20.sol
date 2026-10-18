// Original: contracts/9/contracts/common/Accounts.sol:15-29 (relevant state)
contract Accounts is
  IAccounts,
  ICeloVersionedContract,
  Ownable,
  ReentrancyGuard,
  Initializable,
  UsingRegistry
{
  using FixidityLib for FixidityLib.Fraction;
  using SafeMath for uint256;

  struct Signers {
    // The address that is authorized to vote in governance and validator elections on behalf of the
    // account. The account can vote as well, whether or not a vote signing key has been specified.
    address vote;
