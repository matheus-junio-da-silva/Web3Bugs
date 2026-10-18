// Original: contracts/9/specs/harnesses/ReserveHarness.sol:12-16 (getExchangeAddress)
  function getExchangeAddress() public view returns (address) {
    return address(getExchange());
  }
}


// Original: contracts/9/specs/harnesses/ReserveHarness.sol:8-16 (contractBalance)
  function contractBalance() public view returns (uint256) {
    return address(this).balance;
  }

  function getExchangeAddress() public view returns (address) {
    return address(getExchange());
  }
}
