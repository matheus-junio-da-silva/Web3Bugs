// Project 23 exact historical source: Splits.spec
// Property correctnessOfHashSplits original lines 118-133 SHA256 fd33e4dfbd9de0475563058b315372ba994e148effe8b878eaf4b58ad6927f84
//// ## Verification of Splits.sol
//// 
//// `Splits.sol` is part of the Drips protocol
//// 
//// The splits functionality, as explained in DripsHub.sol by the developers:
//// The user can share collected funds with other users by using splits.
//// When collecting, the user gives each of their splits receivers a fraction of the received funds.
//// Funds received from splits are available for collection immediately regardless of the cycle.
//// They aren't exempt from being split, so they too can be split when collected.
//// Users can build chains and networks of splits between each other.
//// Anybody can request collection of funds for any user,
//// which can be used to enforce the flow of funds in the network of splits.
//// 
//// ### Assumptions and Simplifications
//// - All the internal methods are wrapped in CVT callable versions
//// - Dummy functions used to control the SplitsReceiver[] receivers
//// - When testing the split weight functionality we safely assumed weight < _TOTAL_SPLITS_WEIGHT
////   since the method _assertSplitsValid() validates them before assignment
//// 
//// ### Properties


/// @notice Calculate results of splitting an amount using the current splits configuration.
/// We verify that amount == collectableAmt + splitAmt
/// Since compiling with Solidity >0.8.0 there are no overflows

rule correctnessOfHashSplits() {
    env e; uint256 index; uint256 length1; uint256 length2;  
    uint256 userId1; uint32 weight1; uint256 userId2; uint32 weight2;
    bytes32 receiversHash1; bytes32 receiversHash2;

    length1 = getCurrSplitsReceiverLocaLength(e, true);
    length2 = getCurrSplitsReceiverLocaLength(e, false);

    userId1, weight1 = getCurrSplitsReceiverLocalArr(e, true, index);
    userId2, weight2 = getCurrSplitsReceiverLocalArr(e, false, index);

    receiversHash1 = hashSplits(e, true);
    receiversHash2 = hashSplits(e, false);

    assert (receiversHash1 == receiversHash2) => ((length1 == length2) && (userId1 == userId2) && (weight1 == weight2));
}
