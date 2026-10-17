// Original: contracts/7/contracts/protocol/tokenization/base/DebtTokenBase.sol, lines 43-68
function delegationWithSig(
    address delegator,
    address delegatee,
    uint256 value,
    uint256 deadline,
    uint8 v,
    bytes32 r,
    bytes32 s
  ) external {
    require(delegator != address(0), Errors.ZERO_ADDRESS_NOT_VALID);
    //solium-disable-next-line
    require(block.timestamp <= deadline, Errors.INVALID_EXPIRATION);
    uint256 currentValidNonce = _nonces[delegator];
    bytes32 digest = keccak256(
      abi.encodePacked(
        '\x19\x01',
        DOMAIN_SEPARATOR(),
        keccak256(
          abi.encode(DELEGATION_WITH_SIG_TYPEHASH, delegatee, value, currentValidNonce, deadline)
        )
      )
    );
    require(delegator == ecrecover(digest, v, r, s), Errors.INVALID_SIGNATURE);
    _nonces[delegator] = currentValidNonce + 1;
    _approveDelegation(delegator, delegatee, value);
  }

// Original: contracts/7/contracts/protocol/tokenization/base/DebtTokenBase.sol, lines 71-76
function borrowAllowance(
    address fromUser,
    address toUser
  ) external view override returns (uint256) {
    return _borrowAllowances[fromUser][toUser];
  }
