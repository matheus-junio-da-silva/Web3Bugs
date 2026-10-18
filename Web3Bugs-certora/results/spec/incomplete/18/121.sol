// ORIGINAL HISTORICAL SOLIDITY excerpts; content copied literally from contracts/18
// CVL property: GovernorCountingSimple.spec:207-217 privilegedOnlyTimelock

// Original: contracts/18/contracts/governance/extensions/GovernorTimelockControl.sol lines 75-77 function/modifier timelock
    function timelock() public view virtual override returns (address) {
        return address(_timelock);
    }
