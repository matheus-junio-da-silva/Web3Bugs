// Origin OUSD historical CVL, extracted WITHOUT changing original rule/invariant text.
// Source: contracts/19/spec/math.spec lines 38-49; target: Dummy

definition divPrecisely(mathint x, mathint y) returns mathint 
	= x*1000000000000000000 / y ;

definition MAX_UINT256() returns uint 
	= 115792089237316195423570985008687907853269984665640564039457584007913129639935 ;

definition MAX_SUPPLY() returns uint
	= 340282366920938463463374607431768211455 ; // 2^128 - 1

rule mathOfChangeSupply(uint T, uint NR, uint RC) {
	require T <= MAX_SUPPLY();
	require T > 0 && NR > 0 && T > NR;
	require RC > 0; // is this reasonable?
	
	mathint RCPT = divPrecisely(RC, (T - NR));
	require RCPT <= MAX_UINT256();
	
	mathint T2 = divPrecisely(RC, RCPT) + NR;
	
	assert T2 <= T || T2 == NR;
}
