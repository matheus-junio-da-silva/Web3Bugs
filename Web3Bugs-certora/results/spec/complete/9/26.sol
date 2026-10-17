// Original: contracts/9/contracts/common/Accounts.sol:1-24 (concrete target inheritance and Ownable import)
pragma solidity ^0.5.13;

import "openzeppelin-solidity/contracts/math/SafeMath.sol";
import "openzeppelin-solidity/contracts/ownership/Ownable.sol";

import "./interfaces/IAccounts.sol";

import "../common/FixidityLib.sol";
import "../common/Initializable.sol";
import "../common/interfaces/ICeloVersionedContract.sol";
import "../common/Signatures.sol";
import "../common/UsingRegistry.sol";
import "../common/libraries/ReentrancyGuard.sol";

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
