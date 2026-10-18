// ORIGINAL HISTORICAL SOLIDITY excerpts; content copied literally from contracts/18
// CVL property: AccessControl.spec:15-25 onlyRoleModifierCheckGrant

// Original: contracts/18/contracts/access/AccessControl.sol lines 96-98 function/modifier _checkRole
    function _checkRole(bytes32 role) internal view virtual {
        _checkRole(role, _msgSender());
    }

// Original: contracts/18/contracts/access/AccessControl.sol lines 107-120 function/modifier _checkRole
    function _checkRole(bytes32 role, address account) internal view virtual {
        if (!hasRole(role, account)) {
            revert(
                string(
                    abi.encodePacked(
                        "AccessControl: account ",
                        Strings.toHexString(uint160(account), 20),
                        " is missing role ",
                        Strings.toHexString(uint256(role), 32)
                    )
                )
            );
        }
    }

// Original: contracts/18/contracts/access/AccessControl.sol lines 128-130 function/modifier getRoleAdmin
    function getRoleAdmin(bytes32 role) public view virtual override returns (bytes32) {
        return _roles[role].adminRole;
    }

// Original: contracts/18/contracts/access/AccessControl.sol lines 144-146 function/modifier grantRole
    function grantRole(bytes32 role, address account) public virtual override onlyRole(getRoleAdmin(role)) {
        _grantRole(role, account);
    }

// Original: contracts/18/contracts/access/AccessControl.sol lines 69-72 function/modifier onlyRole
    modifier onlyRole(bytes32 role) {
        _checkRole(role);
        _;
    }

// Original: contracts/18/contracts/access/AccessControl.sol lines 84-86 function/modifier hasRole
    function hasRole(bytes32 role, address account) public view virtual override returns (bool) {
        return _roles[role].members[account];
    }

// Original: contracts/18/contracts/access/AccessControl.sol lines 159-161 function/modifier revokeRole
    function revokeRole(bytes32 role, address account) public virtual override onlyRole(getRoleAdmin(role)) {
        _revokeRole(role, account);
    }

// Original: contracts/18/contracts/access/AccessControl.sol lines 55-55 state declaration
    mapping(bytes32 => RoleData) private _roles;
