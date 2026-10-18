// ORIGINAL HISTORICAL SOLIDITY excerpts; content copied literally from contracts/18
// CVL property: AccessControl.spec:45-57 grantRoleEffect

// Original: contracts/18/contracts/access/AccessControl.sol lines 84-86 function/modifier hasRole
    function hasRole(bytes32 role, address account) public view virtual override returns (bool) {
        return _roles[role].members[account];
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

// Original: contracts/18/contracts/access/AccessControl.sol lines 159-161 function/modifier revokeRole
    function revokeRole(bytes32 role, address account) public virtual override onlyRole(getRoleAdmin(role)) {
        _revokeRole(role, account);
    }

// Original: contracts/18/contracts/access/AccessControl.sol lines 55-55 state declaration
    mapping(bytes32 => RoleData) private _roles;
