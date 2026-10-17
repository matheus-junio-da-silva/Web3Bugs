// Project 10 — literal active cubeCounterGreaterThan0IffSenderInitialized from contracts/10/specs/proxy.spec:552-556
// CVL dependencies selected by transitive reference; historical CVL syntax is not migrated.
// Snapshot is not an executable proof of the 2021 audit.


methods {
    getSender() returns (address) envfree
    getCubeCounter() returns (uint256) envfree
}

definition MAX_UINT256() returns uint256 = 115792089237316195423570985008687907853269984665640564039457584007913129639935
    ;

invariant cubeCounterGreaterThan0IffSenderInitialized() getCubeCounter() > 0 <=> getSender() != 0 {
    preserved {
        require getCubeCounter() < MAX_UINT256();
    }
}
