# Direct inspection of Certora PDF pages — Project 21

- Official PDF: https://certora.cdn.prismic.io/certora/e30d7822-bfb8-4781-83b5-8a9ade66ddf6_Certora-Lido-V2-Audit-Report.pdf
- Pages inspected directly (image rendering): p.31-32 (viewer screenshots 30-31)
- Source-specific findings: The 18 DSM properties named in the PDF do NOT include the two cataloged CVL names; agreedRevertsSimple is conditional whereas the archived rule requires non-revert for arbitrary args. Assumptions include beacon-deposit simplification, guardian-array cap and loop unrolling bound 3.
- Archived PDF identity: not established by byte comparison with the currently published Certora PDF. The original project resource was hashed independently; public PDF pages must not be assumed to be exact same revision.
- Audit-result transfer rule: only named formulas with matching assumptions/target can inherit a historical Result; direct page inspection is not a new Prover run.
