// Project 10 example 191; handler HComptroller, property cubeCounterIsAlwaysCleanedUp. Historical source excerpts only, NOT compilable assembly.
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

// Source: contracts/10/specs/harnesses/ProxyHarness.sol original lines 30-36 (literal excerpt)
        return _getSender();
    }

    function getCubeCounter() public view returns (uint256) {
        return _getCubeCounter();
    }
