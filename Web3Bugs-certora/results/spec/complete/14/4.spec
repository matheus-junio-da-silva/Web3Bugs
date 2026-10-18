// Project 14 — Opyn Gamma Protocol; historical CVL (not CVL2)
// Literal active declaration: specs/MarginVault.spec:73-89
// Minimal explicit CVL declaration closure; model-wide ABI/implicit selector dependencies are in the historical target and scripts.
methods {
	collateralAmountLength() returns uint256 envfree
	collateralAssetsLength() returns uint256 envfree
	getCollateralAmount(uint256) returns uint256 envfree
	shortAmountLength() returns uint256 envfree
	shortOtokensLength() returns uint256 envfree
	getShortAmount(uint256) returns uint256 envfree
	longAmountLength() returns uint256 envfree
	longOtokensLength() returns uint256 envfree
	getLongAmount(uint256) returns uint256 envfree
}

invariant validVault() 	longAmountLength() == longOtokensLength() &&  
						shortAmountLength() == shortOtokensLength() &&
						collateralAmountLength() == collateralAssetsLength()

rule changeToOneEntity(uint256 shortIndex, uint256 longIndex, uint256 collateralIndex, method f ) {
	
	requireInvariant validVault();
	uint256 longAmountBefore = getLongAmount(longIndex);
	uint256 shortAmountBefore = getShortAmount(shortIndex);
	uint256 collateralAmountBefore = getCollateralAmount(collateralIndex);
	calldataarg args;
	env e;
	sinvoke f(e,args);
	uint256 longAmountAfter = getLongAmount(longIndex);
	uint256 shortAmountAfter = getShortAmount(shortIndex);
	uint256 collateralAmountAfter = getCollateralAmount(collateralIndex);

	assert (longAmountBefore != longAmountAfter => (shortAmountBefore == shortAmountAfter && collateralAmountBefore == collateralAmountAfter)) &&
		   (shortAmountBefore != shortAmountAfter  => (longAmountBefore == longAmountAfter && collateralAmountBefore == collateralAmountAfter)) &&
		   (collateralAmountBefore != collateralAmountAfter  => (longAmountBefore == longAmountAfter && shortAmountBefore == shortAmountAfter)); 
}
