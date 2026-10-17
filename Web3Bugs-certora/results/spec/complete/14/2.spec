// Project 14 — Opyn Gamma. Historical CVL, no modern migration.
// Selected active invariant: validVault, original specs/MarginVault.spec:39-41
// Included original CVL ranges: specs/MarginVault.spec:1-42;90-100;124-132;141-147;168-175;184-187;197-200;221-224;233-237;247-250;271-274;283
// Conservative original spec-wide methods/helper context; other properties excluded.

methods {
	//core functions wrappers
	addShort(address, uint256, uint256) envfree
	removeShort(address, uint256, uint256) envfree
	addLong(address, uint256, uint256) envfree
	removeLong(address, uint256, uint256) envfree
	addCollateral(address, uint256, uint256) envfree
	removeCollateral(address, uint256, uint256) envfree
	//getters for collateral
	totalCollateral() returns uint256 envfree
	collateralAmountLength() returns uint256 envfree
	collateralAssetsLength() returns uint256 envfree
	getCollateralAmount(uint256) returns uint256 envfree
	getCollateralAsset(uint256) returns address envfree
	//getters for shorts
	totalShortAmount() returns uint256 envfree
	shortAmountLength() returns uint256 envfree
	shortOtokensLength() returns uint256 envfree
	getShortOtoken(uint256) returns address envfree
	getShortAmount(uint256) returns uint256 envfree
	//getters for longs
	totalLongAmount() returns uint256 envfree
	longAmountLength() returns uint256 envfree
	longOtokensLength() returns uint256 envfree
	getLongOtoken(uint256) returns address envfree
	getLongAmount(uint256) returns uint256 envfree
}

definition MAXINT() returns uint256 = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF;
definition ADDRESSZERO() returns address = 0;

/**
@title Valid state of a vault
@notice A vault v  is in a valid state if for each of the entities (collateral, long, short):
(i) The length of the list of amounts of entity equals to the length of the list of addresses of this entity
(ii) The entity amount at index i is greater than zero iff there is a non zero address at index i of this entity
*/
invariant validVault() 	longAmountLength() == longOtokensLength() &&  
						shortAmountLength() == shortOtokensLength() &&
						collateralAmountLength() == collateralAssetsLength() 
						
	

/**
@title Success characteristic of addCollateral 
@notice One should be able to add collateral on a valid vault v under realistic circumstances
		{ x > 0 ∧
		    ( i < v.collateralAmounts.length ⇒  ( v.collateralAssets[i] = a ∧ v.collateralAmounts[i] + x < MAX_UINT) ) }
           r = addCollateral(v,a,x,i)
        { r }

*/


/**
@title Integrity of addCollateral 
@notice When successfully adding x collateral to a vault, the totalCollateral increases by x. 
	{ b = totalCollateral(v) }
		addCollateral(v,a,x);
	{ totalCollateral(v) = b + x }
*/

/**
@title Additive addCollateral 
@notice Adding collateral to a vault is additive, i.e., it can be performed either all at once or in steps.	
		addCollateral(v,a,x);addCollateral(v,a,y) ~ addCollateral(v,a,x+y) 
	{ totalCollateral1(v) = totalCollateral2(v) }
*/

/**
@title Inverse addCollateral and removeCollateral
@notice Adding and removing collateral are inverse operations 
	{ b = totalCollateral(v) }
		addCollateral(v,a,x);removeCollateral(x,a,x)
	{ totalCollateral(v) = b }
*/

/**
@title Integrity of addShort 
*/

/**
@title Additive addShort 
*/

/**
@title Inverse addShort and removeShort
*/


/**
@title Integrity of addLong 
*/

/**
@title Additive addLong 
*/

/**
@title Inverse addLong and removeLong
*/

