// Extracted from Project 4 — AAVE Staked Token v1.5
// Property: cooldownDataCorrectness
// Dependency status: incomplete
// CVL2 migration is intentionally out of scope.
// Included original CVL ranges: certora/specs/base.spec:4-4; certora/specs/base.spec:16-16; certora/specs/base.spec:17-17; certora/specs/base.spec:48-48; certora/specs/invariants.spec:35-44

methods {
    cooldownAmount(address) returns (uint216) envfree
    cooldownTimestamp(address) returns (uint40) envfree
}
invariant cooldownDataCorrectness(address user, env e)
    cooldownAmount(user) > 0 => cooldownTimestamp(user) > 0
    {
        preserved with (env e2)
        {
            require e2.block.timestamp == e.block.timestamp;
            require e.block.timestamp > 0;
            require e.block.timestamp < 2^32;
        }
    }
