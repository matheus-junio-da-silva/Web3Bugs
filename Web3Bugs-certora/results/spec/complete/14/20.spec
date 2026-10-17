// Project 14 — Opyn Gamma. Historical CVL, no modern migration.
// Selected active rule: privilegedOperation, original specs/Privileged.spec:12-31
// Included original CVL ranges: specs/Privileged.spec:1-31
// Conservative original spec-wide methods/helper context; other properties excluded.
definition knownAsNonPrivileged(method f) returns bool  =
	( 	f.selector == isWhitelistedOtoken(address).selector  ||
		f.selector == isWhitelistedProduct(address,address,address,bool).selector ||
		f.selector == owner().selector ||
    	f.selector == isWhitelistedCallee(address).selector ||
		f.selector == whitelistOtoken(address).selector ||
		f.selector == addressBook().selector || 
		f.selector == isWhitelistedCollateral(address).selector ); 



rule privilegedOperation(method f, address privileged)
description "$f can be called by more than one user without reverting"
{
	env e1;
	calldataarg arg;
	require !knownAsNonPrivileged(f);
	require e1.msg.sender == privileged;

	storage initialStorage = lastStorage;
	invoke f(e1, arg); // privileged succeeds executing candidate privileged operation.
	bool firstSucceeded = !lastReverted;

	env e2;
	calldataarg arg2;
	require e2.msg.sender != privileged;
	invoke f(e2, arg2) at initialStorage; // unprivileged
	bool secondSucceeded = !lastReverted;

	assert  !(firstSucceeded && secondSucceeded), "${f.selector} can be called by both ${e1.msg.sender} and ${e2.msg.sender}, so it is not privileged";
}
