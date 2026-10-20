# AGENTE-05 — RODADA 8 / EVIDÊNCIAS CVL2 E GATES

**Data de referência:** 2026-10-20. **PR:** [#40](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/40) **Draft**; branch `research/cvl2-agente-05`. **HEAD conferida antes de editar:** `5a50cd43a56add63d91e2476b3d0460e991cdacc`. **Original imutável:** [`main@2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`](https://github.com/matheus-junio-da-silva/Web3Bugs/tree/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora). A [coordenação R7](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/main/Web3Bugs-certora/docs/cvl2/coordination/ROUND7_DASHBOARD.md) está na main após merge documental de #47; esse merge **não autoriza CVL2 nem o merge de #40**. **Nenhum comando foi enviado ao WSL com EIO/EROFS/SIGBUS.**

## 1. Integridade e separação de evidências

[`ROUND8_MATRIX_148.csv`](ROUND8_MATRIX_148.csv) contém **148 chaves únicas** `(project_id,original_status,example_id)` de P3 (3), P6 (32), P7 (74), P19 (37) e P21 (2). Os dados `Property`, `Target Contract`, `Result`, `Detection Outcome`, `Bug Label(s)`, caminho `N.spec`, fonte/linhas e SHA registrado foram reconciliados via conector com [`results/spec/spec_buglabel.csv` no baseline](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/results/spec/spec_buglabel.csv), os cinco `properties.csv` e a matriz R7: **148 propriedades, 149 relações históricas**, zero identidades repetidas, zero divergências. `N.spec` SHA-256 foi confrontado aos hashes já calculados em rodadas anteriores; **R8 não recalculou SHA dos bytes de todos os 148 originais**.

As três colunas da matriz **`source_or_report_fact`**, **`inference`** e **`missing_proof`** diferenciam observação rastreável, análise condicional e ausência de prova. `COMPILE_OK` **não** equivale a `SEMANTIC_PROVEN`; nenhum projeto é `MIGRATED_COMPLETE`. Em R8, **zero execuções CVL2** (ver [QA](ROUND8_QA.md)).

| Carteira | Documentadas | `COMPILE_OK` anterior (restrito) | `COMPILE_ERROR` anterior | `NOT_RUN` histórico | Testes CVL2 R8 |
| --- | ---: | ---: | ---: | ---: | ---: |
| P7 | 74 | 2 (complete/37,65, **fragmentos N.spec somente**) | 5 (complete/36,41,47,63,73) | 67 | 0 |
| P19 | 37 | 2 (complete/1,2, **derivadas mathint somente**) | 0 | 35 | 0 |
| P6 | 32 | 0 | 0 | 32 | 0 |
| P3 | 3 | 0 | 0 | 3 | 0 |
| P21 | 2 | 0 | 0 | 2 | 0 |
| **TOTAL** | **148** | **4** | **5** | **139** | **0** |

**Autoria:** 5 `COMPILE_ERROR` P7 foram produzidos por AGENTE-05 na R5 (CLI 8.19.0 `--compilation_steps_only`, target concreto, 0.8.10, EXIT 1, manifest e logs); 4 `COMPILE_OK` limitados são observações **anteriores do COORDENADOR**. Uma preparação de variante P7/47 em R6 abortou antes do `certoraRun`; R7 e R8 não a executaram. No dashboard global R7: **1.386 catalogadas, 4 OK limitados, 12 erros de parser e 1.370 sem teste, zero equivalências**. Não somar resultados do restante da equipe à carteira AGENTE-05.

## 2. P7/complete/47 — diff exato `sig:` com código da regra congelado

**Fonte (fato):** [`results/spec/complete/7/47.spec`](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/results/spec/complete/7/47.spec#L6-L19), Git blob SHA-1 `be479705943bcb3300e74e0c425bebfb2cf526a3`, **SHA-256 do N.spec original `0cf2150c11cfb9926d3e24eecc1fb7ce0c9ffeb956ec3553dab606d026a8416e`**. A definição `disAllowedFunctions(method f)` ocupa as linhas 6–12; a rule começa na linha 14; a chamada `f@withrevert(e,args)` é linha 18 e `assert lastReverted` linha 19. Fonte integral [StableDebtToken.spec:14–20,338–344](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/contracts/7/specs/StableDebtToken.spec#L338-L344). O arquivo **ainda contém CVL1**, sem nenhum `sig:`.

**Verificação textual R8 EXECUTADA em memória pela API GitHub:** para cada nome `transfer`, `allowance`, `approve`, `transferFrom`, `increaseAllowance`, `decreaseAllowance`, a subsequência `f.selector == NOME(` ocorreu **uma única vez**; após adicionar `sig:` apenas nessas seis ocorrências, o trecho que inicia em `rule disallowedFunctionalities(method f)` foi comparado textualmente e resultou **idêntico**. Total de seis prefixos, sem editar `method f`, parâmetros, `filtered`, `require`, `assert`, `@withrevert`, casts, hooks ou summaries. Isso valida o **plano de diff**, não gera variante de spec persistente nem certificado de compilação.

```diff
-            f.selector == transfer(address, uint256).selector ||
+            f.selector == sig:transfer(address, uint256).selector ||
-            f.selector == allowance(address, address).selector ||
+            f.selector == sig:allowance(address, address).selector ||
-            f.selector == approve(address, uint256).selector ||
+            f.selector == sig:approve(address, uint256).selector ||
-            f.selector == transferFrom(address, address, uint256).selector ||
+            f.selector == sig:transferFrom(address, address, uint256).selector ||
-            f.selector == increaseAllowance(address, uint256).selector ||
+            f.selector == sig:increaseAllowance(address, uint256).selector ||
-            f.selector == decreaseAllowance(address, uint256).selector;
+            f.selector == sig:decreaseAllowance(address, uint256).selector;
```

A [documentação oficial CVL2 Changes, “Method literals require `sig:`”](https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html#method-literals-require-sig) documenta exatamente esse padrão lexical. **Inferência limitada:** o diff pode sanar *esse* erro de tipagem; não há prova de que toda compilação passaria, nem do mesmo conjunto de funções, reverts ou contraprovas.

**Plano futuro, NÃO EXECUTADO:** depois de (1) administrador declarar WSL recuperado, (2) gate escrito por property/target da coordenação, conferir HEAD/worktree, checks Python e `git diff --check`; em **scratch novo** copiar `N.spec` original e **todos** os Solidity envolvidos com SHA-256 e comparação byte a byte, gerar uma única variante com exatamente os seis prefixos, registrar manifesto de hashes da árvore + `cmp`, CLI **direto** `/home/mat/certora-ac-audit/certora_venv/bin/certoraRun` 8.19.0, target `StableDebtToken`, solc **0.8.10** fixado, `--compilation_steps_only`, timeout ~60–65s, `stdout/stderr` completos e exit. **Somente EXIT 0 real para esse arquivo+target** poderia receber `SNAPSHOT_SIG_VARIANT_COMPILE_OK`, jamais `SEMANTIC_PROVEN`. Não subir derived, não usar token ou Prover, não executar por mera disponibilidade de máquina.

## 3. P7/73 separado de P7/47: selector, ABI, domain e soundness

| Atributo observável | P7/47 StableDebtToken | P7/73 VariableDebtToken |
| --- | --- | --- |
| N.spec SHA-256 do catálogo | `0cf2150c11cfb9926d3e24eecc1fb7ce0c9ffeb956ec3553dab606d026a8416e` | `c82afdd9a07a75c9c6cad9b20eee201cb212017cc4cd01c6266bc90b42c8a76b` |
| N.spec Git blob | `be479705943bcb3300e74e0c425bebfb2cf526a3` | `fd4dcce2c6c96f4dbc4164dc776084123449f268` |
| Spec global | `StableDebtToken.spec:14–20,338–344` | `VariableDebtToken.spec:23–29,252–258` |
| Funções na ABI compilada apenas com solc (R5) | **33** | **30** |
| Seis selectors disallowed | **seis presentes** | **seis presentes** |
| Solidity source | [`StableDebtToken.sol:365–386`](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/contracts/7/contracts/protocol/tokenization/StableDebtToken.sol#L365-L386) | [`VariableDebtToken.sol:127–148`](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/contracts/7/contracts/protocol/tokenization/VariableDebtToken.sol#L127-L148) |
| Chamada/assert originais | `f@withrevert(e,args); assert lastReverted;` | `f@withrevert(e,args); assert lastReverted;` |

Os seis selectors reais em **ambas** as ABIs são `transfer(address,uint256)`, `allowance(address,address)`, `approve(address,uint256)`, `transferFrom(address,address,uint256)`, `increaseAllowance(address,uint256)`, `decreaseAllowance(address,uint256)`. No Solidity acima, as seis funções terminam em `revert(Errors.OPERATION_NOT_SUPPORTED)`. `allowance` é **view**, mas **o filtro P7/47 e /73 não contém `!f.isView`**; excluí-la alteraria o domínio. O conjunto **ABI de selectors** não está vazio, mas o universo parametrizado real de `method f` e a instanciação da rule **ainda não foram verificados**.

[Fonte CVL oficial, Statements § Revert](https://docs.certora.com/en/latest/docs/cvl/statements.html): `@withrevert` mantém caminhos revertidos para observação em `lastReverted`, ao passo que chamadas sem essa anotação assumem sucesso. [Methods § Summaries](https://docs.certora.com/en/latest/docs/cvl/methods.html) avisa explicitamente que summaries podem alterar a interpretação das chamadas e ser **unsound**, com exceções documentadas. Portanto, mesmo que o Solidity snapshot sustente a expectativa de revert das seis funções, **não** se pode derivar soundness de CVL1→CVL2 ou satisfatibilidade do método quantificado sem receivers, summaries, imports, ABI e runner **da auditoria original**. `P7/73` depende de gate **independente** e não deve reaproveitar o exit hipotético de P7/47.

## 4. P7/41,63,36: domínio não-view, EIP-712 e vacuidade

| ID | Source original | Fato da ABI snapshot / regra | Inferência e missing proof |
| --- | --- | --- | --- |
| **41** `nonceChangePermits` | [StableDebtToken.spec:226–236](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/contracts/7/specs/StableDebtToken.spec#L226-L236) | `!f.isView && !disAllowedFunctions(f)`: seis funções ABI elegíveis `approveDelegation`, `burn(address,uint256)`, `delegationWithSig`, `initialize`, `mint`, `setIncentivesController`. `f(e,args)` **sem** `@withrevert`. | [DebtTokenBase.sol:43–68](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/contracts/7/contracts/protocol/tokenization/base/DebtTokenBase.sol#L43-L68) só atualiza nonce após prazo válido e `ecrecover` aceito. Não inventar assinaturas válidas; se nonce não muda, implicação é verdadeira sem testar caminho relevante. |
| **63** `nonceChangePermits` | [VariableDebtToken.spec:89–99](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/contracts/7/specs/VariableDebtToken.spec#L89-L99) | Mesmo conjunto de famílias ABI, porém `burn(address,uint256,uint256)` vs Stable de dois argumentos. `f(e,args)` sem `@withrevert`. | Variable tem `gRNVB` e hooks diferentes; não transferir prova de Stable; autenticar receiver, mundo de `nonce` e modelos de revert. |
| **36** `integrityTimeStamp` | [StableDebtToken.spec:166–174](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/contracts/7/specs/StableDebtToken.spec#L166-L174) | Filtra as mesmas seis famílias `!f.isView && !disAllowedFunctions(f)`, faz `require getUserLastUpdated(e,user) <= e.block.timestamp`, chama `f(e,arg)` e assert a mesma cota. | `initialize`, mint/burn e `onlyPool` afetam alcance; não inserir precondição nova ou converter `f` para `@withrevert` arbitrariamente. |

**Full-spec vs fragmento:** a [StableDebtToken.spec:1–10,22–123](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/contracts/7/specs/StableDebtToken.spec) tem métodos legados, summaries `calculateCompoundedInterest/rayMul/rayDiv/handleAction`, ghosts, `sumAllBalance`, hook `Sstore` `_userState.balance` e `Sload`; a [VariableDebtToken.spec:1–50](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/contracts/7/specs/VariableDebtToken.spec) tem `gRNVB`, summaries e hooks. A ausência dessas definições nos `N.spec` pode alterar resultados para `f=mint/burn`; os dois fragmentos de `delegationWithSig` P7/37,65 **compilaram isolados** na Rodada anterior, mas as **especificações globais falharam CVL2**. O aviso auxiliar `Stack too deep` do autofinder Stable e fallback na R5 é distinto do EXIT 1 *CVL2 selector* do N.spec. Não alegar que um compila toda a cena.

## 5. P19/complete/1,2 — caso matemático encerrado como `02_unresolved`

**Source facts:** [`math.spec` extraída P19/1](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/results/spec/complete/19/1.spec) e [P19/2](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/results/spec/complete/19/2.spec): `divPrecisely(uint x,uint y) returns mathint = x*10^18/y` e dois asserts **diferentes**: `T2<=MAX_SUPPLY()` no exemplo 1; `T2<=T || T2==NR` no exemplo 2. Ambos preservam as mesmas condições `T<=2^128-1`, `T>0,NR>0,T>NR,RC>0`, e `RCPT<=2^256-1`; **não** há `require RCPT>0`. As cópias *derivadas* do [PR #46](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/46) mudam apenas os tipos de dois parâmetros para `mathint`, compilaram anteriormente com CLI 8.19.0, mas seguem **`02_unresolved`** sem equivalência nem merge.

**Dedução matemática CONDICIONAL, não execução CVL:** se `divPrecisely` operar como divisão inteira de inteiros matemáticos para denominador positivo, `T=2^128-1, NR=RC=1` dá primeiro denominador `2^128-2` e `RCPT=floor(10^18/(2^128-2))=0`; a segunda chamada usa denominador **zero**, que a documentação consultada não resolve para **o pipeline CVL1 histórico versus o CLI CVL2 atual**. Um modelo formal precisa tratar esse ponto, e coerções/overflow dos intermediários ainda não têm prova de equivalência. Revisão concluída no [documento de adjudicação do coordenador](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/62754c10e3e9dc23d122aad3333eac2ec60f817d/Web3Bugs-certora/docs/cvl2/implementation/AGENTE-05/P19_mathOfChangeSupply/COORDINATOR_SEMANTIC_ADJUDICATION.md). **Não** adicionar `require RCPT>0`, cast restritivo, novo derived ou repetir experimentos sem fonte nova. Essas duas properties ficam 02_unresolved sem tratamento adicional especulativo.

## 6. P3/P6/P21 — triagem de fontes e caso tecnicamente fechado

| Família | `source_or_report_fact` | `inference` | `missing_proof` |
| --- | --- | --- | --- |
| **P3 incomplete/1–3** | `bgd-labs/rescue-mission-phase-1@33c1aeca28d6d61659c1b28775ad2644b7e2ac6e` registra gitlink `lib/solidity-utils@49f2bd22950cf8dfe32d3f01e30a221b1f2f95dd`, tree `36cb441858e6d959387713deb832e47e4377efe5`, com IERC20 real importado por `LendToAaveMigrator.sol:4`. | A **identidade do submódulo** está fechada; isso sozinho não fecha `solc_map`, links token/harness nem identidade dos jobs LEND/stkAAVE. | Recuperar run autenticado por rule, linkage `LEND/AAVE` e `StakedTokenV2Rev4` separadamente; **não existe ainda caso completo para compilação CVL2 segura**. |
| **P6 incomplete/1–32** | [`reports/6.md:13,47`](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/reports/6.md#L37-L47) diz revisão `ac92951`; publicação Certora 2023 registra `51d46b1` segundo pesquisa prévia; snapshot `13a00473...`. | Fontes podem refletir revisões diferentes; não escolher commit “parecido” como audit SHA. | Obter SHA longo/repositorio, PDF com hash e runner/ABI auditados. Buscas anteriores nos 3 repos Aave não encontraram os SHAs curtos; **limite de busca**, não inexistência universal. |
| **P21 incomplete/1–2** | [`DSM.spec:1–38`](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/contracts/21/specs/DSM.spec) cita `DepositSecurityModuleHarness`, `getGuardianLength`, e para /1 `depositBufferedEtherHarness@withrevert`. [`DepositSecurityModule.sol:218–235`](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/contracts/21/0.8.9/DepositSecurityModule.sol#L218-L235) permite expressamente quorum maior que número de guardians. | /2 `quorumLeGuardian` é potencialmente incompatível com o Solidity se `getGuardianLength` representar a contagem, mas sem implementação real nem Prover não existe resultado formal. /1 `assert !lastReverted` pode depender de precondições do harness. | Exigir bytes/hash do harness e getter com report por rule; **não sintetizar** `getGuardianLength()` nem presumir invariância. |

**Caso documental fechado nesta triagem:** apenas **pin e conteúdo do submódulo P3**; nenhum dos casos P3/P6/P21 reúne simultaneamente target/ABI/harness original+runner+CVL global. Logo **nenhuma execução é justificável atualmente**. Pesquisa avançou de P3 para P6 e P21 e retornou P7 como prioridade máxima, registrando as faltas em vez de repetir buscas negativas sem pista.

## 7. Cross-review do [PR #38](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/38) — READ-ONLY, HEAD atual R7

**HEAD consultada:** `e4527033b3c2b1a6aa638f6b7c351ee996d0ae79`, Draft. Fonte [AGENTE-06/ROUND7_EVIDENCE.md](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/e4527033b3c2b1a6aa638f6b7c351ee996d0ae79/Web3Bugs-certora/docs/cvl2/research/AGENTE-06/ROUND7_EVIDENCE.md) e specs do baseline foram lidas sem escrita na branch alheia:

- **P1 `queue2`:** o commit auditado junho/2022 `aave/governance-crosschain-bridges@303bd3e16c8d3465325389a72564126c3bacc4f9` tem produção `queue` com arrays dinâmicos. Um [harness público de setembro/2022 `93c39de...`, L45–61](https://github.com/aave/governance-crosschain-bridges/blob/93c39de7065a7dc3bb08cddf7dadb466f9a393b8/certora/harness/L2BridgeExecutorHarness.sol#L45-L61) inclui `queue2` com **cinco arrays de tamanho fixo 2**, logo os conjuntos de argumentos/branches são diferentes. Embora quatro Git blobs dos contratos de produção junho/setembro coincidam, **não há evidência do runner/harness junho**. `_mock` aparece no `OptimismHarness.sol:21` posterior com link por rede; não extrapolar links Polygon/L2.
- **P17 Specify 2019**: `results/spec/complete/17/8.spec:19–28,64–65,114–117` usa `havoc` de env e local, `static_require result==invoke borrowFreshPub` e `lastReverted`; /9 `:19–32,67–68` apresenta contextos payer/borrower; /39 `:21–32,69–80` usa `havoc doApprove` e `sinvoke approve` **potencialmente mutável** antes de `invoke transferFrom`. Trocar `sinvoke/invoke/static_require` por CVL2 sem gramática/runtime `.spclnk` **não** preserva automaticamente snapshots, permissões e reverts. O [guia CVL2](https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html) não documenta por si só o engine Specify 2019. Não há compile-only da AGENTE-06 nesta carteira.
- **Parecer:** manter P1/70 e P17/41 **unresolved** sem inferir Fase 2; review **amostral** em P17/8,9,39 e P1 `queue2/_mock`, não revalidação de 159 provas. Nenhuma escrita/commit no PR #38.

## 8. Duas próximas experiências para decisão do coordenador

| Ordem | Experiência candidata | Evidência a exigir ANTES da execução | Saída que seria legítima |
| --- | --- | --- | --- |
| **1** | **P7/47 StableDebtToken**, seis prefixos `sig:` exclusivamente em `disAllowedFunctions`, `f@withrevert` intacto | WSL recuperado; gate humano da property; SHA original `0cf2150...`, ABI Stable R5, solc 0.8.10, full-method scene/receiver revisados, `cmp` de todos os inputs; CLI 8.19.0 em scratch | Somente `SNAPSHOT_VARIANT_COMPILE_OK` se de fato exit 0 com manifest/log, **nunca equivalência** |
| **2** | **P7/73 VariableDebtToken**, o mesmo *tipo* de proposta lexical mas **novo target e gate independente** | WSL/gate; SHA original `c82afdd...`, ABI Variable 30 funções, `burn` de três argumentos e globals Variable; revisar dispatch e reverts | `SNAPSHOT_VARIANT_COMPILE_OK` apenas se execução própria exit 0; **não herdar sucesso** de P7/47 |

**Risco VERMELHO (semântico):** domínio real de `method f` não provado, summaries possivelmente insound em cena global, hooks/ghosts, reverts podados em 41/63/36, EIP-712, P19 divisão por zero, P21 getter/harness e discrepância de quorum. **Risco VERMELHO (operacional):** WSL sem recuperação atestada; qualquer compile/QA local é proibido até decisão do administrador.

**AGENTE-05 — RODADA 8 / PESQUISA, QA E EVIDÊNCIAS.**
