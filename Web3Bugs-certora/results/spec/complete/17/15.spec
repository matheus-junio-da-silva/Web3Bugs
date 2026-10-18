// Source: PropertyGPT/certora_projects/compound_moneymarket/spec/formal/liquidateFresh.cvl
// Rule seize original lines 221-331; SHA256 afcb80710e40995c98a14279a847b9e0215bfaeac47f82c9410dc252816a32ee
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
    seize(address, address, uint256) returns uint256
}

seize(uint result, address liquidator, address borrower, uint256 seizeTokens)
description "Break seize" {
    // Pre/action/post environments
    env e0; havoc e0;
    env e1; havoc e1;
    env e2; havoc e2;

    static_require e1.block.number >= e0.block.number;
    static_require e2.block.number >= e1.block.number;

    // Any other account
    address other; havoc other;
    static_require other != liquidator && other != borrower && other != currentContract;

    /*
      - no effect on exchange rate
      |----------+--------+------------+----------+-------|
      |          | CToken | Liquidator | Borrower | Other |
      |----------+--------+------------+----------+-------|
      | cash     |    0   |      0     |     0    |   0   |
      | borrows  |    0   |      0     |     0    |   0   |
      | tokens   |    0   |     +T     |    -T    |   0   |
      | reserves |    0   |            |          |       |
      |----------+--------+------------+----------+-------|
    */

    /* Pre */

    uint256 exchangeRatePre = sinvoke exchangeRateStored(e0);

    uint256 cTokenCashPre = sinvoke getCash(e0);
    uint256 liquidatorCashPre = sinvoke getCashOf(e0, liquidator);
    uint256 borrowerCashPre = sinvoke getCashOf(e0, borrower);
    uint256 otherCashPre = sinvoke getCashOf(e0, other);

    uint256 cTokenBorrowsPre = sinvoke totalBorrows(e0);
    uint256 liquidatorBorrowsPre = sinvoke borrowBalanceStored(e0, liquidator);
    uint256 borrowerBorrowsPre = sinvoke borrowBalanceStored(e0, borrower);
    uint256 otherBorrowsPre = sinvoke borrowBalanceStored(e0, other);

    uint256 cTokenTokensPre = sinvoke totalSupply(e0);
    uint256 liquidatorTokensPre = sinvoke balanceOf(e0, liquidator);
    uint256 borrowerTokensPre = sinvoke balanceOf(e0, borrower);
    uint256 otherTokensPre = sinvoke balanceOf(e0, other);

    uint256 cTokenReservesPre = sinvoke totalReserves(e0);

    // Just Do It
    static_require result == invoke seize(e1, liquidator, borrower, seizeTokens);
    bool seizeReverted = lastReverted;

    /* Post */

    uint256 exchangeRatePost = sinvoke exchangeRateStored(e2);

    uint256 cTokenCashPost = sinvoke getCash(e2);
    uint256 liquidatorCashPost = sinvoke getCashOf(e2, liquidator);
    uint256 borrowerCashPost = sinvoke getCashOf(e2, borrower);
    uint256 otherCashPost = sinvoke getCashOf(e2, other);

    uint256 cTokenBorrowsPost = sinvoke totalBorrows(e2);
    uint256 liquidatorBorrowsPost = sinvoke borrowBalanceStored(e2, liquidator);
    uint256 borrowerBorrowsPost = sinvoke borrowBalanceStored(e2, borrower);
    uint256 otherBorrowsPost = sinvoke borrowBalanceStored(e2, other);

    uint256 cTokenTokensPost = sinvoke totalSupply(e2);
    uint256 liquidatorTokensPost = sinvoke balanceOf(e2, liquidator);
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
        (liquidatorCashPost == liquidatorCashPre) &&
        (liquidatorBorrowsPost == liquidatorBorrowsPre) &&
        (liquidatorTokensPost == liquidatorTokensPre) &&
        (borrowerCashPost == borrowerCashPre) &&
        (borrowerBorrowsPost == borrowerBorrowsPre) &&
        (borrowerTokensPost == borrowerTokensPre) &&
        (otherCashPost == otherCashPre) &&
        (otherBorrowsPost == otherBorrowsPre) &&
        (otherTokensPost == otherTokensPre);

    bool dynamicBalance =
        (seizeTokens != 0) &&
        (exchangeRatePost == exchangeRatePre) &&
        (cTokenCashPost == cTokenCashPre) &&
        (cTokenBorrowsPost == cTokenBorrowsPre) &&
        (cTokenTokensPost == cTokenTokensPre) &&
        (cTokenReservesPost == cTokenReservesPre) &&
        (liquidatorCashPost == liquidatorCashPre) &&
        (liquidatorBorrowsPost == liquidatorBorrowsPre) &&
        (liquidatorTokensPost == liquidatorTokensPre + seizeTokens) &&
        (borrowerCashPost == borrowerCashPre) &&
        (borrowerBorrowsPost == borrowerBorrowsPre) &&
        (borrowerTokensPost == borrowerTokensPre - seizeTokens) &&
        (otherCashPost == otherCashPre) &&
        (otherBorrowsPost == otherBorrowsPre) &&
        (otherTokensPost == otherTokensPre);

    static_assert (!seizeReverted =>
                   ((result != 0 || seizeTokens == 0 || liquidator == borrower) <=> staticBalance)), "Mismatch in static case";
    static_assert (!seizeReverted =>
                   ((result == 0 && seizeTokens != 0) <=> dynamicBalance)), "Mismatch in dynamic case";
}