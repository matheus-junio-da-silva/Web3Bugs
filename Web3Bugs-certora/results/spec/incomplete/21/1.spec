// Extracted literal original CVL declarations from contracts/21/specs/DSM.spec
using DepositSecurityModuleHarness as DSMH
methods{
getGuardianQuorum() returns (uint256) envfree
getGuardianLength() returns (uint256) envfree
}
rule  depositBufferEtherRevertCheck(){
        env e;
        bytes32 depositRoot;
        uint256 keysOpIndex;
        uint256 blockNumber;
        bytes32 blockHash;
        DSMH.Signature guardianSignature1;
        DSMH.Signature guardianSignature2;
        DSMH.Signature guardianSignature3;

        uint256 quorum;

        quorum = getGuardianQuorum();

        // callHelper();
        depositBufferedEtherHarness@withrevert(e, depositRoot,
                                        keysOpIndex,
                                        blockNumber,
                                        blockHash,
                                        guardianSignature1,
                                        guardianSignature2,
                                        guardianSignature3);

        assert !lastReverted;
        }
