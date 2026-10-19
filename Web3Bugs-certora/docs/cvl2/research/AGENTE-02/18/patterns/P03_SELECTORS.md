# P03 — typed selector literals

**Authority:** A2-SELECTOR. A CVL1 literal `schedule(address,uint256,bytes,bytes32,bytes32,uint256).selector` is a candidate for `sig:schedule(address,uint256,bytes,bytes32,bytes32,uint256).selector`. `f.selector` is NOT prefixed. Independently, Timelock's original `methods` lists `schedule(address,uint256,bytes32,bytes32,bytes32,uint256)`; Solidity uses `bytes` in that position: resolving the discrepancy needs historical harness/target investigation, not a mechanical parser adjustment.

Use property SRC18-### to confirm typed literal in its own body and inspect selector comparison for affected cases. If mismatch remains, UNRESOLVED_CANDIDATE.
