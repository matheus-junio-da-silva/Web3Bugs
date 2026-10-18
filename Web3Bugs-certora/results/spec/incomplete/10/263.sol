// Project 10 example 263; handler HYVault, property cubeCounterIsAlwaysCleanedUp. Historical source excerpts only, NOT compilable assembly.
// Source: contracts/10/contracts/handlers/yearn/HYVault.sol original lines 14-39
    }

    function deposit(
        address vault,
        uint256 _amount
    ) external payable returns (uint256) {
        IYVault yVault = IYVault(vault);
        uint256 beforeYTokenBalance = IERC20(address(yVault)).balanceOf(
            address(this)
        );

        address token = yVault.token();
        // if amount == type(uint256).max return balance of Proxy
        _amount = _getBalance(token, _amount);
        _tokenApprove(token, address(yVault), _amount);
        try yVault.deposit(_amount) {} catch Error(string memory reason) {
            _revertMsg("deposit", reason);
        } catch {
            _revertMsg("deposit");
        }
        _tokenApproveZero(token, address(yVault));

        uint256 afterYTokenBalance = IERC20(address(yVault)).balanceOf(
            address(this)
        );


// Source: contracts/10/contracts/handlers/yearn/HYVault.sol original lines 42-67
    }

    function depositETH(
        uint256 value,
        address vault
    ) external payable returns (uint256) {
        IYVault yVault = IYVault(vault);
        uint256 beforeYTokenBalance = IERC20(address(yVault)).balanceOf(
            address(this)
        );
        // if amount == type(uint256).max return balance of Proxy
        value = _getBalance(address(0), value);
        try yVault.depositETH{value: value}() {} catch Error(
            string memory reason
        ) {
            _revertMsg("depositETH", reason);
        } catch {
            _revertMsg("depositETH");
        }
        uint256 afterYTokenBalance = IERC20(address(yVault)).balanceOf(
            address(this)
        );

        _updateToken(address(yVault));
        return afterYTokenBalance - beforeYTokenBalance;
    }

// Source: contracts/10/specs/harnesses/ProxyHarness.sol original lines 30-36 (literal excerpt)
        return _getSender();
    }

    function getCubeCounter() public view returns (uint256) {
        return _getCubeCounter();
    }
