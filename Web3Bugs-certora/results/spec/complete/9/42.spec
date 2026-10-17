// Original: contracts/9/specs/governance.spec:291-309; property text copied without modification.
// Original CVL syntax preserved. Status: complete.
using Accounts as accounts

methods {
	stageDurations() returns uint256,uint256,uint256 envfree
}

function callArbitrary(method f) {
	env e;
	calldataarg arg;
	f(e, arg);
}

rule modifying_stageDuration(method f) filtered { f -> 
    !f.isView 
    && f.selector != initialize(address,address,uint256,uint256,uint256,uint256,uint256,uint256,uint256,uint256,uint256,uint256,uint256).selector
    && f.selector != setApprovalStageDuration(uint256).selector
    && f.selector != setExecutionStageDuration(uint256).selector
    && f.selector != setReferendumStageDuration(uint256).selector
} {
	uint256 old1; uint256 old2; uint256 old3;
    old1, old2, old3 = stageDurations();
	
    callArbitrary(f);
  	
    uint256 new1;
	uint256 new2;
	uint256 new3;
	new1, new2, new3 = stageDurations();

    assert old1 == new1 && old2 == new2 && old3 == new3;
}
