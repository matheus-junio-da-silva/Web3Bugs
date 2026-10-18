// Original: contracts/9/specs/governance.spec:58-59; property text copied without modification.
// Original CVL syntax preserved. Status: complete.
using Accounts as accounts

methods {
	proposalCount() returns uint256 envfree
	getFromDequeued(uint256) returns uint256 envfree
}

invariant dequeuedIsWithinRange(uint i) getFromDequeued(i) <= proposalCount()

