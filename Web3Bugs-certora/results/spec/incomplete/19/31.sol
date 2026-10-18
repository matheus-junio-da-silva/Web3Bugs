// Historical Solidity source excerpts, with ORIGINAL source lines; no edits/reconstruction.

// Original: contracts/19/contracts/contracts/token/OUSD.sol lines 83-87
  83 |     function balanceOf(address _account) public view returns (uint256) {
  84 |         if (_creditBalances[_account] == 0) return 0;
  85 |         return
  86 |             _creditBalances[_account].divPrecisely(_creditsPerToken(_account));
  87 |     }

// Original: contracts/19/contracts/contracts/token/OUSD.sol lines 154-186
 154 |     function _executeTransfer(
 155 |         address _from,
 156 |         address _to,
 157 |         uint256 _value
 158 |     ) internal {
 159 |         bool isNonRebasingTo = _isNonRebasingAccount(_to);
 160 |         bool isNonRebasingFrom = _isNonRebasingAccount(_from);
 161 | 
 162 |         // Credits deducted and credited might be different due to the
 163 |         // differing creditsPerToken used by each account
 164 |         uint256 creditsCredited = _value.mulTruncate(_creditsPerToken(_to));
 165 |         uint256 creditsDeducted = _value.mulTruncate(_creditsPerToken(_from));
 166 | 
 167 |         _creditBalances[_from] = _creditBalances[_from].sub(
 168 |             creditsDeducted,
 169 |             "Transfer amount exceeds balance"
 170 |         );
 171 |         _creditBalances[_to] = _creditBalances[_to].add(creditsCredited);
 172 | 
 173 |         if (isNonRebasingTo && !isNonRebasingFrom) {
 174 |             // Transfer to non-rebasing account from rebasing account, credits
 175 |             // are removed from the non rebasing tally
 176 |             nonRebasingSupply = nonRebasingSupply.add(_value);
 177 |             // Update rebasingCredits by subtracting the deducted amount
 178 |             rebasingCredits = rebasingCredits.sub(creditsDeducted);
 179 |         } else if (!isNonRebasingTo && isNonRebasingFrom) {
 180 |             // Transfer to rebasing account from non-rebasing account
 181 |             // Decreasing non-rebasing credits by the amount that was sent
 182 |             nonRebasingSupply = nonRebasingSupply.sub(_value);
 183 |             // Update rebasingCredits by adding the credited amount
 184 |             rebasingCredits = rebasingCredits.add(creditsCredited);
 185 |         }
 186 |     }
