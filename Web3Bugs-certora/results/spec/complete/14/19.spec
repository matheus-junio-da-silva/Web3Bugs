// Project 14 — Opyn Gamma Protocol; historical CVL (not CVL2)
// Literal active declaration: specs/NoBankruptcy.spec:600-692
// Minimal explicit CVL declaration closure; model-wide ABI/implicit selector dependencies are in the historical target and scripts.
using OtokenHarnessA as shortOtoken

using OtokenHarnessB as longOtoken

using DummyERC20C as collateralToken

methods {
    anOtokenA() returns address envfree
    anOtokenB() returns address envfree
    dummyERC20C() returns address envfree
}

function links() {
    require anOtokenA() == shortOtoken;
    require anOtokenB() == longOtoken;
    require dummyERC20C() == collateralToken;
}

rule putOptionsPreExpiryCase3StartingWithAllCasesNoCode(
    address owner,
    uint256 vaultId,
    uint256 index,
    address asset,
    uint256 _shortAmount,
    uint256 _longAmount,
    uint256 _collateral,
    uint256 _poolAssetBalance,
    uint256 _poolShortOtokenBalance,
    uint256 _poolLongOtokenBalance,
    uint256 _totalSupplyShortOtoken,
    uint256 _totalSupplyLongOtoken,
    uint256 shortPrice,
    uint256 longPrice,
    uint256 shortAmount_,
    uint256 longAmount_,
    uint256 collateral_,
    uint256 poolAssetBalance_,
    uint256 poolShortOtokenBalance_,
    uint256 poolLongOtokenBalance_,
    uint256 totalSupplyShortOtoken_,
    uint256 totalSupplyLongOtoken_
) {
    links();
    env e;
    require asset == collateralToken;

    // assume no bankruptcy
	mathint _obligation = (_totalSupplyShortOtoken - _poolShortOtokenBalance ) * shortPrice
                                         +  (_totalSupplyLongOtoken -  _poolLongOtokenBalance ) * longPrice;
    require _poolAssetBalance >= _obligation ;

    // based on Mathematica proof:
    mathint _debt = 0;
    if( _longAmount <= _shortAmount && ( _longAmount * longPrice <= _shortAmount * shortPrice )) {
            _debt = _shortAmount * shortPrice  -  _longAmount *  longPrice ;
    } else if ( _longAmount > _shortAmount && longPrice < shortPrice) {
            _debt = _shortAmount * (shortPrice - longPrice) ;
    }
    //assume vault is in a valid state
    require _collateral >= _debt ;

     require shortPrice != longPrice; // <============= make sure this is a valid requirement ADD rule
    //assume valid state based on  valid balances rules
    require ( _totalSupplyShortOtoken >= _poolShortOtokenBalance + _shortAmount) &&
              _totalSupplyLongOtoken >= _poolLongOtokenBalance &&
              _poolLongOtokenBalance >= _longAmount &&
              _poolAssetBalance >= _collateral ;

	//compute excess collateral of other vaults
	mathint _obligationWithoutThisVault = (_totalSupplyShortOtoken - _poolShortOtokenBalance - _shortAmount) * shortPrice
                                             +  (_totalSupplyLongOtoken -  _poolLongOtokenBalance +_longAmount ) * longPrice  ;

    // assume excess collateral of other vaults is not cover by this vault's collateral
    require ( _poolAssetBalance - _collateral >= _obligationWithoutThisVault );

	
    //everything changed beside:
    // 1. total supply of long (it changes only when minting - adding as short) 
    require totalSupplyLongOtoken_ == _totalSupplyLongOtoken;
    // 2.  pool holding of short (it changes only when adding as long) 
    require poolShortOtokenBalance_  == _poolShortOtokenBalance;

    mathint obligation_ = (totalSupplyShortOtoken_ - poolShortOtokenBalance_ ) * shortPrice
                                                 +  (totalSupplyLongOtoken_ -  poolLongOtokenBalance_ ) * longPrice  ;


    //assume isValid vault case 3
    require !( (longAmount_ > shortAmount_ && longPrice < shortPrice) 
            || (longAmount_ <= shortAmount_ && ( longAmount_ * longPrice <= shortAmount_ * shortPrice )));

    
            
    mathint debt_ = 0;
    
    //assume vault is in a valid state
    require collateral_ >= debt_ ;

    // valid state - need to prove this as in invariant also when the vault is not valid should hold
    require  (totalSupplyShortOtoken_ >=  poolShortOtokenBalance_ + shortAmount_) &&
             totalSupplyLongOtoken_  >=  poolLongOtokenBalance_  &&
             poolLongOtokenBalance_ >= longAmount_ &&
             poolAssetBalance_ >= collateral_ ;

    // assume changes are coherent based on total required rules
    require collateral_ - _collateral ==  poolAssetBalance_-  _poolAssetBalance;
    require longAmount_ - _longAmount == poolLongOtokenBalance_ -  _poolLongOtokenBalance;
    require shortAmount_ - _shortAmount ==  totalSupplyShortOtoken_ - _totalSupplyShortOtoken;

    //verify no bankruptchy 
    assert poolAssetBalance_ >= obligation_ ;
}
