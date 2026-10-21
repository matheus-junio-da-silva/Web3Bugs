# AGENTE-04 — QA de segunda revisão independente (2026-10-19)

## Fonte e escopo

- Revisão do coordenador em PR #42 em 2026-10-19, após HEAD `5f90cbea624b5b285aa5b26b26c2cfbb9fa24909`: pesquisa melhorada, três projetos bloqueados para Fase 2.
- Branch existente `research/cvl2-agente-04`; base congelada `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`. Os únicos arquivos modificados pertencem a `Web3Bugs-certora/docs/cvl2/research/AGENTE-04/`.
- Estudos históricos por projeto: `15/HISTORICAL_PACKAGE_CLOSURE.md`, `12/HISTORICAL_HARNESS_COMPARISON.md`, `2/HISTORICAL_ABI_SEARCH.md`; dossiês e `properties.csv` atualizados para 116+26+15 instâncias. Os índices mantêm `proposed_migration_bucket` originais para rastreabilidade, mas acrescentam `phase2_readiness_second_review` explícito (todos unresolved).
- 17 casos completos P12 e 1 completo P2 classificados lexicalmente `01_documented_CANDIDATE` continuam `UNRESOLVED_ABI_TARGET_SEMANTICS`. Outros 139 continuam `UNRESOLVED_HISTORICAL_CLOSURE`.

## Comandos reais no WSL DESKTOP-5E26TVU

Checkout independente: `/tmp/cvl2-agent04-20261019/repo`; diretório de execução dos validadores: `/tmp/cvl2-agent04-20261019/repo/Web3Bugs-certora`.

| Comando exato | Exit code observado | Resultado |
|---|---:|---|
| `python3 scripts/check_specs.py .` | 0 | 1386 spec examples / 1390 relações estruturalmente consistentes |
| `python3 scripts/check_contests_csv.py .` | 0 | contests.csv consistente com reports |
| `python3 scripts/check_contracts.py .` | 0 | contracts consistente com reports |

Em `/tmp/cvl2-agent04-20261019/repo`, `git diff --check` retornou **0** na worktree, antes de commit; lista de caminhos modificados fora do diretório autorizado: **0**. Depois da publicação, rodar também `git diff --check 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3 HEAD` para validar o diff completo da base, incluindo commits anteriores.

Os validadores verificam apenas integridade estrutural do dataset, **não** ABI, compiler, proof outcomes, Prover ou equivalência semântica CVL1/CVL2.

## Evidências reproduzíveis e limites

- GHO: `package-lock.json` de `aave/gho-core@ce49fb0c94cfebf0159222ceb288e4f9a55d305f` fixa core-v3 1.17.2, periphery-v3 2.0.1, OZ contracts 4.8.1. Tarballs públicos das três versões recuperados e comparados por SHA512 SRI com lock; correspondência positiva; SHA256 dos arquivos registrado em estudo. Trata-se de **checksum de distribuição**, não instalação/compilação. O patch/munged pode mudar comportamento Solidity; runtime indisponível.
- AAVE V2: commit auditado `750920303e33b66bc29862ea3b85206dda9ce786` possui construtor historical diferente do snapshot. Scripts de época mostram `--solc solc6.8`, sem resolução comprovada do binário; sem reconstrução de harness com outra variante.
- Proof of Reserve: `12296ce4c6f9bde6663e1baa02cf19f179c1048b` tem fontes centrais coincidentes, mas as implementações dos helpers CVL, receivers dummy e configuração Prover não foram encontradas nas árvores e buscas delimitadas. Resultados agregados do PDF não provam status da instância extraída.
- PDF e N.md: pesquisa documental de 13/25/6 páginas e os 157 N.md foi feita na etapa anterior; as menções antigas a não leitura são registros da primeira coleta e foram explicitamente superadas. Preservar por property a diferença entre correspondência nominal e prova executada.
- Fontes esgotadas nesta rodada: tree auditado, snapshot, scripts, reports, N.md/N.txt e busca de símbolos específicos; **negativa local não prova inexistência absoluta**. Não foi fabricada versão ou log de Prover.

**Executado nesta rodada:** leitura/checagem documental, hashes de arquivo e validadores Python. **Proibido e não executado:** Certora Prover, CVL1, compilação CVL2, compilação Solidity, alterações em specs, contratos, configs ou catálogo original, merge e Fase 2.

**Decisão:** manter PR #42 Draft; Fase 1 encerrada nesta rodada por limites da evidência; aguardar parecer do coordenador. Alerta **LARANJA** devido à ausência de fecho histórico/ABI.
