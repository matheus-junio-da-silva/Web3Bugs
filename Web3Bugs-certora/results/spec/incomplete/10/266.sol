// Project 10 example 266; handler HYVault, property noOverwrite. Historical source excerpts only, NOT compilable assembly.
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
