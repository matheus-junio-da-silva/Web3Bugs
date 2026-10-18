// Source: contracts/7/specs/ReserveConfiguration.spec
// Literal property: rule setPausedIntegrity, lines 97-100
// Literal dependency source lines: 1;14-15;57;97-100
// Historical syntax retained; no reconstruction or CVL2 migration.

methods {
    setPaused(bool) envfree
    getPaused() returns (bool) envfree
}

rule setPausedIntegrity(bool paused) {
    setPaused(paused);
    assert getPaused() == paused;
}
