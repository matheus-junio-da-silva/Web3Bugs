# P07 — multicontract using aliases

**Authority:** A1-USING, A2-METHODS. Check `using ERC20VotesHarness as erc20votes`-type declarations against concrete targets, import propagation and method receiver semantics. The guide says a multicontract using declaration is not imported in CVL2. Only repeat/rename alias where the source actually depends on it; use contract names for user-defined types. No new aliases introduced in Fase 1.
