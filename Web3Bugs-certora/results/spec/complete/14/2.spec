// Project 14 — Opyn Gamma Protocol; historical CVL (not CVL2)
// Literal active declaration: specs/MarginVault.spec:39-41
// Minimal explicit CVL declaration closure; model-wide ABI/implicit selector dependencies are in the historical target and scripts.
methods {
	collateralAmountLength() returns uint256 envfree
	collateralAssetsLength() returns uint256 envfree
	shortAmountLength() returns uint256 envfree
	shortOtokensLength() returns uint256 envfree
	longAmountLength() returns uint256 envfree
	longOtokensLength() returns uint256 envfree
}

invariant validVault() 	longAmountLength() == longOtokensLength() &&  
						shortAmountLength() == shortOtokensLength() &&
						collateralAmountLength() == collateralAssetsLength()
