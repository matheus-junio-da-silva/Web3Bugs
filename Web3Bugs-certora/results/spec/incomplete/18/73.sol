// ORIGINAL HISTORICAL SOLIDITY excerpts; content copied literally from contracts/18
// CVL property: ERC20Votes.spec:180-198 delegatee_receives_votes

// Original: contracts/18/contracts/token/ERC20/extensions/ERC20Votes.sol lines 57-59 function/modifier delegates
    function delegates(address account) public view virtual override returns (address) {
        return _delegates[account];
    }

// Original: contracts/18/contracts/token/ERC20/extensions/ERC20Votes.sol lines 64-67 function/modifier getVotes
    function getVotes(address account) public view virtual override returns (uint256) {
        uint256 pos = _checkpoints[account].length;
        return pos == 0 ? 0 : _checkpoints[account][pos - 1].votes;
    }

// Original: contracts/18/contracts/token/ERC20/extensions/ERC20Votes.sol lines 198-206 function/modifier _delegate
    function _delegate(address delegator, address delegatee) internal virtual {
        address currentDelegate = delegates(delegator);
        uint256 delegatorBalance = balanceOf(delegator);
        _delegates[delegator] = delegatee;

        emit DelegateChanged(delegator, currentDelegate, delegatee);

        _moveVotingPower(currentDelegate, delegatee, delegatorBalance);
    }

// Original: contracts/18/contracts/governance/utils/Votes.sol lines 47-49 function/modifier getVotes
    function getVotes(address account) public view virtual override returns (uint256) {
        return _delegateCheckpoints[account].latest();
    }

// Original: contracts/18/contracts/governance/utils/Votes.sol lines 88-90 function/modifier delegates
    function delegates(address account) public view virtual override returns (address) {
        return _delegation[account];
    }

// Original: contracts/18/contracts/governance/utils/Votes.sol lines 127-133 function/modifier _delegate
    function _delegate(address account, address delegatee) internal virtual {
        address oldDelegate = delegates(account);
        _delegation[account] = delegatee;

        emit DelegateChanged(account, oldDelegate, delegatee);
        _moveDelegateVotes(oldDelegate, delegatee, _getVotingUnits(account));
    }

// Original: contracts/18/contracts/token/ERC20/ERC20.sol lines 101-103 function/modifier balanceOf
    function balanceOf(address account) public view virtual override returns (uint256) {
        return _balances[account];
    }

// Original: contracts/18/contracts/token/ERC20/extensions/ERC20Votes.sol lines 208-224 function/modifier _moveVotingPower
    function _moveVotingPower(
        address src,
        address dst,
        uint256 amount
    ) private {
        if (src != dst && amount > 0) {
            if (src != address(0)) {
                (uint256 oldWeight, uint256 newWeight) = _writeCheckpoint(_checkpoints[src], _subtract, amount);
                emit DelegateVotesChanged(src, oldWeight, newWeight);
            }

            if (dst != address(0)) {
                (uint256 oldWeight, uint256 newWeight) = _writeCheckpoint(_checkpoints[dst], _add, amount);
                emit DelegateVotesChanged(dst, oldWeight, newWeight);
            }
        }
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
