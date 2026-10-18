// ORIGINAL HISTORICAL SOLIDITY excerpts; content copied literally from contracts/18
// CVL property: Initializable.spec:109-117 reinitializeLiveness

// Original: contracts/18/contracts/mocks/InitializableMock.sol lines 82-84 function/modifier reinitialize
    function reinitialize(uint8 i) public reinitializer(i) {
        doStuff();
    }

// Original: contracts/18/contracts/proxy/utils/Initializable.sol lines 78-93 function/modifier initializer
    modifier initializer() {
        bool isTopLevelCall = !_initializing;
        require(
            (isTopLevelCall && _initialized < 1) || (!Address.isContract(address(this)) && _initialized == 1),
            "Initializable: contract is already initialized"
        );
        _initialized = 1;
        if (isTopLevelCall) {
            _initializing = true;
        }
        _;
        if (isTopLevelCall) {
            _initializing = false;
            emit Initialized(1);
        }
    }

// Original: contracts/18/contracts/proxy/utils/Initializable.sol lines 107-114 function/modifier reinitializer
    modifier reinitializer(uint8 version) {
        require(!_initializing && _initialized < version, "Initializable: contract is already initialized");
        _initialized = version;
        _initializing = true;
        _;
        _initializing = false;
        emit Initialized(version);
    }

// Original: contracts/18/contracts/proxy/utils/Initializable.sol lines 62-62 state declaration
    uint8 private _initialized;

// Original: contracts/18/contracts/proxy/utils/Initializable.sol lines 67-67 state declaration
    bool private _initializing;

// Original: contracts/18/contracts/mocks/MultipleInheritanceInitializableMocks.sol lines 116-116 state declaration
    ) public initializer {
