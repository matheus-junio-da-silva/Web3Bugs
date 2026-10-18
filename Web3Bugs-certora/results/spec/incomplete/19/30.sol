// Historical Solidity source excerpts, with ORIGINAL source lines; no edits/reconstruction.

// Original: contracts/19/contracts/contracts/token/OUSD.sol lines 83-87
  83 |     function balanceOf(address _account) public view returns (uint256) {
  84 |         if (_creditBalances[_account] == 0) return 0;
  85 |         return
  86 |             _creditBalances[_account].divPrecisely(_creditsPerToken(_account));
  87 |     }

// Original: contracts/19/contracts/contracts/token/OUSD.sol lines 109-121
 109 |     function transfer(address _to, uint256 _value) public returns (bool) {
 110 |         require(_to != address(0), "Transfer to zero address");
 111 |         require(
 112 |             _value <= balanceOf(msg.sender),
 113 |             "Transfer greater than balance"
 114 |         );
 115 | 
 116 |         _executeTransfer(msg.sender, _to, _value);
 117 | 
 118 |         emit Transfer(msg.sender, _to, _value);
 119 | 
 120 |         return true;
 121 |     }
