# Direct inspection of Certora PDF pages — Project 3

- Official PDF: https://certora.cdn.prismic.io/certora/c235edb3-0af1-4293-817f-ff039c4e6c71_Rescue-Mission-Phase-1.pdf
- Pages inspected directly (image rendering): p.4-5 (viewer screenshot indices 3-4)
- Source-specific findings: LendIsBackedByAave appears violated in some reviewed version, LendIsBackedByAaveIncInitialize and StkAaveIsBackedByAave appear verified; report names 4c59da8d and later fixes and limits. Property 2 refers to a coordinated two-step initialization, not arbitrary intermediate states.
- Archived PDF identity: not established by byte comparison with the currently published Certora PDF. The original project resource was hashed independently; public PDF pages must not be assumed to be exact same revision.
- Audit-result transfer rule: only named formulas with matching assumptions/target can inherit a historical Result; direct page inspection is not a new Prover run.
