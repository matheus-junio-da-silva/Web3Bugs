// Project 14 — Opyn Gamma Protocol; historical CVL (not CVL2)
// Literal active declaration: specs/NoBankruptcy.spec:197-316
// Minimal explicit CVL declaration closure; model-wide ABI/implicit selector dependencies are in the historical target and scripts.
using OtokenHarnessA as shortOtoken

using OtokenHarnessB as longOtoken

using DummyERC20C as collateralToken

using MarginPoolHarness as pool

methods {
    pool.getStoredBalance(address) returns uint256 envfree
    assetTotalSupply(address) returns uint256 envfree
    getVaultCollateralAmount(address, uint256, uint256)  returns uint256 envfree
    getVaultCollateralAsset(address, uint256, uint256)  returns address envfree
    getVaultLongAmount(address, uint256, uint256)  returns uint256 envfree
    getVaultLongOtoken(address, uint256, uint256)  returns address envfree
    getVaultShortAmount(address, uint256, uint256)  returns uint256 envfree
    getVaultShortOtoken(address, uint256, uint256)  returns address envfree
    isVaultExpired(address, uint256) returns bool
    shortOtoken.strikePrice() returns uint256 envfree
    longOtoken.strikePrice() returns uint256 envfree
    shortOtoken.havocTotalSupply(uint256) envfree
    pool.havocSystemBalance(address) envfree
    havocVault(address, uint256, uint256, uint256, uint256, uint256 ) envfree
    anOtokenA() returns address envfree
    anOtokenB() returns address envfree
    dummyERC20C() returns address envfree
}

function links() {
    require anOtokenA() == shortOtoken;
    require anOtokenB() == longOtoken;
    require dummyERC20C() == collateralToken;
}

rule putOptionsPreExpiryCase2StartingWithAllCases(
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
    require shortOtoken == getVaultShortOtoken(owner, vaultId, index);
    require longOtoken == getVaultLongOtoken(owner, vaultId, index);
    require collateralToken == getVaultCollateralAsset(owner, vaultId, index);
    require asset == collateralToken;

    require _shortAmount == getVaultShortAmount(owner, vaultId, index);
    require _longAmount == getVaultLongAmount(owner, vaultId, index);
    require _collateral == getVaultCollateralAmount(owner, vaultId, index);
    require _poolAssetBalance == pool.getStoredBalance(asset);
    require _poolShortOtokenBalance == pool.getStoredBalance(shortOtoken);
    require _poolLongOtokenBalance == pool.getStoredBalance(longOtoken);
    require _totalSupplyShortOtoken == assetTotalSupply(shortOtoken);
    require _totalSupplyLongOtoken == assetTotalSupply(longOtoken);
    require shortPrice == shortOtoken.strikePrice();
    require longPrice == longOtoken.strikePrice();

    // assume before expiry
    require !isVaultExpired(e, owner, vaultId);

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

	
    // simulate many operations in one step
    uint256 newShortAmount;
    uint256 newLongAmount;
    uint256 newcollateralAmount;
    uint256 newTotalSupply;
    sinvoke havocVault(owner, vaultId, index, newShortAmount, newLongAmount, newcollateralAmount); 
    sinvoke pool.havocSystemBalance(longOtoken);
    sinvoke pool.havocSystemBalance(asset);
    sinvoke shortOtoken.havocTotalSupply(newTotalSupply);


    require shortAmount_ == getVaultShortAmount(owner, vaultId, index);
    require longAmount_ == getVaultLongAmount(owner, vaultId, index);
    require collateral_ == getVaultCollateralAmount(owner, vaultId, index);
    require poolAssetBalance_ == pool.getStoredBalance(asset);
    require poolShortOtokenBalance_ == pool.getStoredBalance(shortOtoken);
    require poolLongOtokenBalance_ == pool.getStoredBalance(longOtoken);
    require totalSupplyShortOtoken_ == assetTotalSupply(shortOtoken);
    require totalSupplyLongOtoken_ == assetTotalSupply(longOtoken);

    mathint obligation_ = (totalSupplyShortOtoken_ - poolShortOtokenBalance_ ) * shortPrice
                                                 +  (totalSupplyLongOtoken_ -  poolLongOtokenBalance_ ) * longPrice  ;


    //assume isValid vault case 2
    require longAmount_ > shortAmount_ && longPrice < shortPrice ;
    mathint debt_ =  shortAmount_ * shortPrice  -  longAmount_ *  longPrice ;
   
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
