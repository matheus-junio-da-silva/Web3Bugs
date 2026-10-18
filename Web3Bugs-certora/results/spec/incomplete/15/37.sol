// Original Solidity: contracts/15/gho/GhoToken.sol lines 13-13; contract/state context
contract GhoToken is ERC20, AccessControl, IGhoToken {

// Original Solidity: contracts/15/gho/GhoToken.sol lines 16-16; contract/state context
  mapping(address => Facilitator) internal _facilitators;

// Original Solidity: contracts/15/gho/ERC20.sol lines 27-27; storage
  uint256 public totalSupply;
