// Popsicle V3 Optimizer historical CVL; original source: contracts/22/spec/sanity.spec
// Exact original source intervals: 1-5;17-22
// Original spec lines 1-5
methods {
	getSqrtRatioAtTick(int24) => NONDET
	getTickAtSqrtRatio(uint160) => NONDET
	floor(int24 tick, int24 tickSpacing) => NONDET
}

// Original spec lines 17-22
rule sanityForView(method f) filtered { f -> f.isView }  {
	env e;
	calldataarg args;
	f(e,args);
	assert(false);
}

