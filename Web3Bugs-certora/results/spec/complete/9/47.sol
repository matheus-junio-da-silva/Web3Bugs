// Original: contracts/9/contracts/governance/Governance.sol:1-37 (concrete target inheritance and Ownable import)
pragma solidity ^0.5.13;

import "openzeppelin-solidity/contracts/ownership/Ownable.sol";
import "openzeppelin-solidity/contracts/math/Math.sol";
import "openzeppelin-solidity/contracts/math/SafeMath.sol";
import "openzeppelin-solidity/contracts/utils/Address.sol";

import "./interfaces/IGovernance.sol";
import "./Proposals.sol";
import "../common/interfaces/IAccounts.sol";
import "../common/ExtractFunctionSignature.sol";
import "../common/Initializable.sol";
import "../common/FixidityLib.sol";
import "../common/linkedlists/IntegerSortedLinkedList.sol";
import "../common/UsingRegistry.sol";
import "../common/UsingPrecompiles.sol";
import "../common/interfaces/ICeloVersionedContract.sol";
import "../common/libraries/ReentrancyGuard.sol";

/**
 * @title A contract for making, passing, and executing on-chain governance proposals.
 */
contract Governance is
  IGovernance,
  ICeloVersionedContract,
  Ownable,
  Initializable,
  ReentrancyGuard,
  UsingRegistry,
  UsingPrecompiles
{
  using Proposals for Proposals.Proposal;
  using FixidityLib for FixidityLib.Fraction;
  using SafeMath for uint256;
  using IntegerSortedLinkedList for SortedLinkedList.List;
  using BytesLib for bytes;
  using Address for address payable; // prettier-ignore
