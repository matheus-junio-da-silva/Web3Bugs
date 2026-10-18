// ORIGINAL HISTORICAL SOLIDITY excerpts; content copied literally from contracts/18
// CVL property: ERC20Votes.spec:145-164 transfer_safe

// Original: contracts/18/contracts/token/ERC20/extensions/ERC20Votes.sol lines 50-52 function/modifier numCheckpoints
    function numCheckpoints(address account) public view virtual returns (uint32) {
        return SafeCast.toUint32(_checkpoints[account].length);
    }

// Original: contracts/18/contracts/token/ERC20/extensions/ERC20Votes.sol lines 57-59 function/modifier delegates
    function delegates(address account) public view virtual override returns (address) {
        return _delegates[account];
    }

// Original: contracts/18/contracts/token/ERC20/extensions/ERC20Votes.sol lines 64-67 function/modifier getVotes
    function getVotes(address account) public view virtual override returns (uint256) {
        uint256 pos = _checkpoints[account].length;
        return pos == 0 ? 0 : _checkpoints[account][pos - 1].votes;
    }

// Original: contracts/18/contracts/governance/utils/Votes.sol lines 47-49 function/modifier getVotes
    function getVotes(address account) public view virtual override returns (uint256) {
        return _delegateCheckpoints[account].latest();
    }

// Original: contracts/18/contracts/governance/utils/Votes.sol lines 88-90 function/modifier delegates
    function delegates(address account) public view virtual override returns (address) {
        return _delegation[account];
    }

// Original: contracts/18/contracts/token/ERC20/ERC20.sol lines 158-167 function/modifier transferFrom
    function transferFrom(
        address from,
        address to,
        uint256 amount
    ) public virtual override returns (bool) {
        address spender = _msgSender();
        _spendAllowance(from, spender, amount);
        _transfer(from, to, amount);
        return true;
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

// Original: contracts/18/contracts/token/ERC20/extensions/ERC20Votes.sol lines 226-240 function/modifier _writeCheckpoint
    function _writeCheckpoint(
        Checkpoint[] storage ckpts,
        function(uint256, uint256) view returns (uint256) op,
        uint256 delta
    ) private returns (uint256 oldWeight, uint256 newWeight) {
        uint256 pos = ckpts.length;
        oldWeight = pos == 0 ? 0 : ckpts[pos - 1].votes;
        newWeight = op(oldWeight, delta);

        if (pos > 0 && ckpts[pos - 1].fromBlock == block.number) {
            ckpts[pos - 1].votes = SafeCast.toUint224(newWeight);
        } else {
            ckpts.push(Checkpoint({fromBlock: SafeCast.toUint32(block.number), votes: SafeCast.toUint224(newWeight)}));
        }
    }
