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

// Original: contracts/18/contracts/mocks/MultipleInheritanceInitializableMocks.sol lines 24-47 (callable)
    function initialize() public initializer {
        __SampleHuman_init();
    }

    // solhint-disable-next-line func-name-mixedcase
    function __SampleHuman_init() internal onlyInitializing {
        __SampleHuman_init_unchained();
    }

    // solhint-disable-next-line func-name-mixedcase
    function __SampleHuman_init_unchained() internal onlyInitializing {
        isHuman = true;
    }
}

/**
 * Sample base intializable contract that defines a field mother
 */
contract SampleMother is Initializable, SampleHuman {
    uint256 public mother;

    function initialize(uint256 value) public virtual initializer {
        __SampleMother_init(value);
    }

// Original: contracts/18/contracts/mocks/MultipleInheritanceInitializableMocks.sol lines 45-68 (callable)
    function initialize(uint256 value) public virtual initializer {
        __SampleMother_init(value);
    }

    // solhint-disable-next-line func-name-mixedcase
    function __SampleMother_init(uint256 value) internal onlyInitializing {
        __SampleHuman_init();
        __SampleMother_init_unchained(value);
    }

    // solhint-disable-next-line func-name-mixedcase
    function __SampleMother_init_unchained(uint256 value) internal onlyInitializing {
        mother = value;
    }
}

/**
 * Sample base intializable contract that defines a field gramps
 */
contract SampleGramps is Initializable, SampleHuman {
    string public gramps;

    function initialize(string memory value) public virtual initializer {
        __SampleGramps_init(value);

// Original: contracts/18/contracts/mocks/MultipleInheritanceInitializableMocks.sol lines 67-90 (callable)
    function initialize(string memory value) public virtual initializer {
        __SampleGramps_init(value);
    }

    // solhint-disable-next-line func-name-mixedcase
    function __SampleGramps_init(string memory value) internal onlyInitializing {
        __SampleHuman_init();
        __SampleGramps_init_unchained(value);
    }

    // solhint-disable-next-line func-name-mixedcase
    function __SampleGramps_init_unchained(string memory value) internal onlyInitializing {
        gramps = value;
    }
}

/**
 * Sample base intializable contract that defines a field father and extends from gramps
 */
contract SampleFather is Initializable, SampleGramps {
    uint256 public father;

    function initialize(string memory _gramps, uint256 _father) public initializer {
        __SampleFather_init(_gramps, _father);

// Original: contracts/18/contracts/mocks/MultipleInheritanceInitializableMocks.sol lines 89-112 (callable)
    function initialize(string memory _gramps, uint256 _father) public initializer {
        __SampleFather_init(_gramps, _father);
    }

    // solhint-disable-next-line func-name-mixedcase
    function __SampleFather_init(string memory _gramps, uint256 _father) internal onlyInitializing {
        __SampleGramps_init(_gramps);
        __SampleFather_init_unchained(_father);
    }

    // solhint-disable-next-line func-name-mixedcase
    function __SampleFather_init_unchained(uint256 _father) internal onlyInitializing {
        father = _father;
    }
}

/**
 * Child extends from mother, father (gramps)
 */
contract SampleChild is Initializable, SampleMother, SampleFather {
    uint256 public child;

    function initialize(
        uint256 _mother,
