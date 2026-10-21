# AGENTE-02 — Rodada 4 / contrarrevisão independente, somente leitura, do PR #36 (Rocket Joe)

**Data:** 2026-10-20. **PR pesquisado:** [Web3Bugs #36](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/36), branch `research/cvl2-agente-03`, HEAD observada `9c962ac65013903b2f90fe63a106231dbd05549b`. **Nenhuma alteração realizada em branch, docs, specs ou arquivos de AGENTE-03.** Esta contrarrevisão documenta verificações próprias de proveniência, não validação de equivalência.

## Amostra independente de objetos Git (conector GitHub, commits fixados)

| Repositório/commit | Caminho | Git blob SHA-1 confirmado |
|---|---|---|
| `Certora/rocket-joe-1@dba90f9f54e92a6628bd61a6dffb9d7abd9b9c10` | `certora/helpers/erc20.spec` | `b12fec167edd76a2f59a64bc80bc33a9eeb04f65` |
| Mesmo fork | `certora/applyHarness.patch` | `abfb1eae851307c9a3e7d17a7b3e913962952845` |
| Mesmo fork | `certora/scripts/verifyLEVarTran.sh` | `5f71d4e2089bb1bfb78ec812a3458c3fecff71a8` |
| `lfj-gg/rocket-joe@ef2ef30248661b5509c52ab30af9bd0fc07f6657` | `yarn.lock` | `49939a552262aef9fb0aab38f66b594011a99973` |
| Mesmo fork `dba90f9` | `yarn.lock` | `2e5fe995f869eb0f386229a55ef5ef4765d00ccb` |

A leitura independente dos dois `yarn.lock` confirma resolução divergente de `@openzeppelin/contracts`: **4.4.1 no commit auditado e 4.4.2 no fork**, apesar da mesma faixa declarada `^4.4.1`. O script `verifyLEVarTran.sh` contém referência textual a `Owner.sol`. O `erc20.spec` existe no fork e o patch tem o hash anunciado; isso não prova que qualquer um deles participou do run auditado.

## Confronto do registro da branch

Foram lidos da HEAD do PR #36: `historical_closure_resolution.md`, `historical_artifact_provenance.csv`, `historical_run_config_matrix.csv`, `source_provenance_matrix.csv` e a terceira revisão do coordenador. Registros: 55 artefatos (50 não presentes na árvore auditada, três divergentes, dois idênticos), 192 referências estáticas de imports, seis scripts de run, 164 dossiês incompletos. Os hashes de cinco artefatos prioritários conferem com os objetos remotos acima.

**Adjudicação:** fonte candidata e proveniência dos bytes têm suporte; identidade de *run*, compilação, ABI, linking, versão do Prover, patch aplicado durante auditoria e closure de imports **não estão demonstrados**. A aplicação de patch em scratch com `fuzz 2` na cena auditada demonstra tolerância textual, não equivalência de contrato. A documentação do AGENTE-03 preserva corretamente a diferença entre PDF Rocket Joe correto e relatório estranho arquivado no snapshot e não transfere resultado de PDF para specs atuais.

**Limites desta contrarrevisão:** não executei novamente o patch, não abri PDF nesta revisão, não executei Prover nem CVL1/CVL2, não confirmei por recompilação as 192 arestas ou o comando efetivo do auditado. O conjunto amostral de cinco hashes é uma conferência independente de proveniência, não certificação integral das 164 instâncias.

**Conclusão:** nenhum motivo verificado para promover os 164 casos do PR #36 além de `UNRESOLVED_CANDIDATE`. Sinalizar a divergência 4.4.1/4.4.2, script com `Owner.sol` e ausência de manifest de execução como bloqueios efetivos, evitando mocks substitutos.

**AGENTE-02 — RODADA 4 / CONTRARREVISÃO READ-ONLY.**
