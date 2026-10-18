// Historical Solidity source excerpts, with ORIGINAL source lines; no edits/reconstruction.

// Original: contracts/19/contracts/contracts/token/OUSD.sol lines 194-200
 194 |     function allowance(address _owner, address _spender)
 195 |         public
 196 |         view
 197 |         returns (uint256)
 198 |     {
 199 |         return _allowances[_owner][_spender];
 200 |     }

// Original: contracts/19/contracts/contracts/token/OUSD.sol lines 298-300
 298 |     function burn(address account, uint256 amount) external onlyVault {
 299 |         return _burn(account, amount);
 300 |     }

// Original: contracts/19/contracts/contracts/token/OUSD.sol lines 129-146
 129 |     function transferFrom(
 130 |         address _from,
 131 |         address _to,
 132 |         uint256 _value
 133 |     ) public returns (bool) {
 134 |         require(_to != address(0), "Transfer to zero address");
 135 |         require(_value <= balanceOf(_from), "Transfer greater than balance");
 136 | 
 137 |         _allowances[_from][msg.sender] = _allowances[_from][msg.sender].sub(
 138 |             _value
 139 |         );
 140 | 
 141 |         _executeTransfer(_from, _to, _value);
 142 | 
 143 |         emit Transfer(_from, _to, _value);
 144 | 
 145 |         return true;
 146 |     }

// Original: contracts/19/contracts/contracts/vault/VaultCore.sol lines 158-167
 158 |     function redeem(uint256 _amount, uint256 _minimumUnitAmount)
 159 |         public
 160 |         whenNotCapitalPaused
 161 |         nonReentrant
 162 |     {
 163 |         if (_amount > rebaseThreshold && !rebasePaused) {
 164 |             _rebase();
 165 |         }
 166 |         _redeem(_amount, _minimumUnitAmount);
 167 |     }
