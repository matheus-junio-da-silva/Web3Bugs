// ORIGINAL HISTORICAL SOLIDITY excerpts; content copied literally from contracts/18
// CVL property: ERC721Votes.spec:165-178 delegates_safe

// Original: contracts/18/contracts/governance/utils/Votes.sol lines 88-90 function/modifier delegates
    function delegates(address account) public view virtual override returns (address) {
        return _delegation[account];
    }

// Original: contracts/18/contracts/governance/utils/Votes.sol lines 95-98 function/modifier delegate
    function delegate(address delegatee) public virtual override {
        address account = _msgSender();
        _delegate(account, delegatee);
    }

// Original: contracts/18/contracts/governance/utils/Votes.sol lines 103-120 function/modifier delegateBySig
    function delegateBySig(
        address delegatee,
        uint256 nonce,
        uint256 expiry,
        uint8 v,
        bytes32 r,
        bytes32 s
    ) public virtual override {
        require(block.timestamp <= expiry, "Votes: signature expired");
        address signer = ECDSA.recover(
            _hashTypedDataV4(keccak256(abi.encode(_DELEGATION_TYPEHASH, delegatee, nonce, expiry))),
            v,
            r,
            s
        );
        require(nonce == _useNonce(signer), "Votes: invalid nonce");
        _delegate(signer, delegatee);
    }

// Original: contracts/18/contracts/governance/utils/Votes.sol lines 127-133 function/modifier _delegate
    function _delegate(address account, address delegatee) internal virtual {
        address oldDelegate = delegates(account);
        _delegation[account] = delegatee;

        emit DelegateChanged(account, oldDelegate, delegatee);
        _moveDelegateVotes(oldDelegate, delegatee, _getVotingUnits(account));
    }

// Original: contracts/18/contracts/governance/utils/Votes.sol lines 38-38 state declaration
    mapping(address => address) private _delegation;

// Original: contracts/18/contracts/governance/utils/Votes.sol lines 39-39 state declaration
    mapping(address => Checkpoints.History) private _delegateCheckpoints;

// Original: contracts/18/contracts/governance/utils/Votes.sol lines 40-40 state declaration
    Checkpoints.History private _totalCheckpoints;
