// Extracted from: contracts/2/specs/executorV2.spec
// Property: uniqueArray
// Dependency status: incomplete
// Original source ranges included: 3;8;15;23;31;248-293;296-314
// CVL2 migration is intentionally out of scope for this catalog stage.

methods {
    executeEmergencyAction() envfree
    getAssetsLength() returns (uint256) envfree
}

definition tempOmittedFunc(method f) returns bool = f.selector == executeEmergencyAction().selector;

ghost uint256 old_zero_index;
ghost mapping(address => uint256) reverseMap
{
    axiom forall address a. IS_ADDRESS(a) => IS_UINT256(reverseMap[a]);
}
ghost uint256 _assetsLength
{
    init_state axiom _assetsLength == 0;
}
ghost mapping(uint256 => address) mirrorArray;
ghost mapping(address => bool) mirrorFlag
{
    init_state axiom forall address a. IS_ADDRESS(a) => !mirrorFlag[a];
}
hook Sstore _assets.(offset 0) uint256 newLen (uint256 oldLen) STORAGE {
    require _assetsLength == oldLen;
    reverseMap[mirrorArray[to_uint256(oldLen - 1)]] = ((IS_ZERO_ADDRESS(mirrorArray[to_uint256(oldLen - 1)])) && (newLen == to_uint256(oldLen - 1))?old_zero_index:reverseMap[mirrorArray[to_uint256(oldLen - 1)]]);
    _assetsLength = newLen;
}

hook Sload uint256 len _assets.(offset 0) STORAGE {
    require _assetsLength == len;
}
hook Sstore _assets[INDEX uint256 index] address newValue (address oldValue) STORAGE {
    require mirrorArray[index] == oldValue;
    mirrorArray[index] = newValue;
    old_zero_index = (IS_ZERO_ADDRESS(newValue) && index == to_uint256(_assetsLength - 1)? reverseMap[newValue]:old_zero_index);
    reverseMap[newValue] = index;

    }
hook Sload address value _assets[INDEX uint256 index] STORAGE {
    require mirrorArray[index] == value;
}


hook Sstore _assetsState[KEY address a] bool newValue (bool oldValue) STORAGE {
    require mirrorFlag[a] == oldValue;
    mirrorFlag[a] = newValue;
    }
hook Sload bool value _assetsState[KEY address a] STORAGE {
    require mirrorFlag[a] == value;
}

definition IS_UINT256(uint256 x) returns bool = ((x >= 0) && (x <= max_uint256));
definition IS_ADDRESS(address x) returns bool = ((x >= 0) && (x <= max_uint160));
definition IS_ZERO_ADDRESS(address x) returns bool = x == 0;

invariant flagConsistancy()
    (forall address a. IS_ADDRESS(a) => ((mirrorFlag[a] => (((reverseMap[a] < _assetsLength) && (mirrorArray[reverseMap[a]] == a)))))) && (forall uint256 i. IS_UINT256(i) => (i < _assetsLength => (mirrorFlag[mirrorArray[i]])))
    filtered { f -> !tempOmittedFunc(f) }
    {
        preserved{
            requireInvariant uniqueArray();
            require getAssetsLength() < max_uint160 - 1;
        }
    }

/* !!!! Temp filtering until the prover will be updated !!!! */
invariant uniqueArray()
    forall uint256 i. IS_UINT256(i) => (forall uint256 j. IS_UINT256(j) => ((i < _assetsLength && j < _assetsLength) => ( i != j => mirrorArray[i] != mirrorArray[j])))
    filtered { f -> !tempOmittedFunc(f) }
    {
        preserved{
            requireInvariant flagConsistancy();
        }
    }