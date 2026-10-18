// Original: contracts/23/src/Reserve.sol lines 169-182
    /// @param from The address from which funds are deposited.
    /// @param amt The deposited amount.
    function deposit(
        IERC20 token,
        address from,
        uint256 amt
    ) public override onlyUser {
        IReservePlugin plugin = plugins[token];
        require(from != address(plugin) && from != address(this), "Reserve: deposition from self");
        deposited[token] += amt;
        _transfer(token, from, _pluginAddr(plugin), amt);
        if (plugin != NO_PLUGIN) plugin.afterDeposition(token, amt);
        emit Deposited(msg.sender, token, from, amt);
    }

// Original: contracts/23/src/Reserve.sol lines 189-203
    /// @param to The address to which funds are withdrawn.
    /// @param amt The withdrawn amount.
    function withdraw(
        IERC20 token,
        address to,
        uint256 amt
    ) public override onlyUser {
        uint256 balance = deposited[token];
        require(balance >= amt, "Reserve: withdrawal over balance");
        deposited[token] = balance - amt;
        IReservePlugin plugin = plugins[token];
        if (plugin != NO_PLUGIN) plugin.beforeWithdrawal(token, amt);
        _transfer(token, _pluginAddr(plugin), to, amt);
        emit Withdrawn(msg.sender, token, to, amt);
    }
