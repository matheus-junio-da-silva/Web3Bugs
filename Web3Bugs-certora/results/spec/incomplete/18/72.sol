// ORIGINAL HISTORICAL SOLIDITY excerpts; content copied literally from contracts/18
// CVL property: ERC20Votes.spec:167-177 delegates_safe

// Original: contracts/18/contracts/token/ERC20/extensions/ERC20Votes.sol lines 57-59 function/modifier delegates
    function delegates(address account) public view virtual override returns (address) {
        return _delegates[account];
    }

// Original: contracts/18/contracts/token/ERC20/extensions/ERC20Votes.sol lines 126-128 function/modifier delegate
    function delegate(address delegatee) public virtual override {
        _delegate(_msgSender(), delegatee);
    }

// Original: contracts/18/contracts/token/ERC20/extensions/ERC20Votes.sol lines 133-150 function/modifier delegateBySig
    function delegateBySig(
        address delegatee,
        uint256 nonce,
        uint256 expiry,
        uint8 v,
        bytes32 r,
        bytes32 s
    ) public virtual override {
        require(block.timestamp <= expiry, "ERC20Votes: signature expired");
        address signer = ECDSA.recover(
            _hashTypedDataV4(keccak256(abi.encode(_DELEGATION_TYPEHASH, delegatee, nonce, expiry))),
            v,
            r,
            s
        );
        require(nonce == _useNonce(signer), "ERC20Votes: invalid nonce");
        _delegate(signer, delegatee);
    }

// Original: contracts/18/contracts/token/ERC20/extensions/ERC20Votes.sol lines 198-206 function/modifier _delegate
    function _delegate(address delegator, address delegatee) internal virtual {
        address currentDelegate = delegates(delegator);
        uint256 delegatorBalance = balanceOf(delegator);
        _delegates[delegator] = delegatee;

        emit DelegateChanged(delegator, currentDelegate, delegatee);

        _moveVotingPower(currentDelegate, delegatee, delegatorBalance);
    }

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

// Original: contracts/18/contracts/token/ERC20/extensions/ERC20Votes.sol lines 36-36 state declaration
    mapping(address => address) private _delegates;

// Original: contracts/18/contracts/token/ERC20/extensions/ERC20Votes.sol lines 37-37 state declaration
    mapping(address => Checkpoint[]) private _checkpoints;

// Original: contracts/18/contracts/governance/utils/Votes.sol lines 38-38 state declaration
    mapping(address => address) private _delegation;

// Original: contracts/18/contracts/governance/utils/Votes.sol lines 39-39 state declaration
    mapping(address => Checkpoints.History) private _delegateCheckpoints;

// Original: contracts/18/contracts/governance/utils/Votes.sol lines 40-40 state declaration
    Checkpoints.History private _totalCheckpoints;
