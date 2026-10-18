// Historical Solidity excerpts; not a compilable harness.
// Original: contracts/18/contracts/proxy/utils/Initializable.sol lines 23-46 (callable)
 *     function initialize() initializer public {
 *         __ERC20_init("MyToken", "MTK");
 *     }
 * }
 * contract MyTokenV2 is MyToken, ERC20PermitUpgradeable {
 *     function initializeV2() reinitializer(2) public {
 *         __ERC20Permit_init("MyToken");
 *     }
 * }
 * ```
 *
 * TIP: To avoid leaving the proxy in an uninitialized state, the initializer function should be called as early as
 * possible by providing the encoded function call as the `_data` argument to {ERC1967Proxy-constructor}.
 *
 * CAUTION: When used with inheritance, manual care must be taken to not invoke a parent initializer twice, or to ensure
 * that all initializers are idempotent. This is not verified automatically as constructors are by Solidity.
 *
 * [CAUTION]
 * ====
 * Avoid leaving a contract uninitialized.
 *
 * An uninitialized contract can be taken over by an attacker. This applies to both a proxy and its implementation
 * contract, which may impact the proxy. To prevent the implementation contract from being used, you should invoke
 * the {_disableInitializers} function in the constructor to automatically lock it when it is deployed:

// Original: contracts/18/contracts/mocks/InitializableMock.sol lines 16-39 (callable)
    function initialize() public initializer {
        initializerRan = true;
    }

    function initializeOnlyInitializing() public onlyInitializing {
        onlyInitializingRan = true;
    }

    function initializerNested() public initializer {
        initialize();
    }

    function onlyInitializingNested() public initializer {
        initializeOnlyInitializing();
    }

    function initializeWithX(uint256 _x) public payable initializer {
        x = _x;
    }

    function nonInitializable(uint256 _x) public payable {
        x = _x;
    }

// Original: contracts/18/contracts/mocks/InitializableMock.sol lines 24-47 (callable)
    function initializerNested() public initializer {
        initialize();
    }

    function onlyInitializingNested() public initializer {
        initializeOnlyInitializing();
    }

    function initializeWithX(uint256 _x) public payable initializer {
        x = _x;
    }

    function nonInitializable(uint256 _x) public payable {
        x = _x;
    }

    function fail() public pure {
        require(false, "InitializableMock forced failure");
    }
}

contract ConstructorInitializableMock is Initializable {
    bool public initializerRan;
    bool public onlyInitializingRan;

// Original: contracts/18/contracts/mocks/InitializableMock.sol lines 54-77 (callable)
    function initialize() public initializer {
        initializerRan = true;
    }

    function initializeOnlyInitializing() public onlyInitializing {
        onlyInitializingRan = true;
    }
}

contract ChildConstructorInitializableMock is ConstructorInitializableMock {
    bool public childInitializerRan;

    constructor() initializer {
        childInitialize();
    }

    function childInitialize() public initializer {
        childInitializerRan = true;
    }
}

contract ReinitializerMock is Initializable {
    uint256 public counter;

// Original: contracts/18/contracts/mocks/InitializableMock.sol lines 78-101 (callable)
    function initialize() public initializer {
        doStuff();
    }

    function reinitialize(uint8 i) public reinitializer(i) {
        doStuff();
    }

    function nestedReinitialize(uint8 i, uint8 j) public reinitializer(i) {
        reinitialize(j);
    }

    function chainReinitialize(uint8 i, uint8 j) public {
        reinitialize(i);
        reinitialize(j);
    }

    function disableInitializers() public {
        _disableInitializers();
    }

    function doStuff() public onlyInitializing {
        counter++;
    }

// Original: contracts/18/contracts/mocks/SingleInheritanceInitializableMocks.sol lines 14-37 (callable)
    function initialize(uint256 value) public payable initializer {
        x = value;
    }
}

/**
 * @title MigratableMockV2
 * @dev This contract is a mock to test migratable functionality with params
 */
contract MigratableMockV2 is MigratableMockV1 {
    bool internal _migratedV2;
    uint256 public y;

    function migrate(uint256 value, uint256 anotherValue) public payable {
        require(!_migratedV2);
        x = value;
        y = anotherValue;
        _migratedV2 = true;
    }
}

/**
 * @title MigratableMockV3
 * @dev This contract is a mock to test migratable functionality without params
