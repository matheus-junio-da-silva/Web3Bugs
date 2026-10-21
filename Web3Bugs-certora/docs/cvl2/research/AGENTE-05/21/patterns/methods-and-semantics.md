# P21 — padrões de investigação CVL2 (não patches)

- **M21-01/M21-02:** as entradas de `methods` precisam de `function`, `internal` ou `external`, e `;`. Fonte A1-METHOD-ENTRY: https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html#changes-to-methods-block-entries; a escolha de receptor/visibilidade exige prova da ABI e call graph, não inferência automática. Caso concreto: ambas as properties declaram `getGuardianLength`; somente uma usa `getGuardianQuorum` para uma chamada em rule. A ausência do getter não é erro CVL2.
- **M21-03:** `using` exige `;` em CVL2 (A1-USING-SEMICOLON), usado só no exemplo 1. A conversão textual não materializa DSMH.
- **M21-04:** invariantes normalmente terminam com `;`, exceto os que trazem blocos `preserved`/`filtered` subsequentes (A1-INVARIANT-TERMINATOR). Aplica-se a #2 sob inspeção da declaração completa.
- **M21-05 (sem proposta automática):** resguardar `@withrevert` e `lastReverted`: o assert é de não-reversão para entradas arbitrárias; converter em requisição para não reverter ocultaria contraexemplo.

Nenhum pattern autoriza trocar o módulo real pelo harness nem declarar resultado experimental. Fonte de referência: https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html#step-4-review-your-methods-blocks.
