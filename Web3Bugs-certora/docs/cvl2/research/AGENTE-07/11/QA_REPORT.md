# AGENTE-07 — QA Project 11

## Reconciliação contra baseline 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3
- CSV canônico Git blob SHA: `97e20443586540034a4c0305ce1db19b0d2f8cb5`; referências de metadata: 16; exemplos únicos após chave canônica: **16**.
- Complete: **0**; incomplete: **16**; esperados 0/16.
- Diretórios de artefatos de `results/spec` consultados no GitHub: 0 `.spec` complete + 16 `.spec` incomplete, e 16 `N.txt` incomplete.
- Árvore documental publicada no PR #41 (draft); dossiês numerados sem lacunas para os IDs atribuídos, validados novamente após publicação.

## Riscos que impedem promoção para status definitivo
- O catálogo identifica 46 blobs iguais ao branch histórico keep-ecdsa, mas o commit do relatório é distinto e não comparado. O harness pode alterar o vínculo de bond IDs e getters.
- Histórico auditado e módulos transitivos não reconstruídos com prova individual do blob/commit para cada incomplete. Manifesto registra BLOCKED_PROVENANCE, não recuperações fictícias.
- Alguns dossiês incluem um trecho de CVL limitado a ~2.100 caracteres como orientação documental; esse trecho NÃO deve substituir a declaração integral na `.spec` histórica. Revisão independente deve confirmar integralmente assertions, dependencies e bounds antes de Fase 2.
- IDs de padrões referidos nas hipóteses são candidatos sintáticos; `cvl1_cvl2_change_ids` do CSV aponta ao relatório individual, não representa mudança aprovada.

## Validações realmente realizadas
- Leitura via conector GitHub de HEADs Web3Bugs e PropertyGPT: conferidos contra os baselines fornecidos.
- Contagem dos nomes de `.spec`/`.txt` por diretório GitHub e confronto com CSV; deduplicação por (Project ID, Status, Example ID) feita em memória.
- Contraste de exemplos individuais com `.spec`, `.md` e `N.txt` do catálogo, sem reescrita das fontes.
- Exame de documentação oficial Certora CVL2 (link e seção em evidence_register.csv).
- NÃO executados nesta fase: validadores Python do repositório, `git diff --check` local, CVL1, CVL2, Prover, equivalência experimental. **Nenhum exit code é atribuído a comandos não rodados**.

## Encaminhamento
- Antes de qualquer Fase 2: fechamento do commit auditado, comparação ABI/harness, provabilidade dos axiomas e revisão humana de alterações candidatas. Nenhuma autorização de implementação inferida.
- SEM ALTERAÇÕES EM SPECS; SEM COMPILAÇÃO CVL2; SEM PROVER; SEM TESTE CVL1.

## QA complementar de referências CVL2
- `properties.csv` agora contém IDs P-... explícitos para cada dossiê com padrão detectado; IDs derivam das hipóteses documentadas, não representam alterações CVL2 aprovadas. Campo vazio significa sem padrão sinalizado nesta pesquisa, nunca compilação bem-sucedida.


## Integral-source follow-up — 2026-10-19
- Full extracted N.spec and N.txt files inspected for 16/16 examples, without excerpt cutoff. Exact byte hashes and all structural token line anchors in full_spec_audit.csv and each dossier.
- Inspection is static textual and reproducible; not CVL parsing, imported ABI closure, satisfiable model or historical Prover proof. Historical dependency closures remain incomplete.
- Changes are conditional text proposals with source line + A1/A2 link. No sources/historical status modified, and no CVL1/CVL2 run.

## Executed independent checks — WSL / 2026-10-19
Environment: DESKTOP-5E26TVU; clean isolated clone under /home/mat/cvl2-agent07-isolated/Web3Bugs, branch research/cvl2-agente-07, starting HEAD e617417ff27571baa7e008474c55f18c41dc9811.

- python3 Web3Bugs-certora/scripts/check_specs.py Web3Bugs-certora => EXIT 0; 1,386 examples / 1,390 bug-label relationships valid.
- python3 Web3Bugs-certora/scripts/check_contracts.py Web3Bugs-certora => EXIT 0.
- python3 Web3Bugs-certora/scripts/check_contests_csv.py Web3Bugs-certora => EXIT 0.
- bash Web3Bugs-certora/scripts/check_git.sh Web3Bugs-certora => EXIT 0. Initial call with no path was a usage error (EXIT 1), subsequently corrected; no successful result inferred from that first call.
- git diff --check => EXIT 0, after removal of CSV CRLF/trailing Markdown spaces introduced in the working documentation edits.
- Independent canonical-index/hash check => PASS: all 156 rows correspond to a full extracted source SHA-256 and property dossier; all existing properties.csv fields, identity, original_status and historical result unchanged from branch starting HEAD; all changed files in AGENTE-07.
- Three lockfile npm packages independently fetched and SHA-512 verified (P11); 22 directly referenced external import paths found inside those archives. Not proof of nested graph/compiler closure.
- No CVL1, CVL2, Certora Prover, compilation, migration script, or equivalence experiment executed.

**Research gate:** partial historical dependency recovery only. Manual ABI/receiver/summary verification, transitive imports, exact original compiler/harness/run and byte-to-PDF audit linkage remain blocked; no migration or Fase 2 authorization.

## Terceira revisão — correção de whitespace (2026-10-19)

- Baseline oficial: `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`.
- Check CLI original contra `527e3d9d`: `git -c core.whitespace=cr-at-eol diff --check 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3...HEAD` retornou **EXIT 2**, com 15 diagnósticos `space before tab in indent`.
- Commits de correção documentais na mesma branch: `e2478537ebafcb31f2b208004f93fe8112e2631f` e `0dca08521ab6b74c3a87b14f941a5f1e642df1cb`. Somente 10 dossiers de P9/P20; as 15 linhas modificadas mudaram exclusivamente os prefixos de indentação.
- Comparação GitHub antes/depois com `trimStart()` em cada linha: **10/10 dossiês integralmente idênticos após remover indentação**. Nenhuma modificação em specs, contratos, catálogo ou axiomas.
- Auditoria estática independente do diff integral BASE...HEAD exposto pelo GitHub no commit `0dca08521...`: **217 arquivos, 18.605 linhas adicionadas; 0 space-before-tab e 0 trailing whitespace**. É verificação do patch completo, NÃO resultado do processo Git CLI.
- GitHub Actions `validate` na SHA `0dca08521...`, [execução 39325916294](https://github.com/matheus-junio-da-silva/Web3Bugs/actions/runs/39325916294): SUCCESS, com `check_contests_csv`, `check_contracts`, `check_git` completados. Este workflow não substitui o check do diff exigido.
- **Limitação de execução:** o checkout isolado WSL (`DESKTOP-5E26TVU`) ficou offline após a publicação. O comando CLI exato no HEAD corrigido NÃO foi executado nem teve seu exit code observado; não se pode afirmar EXIT 0. A última execução literal observada continua sendo EXIT 2 no HEAD antigo.
- Check CLI de fechamento pendente no checkout atualizado: `git -c core.whitespace=cr-at-eol diff --check 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3...HEAD`.
- Bloqueios históricos continuam unresolved: P9 equivalência ABI/revisões Celo; P8 vacuidade W1/W2/W3; P20 scripts que reescrevem harness, `MAX_INT()` e closure das dependências; P11 imports transitivos e commit auditado. Sem Fase 2, migração CVL2 ou Prover.
