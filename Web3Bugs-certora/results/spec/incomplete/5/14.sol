// Relevant excerpts for alwaysUnSent.
// Target Contract: BridgeHarness
// NOTE: BridgeHarness was the historical verification target but is absent from the supplied snapshot; excerpts below are available production-code context and may be from a later source revision.

// Source: contracts/5/contracts/l1/Bridge.sol
// Original lines: 143-161

    function withdraw(
        address l1AToken,
        uint256 l2sender,
        address recipient,
        uint256 staticAmount,
        uint256 l2RewardsIndex,
        bool toUnderlyingAsset
    ) external override {
        require(recipient != address(0), Errors.B_INVALID_ADDRESS);
        require(staticAmount > 0, Errors.B_INSUFFICIENT_AMOUNT);

        _consumeMessage(
            l1AToken,
            l2sender,
            recipient,
            staticAmount,
            l2RewardsIndex,
            toUnderlyingAsset ? 1 : 0
        );

// Source: contracts/5/contracts/l1/Bridge.sol
// Original lines: 222-233

    function receiveRewards(
        uint256 l2sender,
        address recipient,
        uint256 amount
    ) external override {
        require(recipient != address(0), Errors.B_INVALID_ADDRESS);
        require(amount > 0, Errors.B_INSUFFICIENT_AMOUNT);
        //check if enough rewards are available on the bridge before consuming the message from l2
        require(getAvailableRewards() >= amount, Errors.B_NOT_ENOUGH_REWARDS);
        _consumeBridgeRewardMessage(l2sender, recipient, amount);
        _transferRewards(recipient, amount);
        emit RewardsTransferred(l2sender, recipient, amount);
