// ORIGINAL HISTORICAL SOLIDITY excerpts; content copied literally from contracts/18
// CVL property: ERC20Votes.spec:69-79 votes_solvency

// Original: contracts/18/contracts/token/ERC20/extensions/ERC20Votes.sol lines 50-52 function/modifier numCheckpoints
    function numCheckpoints(address account) public view virtual returns (uint32) {
        return SafeCast.toUint32(_checkpoints[account].length);
    }

// Original: contracts/18/contracts/token/ERC20/extensions/ERC20Votes.sol lines 172-176 function/modifier _burn
    function _burn(address account, uint256 amount) internal virtual override {
        super._burn(account, amount);

        _writeCheckpoint(_totalSupplyCheckpoints, _subtract, amount);
    }

// Original: contracts/18/contracts/token/ERC20/ERC20.sol lines 94-96 function/modifier totalSupply
    function totalSupply() public view virtual override returns (uint256) {
        return _totalSupply;
    }

// Original: contracts/18/contracts/token/ERC20/ERC20.sol lines 101-103 function/modifier balanceOf
    function balanceOf(address account) public view virtual override returns (uint256) {
        return _balances[account];
    }

// Original: contracts/18/contracts/token/ERC20/ERC20.sol lines 280-295 function/modifier _burn
    function _burn(address account, uint256 amount) internal virtual {
        require(account != address(0), "ERC20: burn from the zero address");

        _beforeTokenTransfer(account, address(0), amount);

        uint256 accountBalance = _balances[account];
        require(accountBalance >= amount, "ERC20: burn amount exceeds balance");
        unchecked {
            _balances[account] = accountBalance - amount;
        }
        _totalSupply -= amount;

        emit Transfer(account, address(0), amount);

        _afterTokenTransfer(account, address(0), amount);
    }

// Original: contracts/18/contracts/mocks/ERC20VotesMock.sol lines 14-16 function/modifier burn
    function burn(address account, uint256 amount) public {
        _burn(account, amount);
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
