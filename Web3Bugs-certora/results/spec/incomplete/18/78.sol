// ORIGINAL HISTORICAL SOLIDITY excerpts; content copied literally from contracts/18
// CVL property: ERC20Votes.spec:294-307 burn_decreases_totalSupply

// Original: contracts/18/contracts/token/ERC20/extensions/ERC20Votes.sol lines 89-92 function/modifier getPastTotalSupply
    function getPastTotalSupply(uint256 blockNumber) public view virtual override returns (uint256) {
        require(blockNumber < block.number, "ERC20Votes: block not yet mined");
        return _checkpointsLookup(_totalSupplyCheckpoints, blockNumber);
    }

// Original: contracts/18/contracts/governance/utils/Votes.sol lines 73-76 function/modifier getPastTotalSupply
    function getPastTotalSupply(uint256 blockNumber) public view virtual override returns (uint256) {
        require(blockNumber < block.number, "Votes: block not yet mined");
        return _totalCheckpoints.getAtBlock(blockNumber);
    }

// Original: contracts/18/contracts/token/ERC20/ERC20.sol lines 94-96 function/modifier totalSupply
    function totalSupply() public view virtual override returns (uint256) {
        return _totalSupply;
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

// Original: contracts/18/contracts/token/ERC20/ERC20.sol lines 40-40 state declaration
    uint256 private _totalSupply;
