// Project 13: original historical CVL, Example 58
// Original source: certora/sanity.spec:1-6
// Included original CVL ranges: certora/sanity.spec:1-6
// CVL2 conversion intentionally out of scope


rule r (method f) {
	env e; calldataarg arg;
	f(e,arg);
	assert false;

}
