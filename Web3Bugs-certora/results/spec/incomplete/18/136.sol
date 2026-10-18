// ORIGINAL HISTORICAL SOLIDITY excerpts; content copied literally from contracts/18
// CVL property: Initializable.spec:49-55 initOnce

// Original: contracts/18/contracts/mocks/InitializableMock.sol lines 16-18 function/modifier initialize
    function initialize() public initializer {
        initializerRan = true;
    }

// Original: contracts/18/contracts/mocks/InitializableMock.sol lines 54-56 function/modifier initialize
    function initialize() public initializer {
        initializerRan = true;
    }

// Original: contracts/18/contracts/mocks/InitializableMock.sol lines 78-80 function/modifier initialize
    function initialize() public initializer {
        doStuff();
    }

// Original: contracts/18/contracts/mocks/SingleInheritanceInitializableMocks.sol lines 14-16 function/modifier initialize
    function initialize(uint256 value) public payable initializer {
        x = value;
    }

// Original: contracts/18/contracts/mocks/MultipleInheritanceInitializableMocks.sol lines 24-26 function/modifier initialize
    function initialize() public initializer {
        __SampleHuman_init();
    }

// Original: contracts/18/contracts/mocks/MultipleInheritanceInitializableMocks.sol lines 45-47 function/modifier initialize
    function initialize(uint256 value) public virtual initializer {
        __SampleMother_init(value);
    }

// Original: contracts/18/contracts/mocks/MultipleInheritanceInitializableMocks.sol lines 67-69 function/modifier initialize
    function initialize(string memory value) public virtual initializer {
        __SampleGramps_init(value);
    }

// Original: contracts/18/contracts/mocks/MultipleInheritanceInitializableMocks.sol lines 89-91 function/modifier initialize
    function initialize(string memory _gramps, uint256 _father) public initializer {
        __SampleFather_init(_gramps, _father);
    }

// Original: contracts/18/contracts/proxy/utils/Initializable.sol lines 62-62 state declaration
    uint8 private _initialized;

// Original: contracts/18/contracts/proxy/utils/Initializable.sol lines 67-67 state declaration
    bool private _initializing;

// Original: contracts/18/contracts/mocks/MultipleInheritanceInitializableMocks.sol lines 116-116 state declaration
    ) public initializer {
