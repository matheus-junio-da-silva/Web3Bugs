// Extracted from: contracts/2/specs/executorV3.spec
// Property: flagConsistancy
// Dependency status: incomplete
// Original source ranges included: 4;9;15;16;17;26;28;259-332;335-343
// CVL2 migration is intentionally out of scope for this catalog stage.

methods {
    executeEmergencyAction() envfree
    getAssetState(address) returns (bool) envfree
    getAssetsLength() returns (uint256) envfree
    getAsset(uint256) returns (address) envfree
}

definition tempOmittedFunc(method f) returns bool = f.selector == executeEmergencyAction().selector;

ghost mapping(uint256 => address) indexSetArrayFlag;
ghost mapping(address => uint256) indexSetShortcutFlag;
ghost mapping(address => bool) mirrorInitFlag;
ghost uint256 setLengthFlag;
ghost bool Consistant_flag;

ghost mapping(uint256 => uint256) indexSetArray;
ghost mapping(uint256 => uint256) indexSetShortcut;
ghost mapping(address => uint256) reverseMapInit;
ghost uint256 setLength;
ghost bool OneToOne_arrOfTokens;

ghost mapping(uint256 => address) mirrorInitArray;
ghost mapping(address => uint256) reverseMap;
ghost uint256 assetInitLength;

hook Sstore _assets[INDEX uint256 index] address newValue (address oldValue) STORAGE {

    // this is for the require that the _assets array is unique 
    uint256 shortcutIndex = indexSetShortcut[index];
    bool firstAccess = (shortcutIndex >= setLength) || indexSetArray[shortcutIndex] != index;
    indexSetShortcut[index] = firstAccess?setLength:indexSetShortcut[index];
    indexSetArray[setLength] = index;
    setLength = setLength + (firstAccess?to_uint256(1):to_uint256(0));
    require (OneToOne_arrOfTokens && firstAccess) => (reverseMapInit[oldValue] == index);
    //end

    require (Consistant_flag && firstAccess) => (mirrorInitFlag[oldValue]);
    require firstAccess => mirrorInitArray[index] == oldValue;
    reverseMap[newValue] = index;
    }
hook Sload address value _assets[INDEX uint256 index] STORAGE {

    //this is for the require that the _assets array is unique 
    uint256 shortcutIndex = indexSetShortcut[index];
    bool firstAccess = (shortcutIndex >= setLength) || indexSetArray[shortcutIndex] != index;
    indexSetShortcut[index] = firstAccess?setLength:indexSetShortcut[index];
    indexSetArray[setLength] = index;
    setLength = setLength + (firstAccess?to_uint256(1):to_uint256(0));
    require (OneToOne_arrOfTokens && firstAccess) => (reverseMapInit[value] == index);
    //end

    require (Consistant_flag && firstAccess) => (mirrorInitFlag[value]);
    require firstAccess => mirrorInitArray[index] == value;
}


hook Sstore _assetsState[KEY address a] bool newValue (bool oldValue) STORAGE {

    //this is for the require that the validator array is unique 
    uint256 shortcutIndex = indexSetShortcutFlag[a];
    bool firstAccess = (shortcutIndex >= setLengthFlag) || indexSetArrayFlag[shortcutIndex] != a;
    indexSetShortcutFlag[a] = firstAccess?setLengthFlag:indexSetShortcutFlag[a];
    indexSetArrayFlag[setLengthFlag] = a;
    setLengthFlag = setLengthFlag + (firstAccess?to_uint256(1):to_uint256(0));
    require firstAccess => (mirrorInitFlag[a] == oldValue);
    require (Consistant_flag && firstAccess && oldValue) => (reverseMapInit[a] < assetInitLength);
    require (Consistant_flag && firstAccess && oldValue) => mirrorInitArray[reverseMapInit[a]] == a;
    //end

    }
hook Sload bool value _assetsState[KEY address a] STORAGE {

    //this is for the require that the validator array is unique 
    uint256 shortcutIndex = indexSetShortcutFlag[a];
    bool firstAccess = (shortcutIndex >= setLengthFlag) || indexSetArrayFlag[shortcutIndex] != a;
    indexSetShortcutFlag[a] = firstAccess?setLengthFlag:indexSetShortcutFlag[a];
    indexSetArrayFlag[setLengthFlag] = a;
    setLengthFlag = setLengthFlag + (firstAccess?to_uint256(1):to_uint256(0));
    require firstAccess => (mirrorInitFlag[a] == value);
    require (Consistant_flag && firstAccess && value) => (reverseMapInit[a] < assetInitLength);
    require (Consistant_flag && firstAccess && value) => mirrorInitArray[reverseMapInit[a]] == a;
    //end
}

invariant flagConsistancy(uint256 i)
    i < getAssetsLength() => getAssetState(getAsset(i))
    filtered { f -> !tempOmittedFunc(f) }
    {
        preserved{
            require OneToOne_arrOfTokens && (setLength == 0);
            require Consistant_flag && setLengthFlag == 0;
        }
    }
