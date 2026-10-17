// Project 10: relevant preserved Solidity excerpts; line annotations retain original provenance.
// Illustration only; no target proof attributed to this contract.

// Exact source excerpt: contracts/10/contracts/Proxy.sol:82-105
// L82:     /**
// L83:      * @notice Direct transfer from EOA should be reverted.
// L84:      */
// L85:     receive() external payable {
// L86:         require(Address.isContract(msg.sender), "Not allowed from EOA");
// L87:     }
// L88: 
// L89:     /**
// L90:      * @notice Combo execution function. Including three phases: pre-process,
// L91:      * exection and post-process.
// L92:      * @param tos The handlers of combo.
// L93:      * @param configs The configurations of executing cubes.
// L94:      * @param datas The combo datas.
// L95:      * @param ruleIndexes The indexes of rules.
// L96:      */
// L97:     function batchExec(
// L98:         address[] calldata tos,
// L99:         bytes32[] calldata configs,
// L100:         bytes[] memory datas,
// L101:         uint256[] calldata ruleIndexes
// L102:     ) external payable override isNotHalted isNotBanned {
// L103:         _preProcess(ruleIndexes);
// L104:         _execs(tos, configs, datas);
// L105:         _postProcess();
