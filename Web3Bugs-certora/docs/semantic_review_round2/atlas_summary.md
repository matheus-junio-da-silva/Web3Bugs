# ATLAS — auditoria semântica independente, rodada 2

## Identidade, método e alcance

- Baseline: Web3Bugs main SHA 80f551f23bbd86d7901c6a28e7f44c68aebae8fd; branch isolada audit/semantic-round2-atlas-20261018.
- Exatamente 192 IDs únicos: 42 Project 8, 116 Project 15, 2 Project 21 e 32 Project 10, IDs 1–32.
- Para cada exemplo foram lidos N.spec, N.md, N.sol, o arquivo CVL original, os arquivos Solidity citados quando preservados e as páginas textuais dos PDFs originais com PyMuPDF. As páginas foram obtidas dos PDFs físicos, não apenas de transcrições Markdown.
- Não houve execução do Certora Prover, nem reconstrução do ambiente completo de harness/dependências. A revisão não comprova satisfatibilidade e nem identidade do binário do Prover histórico.
- CONFIRMED requer CVL, target, fórmula, assumptions, storage, resultado individual do PDF, modelo satisfatível e interpretação histórica coerentes; a correspondência de nome e checkmark isoladamente é insuficiente.
- CORRECTION_REQUIRED indica divergência concreta da documentação/uso de NO_FINDING sem prova de modelo satisfatível; NÃO significa modificar o campo histórico Result. INCONCLUSIVE mantém o limite de evidência.

## Matriz de decisões

| Projeto | Exemplos | CONFIRMED | CORRECTION_REQUIRED | INCONCLUSIVE |
|---|---:|---:|---:|---:|
| 8 — AAVE Vault | 42 | 0 | 1 | 41 |
| 15 — AAVE GHO Core | 116 | 0 | 0 | 116 |
| 21 — Lido V2 | 2 | 0 | 0 | 2 |
| 10 — Furucombo (IDs 1–32) | 32 | 0 | 0 | 32 |
| **Total** | **192** | **0** | **1** | **191** |

Prioridades: P0=23, P1=98, P2=71. Valores históricos Result: NOT_STATED=102, VERIFIED=80, VIOLATED=10.

## P0 — soundness de AAVE Vault

**W2/W3 (ID 1):** em accrueYieldCheck.spec, o axioma de mulDiv_g admite x=y=denominator=0, rounding=0, e força 0<0; o de rayDiv_g com x=y=0 também força 0<0. São contradições da teoria CVL arquivada sob quantificação universal.

**W1 (IDs 14–35):** os axiomas rayMul_g(1,0)=0 e 1<=rayMul_g(1,0) não podem coexistir em inteiros. Como universais, podem contaminar a teoria de uma instância mesmo quando a rule não chama explicitamente o ghost.

A propriedade logicamente demonstrada é a inconsistência das assumptions arquivadas, não a falha de uma implementação Solidity. Os campos VERIFIED/VIOLATED reproduzem a fonte histórica e não devem ser apagados. Já NO_FINDING não sustenta, por si, uma conclusão de ausência de vulnerabilidade sem checagem de satisfatibilidade/execução não-vácua.

## P1 — GHO Core: auditoria dos 64 VERIFIED

- PDF original de 13 páginas. Reviewed commit relatado ce49fb0; versão final auditada não se confunde com a HEAD do dataset.
- VERIFIED atribuído a 64 regras; nome exato associado à marca ✔ no PDF original para 64 instâncias, sem pareamento nominal direto para 0. Os pormenores estão na coluna pdf_evidence.
- O pareamento nome/checkmark é condição NECESSÁRIA, não suficiente: fórmulas, escala, rounding, índices, assumptions de POOL, somente-caller, summaries NONDET, target e harness precisam coincidir com o ambiente histórico.
- Há bugs de rebalance timelock, conformidade maxFlashLoan e juros no relatório. Uma property comprovada no commit final pode ter apoiado finding anterior; Outcome não deve ser inferido mecanicamente da marca ✔.

## P1 — Lido V2: guardian, quorum e DSM

- ID 1: depositBufferEtherRevertCheck invoca depositBufferedEtherHarness@withrevert com input simbólico e exige !lastReverted; quorum é lido mas não restringe a chamada. Falhas legítimas de root, assinatura, quorum ou nonce podem falsificar a assertion. O DepositSecurityModuleHarness histórico não está presente para reexecução.
- ID 2: quorumLeGuardian afirma guardianLength>=guardianQuorum; isto limita configuração, NÃO valida guardianSignatures nem autenticação de deposito.
- As 18 regras Deposit Security Module enumeradas no PDF de 40 páginas, pp.31–32, não devem ter outcomes transplantados para as duas únicas declarações CVL ativas do snapshot; ambos mantidos NOT_STATED.

## P1 — Furucombo IDs 1–32

- O relatório original de 31 páginas descreve regras, targets e handlers e diversas condições em conjuntos, que não são equivalentes à execução histórica individual de cada par property × target.
- Relevância de storage de Registry, permissões de Proxy, selectors e ABI é delimitada por requires/filters e summaries. O N.sol foi cotejado com o arquivo Solidity indicado, quando presente, sem presumir que o mesmo harness tinha todos os métodos.
- Não transformar automaticamente VIOLATED em FINDING ou VERIFIED em ausência histórica de issue; diferenciar findings de versões anteriores dos resultados finais e casos aceitos.

## PDF original: proveniência verificada

| Projeto | PDF | Páginas | SHA256 |
|---|---|---:|---|
| 8 | resources/8/Aave-Vault-Formal-Verification-2.pdf | 14 | cd744576df09e429176c1dae87187db96e52eec18db012760cfeb43868eac766 |
| 15 | resources/15/Aave_Gho_Formal_Verification_Report.pdf | 13 | ced8ba5de87ae727c0df889d5e916f32a759394465acf1ce83b1afddf832df06 |
| 21 | resources/21/Certora-Lido-V2-Audit-Report-04-23.pdf | 40 | b8acbf2e980db873706a40ac1abefdbffa6ad3e6f649445f2000e93e905f9c5b |
| 10 | resources/10/FurucomboMay2021.pdf | 31 | a42e33196f3bdadb7df52c5554aca0e2d15d7aaa517b42db118db015b278d769 |

## Priorização operacional

P0: testar satisfatibilidade das teorias W1–W3 com axiomas ativos e provar não-vacuidade antes de atribuir confiança operacional aos resultados de Vault.

P1: revisar cada um dos 64 GHO por índice de regra, fórmula, página, target e assumptions; restaurar harness Lido; fechar vínculo por par handler/regra nos registros de Furucombo.

P2: ampliar citações de funções Solidity quando o trecho é apenas contexto de contrato; não presumir transição de storage a partir de nome de property.

## Integridade

- Colunas Result e Detection Outcome permanecem independentes, preservando os valores históricos até evidência corretiva específica.
- Uma mesma regra pode ter mais de um cenário de contramodelo; a matriz descreve o comportamento hipotético que negaria a condição, nunca um Prover rerun ocorrido.
- Somente docs/semantic_review_round2/atlas_review.csv e atlas_summary.md devem permanecer no diff final; CVL, Solidity, PDF e arquivos N.md intactos.
- Critérios de controle: 192 linhas, IDs únicos, ausência de placeholders, decisões em CONFIRMED / CORRECTION_REQUIRED / INCONCLUSIVE, prioridades P0/P1/P2 e git diff --check.
