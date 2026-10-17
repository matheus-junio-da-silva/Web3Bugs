// Original: contracts/7/contracts/protocol/tokenization/StableDebtToken.sol, lines 365-367
function transfer(address, uint256) external virtual override returns (bool) {
    revert(Errors.OPERATION_NOT_SUPPORTED);
  }

// Original: contracts/7/contracts/protocol/tokenization/StableDebtToken.sol, lines 369-371
function allowance(address, address) external view virtual override returns (uint256) {
    revert(Errors.OPERATION_NOT_SUPPORTED);
  }

// Original: contracts/7/contracts/protocol/tokenization/StableDebtToken.sol, lines 373-375
function approve(address, uint256) external virtual override returns (bool) {
    revert(Errors.OPERATION_NOT_SUPPORTED);
  }

// Original: contracts/7/contracts/protocol/tokenization/StableDebtToken.sol, lines 377-379
function transferFrom(address, address, uint256) external virtual override returns (bool) {
    revert(Errors.OPERATION_NOT_SUPPORTED);
  }

// Original: contracts/7/contracts/protocol/tokenization/StableDebtToken.sol, lines 381-383
function increaseAllowance(address, uint256) external virtual override returns (bool) {
    revert(Errors.OPERATION_NOT_SUPPORTED);
  }

// Original: contracts/7/contracts/protocol/tokenization/StableDebtToken.sol, lines 385-387
function decreaseAllowance(address, uint256) external virtual override returns (bool) {
    revert(Errors.OPERATION_NOT_SUPPORTED);
  }
