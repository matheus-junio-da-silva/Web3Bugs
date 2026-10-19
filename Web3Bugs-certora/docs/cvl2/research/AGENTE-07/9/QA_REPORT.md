# AGENTE-07 — QA Project 9

## Reconciliação contra baseline 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3
- CSV canônico Git blob SHA: `97e20443586540034a4c0305ce1db19b0d2f8cb5`; referências de metadata: 61; exemplos únicos após chave canônica: **61**.
- Complete: **50**; incomplete: **11**; esperados 50/11.
- Diretórios de artefatos de `results/spec` consultados no GitHub: 50 `.spec` complete + 11 `.spec` incomplete, e 11 `N.txt` incomplete.
- Árvore documental publicada no PR #41 (draft); dossiês numerados sem lacunas para os IDs atribuídos, validados novamente após publicação.

## Riscos que impedem promoção para status definitivo
- Três rules ativas de governance_old_rules.spec, mesmo com aviso Requires correction; também helpers sem linkage em incomplete, e estados ABI incompatíveis em exemplos específicos.
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
- Full extracted N.spec and N.txt files inspected for 61/61 examples, without excerpt cutoff. Exact byte hashes and all structural token line anchors in full_spec_audit.csv and each dossier.
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
