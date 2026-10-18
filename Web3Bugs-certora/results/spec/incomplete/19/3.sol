// Historical Solidity source excerpts, with ORIGINAL source lines; no edits/reconstruction.

// Original: contracts/19/contracts/contracts/token/OUSD.sol lines 73-75
  73 |     function totalSupply() public view returns (uint256) {
  74 |         return _totalSupply;
  75 |     }

// Original: contracts/19/contracts/contracts/token/OUSD.sol lines 472-507
 472 |     function changeSupply(uint256 _newTotalSupply)
 473 |         external
 474 |         onlyVault
 475 |         nonReentrant
 476 |     {
 477 |         require(_totalSupply > 0, "Cannot increase 0 supply");
 478 | 
 479 |         if (_totalSupply == _newTotalSupply) {
 480 |             emit TotalSupplyUpdated(
 481 |                 _totalSupply,
 482 |                 rebasingCredits,
 483 |                 rebasingCreditsPerToken
 484 |             );
 485 |             return;
 486 |         }
 487 | 
 488 |         _totalSupply = _newTotalSupply > MAX_SUPPLY
 489 |             ? MAX_SUPPLY
 490 |             : _newTotalSupply;
 491 | 
 492 |         rebasingCreditsPerToken = rebasingCredits.divPrecisely(
 493 |             _totalSupply.sub(nonRebasingSupply)
 494 |         );
 495 | 
 496 |         require(rebasingCreditsPerToken > 0, "Invalid change in supply");
 497 | 
 498 |         _totalSupply = rebasingCredits
 499 |             .divPrecisely(rebasingCreditsPerToken)
 500 |             .add(nonRebasingSupply);
 501 | 
 502 |         emit TotalSupplyUpdated(
 503 |             _totalSupply,
 504 |             rebasingCredits,
 505 |             rebasingCreditsPerToken
 506 |         );
 507 |     }

// Original: contracts/19/contracts/contracts/token/OUSD.sol lines 37-40
  37 |     enum RebaseOptions { NotSet, OptOut, OptIn }
  38 | 
  39 |     uint256 private constant MAX_SUPPLY = ~uint128(0); // (2^128) - 1
  40 |     uint256 public _totalSupply;

// Original: contracts/19/spec/harnesses/OUSDHarness.sol lines 5-5
   5 | 	function Certora_maxSupply() external view returns (uint) { return MAX_SUPPLY; }
