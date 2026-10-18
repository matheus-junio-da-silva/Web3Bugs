// Original source: contracts/12/specs/StableDebtToken.spec:5-12
// Original dependency lines: 1-3;
// Target: StableDebtTokenHarness (historical simplified model)
// CVL syntax preserved verbatim; not migrated to CVL2.
methods {
	getUserLastUpdated(address) returns uint40 envfree
}

rule integrityTimeStamp(address user, method f) {
	env e;
	require sinvoke getIncentivesController(e) == 0;
	require getUserLastUpdated(user) <= e.block.timestamp;
	calldataarg arg;
	sinvoke f(e,arg);
	assert getUserLastUpdated(user) <= e.block.timestamp;
}
