// Source: PropertyGPT/certora_projects/compound_moneymarket/spec/formal/borrowAndRepayFresh.cvl
// Rule borrowFresh original lines 20-122; SHA256 a218723ac40a0a4dbe0946e48dc8bad20e13ca3bda40e66f5b1a71286b91ae4a
// Original legacy Specify/CVL syntax; not migrated to CVL2.
methods {
    totalSupply() returns uint256
    totalBorrows() returns uint256
    totalReserves() returns uint256
    balanceOf(address) returns uint256
    borrowBalanceStored(address) returns uint256
    exchangeRateStored() returns uint256
    getCash() returns uint256
    getCashOf(address) returns uint256 // not part of API
    borrowFreshPub(address, uint256) returns uint256
}

borrowFresh(uint result, address borrower, uint256 borrowAmount)
description "Break borrow with result=$result borrower=$borrower borrowAmount=$borrowAmount" {
    // Pre/action/post environments
    env e0; havoc e0;
    env e1; havoc e1;
    env e2; havoc e2;

    static_require e1.block.number >= e0.block.number;
    static_require e2.block.number >= e1.block.number;

    // Any other account
    address other; havoc other;
    static_require other != borrower && other != currentContract;

    /*
      - exchange rate should not change
      - errors should have no effect
      - no *other* storage should change - XXX can we specify this?

      |----------+--------+----------+-------|
      |          | CToken | Borrower | Other |
      |----------+--------+----------+-------|
      | cash     |   -A   |    +A    |   0   |
      | borrows  |   +A   |    +A    |   0   |
      | tokens   |    0   |     0    |   0   |
      | reserves |    0   |          |       |
      |----------+--------+----------+-------|
    */

    /* Pre */

    uint256 exchangeRatePre = sinvoke exchangeRateStored(e0);

    uint256 cTokenCashPre = sinvoke getCash(e0);
    uint256 borrowerCashPre = sinvoke getCashOf(e0, borrower);
    uint256 otherCashPre = sinvoke getCashOf(e0, other);

    uint256 cTokenBorrowsPre = sinvoke totalBorrows(e0);
    uint256 borrowerBorrowsPre = sinvoke borrowBalanceStored(e0, borrower);
    uint256 otherBorrowsPre = sinvoke borrowBalanceStored(e0, other);

    uint256 cTokenTokensPre = sinvoke totalSupply(e0);
    uint256 borrowerTokensPre = sinvoke balanceOf(e0, borrower);
    uint256 otherTokensPre = sinvoke balanceOf(e0, other);

    uint256 cTokenReservesPre = sinvoke totalReserves(e0);

    // Just Do It
    static_require result == invoke borrowFreshPub(e1, borrower, borrowAmount);
    bool borrowFreshReverted = lastReverted;

    /* Post */

    uint256 exchangeRatePost = sinvoke exchangeRateStored(e2);

    uint256 cTokenCashPost = sinvoke getCash(e2);
    uint256 borrowerCashPost = sinvoke getCashOf(e2, borrower);
    uint256 otherCashPost = sinvoke getCashOf(e2, other);

    uint256 cTokenBorrowsPost = sinvoke totalBorrows(e2);
    uint256 borrowerBorrowsPost = sinvoke borrowBalanceStored(e2, borrower);
    uint256 otherBorrowsPost = sinvoke borrowBalanceStored(e2, other);

    uint256 cTokenTokensPost = sinvoke totalSupply(e2);
    uint256 borrowerTokensPost = sinvoke balanceOf(e2, borrower);
    uint256 otherTokensPost = sinvoke balanceOf(e2, other);

    uint256 cTokenReservesPost = sinvoke totalReserves(e2);

    // Measure
    bool staticBalance =
        (exchangeRatePost == exchangeRatePre) &&
        (cTokenCashPost == cTokenCashPre) &&
        (cTokenBorrowsPost == cTokenBorrowsPre) &&
        (cTokenTokensPost == cTokenTokensPre) &&
        (cTokenReservesPost == cTokenReservesPre) &&
        (borrowerCashPost == borrowerCashPre) &&
        (borrowerBorrowsPost == borrowerBorrowsPre) &&
        (borrowerTokensPost == borrowerTokensPre) &&
        (otherCashPost == otherCashPre) &&
        (otherBorrowsPost == otherBorrowsPre) &&
        (otherTokensPost == otherTokensPre);

    bool dynamicBalance =
        (borrowAmount != 0) &&
        (exchangeRatePost == exchangeRatePre) &&
        (cTokenCashPost == cTokenCashPre - borrowAmount) &&
        (cTokenBorrowsPost == cTokenBorrowsPre + borrowAmount) &&
        (cTokenTokensPost == cTokenTokensPre) &&
        (cTokenReservesPost == cTokenReservesPre) &&
        (borrowerCashPost == borrowerCashPre + borrowAmount) &&
        (borrowerBorrowsPost == borrowerBorrowsPre + borrowAmount) &&
        (borrowerTokensPost == borrowerTokensPre) &&
        (otherCashPost == otherCashPre) &&
        (otherBorrowsPost == otherBorrowsPre) &&
        (otherTokensPost == otherTokensPre);

    // XXX would be nice to pull named enums from actual contract?
    static_assert (!borrowFreshReverted =>
                   ((result != 0 || borrowAmount == 0) <=> staticBalance)), "Mismatch in static case";
    static_assert (!borrowFreshReverted =>
                   ((result == 0 && borrowAmount != 0 && borrower != currentContract) <=> dynamicBalance)), "Mismatch in dynamic case";
}
