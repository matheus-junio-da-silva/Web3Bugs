// Project 10: relevant preserved Solidity excerpts; line annotations retain original provenance.

// Exact source excerpt: contracts/10/contracts/handlers/compound/HSCompound.sol:13-18
    using SafeERC20 for IERC20;

    // prettier-ignore
    address public constant FCOMPOUND_ACTIONS = 0x05EF8eb657027927fAB9b279138f0189CB144976;
    // prettier-ignore
    address public constant COMPTROLLER = 0x3d9819210A31b4961b30EF54bE2aeD79B9c9Cd3B;

// Exact source excerpt: contracts/10/contracts/handlers/compound/HSCompound.sol:75-92
            } else {
                underlying = _getToken(cTokenBorrow);
            }
            // Execute borrow, borrowed token will stay in the DSProxy
            try
                IDSProxy(dsProxy).execute(
                    FCOMPOUND_ACTIONS,
                    abi.encodeWithSelector(
                        // selector of "borrow(address,uint256)"
                        0x4b8a3529,
                        cTokenBorrow,
                        uBorrowAmount
                    )
                )
            {} catch Error(string memory reason) {
                _revertMsg("borrow", reason);
            } catch {
                _revertMsg("borrow");

// Exact source excerpt: contracts/10/specs/harnesses/Summary.sol:77-94
    // for HMaker, HSCompound
    address[] delegated;
    function lenDelegated() external returns (uint256) { return delegated.length; }
    function checkDelegated(address allowed) external returns (bool) {
        for (uint i = 0 ; i < delegated.length; i++) {
            if (delegated[i] != allowed) {
                return false;
            }
        }

        return true;
    }

    function execute(address a, bytes calldata b) external payable returns (bytes32) {
        delegated.push(a);
        havocDummyToken();
        return executeRet;
    }
