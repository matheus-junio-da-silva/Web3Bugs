// Source: contracts/11/specs/fullyBackedBonding.spec
// Property: validOperator (original lines 104-105)
// Original CVL dependency source lines: 14,15,17,24,28;104-105
// Dependency status: incomplete; historical source syntax kept unchanged.

methods {
    authorizerOf(address) returns address envfree
    beneficiaryOf(address) returns address envfree
    ownerOf(address) returns address envfree
}

invariant validOperator(address operator)
        beneficiaryOf(operator) != 0  <=>  ( operator != 0 && ownerOf(operator) != 0 && authorizerOf(operator) != 0 )
