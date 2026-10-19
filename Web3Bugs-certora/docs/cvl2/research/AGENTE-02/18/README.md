# AGENTE-02 — Project 18 / OpenZeppelin — Fase 1 (CVL2)
> **Retorno da revisao 2026-10-19:** contagens e buckets anteriores neste README sao registro da primeira rodada e foram substituidos por properties.csv (50 DOCUMENTED_CANDIDATE exclusivamente lexicais; 131 UNRESOLVED_CANDIDATE). Consultar REVIEW_RESPONSE.md, pdf_page_review.md e source_comparison.csv. Nenhuma equivalencia de jobs/provas demonstrada.


**Somente PESQUISA DOCUMENTAL.** Sem alterações em specs ou Solidity; **SEM COMPILAÇÃO CVL2; SEM PROVER; SEM TESTE CVL1**. Todo estado é PROVISÓRIO; nenhum dos buckets designa resultado de execução.

## Proveniência e baseline
- Web3Bugs `main`: `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3` (HEAD consultado em 2026-10-19).
- PropertyGPT `main`: `687f654c679ed45ab127b7949e2a29c8f5e491b9` (HEAD consultado em 2026-10-19); subdir `certora_projects/openzepplin/`.
- Fonte histórica do PDF: `resources/18/OZ-final-report.pdf` (13 pp, maio–junho 2022). O PDF informa commit OpenZeppelin `109778c`, resolvido via GitHub a `109778c17c7020618ea4e035efb9f0f9b82d43ca`. A ligação individual das specs ao job não está provada.
- Conferência de arquivos Solidity: os Git blobs de `contracts/governance/Governor.sol` e `contracts/token/ERC1155/ERC1155.sol` no snapshot coincidem com os blobs no commit 109778c. Em contrapartida `GovernorBase.spec`, `GovernorCountingSimple.spec`, `RulesInProgress.spec` e `sanity.spec` do catálogo não têm blob idêntico às specs homônimas no certora/ do commit.
- Referência de integridade: `docs/spec_catalog_project_18_integrity.json`; 307 arquivos originais preservados sem edição na origem (histórico do catálogo).

## Inventário reconciliado

**168** declarações ativas em 16 specs + `erc20.spec` auxiliar sem regra. **181** instâncias target-context, 69 complete + 112 incomplete. A expansão de Initializable gera 26 exemplos distintos para 13 declarações e **não pode ser colapsada**. Status original não equivale a executável em CVL2.

| Spec | Complete | Incomplete | Total |
|---|---:|---:|---:|
| AccessControl.spec | 2 | 2 | 4 |
| ERC1155.spec | 41 | 0 | 41 |
| ERC1155Burnable.spec | 6 | 0 | 6 |
| ERC1155Pausable.spec | 8 | 0 | 8 |
| ERC1155Supply.spec | 0 | 4 | 4 |
| ERC20FlashMint.spec | 0 | 1 | 1 |
| ERC20Votes.spec | 0 | 16 | 16 |
| ERC20Wrapper.spec | 0 | 9 | 9 |
| ERC721Votes.spec | 0 | 11 | 11 |
| GovernorBase.spec | 0 | 13 | 13 |
| GovernorCountingSimple.spec | 0 | 8 | 8 |
| GovernorPreventLateQuorum.spec | 0 | 11 | 11 |
| Initializable.spec | 0 | 26 | 26 |
| RulesInProgress.spec | 0 | 2 | 2 |
| TimelockController.spec | 12 | 8 | 20 |
| sanity.spec | 0 | 1 | 1 |
| **Total** | **69** | **112** | **181** |

Resultado do catálogo: 4 `VIOLATED` históricas (por nome de rules GovernorPreventLateQuorum; revisão original, não build atual); 0 `VERIFIED`; demais `NOT_STATED`. Os sete testes de bug injection são **mutantes deliberados**, não sete vulnerabilidades de produção. Não equiparar `Result` a `Detection Outcome`.

## Prioridades e bloqueios
1. **Initializable (133–158):** dois harness contexts flat/múltipla herança não encontrados, setters versionados e visibilidade privada historicamente modificada (PDF pp. 4–6).
2. **ERC1155Supply (60–63):** `exists_wrapper`, mint/burn owner-only e hooks/ghosts sem harness equivalente (PDF p. 9).
3. **Governors (101–132):** divergência entre specs do catálogo e arquivos do commit auditado; alguns harnesses/scripts/patch são recuperáveis no upstream, mas o `GovernorPreventLateQuorumHarness` exato continua não comprovado. Quatro rules historicamente quebradas em revisão de código anterior não implicam vulnerabilidade atual.
4. **Votes (65–100):** getters e delegação/checpoints dependem de ABI exposta historicamente, não satisfeita por mocks atuais só pelo nome.
5. **Timelock (161–180):** methods de `schedule` possuem `bytes32` numa posição cujo Solidity original exige `bytes`; unresolved mesmo quando o catálogo aponta complete. Outros getters internal/private bloqueiam versões-alvo.
6. **Solidity e CVL:** `methods` exige função/visibilidade, summaries recebem receptor diferente por padrão, `sig:` em literais, invariants semicolon condicionais e `mathint`/casts cuidadosamente revisados.

## Documentos produzidos
- `properties.csv`: uma linha por exemplo único com chave (project_id, original_status, example_id), não por label.
- `properties/{complete,incomplete}/N.md`: 181 dossiês com trechos originais imutáveis, hashes, assertion ou limite de inferência, target, risco e plano apenas candidato.
- `patterns/`: riscos técnicos P01–P08, com critérios de aplicabilidade.
- `evidence_register.csv`: referências oficiais A1/A2, fonte GitHub histórica e 181 anchors de código.
- `recovery_manifest.csv`: upstream recuperável individualmente vs harnesses não localizados.
- `QA_REPORT.md`: reconciliação, validações, pendências e decisões para revisão.

## Buckets preliminares
- `UNRESOLVED_CANDIDATE`: 112 (documental, NÃO compilado).
- `DOCUMENTED_CANDIDATE`: 57 (documental, NÃO compilado).
- `INDIRECT_CANDIDATE`: 12 (documental, NÃO compilado).

**Política:** proibição de editar fontes históricas, scripts/configs, qualquer outro Project ID, ou executar migração in-place. Nunca adicionar `require_`, `NONDET`, mocks ou harnesses para fazer a propriedade passar sem evidência histórica. O próximo passo é revisão independente do PR; Fase 2 não autorizada.
