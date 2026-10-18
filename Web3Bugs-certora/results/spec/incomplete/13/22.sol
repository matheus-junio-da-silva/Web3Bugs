// Source: contracts/13/contracts/mocks/certora/AccountPortfolioHarness.sol
// Original lines: 65-97
    }

    function getMaturityAtBitNum(address account, uint256 bitNum) public returns (uint256) {
        AccountContext memory accountContext = symbolicAccountContext;
        return DateTime.getMaturityFromBitNum(accountContext.nextSettleTime, bitNum);
    }

    function getifCashNotional(
        address account,
        uint256 currencyId,
        uint256 maturity
    ) external view returns (int256) {
        return BitmapAssetsHandler.getifCashNotional(account, currencyId, maturity);
    }

    function getCashBalance(address account, uint256 currencyId) public returns (int256) {
        // prettier-ignore
        (int256 cashBalance, /* */, /* */, /* */) = BalanceHandler.getBalanceStorage(account, currencyId);
        return cashBalance;
    }

    function getNTokenBalance(address account, uint256 currencyId) public returns (int256) {
        // prettier-ignore
        (/* */, int256 nTokenBalance, /* */, /* */) = BalanceHandler.getBalanceStorage(account, currencyId);
        return nTokenBalance;
    }

    function getLastClaimTime(address account, uint256 currencyId) public returns (uint256) {
        // prettier-ignore
        (/* */, /* */, uint256 lastClaimTime, /* */) = BalanceHandler.getBalanceStorage(account, currencyId);
        return lastClaimTime;
    }


// Source: contracts/13/contracts/mocks/certora/AccountPortfolioHarness.sol
// Original lines: 70-102
    }

    function getifCashNotional(
        address account,
        uint256 currencyId,
        uint256 maturity
    ) external view returns (int256) {
        return BitmapAssetsHandler.getifCashNotional(account, currencyId, maturity);
    }

    function getCashBalance(address account, uint256 currencyId) public returns (int256) {
        // prettier-ignore
        (int256 cashBalance, /* */, /* */, /* */) = BalanceHandler.getBalanceStorage(account, currencyId);
        return cashBalance;
    }

    function getNTokenBalance(address account, uint256 currencyId) public returns (int256) {
        // prettier-ignore
        (/* */, int256 nTokenBalance, /* */, /* */) = BalanceHandler.getBalanceStorage(account, currencyId);
        return nTokenBalance;
    }

    function getLastClaimTime(address account, uint256 currencyId) public returns (uint256) {
        // prettier-ignore
        (/* */, /* */, uint256 lastClaimTime, /* */) = BalanceHandler.getBalanceStorage(account, currencyId);
        return lastClaimTime;
    }

    function getLastClaimSupply(address account, uint256 currencyId) public returns (uint256) {
        // prettier-ignore
        (/* */, /* */, /* */, uint256 lastClaimSupply) = BalanceHandler.getBalanceStorage(account, currencyId);
        return lastClaimSupply;
    }
