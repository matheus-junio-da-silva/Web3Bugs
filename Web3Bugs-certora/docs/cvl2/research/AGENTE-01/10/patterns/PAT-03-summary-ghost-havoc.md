# PAT-03 — Summaries, ghosts, storage and vacuity

Evidence: EV-A1-RECEIVER, EV-A1-SIGHASH, EV-A1-GHOST, EV-SRC-HANDLER, EV-UP-SCRIPT. The `proxy.spec` family has a raw `0x12345678 => NONDET` methods entry, `DISPATCHER(true/false)` summaries, a `cacheTouched` ghost and `hook Sstore cache[...]` with havoc assumption.

An unrecognized raw method sighash cannot be converted to a fabricated function; require ABI evidence identifying the method, or mark unresolved. Preserve exact summary scope and havoc effects; do not weaken the ghost hook or insert `require_` casts that exclude cases. The contract uses handler-dependent `method f`, getter injections, `requireInvariant` and target-specific storage. `Summary.checkDelegated` can be true for zero entries; its vacuity must not be silently treated as proof of legitimate delegated calls.

**Not run:** hook resolution, solver semantics, key slots, post-Perl ABI. 