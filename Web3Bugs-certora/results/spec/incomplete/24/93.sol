// Historical LaunchEvent Solidity implementation excerpts — contracts/24/contracts/LaunchEvent.sol
// State line 90
    bool public stopped;
// State line 97
    IJoePair public pair;
// State line 129
    uint256 private avaxReserve;
// Function depositAVAX lines 333-387
    function depositAVAX()
        external
        payable
        isStopped(false)
        atPhase(Phase.PhaseOne)
    {
        require(msg.sender != issuer, "LaunchEvent: issuer cannot participate");
        require(
            msg.value > 0,
            "LaunchEvent: expected non-zero AVAX to deposit"
        );

        UserInfo storage user = getUserInfo[msg.sender];
        uint256 newAllocation = user.balance + msg.value;
        require(
            newAllocation <= maxAllocation,
            "LaunchEvent: amount exceeds max allocation"
        );

        uint256 rJoeNeeded;
        // check if additional allocation is required.
        if (newAllocation > user.allocation) {
            // Get amount of rJOE tokens needed to burn and update allocation
            rJoeNeeded = getRJoeAmount(newAllocation - user.allocation);
            // Set allocation to the current balance as it's impossible
            // to buy more allocation without sending AVAX too
            user.allocation = newAllocation;
        }

        user.balance = newAllocation;
        avaxReserve += msg.value;

        if (rJoeNeeded > 0) {
            rJoe.burnFrom(msg.sender, rJoeNeeded);
        }

        emit UserParticipated(msg.sender, msg.value, rJoeNeeded);
    }

    /// @notice Withdraw AVAX, only permitted during phase 1 and 2
    /// @param _amount The amount of AVAX to withdraw
    function withdrawAVAX(uint256 _amount) external isStopped(false) {
        Phase _currentPhase = currentPhase();
        require(
            _currentPhase == Phase.PhaseOne || _currentPhase == Phase.PhaseTwo,
            "LaunchEvent: unable to withdraw"
        );
        require(_amount > 0, "LaunchEvent: invalid withdraw amount");
        UserInfo storage user = getUserInfo[msg.sender];
        require(
            user.balance >= _amount,
            "LaunchEvent: withdrawn amount exceeds balance"
        );
        user.balance -= _amount;

