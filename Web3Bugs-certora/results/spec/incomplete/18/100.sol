// ORIGINAL HISTORICAL SOLIDITY excerpts; content copied literally from contracts/18
// CVL property: ERC721Votes.spec:236-271 delegate_no_frontrunning

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

// Original: contracts/18/contracts/token/ERC721/ERC721.sol lines 62-65 function/modifier balanceOf
    function balanceOf(address owner) public view virtual override returns (uint256) {
        require(owner != address(0), "ERC721: address zero is not a valid owner");
        return _balances[owner];
    }

// Original: contracts/18/contracts/utils/Checkpoints.sol lines 39-53 function/modifier getAtBlock
    function getAtBlock(History storage self, uint256 blockNumber) internal view returns (uint256) {
        require(blockNumber < block.number, "Checkpoints: block not yet mined");

        uint256 high = self._checkpoints.length;
        uint256 low = 0;
        while (low < high) {
            uint256 mid = Math.average(low, high);
            if (self._checkpoints[mid]._blockNumber > blockNumber) {
                high = mid;
            } else {
                low = mid + 1;
            }
        }
        return high == 0 ? 0 : self._checkpoints[high - 1]._value;
    }

// Original: contracts/18/contracts/governance/utils/Votes.sol lines 38-38 state declaration
    mapping(address => address) private _delegation;

// Original: contracts/18/contracts/governance/utils/Votes.sol lines 39-39 state declaration
    mapping(address => Checkpoints.History) private _delegateCheckpoints;

// Original: contracts/18/contracts/governance/utils/Votes.sol lines 40-40 state declaration
    Checkpoints.History private _totalCheckpoints;
