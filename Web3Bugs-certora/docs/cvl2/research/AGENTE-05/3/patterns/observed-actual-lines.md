# P3 — patterns observed in complete N.spec inspection

Methodology: exact original/derived lines and minimal candidate text are in the numbered dossiers. No edits to historical .spec, Solidity, configs or snapshot.

## A1-METHODS: 15 actual syntax occurrences

Occurrences: 3/incomplete/1:10, 3/incomplete/1:11, 3/incomplete/1:12, 3/incomplete/1:13, 3/incomplete/1:14, 3/incomplete/1:15, 3/incomplete/2:11, 3/incomplete/2:12, 3/incomplete/2:13, 3/incomplete/2:14, 3/incomplete/2:15, 3/incomplete/2:16, 3/incomplete/3:9, 3/incomplete/3:10, 3/incomplete/3:11.

Official reference: https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html#function-and-required-for-methods-block-entries

## A1-SELECTOR: 1 actual syntax occurrences

Occurrences: 3/incomplete/2:24.

Official reference: https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html#method-literals-require-sig

## A1-SEMICOLON: 6 actual syntax occurrences

Occurrences: 3/incomplete/1:7, 3/incomplete/1:8, 3/incomplete/2:7, 3/incomplete/2:8, 3/incomplete/2:9, 3/incomplete/3:7.

Official reference: https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html#required-in-more-places

## Negative findings and assumptions
Compilation was not performed. Matching source text is not proof the receiver or ABI is correct. Summary reach, quantified domains, ghost storage, havoc, selector sig, imported ABI, revert paths and mathint casts require review. No require_ additions proposed.
