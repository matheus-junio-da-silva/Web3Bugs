# P08 — mathint and bounds

**Authority:** A1-CAST, A2-MATH. CVL2 arithmetic yields mathint. Where the actual property assigns arithmetic to bounded integers or calls Solidity with arithmetic, review type conversions. `assert_uintX` reports out-of-range counterexample, while `require_uintX` discards them; choose neither without proof of the intended specification. Document original range constraints and equivalent behavior before any candidate patch.
