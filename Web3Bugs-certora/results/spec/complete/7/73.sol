// Original: contracts/7/contracts/protocol/tokenization/VariableDebtToken.sol, lines 127-129
function transfer(address, uint256) external virtual override returns (bool) {
    revert(Errors.OPERATION_NOT_SUPPORTED);
  }

// Original: contracts/7/contracts/protocol/tokenization/VariableDebtToken.sol, lines 131-133
function allowance(address, address) external view virtual override returns (uint256) {
    revert(Errors.OPERATION_NOT_SUPPORTED);
  }

// Original: contracts/7/contracts/protocol/tokenization/VariableDebtToken.sol, lines 135-137
function approve(address, uint256) external virtual override returns (bool) {
    revert(Errors.OPERATION_NOT_SUPPORTED);
  }

// Original: contracts/7/contracts/protocol/tokenization/VariableDebtToken.sol, lines 139-141
function transferFrom(address, address, uint256) external virtual override returns (bool) {
    revert(Errors.OPERATION_NOT_SUPPORTED);
  }

// Original: contracts/7/contracts/protocol/tokenization/VariableDebtToken.sol, lines 143-145
function increaseAllowance(address, uint256) external virtual override returns (bool) {
    revert(Errors.OPERATION_NOT_SUPPORTED);
  }

// Original: contracts/7/contracts/protocol/tokenization/VariableDebtToken.sol, lines 147-149
function decreaseAllowance(address, uint256) external virtual override returns (bool) {
    revert(Errors.OPERATION_NOT_SUPPORTED);
  }
