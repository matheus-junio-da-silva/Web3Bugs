// HELIX Project 15 historical CVL extraction
// Source contracts/15/set.spec property lines 230-242
// Historic syntax unchanged; dependency-incomplete, no CVL2 migration

// Original CVL non-property helpers from contracts/15/set.spec



/**
 * @title get Set array length
 * @dev user should define getFacilitatorsListLen() in Solidity harness file.
 */
methods{
    getFacilitatorsListLen() returns (uint256) envfree
}
/**
* @title max uint256
* @return 2^256-1
*/
definition MAX_UINT256() returns uint256 = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF;
definition MAX_UINT256Bytes32() returns bytes32 = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF; //todo: remove once CERT-1060 is resolved

/**
* @title max address value + 1
* @return 2^160
*/
definition TWO_TO_160() returns uint256 = 0x10000000000000000000000000000000000000000;


/**
* @title Set map entries point to valid array entries
* @notice an essential condition of the set, should hold for evert Set implementation 
* @return true if all map entries points to valid indexes of the array.
*/
definition MAP_POINTS_INSIDE_ARRAY() returns bool = forall bytes32 a. mirrorMap[a] <= mirrorArrayLen;
/**
* @title Set map is the inverse function of set array. 
* @notice an essential condition of the set, should hold for evert Set implementation 
* @notice this condition depends on the other set conditions, but the other conditions do not depend on this condition.
*          If this condition is omitted the rest of the conditions still hold, but the other conditions are required to prove this condition.
* @return true if for every valid index of the array it holds that map(array(index)) == index + 1.
*/
definition MAP_IS_INVERSE_OF_ARRAY() returns bool = forall uint256 i. (i < mirrorArrayLen) => (mirrorMap[mirrorArray[i]]) == to_uint256(i + 1);

/**
* @title Set array is the inverse function of set map
* @notice an essential condition of the set, should hold for evert Set implementation 
* @return true if for every non-zero bytes32 value stored in in the set map it holds that array(map(value) - 1) == value
*/
definition ARRAY_IS_INVERSE_OF_MAP() returns bool = forall bytes32 a. (mirrorMap[a] != 0) => (mirrorArray[to_uint256(mirrorMap[a]-1)] == a);




/**
* @title load array length
* @notice a dummy condition that forces load of array length, using it forces initialization of  mirrorArrayLen
* @return always true
*/
definition CVL_LOAD_ARRAY_LENGTH() returns bool = (getFacilitatorsListLen() == getFacilitatorsListLen());

/**
* @title Set-general condition, encapsulating all conditions of Set 
* @notice this condition recaps the general characteristics of Set. It should hold for all set implementations i.e. AddressSet, UintSet, Bytes32Set
* @return conjunction of the Set three essential properties.
*/
definition SET_INVARIANT() returns bool = MAP_POINTS_INSIDE_ARRAY() && MAP_IS_INVERSE_OF_ARRAY() && ARRAY_IS_INVERSE_OF_MAP() &&  CVL_LOAD_ARRAY_LENGTH(); 

/**
 * @title Size of stored value does not exceed the size of an address type.
 * @notice must be used for AddressSet, must not be used for Bytes32Set, UintSet
 * @return true if all array entries are less than 160 bits.
 **/
definition VALUE_IN_BOUNDS_OF_TYPE_ADDRESS() returns bool = (forall uint256 i. to_uint256(mirrorArray[i]) < TWO_TO_160());

/**
 * @title A complete invariant condition for AddressSet
 * @notice invariant addressSetInvariant proves that this condition holds
 * @return conjunction of the Set-general and AddressSet-specific conditions
 **/
definition ADDRESS_SET_INVARIANT() returns bool = SET_INVARIANT() && VALUE_IN_BOUNDS_OF_TYPE_ADDRESS();

/**
 * @title A complete invariant condition for UintSet, Bytes32Set
 * @notice for UintSet and Bytes2St no type-specific condition is required because the type size is the same as the native type (bytes32) size
 * @return the Set-general condition
 **/
definition UINT_SET_INVARIANT() returns bool = SET_INVARIANT();

/**
 * @title Out of bound array entries are zero
 * @notice A non-essential  condition. This condition can be proven as an invariant, but it is not necessary for proving the Set correctness.
 * @return true if all entries beyond array length are zero
 **/
definition ARRAY_OUT_OF_BOUND_ZERO() returns bool = forall uint256 i. (i >= mirrorArrayLen) => (mirrorArray[i] == 0);

// For CVL use

/**
 * @title ghost mirror map, mimics Set map
 **/
ghost mapping(bytes32 => uint256) mirrorMap{ 
    init_state axiom forall bytes32 a. mirrorMap[a] == 0;
    axiom forall bytes32 a. mirrorMap[a] >= 0 && mirrorMap[a] <= MAX_UINT256(); //todo: remove once https://certora.atlassian.net/browse/CERT-1060 is resolved
    
}

/**
 * @title ghost mirror array, mimics Set array
 **/
ghost mapping(uint256 => bytes32) mirrorArray{
    init_state axiom forall uint256 i. mirrorArray[i] == 0;
    axiom forall uint256 a. mirrorArray[a] & MAX_UINT256Bytes32() == mirrorArray[a];
//    axiom forall uint256 a. to_uint256(mirrorArray[a]) >= 0 && to_uint256(mirrorArray[a]) <= MAX_UINT256(); //todo: remove once CERT-1060 is resolved
//axiom forall uint256 a. to_mathint(mirrorArray[a]) >= 0 && to_mathint(mirrorArray[a]) <= MAX_UINT256(); //todo: use this axiom when cast bytes32 to mathint is supported
}

/**
 * @title ghost mirror array length, mimics Set array length
 * @notice ghost includes an assumption about the array length. 
  * If the assumption were not written in the ghost function it should be written in every rule and invariant.
  * The assumption holds: breaking the assumptions would violate the invariant condition 'map(array(index)) == index + 1'. Set map uses 0 as a sentinel value, so the array cannot contain MAX_INT different values.  
  * The assumption is necessary: if a value is added when length==MAX_INT then length overflows and becomes zero.
 **/
ghost uint256 mirrorArrayLen{
    init_state axiom mirrorArrayLen == 0;
    axiom mirrorArrayLen < TWO_TO_160() - 1; //todo: remove once CERT-1060 is resolved
}


/**
 * @title hook for Set array stores
 * @dev user of this spec must replace _list with the instance name of the Set.
 **/
hook Sstore _facilitatorsList .(offset 0)[INDEX uint256 index] bytes32 newValue (bytes32 oldValue) STORAGE {
    mirrorArray[index] = newValue;
}

/**
 * @title hook for Set array loads
 * @dev user of this spec must replace _list with the instance name of the Set.
 **/
hook Sload bytes32 value _facilitatorsList .(offset 0)[INDEX uint256 index] STORAGE {
    require(mirrorArray[index] == value);
}
/**
 * @title hook for Set map stores
 * @dev user of this spec must replace _list with the instance name of the Set.
 **/
hook Sstore _facilitatorsList .(offset 32)[KEY bytes32 key] uint256 newIndex (uint256 oldIndex) STORAGE {
      mirrorMap[key] = newIndex;
}

/**
 * @title hook for Set map loads
 * @dev user of this spec must replace _list with the instance name of the Set.
 **/
hook Sload uint256 index _facilitatorsList .(offset 32)[KEY bytes32 key] STORAGE {
    require(mirrorMap[key] == index);
}

/**
 * @title hook for Set array length stores
 * @dev user of this spec must replace _list with the instance name of the Set.
 **/
hook Sstore _facilitatorsList .(offset 0).(offset 0) uint256 newLen (uint256 oldLen) STORAGE {
        mirrorArrayLen = newLen;
}

/**
 * @title hook for Set array length load
 * @dev user of this spec must replace _facilitatorsList with the instance name of the Set.
 **/
hook Sload uint256 len _facilitatorsList .(offset 0).(offset 0) STORAGE {
    require mirrorArrayLen == len;
}

/**
 * @title main Set general invariant
 **/
// Required original invariant: contracts/15/set.spec lines 183-189
invariant addressSetInvariant()
    ADDRESS_SET_INVARIANT()


/**
 * @title addAddress() successfully adds an address
 **/

// Exact literal original property follows
rule api_address_contained_after_add()
{
    env e;
    address a;
    requireInvariant addressSetInvariant();
    addAddress(e, a);
    assert contains(e, a);
}

/**
 * @title _removeAddress() succeeds to remove an address if it existed 
 * @notice check set membership using contains()
 **/
