# AGENTE-04 — QA / Project 2

- Conferência GitHub main `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`, 2026-10-19.
- 15 CSV rows, 15 chaves `(2,status,id)`, 15 arquivos CVL individuais lidos pelo conector, dossiês 15. 1 complete/14 incomplete.
- 18 evidências registradas; 14 motivos de incomplete encaminhados por links N.txt históricos, **sem recuperação comprovada**.
- `N.md`, `N.txt` e original PDF não relidos integralmente nesta rodada automatizada; transcrição e catálogos são fontes auxiliares, limitação aberta para revisão independente.
- QA executado: contagem de linhas e sucesso de leitura de 15 arquivos .spec, metadados do catálogo, chaves únicas. Não executados validadores GitHub/worktree, git diff --check, CLI, CVL2, Prover, nem teste CVL1.
- Status estritamente candidatos, necessidade de inspeção de PDF/harness e prova semântica em fase autorizada posterior.

## Contrarrevisao 2026-10-19
PDF p.1 indica commit 12296ce agora resolvido integralmente. Quatro Solidity do snapshot coincidem byte-a-byte com commit auditado; tree nao contem specs/auxiliares CVL. PDF summary arbitario e invariants agregadas nao individualizadas sem origem CVL.

Dossies atualizados 15/15; entradas methods por instancia 50; nomes literais encontrados em PDF 10. Propostas report-only e condicionais; nao houve compilacao, Prover, teste CVL1 ou modificacao de fonte. Buscas negativas nao demonstram inexistencia fora da arvore examinada.


## Validação estrutural em WSL após contrarrevisão — execução efetiva

A afirmação antiga de que o desktop estava indisponível e de que os validadores não tinham sido executados descreve SOMENTE a primeira entrega; está **superada** pela retomada de 2026-10-19. Device remoto DESKTOP-5E26TVU online; checkout isolado em /tmp/cvl2-agent04-20261019/repo (não interfere nos demais agentes).

Diretório de execução dos três validadores: /tmp/cvl2-agent04-20261019/repo/Web3Bugs-certora
- python3 scripts/check_specs.py . — exit 0; saída: Check passed! 1386 spec examples and 1390 Bug Label relationships are structurally consistent.
- python3 scripts/check_contests_csv.py . — exit 0; saída: Check passed! results/contests.csv consistent with reports.
- python3 scripts/check_contracts.py . — exit 0; saída: Check passed! contracts consistent with reports.

Diretório de execução Git: /tmp/cvl2-agent04-20261019/repo
- git diff --check — após normalizar exclusivamente docs/cvl2/research/AGENTE-04, exit 0. O diff inicial contra base detectou whitespace nos dossiês originais; foi sanado APENAS em documentos.
- O comando git diff --check origin/main...HEAD falhou com exit 128 por clone --single-branch sem ref origin/main. Não é resultado negativo do dataset. Para comparação final usar explicitamente o commit base 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3 e o novo SHA, cujo exit deve ser registrado após publicação.

Nota sobre QA: o uso de 1386/1390 é a contagem da main congelada; os índices adicionais de pesquisa (157 chaves) não alteram o catálogo. Nenhuma execução de certoraRun, solc, CVL1, CVL2 ou Prover. Os status históricos continuam intocados.

## Segunda auditoria do coordenador (2026-10-19)
As observacoes antigas de que N.md e PDF nao haviam sido revisitados refletem a PRIMEIRA etapa: 100% dos N.md desta familia foram lidos na etapa posterior, com SHA256 e contexto em dossies, e todas as paginas PDF extraidas (P15 13; P12 25; P2 6). Estudo de pacote/harness/ABI atualizado no diretorio deste projeto. Os indices distinguem SINTAXE, ABI, DEPENDENCIA e RISCO SEMANTICO para cada propriedade. Nao promover DOCUMENTED a READY.
