# Auditoria independente somente leitura — AGENTE-02 / PR #37

**Auditado:** https://github.com/matheus-junio-da-silva/Web3Bugs/pull/37
**HEAD observada:** `3da04efedfe6d75b049b15fa37a040572260eca4`
**Fonte independente:** checkout já existente `/home/mat/cvl2-agente02-revision/repo`; nenhum arquivo alterado, nenhum checkout/branch trocado, nenhum commit publicado no PR #37.

## Verificações executadas somente leitura (2026-10-20)

1. `properties.csv`: **181 chaves distintas** `(original_status,example_id)`: 69 complete + 112 incomplete; buckets 50 `DOCUMENTED_CANDIDATE` e 131 `UNRESOLVED_CANDIDATE`. Conferidos com `results/spec/spec_buglabel.csv` do mesmo checkout: **0 divergências** em Property, Target Contract, Result e Detection Outcome; nenhum dossiê ausente.
2. `abi_resolution_matrix.csv`: **339 linhas**, **0 foreign keys** sem correspondente em `properties.csv`; as 339 registram `runtime_abi_status=NOT_COMPILED_HISTORICAL_ABI_UNKNOWN`. São observações de fonte e grafo de imports, não evidência de ABIs binárias.
3. `source_comparison.csv`: **16 specs** comparadas: 12 `ABSENT_AT_AUDITED_COMMIT` e quatro `CONTENT_DIFFERS` contra `OpenZeppelin/openzeppelin-contracts@109778c17c7020618ea4e035efb9f0f9b82d43ca`. Não foi encontrada neste audit documental uma justificativa para inferir execução histórica equivalendo a cada recorte.
4. `git -c core.whitespace=cr-at-eol diff --check 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3...HEAD`: **exit 0** na HEAD indicada; `git status --porcelain` vazio no checkout do AGENTE-02. Checagem somente leitura.
5. Amostra semântica dirigida: `complete/23`, `ERC1155Mock`, `noTransferEffectOnApproval`. As declarações de `ERC1155` de `isApprovedForAll` e `safeTransferFrom` são `public` na fonte de snapshot, com internal implementation e external wrapper conforme a documentação Certora. O dossiê corretamente deixa ambas alternativas `internal/external` sem resolução; tipos de referência, ABI histórica, modifiers/dispatch e escopo da chamada permanecem condicionais. O source auditado não contém a spec homônima no tree comparado; logo não se pode dar o salto de "documented candidate" a regra experimental.

## Juízo independente

**Sem discrepância estrutural observada na abrangência checada.** A documentação do PR #37 é conservadora quanto a ABI e mantém 0 implementações prontas. Não existe base para liberar CVL2, receiver wildcard, `optional` ou summary específico. A grandeza de 339 observações não fornece 339 vínculos a artefatos ABI reais, e 50 candidatos lexicais não significam 50 specs compiláveis.

Esta é uma revisão independente limitada às tabelas, dossiês amostrados, commit e checks especificados; não é revalidação integral humana das 181 propriedades nem da semântica histórica. **Nenhum arquivo da branch `research/cvl2-agente-02` foi editado.** Recomendo manter Fase 2 bloqueada até fonte exata de harness, patch, ABI/job e grafo de chamadas, com gates individuais.

**AGENTE-01 — RODADA 4 — revisão cruzada, somente leitura.**
