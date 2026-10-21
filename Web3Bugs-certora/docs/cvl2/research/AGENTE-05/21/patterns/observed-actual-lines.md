# P21 — patterns observed in complete N.spec inspection

Methodology: exact original/derived lines and minimal candidate text are in the numbered dossiers. No edits to historical .spec, Solidity, configs or snapshot.

## A1-METHODS: 4 actual syntax occurrences

Occurrences: 21/incomplete/1:4, 21/incomplete/1:5, 21/incomplete/2:3, 21/incomplete/2:4.

Official reference: https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html#function-and-required-for-methods-block-entries

## A1-SEMICOLON: 2 actual syntax occurrences

Occurrences: 21/incomplete/1:2, 21/incomplete/2:6.

Official reference: https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html#required-in-more-places

## Negative findings and assumptions
Compilation was not performed. Matching source text is not proof the receiver or ABI is correct. Summary reach, quantified domains, ghost storage, havoc, selector sig, imported ABI, revert paths and mathint casts require review. No require_ additions proposed.
