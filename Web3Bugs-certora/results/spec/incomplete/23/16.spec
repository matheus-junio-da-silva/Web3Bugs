// Project 23 exact historical source: DripsHubBackup.spec
// Property singleUserTimeUpdateNotChangingOtherUserBalance original lines 392-490 SHA256 386008c4de53d417a81ffd9eba2d2dae15187fabce37947d2b485de383a1fcc2
// This is a backup that works with UpdateReceiverStatesHarness.sol
/*
    This is a specification file for smart contract
    verification with the Certora prover.

    For more information,
    visit: https://www.certora.com/

    This file is run with scripts/...
*/




/**************************************************
 *                LINKED CONTRACTS                *
 **************************************************/
// Declaration of contracts used in the spec

using Reserve as reserve
using ERC20 as IERC20
using UpdateReceiverStatesHarness as DH  // if using with UpdateReceiverStatesHarness.sol
//using DripsHubHarness as DH  // if using with DripsHubHarness.sol

//using DripsConfigImpl for DripsConfig global;
//using DripsConfigImpl as DCI
// using UUPSUpgradeable as UUPSUpgradeable

/*
struct SplitsReceiver {
    /// @notice The user ID.
    uint256 userId;
    /// @notice The splits weight. Must never be zero.
    /// The user will be getting `weight / _TOTAL_SPLITS_WEIGHT`
    /// share of the funds collected by the splitting user.
    uint32 weight;
}
*/

/**************************************************
 *              METHODS DECLARATIONS              *
 **************************************************/
methods {
    // Harness method getters:
    //getMaxDripsReceivers() returns (uint8) envfree
    //getAmtPerSec() returns (uint192) envfree
    getCycleSecs() returns (uint32) envfree
    //_dripsState(uint256, uint256) envfree
    
    // Summarizing external functions:

    // ./src/Drips.sol
    // summarizing with NONDET to resolve timeout of setDrips()

        // _dripsStorage is view only, doesn't change state

        // _hashDrips only does hashing
        /*
        _hashDrips(DripsReceiver[] memory receivers) */
        //////////_hashDrips((uint256, uint256)[] receivers) => NONDET

        // _balanceAt is view only but iterates over the other _balanceAt
        /*
        _balanceAt(
            uint256 userId,
            uint256 assetId,
            DripsReceiver[] memory receivers,
            uint32 timestamp
        ) */
        /*
        _balanceAt(
            uint256 userId,
            uint256 assetId,
            (uint256, uint256)[] receivers,
            uint32 timestamp
        ) => NONDET */

        /*
        _balanceAt(
            uint128 lastBalance,
            uint32 lastUpdate,
            uint32 maxEnd,
            DripsReceiver[] memory receivers,
            uint32 timestamp
        ) */
        /*
        _balanceAt(
            uint128 lastBalance,
            uint32 lastUpdate,
            uint32 maxEnd,
            (uint256, uint256)[] receivers,
            uint32 timestamp
        ) => NONDET */

        // _calcMaxEnd
        /*
        _calcMaxEnd(uint128 balance, DripsReceiver[] memory receivers) */
        //////////_calcMaxEnd(uint128 balance, (uint256, uint256)[] receivers) => NONDET

        // _updateReceiverStates
        /*
        _updateReceiverStates(
            mapping(uint256 => DripsState) storage states,
            DripsReceiver[] memory currReceivers,
            uint32 lastUpdate,
            uint32 currMaxEnd,
            DripsReceiver[] memory newReceivers,
            uint32 newMaxEnd
        ) => NONDET */

        /********** the below is NOT working well
        // when commenting out all the _updateReceiverStates() function -> no timeout!
        _updateReceiverStates(
            // mapping(uint256 => (bytes32, mapping(uint256 => uint32), bytes32, uint32, uint32, uint32, uint128, mapping(uint32 => (int128, int128)))) states,
            (uint256) states, // probably written wrong! to check how mapping translates to abi
            (uint256, uint256)[] currReceivers,
            uint32 lastUpdate,
            uint32 currMaxEnd,
            (uint256, uint256)[] newReceivers,
            uint32 newMaxEnd
        )
        **********/

        /*
        struct DripsState {
        bytes32 dripsHistoryHash;
        mapping(uint256 => uint32) nextSqueezed;
        bytes32 dripsHash;
        uint32 nextReceivableCycle;
        uint32 updateTime;
        uint32 maxEnd;
        uint128 balance;
        mapping(uint32 => AmtDelta) amtDeltas;
        }

        struct AmtDelta {
        int128 thisCycle;
        int128 nextCycle;
        }
        */

        // _currTimestamp is view only, doesn't change state, return current timestamp

        // _hashDripsHistory - is view only, doesn't change state, calculates keccak256
        /*
        _hashDripsHistory(
            bytes32 oldDripsHistoryHash,
            bytes32 dripsHash,
            uint32 updateTime,
            uint32 maxEnd
        ) returns (bytes32 dripsHistoryHash) => NONDET */

        // _drippedAmt
        /*
        _drippedAmt(
            uint256 amtPerSec,
            uint256 start,
            uint256 end
        ) returns (uint256 amt) => NONDET */
    



    /*
    // lib/openzeppelin-contracts/contracts/mocks/UUPS/UUPSLegacy.sol
    upgradeTo(address) => NONDET
    upgradeToAndCall(address, bytes) => NONDET
    */

    // lib/openzeppelin-contracts/contracts/proxy/utils/UUPSUpgradeable.sol
    proxiableUUID() returns (bytes32) => CONSTANT
    upgradeToAndCall(address, bytes) => NONDET
    /*
    upgradeTo(address newImplementation) => NONDET
    upgradeToAndCall(address newImplementation, bytes data) => NONDET

    _upgradeToAndCallUUPS(
        address newImplementation,
        bytes data,
        bool forceCall
    ) => NONDET
    */

    /*
    // lib/openzeppelin-contracts/contracts/utils/Address.sol
    functionDelegateCall(
        address target,
        bytes data,
        string errorMessage
    ) returns (bytes memory) => NONDET
    */

    // src/Reserve.sol -> IReserve
    withdraw(
        address token,
        address to,
        uint256 amt
    ) => DISPATCHER(true);

    deposit(
        address token,
        address from,
        uint256 amt
    ) => DISPATCHER(true);

    transfer(
        address to,
        uint256 amount
    ) returns (bool) => DISPATCHER(true);
    
    transferFrom(
        address from,
        address to,
        uint256 amount
    ) returns (bool) => DISPATCHER(true);


    // src/Reserve.sol -> IReservePlugin
    afterStart(address token, uint256 amt) => NONDET
    afterDeposition(address token, uint256 amt) => NONDET
    beforeWithdrawal(address token, uint256 amt) => NONDET
    beforeEnd(address token, uint256 amt) => NONDET

}




/**************************************************
 *                GHOSTS AND HOOKS                *
 **************************************************/




/**************************************************
 *               CVL FUNCS & DEFS                 *
 **************************************************/

function getReserveContract() returns address {
    return reserve;
}

/**************************************************
 *                 VALID STATES                   *
 **************************************************/
// Describe expressions over the system's variables
// that should always hold.
// Usually implemented via invariants 

/*
// Validity of amount of receivers
// Number of a sender’s drip receivers little equal to MAX_DRIPS_RECEIVERS
invariant isValidAmountOfReceivers()  // NOT FINISHED!
    // currReceivers.length <= maxSplitsReceivers

    100 == getMaxDripsReceivers()  // MUST BE CHANGED!
    //filtered { f -> !f.isView && !f.isFallback && f.selector != initialize(address,(address,uint256,uint256,uint256,(uint256,uint256,uint256))).selector }


// Validity of amount per second
// The amount per second being dripped. Must never be zero.
invariant amtPerSecMustNeverBeZero()
    getAmtPerSec() != 0  // NOT WORKING, NEED TO PASS struct DripsReceiver
*/


/**************************************************
 *               STATE TRANSITIONS                *
 **************************************************/
// Describe validity of state changes by taking into
// account when something can change or who may change




/**************************************************
 *                METHOD INTEGRITY                *
 **************************************************/
 // Describe the integrity of a specific method




/**************************************************
 *             HIGH-LEVEL PROPERTIES              *
 **************************************************/
// Describe more than one element of the system,
// might be even cross-system, usually implemented
// as invariant or parametric rule,
// sometimes require the usage of ghost




/**************************************************
 *                 RISK ANALYSIS                  *
 **************************************************/
// Reasoning about the assets of the user\system and
// from point of view of what should never happen 




/**************************************************
 *                      MISC                      *
 **************************************************/

//  rules for info and checking the ghost and tool
//  expecting to fail

rule singleUserTimeUpdateNotChangingOtherUserBalance(method f, uint256 userId) {
    env e; env eB; env eF;
    calldataarg args;

    // uint8 i;

    // userId1 and userId2 - receivers Id
    uint256 assetId; uint256 userId1; uint256 userId2;
    require userId != userId1; // != userId2;
    require userId1 < userId2; // sorted
    require userId != userId2;

    // step 1 - balance before of user2
    bytes32 dripsHashBefore; bytes32 dripsHistoryHashBefore;
    uint32 updateTimeBefore; uint128 balanceBefore; uint32 maxEndBefore;

    dripsHashBefore, dripsHistoryHashBefore, updateTimeBefore,
     balanceBefore, maxEndBefore = _dripsState(eB, userId2, assetId);
    
    // assert false; // false 0
    
    // step 2 - setup user1 changes and then call _updateReceiverStates()
    /*  //setting values to config by create:
        uint192 _amtPerSec;
        uint32 _start;
        uint32 _duration;
    

    require _amtPerSec != 0;
    */
    DH.DripsConfig configOld1;// = create(_amtPerSec, _start, _duration);
    DH.DripsConfig configOld2;// = DH.create(_amtPerSec+1, _start+1, _duration+1);
    DH.DripsConfig configNew1;// = DH.create(_amtPerSec+2, _start+2, _duration+2);
   // DH.DripsConfig configNew2;

    require configOld1 != configNew1;
    // require configOld2 == configNew2;

    DH.DripsReceiver receiverOld1;
    require receiverOld1.userId == userId1;
    require receiverOld1.config == configOld1;
    
    DH.DripsReceiver receiverOld2;
    require receiverOld2.userId == userId2;
    require receiverOld2.config == configOld2;
    
    DH.DripsReceiver receiverNew1;
    require receiverNew1.userId == userId1;
    require receiverNew1.config == configNew1;
    
    


    // DripsReceiver[] memory currReceivers;
    // DripsReceiver[] memory newReceivers;
    // currReceivers[i].userId = userId1;
    // currReceivers[i].config = configCurr;
    // require sorted
    // require no duplicate
    // require amtPerSec != 0
    // require(i < _MAX_DRIPS_RECEIVERS,"");
    // require currReceivers == newReceivers;

    // newReceivers[i].config = configNew; // the only change in newReceivers is configNew of userId2

    // DripsState storage state = _dripsStorage().states[assetId][userId];
    // uint32 lastUpdate = state.updateTime;
    // uint32 currMaxEnd = state.maxEnd;

    // uint32 newMaxEnd = sizeof(uint32);
    

    // assert false;  // false 1
     //assert configOld2 != configNew2;  //returned 0


    _helperUpdateReceiverStates( e,
            receiverOld1,
            receiverOld2,
            receiverNew1,
            assetId,
            userId
        );

    //assert false;  // false 2

    // step 3 - balance after of user2
    bytes32 dripsHashAfter; bytes32 dripsHistoryHashAfter;
    uint32 updateTimeAfter; uint128 balanceAfter; uint32 maxEndAfter;

    dripsHashAfter, dripsHistoryHashAfter, updateTimeAfter, 
     balanceAfter, maxEndAfter = _dripsState(eF, userId2, assetId);
    
    
    // check that balance of user2 was not modified
    assert balanceBefore == balanceAfter, "balanceOfUser2 changed";

    assert false;
}
