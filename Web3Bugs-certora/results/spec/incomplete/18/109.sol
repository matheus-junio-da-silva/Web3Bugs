// ORIGINAL HISTORICAL SOLIDITY excerpts; content copied literally from contracts/18
// CVL property: GovernorBase.spec:230-242 noStartBeforeCreation

// Original: contracts/18/contracts/governance/Governor.sol lines 182-184 function/modifier proposalSnapshot
    function proposalSnapshot(uint256 proposalId) public view virtual override returns (uint256) {
        return _proposals[proposalId].voteStart.getDeadline();
    }

// Original: contracts/18/contracts/governance/Governor.sol lines 245-284 function/modifier propose
    function propose(
        address[] memory targets,
        uint256[] memory values,
        bytes[] memory calldatas,
        string memory description
    ) public virtual override returns (uint256) {
        require(
            getVotes(_msgSender(), block.number - 1) >= proposalThreshold(),
            "Governor: proposer votes below proposal threshold"
        );

        uint256 proposalId = hashProposal(targets, values, calldatas, keccak256(bytes(description)));

        require(targets.length == values.length, "Governor: invalid proposal length");
        require(targets.length == calldatas.length, "Governor: invalid proposal length");
        require(targets.length > 0, "Governor: empty proposal");

        ProposalCore storage proposal = _proposals[proposalId];
        require(proposal.voteStart.isUnset(), "Governor: proposal already exists");

        uint64 snapshot = block.number.toUint64() + votingDelay().toUint64();
        uint64 deadline = snapshot + votingPeriod().toUint64();

        proposal.voteStart.setDeadline(snapshot);
        proposal.voteEnd.setDeadline(deadline);

        emit ProposalCreated(
            proposalId,
            _msgSender(),
            targets,
            values,
            new string[](targets.length),
            calldatas,
            snapshot,
            deadline,
            description
        );

        return proposalId;
    }

// Original: contracts/18/contracts/mocks/GovernorMock.sol lines 42-49 function/modifier propose
    function propose(
        address[] memory targets,
        uint256[] memory values,
        bytes[] memory calldatas,
        string memory description
    ) public virtual override(Governor, GovernorProposalThreshold) returns (uint256) {
        return super.propose(targets, values, calldatas, description);
    }

// Original: contracts/18/contracts/governance/Governor.sol lines 47-47 state declaration
    mapping(uint256 => ProposalCore) private _proposals;
