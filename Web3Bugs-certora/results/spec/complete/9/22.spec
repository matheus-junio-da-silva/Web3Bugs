// Original: contracts/9/specs/accounts.spec:436-442 (unchanged rule/invariant block)
// CVL declarations copied verbatim; original syntax intentionally preserved.
pragma specify 0.1

methods {
	getVoteSigner(address) returns address envfree
	voteSignerToAccount(address) returns address envfree
	_getVoteRole() returns bytes32 envfree
}

invariant accountToSignerAndInverseVote(address a, address s, bytes32 r)
	r == _getVoteRole() => (s == getVoteSigner(a) => voteSignerToAccount(s) == a)
{
		preserved {
			require a != s;
		}
}
