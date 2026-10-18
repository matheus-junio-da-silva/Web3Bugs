// Project 10 example 194; handler HComptroller, property noOverwrite. Historical source excerpts only, NOT compilable assembly.
// Source: contracts/10/contracts/handlers/compound/HComptroller.sol original lines 17-42
    }

    function claimComp() external payable returns (uint256) {
        IComptroller comptroller = IComptroller(COMPTROLLER);
        address comp = comptroller.getCompAddress();
        address sender = _getSender();

        uint256 beforeCompBalance = IERC20(comp).balanceOf(sender);
        try comptroller.claimComp(sender) {} catch Error(string memory reason) {
            _revertMsg("claimComp", reason);
        } catch {
            _revertMsg("claimComp");
        }
        uint256 afterCompBalance = IERC20(comp).balanceOf(sender);

        return afterCompBalance - beforeCompBalance;
    }

    function claimComp(address holder) external payable returns (uint256) {
        IComptroller comptroller = IComptroller(COMPTROLLER);
        address comp = comptroller.getCompAddress();

        uint256 beforeCompBalance = IERC20(comp).balanceOf(holder);
        try comptroller.claimComp(holder) {} catch Error(string memory reason) {
            _revertMsg("claimComp", reason);
        } catch {

// Source: contracts/10/contracts/handlers/compound/HComptroller.sol original lines 33-49
    }

    function claimComp(address holder) external payable returns (uint256) {
        IComptroller comptroller = IComptroller(COMPTROLLER);
        address comp = comptroller.getCompAddress();

        uint256 beforeCompBalance = IERC20(comp).balanceOf(holder);
        try comptroller.claimComp(holder) {} catch Error(string memory reason) {
            _revertMsg("claimComp", reason);
        } catch {
            _revertMsg("claimComp");
        }
        uint256 afterCompBalance = IERC20(comp).balanceOf(holder);

        return afterCompBalance - beforeCompBalance;
    }
}

// Source: contracts/10/specs/harnesses/ProxyHarness.sol original lines 7-25 (literal excerpt)

    function getSlot(uint256 s) external view returns (uint256 x) {
        assembly {
            x := sload(s)
        }
    }

    function getStackLengthSlot() external view returns (uint256 x) {
        assembly {
            x := stack_slot
        }
    }

    function getStackLength() external view returns (uint256) {
        return stack.length;
    }

    function ethBalance(address who) external view returns (uint256) {
        return who.balance;
