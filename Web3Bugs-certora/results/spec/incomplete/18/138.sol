// Historical Solidity excerpts; not a compilable harness.
// Original: contracts/18/contracts/proxy/utils/Initializable.sol lines 8-23 (target context (no matched entrypoint))
/**
 * @dev This is a base contract to aid in writing upgradeable contracts, or any kind of contract that will be deployed
 * behind a proxy. Since proxied contracts do not make use of a constructor, it's common to move constructor logic to an
 * external initializer function, usually called `initialize`. It then becomes necessary to protect this initializer
 * function so it can only be called once. The {initializer} modifier provided by this contract will have this effect.
 *
 * The initialization functions use a version number. Once a version number is used, it is consumed and cannot be
 * reused. This mechanism prevents re-execution of each "step" but allows the creation of new initialization steps in
 * case an upgrade adds a module that needs to be initialized.
 *
 * For example:
 *
 * [.hljs-theme-light.nopadding]
 * ```
 * contract MyToken is ERC20Upgradeable {
 *     function initialize() initializer public {

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

// Original: contracts/18/contracts/mocks/InitializableMock.sol lines 82-105 (callable)
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
}

contract DisableNew is Initializable {
    constructor() {

// Original: contracts/18/contracts/mocks/InitializableMock.sol lines 86-109 (callable)
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
}

contract DisableNew is Initializable {
    constructor() {
        _disableInitializers();
    }
}

// Original: contracts/18/contracts/mocks/InitializableMock.sol lines 90-113 (callable)
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
}

contract DisableNew is Initializable {
    constructor() {
        _disableInitializers();
    }
}

contract DisableOld is Initializable {
    constructor() initializer {}
}

// Original: contracts/18/contracts/mocks/MultipleInheritanceInitializableMocks.sol lines 7-22 (target context (no matched entrypoint))
// Sample contracts showing upgradeability with multiple inheritance.
// Child contract inherits from Father and Mother contracts, and Father extends from Gramps.
//
//         Human
//       /       \
//      |       Gramps
//      |         |
//    Mother    Father
//      |         |
//      -- Child --

/**
 * Sample base intializable contract that is a human
 */
contract SampleHuman is Initializable {
    bool public isHuman;
