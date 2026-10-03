// Extracted from: contracts/2/specs/aggregator.spec
// Property: PoRFeedChange
// Dependency status: complete
// Original source ranges included: 1-4;6-7;9-10;13;17-28;35-54
// CVL2 migration is intentionally out of scope for this catalog stage.

methods {
    getProofOfReserveFeedForAsset(address) returns (address) envfree
    disableProofOfReserveFeed(address)
    enableProofOfReserveFeed(address, address)
    getBridgeWrapperForAsset(address) returns (address) envfree
    enableProofOfReserveFeedWithBridgeWrapper(address, address, address)

    // summarizations:
    latestRoundData() => NONDET
}

function call_f_with_params(method f, env e, address asset , address PoRFeed, address wrapper){
    calldataarg args;
    if (f.selector == enableProofOfReserveFeed(address, address).selector){
        enableProofOfReserveFeed(e, asset, PoRFeed);
    } else if (f.selector == disableProofOfReserveFeed(address).selector){
        disableProofOfReserveFeed(e, asset);
    } else if (f.selector == enableProofOfReserveFeedWithBridgeWrapper(address, address, address).selector) {
        enableProofOfReserveFeedWithBridgeWrapper(e, asset, PoRFeed, wrapper);
    } else {
        f(e, args);
    }
}

rule PoRFeedChange(address asset, address PoRFeed, address wrapper){
    
    address feedBefore = getProofOfReserveFeedForAsset(asset);
    address bridgeWrapperBefore = getBridgeWrapperForAsset(asset);
    
    method f; env e;
    call_f_with_params(f, e, asset, PoRFeed, wrapper);

    address feedAfter = getProofOfReserveFeedForAsset(asset);
    address bridgeWrapperAfter = getBridgeWrapperForAsset(asset);

    assert f.selector == enableProofOfReserveFeed(address, address).selector => (feedAfter != 0 && feedAfter == PoRFeed);
    assert f.selector == enableProofOfReserveFeedWithBridgeWrapper(address, address, address).selector => 
                        (feedAfter != 0 && feedAfter == PoRFeed && bridgeWrapperAfter != 0 && bridgeWrapperAfter == wrapper);
    assert f.selector == disableProofOfReserveFeed(address).selector => feedAfter == 0 && bridgeWrapperAfter == 0;
    assert (f.selector != enableProofOfReserveFeed(address, address).selector && 
            f.selector != disableProofOfReserveFeed(address).selector &&
            f.selector != enableProofOfReserveFeedWithBridgeWrapper(address, address, address).selector) => 
                        feedBefore == feedAfter && bridgeWrapperBefore == bridgeWrapperAfter;
}
