// Project 14 — Opyn Gamma Protocol; historical CVL (not CVL2)
// Literal active declaration: specs/ValidBalances.spec:355-356
// Minimal explicit CVL declaration closure; model-wide ABI/implicit selector dependencies are in the historical target and scripts.
using Whitelist as whitelist

methods {
    whitelist.isWhitelistedOtoken(address) returns bool envfree
    whitelist.isWhitelistedCollateral(address) returns bool envfree
}

invariant assetIsNotOtoken(address a)
    !(whitelist.isWhitelistedOtoken(a) && whitelist.isWhitelistedCollateral(a))
