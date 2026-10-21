# CVL2 — Revisão independente após a Rodada 10 / próximos prompts

**Data de referência:** 2026-10-20 (America/Sao_Paulo). **Natureza:** evidência, QA e encaminhamento; não migração. **Base histórica imutável:** `main@2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`.  
**Referências de coordenação:** `ROUND9_DASHBOARD.md`, `ROUND9_ATTEMPT_EVENTS.csv`, `scripts/check_cvl2_round9_events.py` e oito PRs de pesquisa #39/#37/#36/#42/#40/#38/#41/#43; derivado P19 #46.

## 1. Constatações de auditoria com fonte e limite

- O catálogo histórico tem **23 projetos, 1.386 chaves de propriedades e 1.390 relações Bug Label**. O ledger consolidado R9 soma **33 eventos** atribuídos a **20 propriedades distintas**, com **11 COMPILE_OK**, **21 COMPILE_ERROR**, **1 SETUP_ERROR**, interseção de 7 e **1.366 sem teste observado**. Nenhum evento demonstra equivalência CVL1→CVL2.
- O PR #49 de coordenação já está merged e o PR #46 permanece DRAFT e classificado `02_unresolved`. Os oito PRs de pesquisa permanecem DRAFT; seus arquivos alterados estão limitados a `docs/cvl2/research/AGENTE-XX/` no levantamento de 20/10, com workflow GitHub `validate` successful nas HEADs consultadas. Isso é **integridade estrutural**, não verificação semântica.
- Durante a R10, relatos de `EIO`/falha de importação de Python no WSL aparecem em `ROUND10_QA.md` dos agentes 01, 02 e 07. **Suspender novas operações no host até comprovação de saúde pelo administrador.** CI remota não substitui os quatro checks locais registrados como `NOT_RUN_INFRA_EIO`.
- **Falha objetiva corrigida nesta proposta de coordenação:** `AG01_34` em `ROUND9_ATTEMPT_EVENTS.csv` usava um `candidate_sha256` incompleto (61 caracteres). `AGENTE-01/ROUND9_DIAGNOSTICS.csv` e `ROUND9_EVIDENCE.md` preservam o derivado correto: `6e27246dc38c51f16c5777b766e2f449531610109e00f5f0590b09e1d00e3e54`. O verificador anterior só rejeitava caracteres inválidos **se** o comprimento fosse 64; a correção rejeita comprimentos diferentes de 64, excetuando sentinelas documentais explícitas. Adicionados testes negativos para valor curto, maiúsculas, sentinela inválida para origem e string vazia. Isto **não é execução Certora nova**.
- **Decisão:** não dar APPROVE nem MERGE a #36–#43 ou #46 como migração. `COMPILE_OK` em fragmento/derivado, Solidity ABI, ou evidência documental de commit não comprovam identidade de runner, domínio, summaries, reverts, satisfatibilidade, universo de métodos e propriedades globais. Nenhuma propriedade pode ser promovida de `02_unresolved` sem gate semântico individual.

## 2. Protocolo obrigatório para TODOS os agentes

1. Trabalhe **somente em sua branch e pasta `Web3Bugs-certora/docs/cvl2/research/AGENTE-XX/`**, mantendo `contracts/`, `results/spec/`, `reports/`, `results/cvl2/` e CSV canônico byte-idênticos. Não faça merge, push de outra branch, reset/rebase nem edite worktrees de colegas. Não altere `N.spec`, `N.sol`, `N.md` históricos para adequar CVL2.
2. Leia integralmente `docs/spec_catalog.md`, `docs/spec_catalog_workflow.md`, `docs/spec_catalog_project_1.md`, `docs/standard.md`, o relatório histórico e os dossiês da(s) propriedade(s) designada(s); **siga a trilha de source, snapshots, harness, dependências, target, métodos e report sem inferências otimistas**.
3. **EIO é STOP**: se Python, Git, leitura ou filesystem retornar `EIO`/`EROFS`/`SIGBUS`, interrompa imediatamente operações locais, **inclusive testes e escrita**. Registre `NOT_RUN_INFRA_BLOCKED` sem exit code e use apenas consulta por GitHub. Não tente reparar, resetar ou substituir arquivos do host. Retome somente após recuperação comprovada por administrador.
4. Preserve separadamente fatos documentais, inferências, `COMPILE_OK` parcial, `COMPILE_ERROR` CVL2, `SETUP_ERROR`, `NOT_RUN` e `SEMANTIC_UNRESOLVED`. Não conte reexecuções como novas properties; fonte original e derivada são eventos distintos.
5. Quando o host voltar a ficar íntegro e o coordenador autorizar um teste **específico**, use scratch isolado, input hashado, versões/flags exatas, mapeamento de contrato/ABI e logs integrais com SHA256. `--compilation_steps_only` não é Prover; preserve `require`, `assert`, `@withrevert`, `method f`, `envfree`, summaries e comportamento de divisão por zero. Sem autorização, faça apenas pesquisa documental.
6. Feche a próxima entrega com matriz CSV por chave canônica, dossiê individual de provas/lacunas, `EVIDENCE.md`, `QA.md`, hashes e paths; reporte exatamente comandos executados ou `NOT_RUN`. Após recuperação, execute na HEAD exata os três validadores `check_specs.py`, `check_contests_csv.py`, `check_contracts.py` e `git -c core.whitespace=cr-at-eol diff --check BASE...HEAD`. Registre HEAD, stdout, stderr, exit, QA GitHub e escopo do diff.
7. **Critério de aprovação:** relatório do auditor e target/runner históricos vinculados por evidência, closure transitiva completa, compatibilidade ABI+Solidity+harness, transformação mínima reproduzível/reversível, ausência de fortalecimento/enfraquecimento silencioso de hipóteses e comparação semântica independente. Se faltar um gate, deixar `UNRESOLVED_CANDIDATE` ou `02_unresolved`.

## 3. Prompts específicos e executáveis para a próxima rodada

### AGENTE-01 — P10 Furucombo (PR #39, 266 properties)

> Revise `complete/10/33` e `34` após a R10. Documente a origem histórica **real** de `lastHasThrown` de #33 na spec global e explique o erro de typechecker sem inventar ghost; para #34, modele o ramo descartado por `require false` e mostre condições sob as quais a assertion restante é não-vácua. Confronte cada método de `LibParamHarness.sol` 2021 com o receiver/public/external e snapshots pós-Perl, sem confundir o driver LibParam com os runners HMaker. Preserve a versão do hash derivado de #34 no registro `ROUND9_DIAGNOSTICS.csv` e verifique que o ledger central agora usa o mesmo valor. Entregue matriz de lacunas (full spec, handlers ABI, Perl 18/116, selectors, semântica), uma avaliação explicitamente `NOT_PROVEN`, QA R10/R11 honesto e um próximo experimento **proposto, não executado sem autorização**.

### AGENTE-02 — P18 OpenZeppelin/Governor (PR #37, 181 properties)

> Adjudique `complete/18/3,23,4,46,53`. Reconfirme a distinção entre 5 erros dos originais e 3 `COMPILE_OK` derivados scratch, sem somar testes duplicados. Compare os 18 métodos críticos e ABI/visibilidade/receivers/summaries com as implementações e o commit **auditado**: 157 specs ausentes naquele commit e 24 fontes divergentes não podem herdar semântica do snapshot. Registre se `Governor` muda `PER_CALLEE_CONSTANT` vs `DISPATCHER(true)` e como isso altera universo de chamadas. Quando autorizado e com host íntegro, revalide bytes dos gzip e patches (12 logs/3 patches) e reversibilidade `--fuzz=0`, sem alterar fontes. Entregue matriz 181/181, as cinco decisões individuais, bloqueios e teste proposto; nenhuma promoção sem replay contextual.

### AGENTE-03 — P24 Rocket Joe (PR #36, 164 properties)

> Reconstrua por property a cena **auditada** `ef2ef302` versus fork `Certora/rocket-joe-1@dba90f9`, evitando mistura de versões OZ 4.4.1/4.4.2. Especifique matematicamente e por fonte como o guard `balance >= reserve` diverge de `balance - value >= reserve` em `LaunchEvent`; preserve comportamento do staking/harness. Distinga `patch --fuzz=0` no fork da aplicação com fuzz 2 na cena auditada; não rotule qualquer patch aplicado como reprodução da auditoria. Atualize matriz de 164 dependências/transitive imports + 6 run configs + 55 artefatos de proveniência, com `UNRESOLVED` por prova ausente, e proponha a menor cena Solidity autenticamente reproduzível. Não execute Prover/solc/CVL até host e gate aprovados.

### AGENTE-04 — P15 GHO, P12 AAVE V2, P2 PoR (PR #42, 157 properties)

> Priorize `P15/incomplete/36`: compare as seis declarações de `methods`, `envfree`, ABI e `@aave/core-v3` com o target `GhoDiscountRateStrategyHarness` e o runner versionado; a derivada `COMPILE_OK` com remapping não valida seus summaries nem a propriedade global. Em `P12/complete/23,25`, diferencie parser CVL2 de incompatibilidade de assinatura `address user` da implementação auditada; nos outros P12 incomplete, preserve a diferença entre construtor e `initialize`. Em P2, enumere helpers, assumptions, unrolling e resultados agregados do PDF não atribuíveis a rules individuais. Entregue tabela evidência/ausência para os três projetos e plano de teste mínimo bloqueado por gate.

### AGENTE-05 — P7 AAVE V3 e P19 (PR #40; experimento #46)

> Examine `P7/complete/47,73` e os pares de rules relacionados, contrastando seis seletores `sig:`, universo `method f`, `@withrevert`, possíveis revert paths e **não-vacuidade**; se a derivada compilar, isso permanece teste limitado. Para `P19/complete/1,2`, mantenha `02_unresolved`: a mudança de assinatura `uint→mathint` não demonstra equivalência histórica, especialmente quando `q=0`, produtos intermediários podem exceder uint256 e há diferenças de coerção entre CVL1/CVL2. Incorpore a adjudicação `COORDINATOR_SEMANTIC_ADJUDICATION.md` como limite, não resultado de Prover. Cheque também P21 (nomes do PDF não coincidem com as duas specs) e status de dependências P3/P6. Publique matriz de contraexemplos matemáticos vs provas realmente executadas e recomendação de gate, sem tocar no derivado #46.

### AGENTE-06 — P1/P17/P4/P22 (PR #38, 159 properties)

> Separe rigorosamente o P1 bridge de junho/setembro: a recuperação posterior de `queue2`/`_mock(env)` não preenche automaticamente o runner da auditoria original. Para P17, leia cada `static_assert`, `static_require`, `invoke` e `havoc` de Specify 2019 na sintaxe/semântica própria (não trate como CVL1 genérico). Para P4, compare `src/munged` do StakedAave e `PoolActions` com contrato e patches auditados, distinguindo `solc` EXIT0, TypeErrors Solidity e erro CVL2. Para P22, FullMathWrapper compilável não implica satisfatibilidade ou prova das rules. Entregue exemplos individuais priorizados, árvore de imports e propostas separadas de compilação de Solidity/compilação CVL, apenas após gate humano.

### AGENTE-07 — P9 Celo/P8 Vault/P20 BentoBox/P11 Keep (PR #41, 156 properties)

> Revise os testemunhos W1/W2/W3 do P8, inclusive o escopo real do axioma em cada job e a distinção entre **contradição matemática textual** e prova de vacuidade de um run histórico. Em P9 `complete/6`, identifique o superproject e fase que forneceu o blob `Accounts.sol@ac937...`, gitlink do Mento e ABI de AccountsHarness; amostrar 16 commits sem match **não** demonstra ausência definitiva. Em P11 `incomplete/1`, faça somente plano documental de binário solc0.5.17, hashes e closure externa. Em P20, mapeie `MAX_INT()` e `applyHarnesses.sh` sem importar helpers de specs irmãs por presunção. Produza matriz de quatro projetos e blockers, com 0 `COMPILE_OK` novos enquanto o WSL estiver EIO.

### AGENTE-08 — P5/P13/P14/P23 (PR #43, 155 properties)

> Para `P5/incomplete/14`, documente o erro parser CVL2 original e as dependências efetivas `BridgeHarness`, `erc20.spec`, 11 seeds/10 links, sem tratar a ABI Solidity como prova CVL. Para P14, compare pré/pós `applyHarness` no `Controller` (mudança 39→42 entradas ABI e comportamento do excesso de colateral), com snapshots e funções de arrays. Em P13, identifique regras de settlement/diagnósticas contraditórias e não atribua outcomes agregados a rules individuais. Em P23, diferencie a branch Certora posterior e wrappers CVT de DripsHub/Splits2 da produção auditada (inclusive timeout #38); sem receiver ou harness autêntico, permaneça unresolved. Entregue 155/155 decisões e uma única próxima tentativa scratch bem delimitada, condicionada à integridade do host e autorização.

## 4. Entregas esperadas do coordenador

- Monitorar mudanças de HEAD e CI das oito branches; validar `ROUND10`/nova rodada na HEAD **mais recente**, não reciclar QA R9.
- Pedir reparo administrativo do EIO antes de qualquer nova execução local. Não disparar Prover, CVL1, build ou scripts do auditor por automação.
- Após o reparo: rerodar validadores, reconciliar hashes brutos contra logs/source, testar em scratch **uma property por gate**, e somente então decidir possível promoção de status/merge.
- Manter PRs de agente e #46 em DRAFT até avaliação semântica independente; PRs exclusivamente de QA podem seguir gate CI + revisão de diff + teste negativo.

**Sem alegação de equivalência, resultado formal novo, ou conclusão de migration.**
