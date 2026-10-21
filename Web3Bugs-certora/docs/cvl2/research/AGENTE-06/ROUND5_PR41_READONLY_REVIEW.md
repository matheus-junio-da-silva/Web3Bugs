# AGENTE-06 — RODADA 5 — auditoria cruzada SOMENTE LEITURA do PR #41

**HEAD revisada:** 96257f027dddefdbc231dd136416020535ad0ecb em 20/10/2026; PR #41 DRAFT, sem edição/commit/checkout/reset/push na branch AGENTE-07. Baseline 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3. Leitura por git show SHA:path a partir de clone preexistente do AGENTE-07. Conferidos o novo ROUND4_MATRIX.csv, ROUND4_EVIDENCE.md, os quatro full_spec_audit.csv, originais e [coordenação P8_AXIOM_CONSISTENCY_REVIEW.md](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/705641e9f8920da648c724ce4c3361f03b8ac821/Web3Bugs-certora/docs/cvl2/coordination/P8_AXIOM_CONSISTENCY_REVIEW.md).

**Checks executados:** git -c core.whitespace=cr-at-eol diff --check BASE...96257f027dddefdbc231dd136416020535ad0ecb → **EXIT 0**; 221 arquivos de diff, 0 fora da pasta AGENTE-07. Python somente leitura reabriu via git show a HEAD exata, comparou todas as 156 entradas dos full_spec_audit.csv com os bytes e SHA-256 das 156 N.spec e todos os N.txt aplicáveis. **156/156 conformes** (P8=42, P9=61, P11=16, P20=37); 156 chaves únicas.

| Escopo | Observação fundamentada | Limite |
| --- | --- | --- |
| **P8 W1** | Em [incomplete/8/14.spec](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/results/spec/incomplete/8/14.spec), axiom rayMul_g(1,0)=0 pelo ramo y=0 e rayMul_g(1,0)>=1 pelo ramo x=1: conjunção impossível na aritmética usual. Matriz do AGENTE-07 marca 22 extrações (IDs 14–35). | Demonstra testemunha contraditória para a fórmula; sem análise da scope/instantiation do run, não prova que VERIFY foi vacuous. |
| **P8 W2** | Em [incomplete/8/1.spec](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/results/spec/incomplete/8/1.spec), mulDiv_g universal com x=0,y=0,denominator=0,rounding=1 exige 0<0. | Contraexemplo da consistência do axioma como escrito, não do contrato. |
| **P8 W3** | Mesma unidade, rayDiv_g universal para x=0,y=0 força 0*RAY()-0/2 < rayDiv_g(0,0)*0, isto é, 0<0 (divisão 0/2 é válida). | Independente de W2; nenhuma conclusão sobre os outros 19 IDs além de ausência desses modelos específicos. |
| **P9 Celo** | phase1 auditada 9d2ec0d9399a6959565062f57efa037d03fd4fbc e phase2 auditada a46ce55ebd3867fa69290bf3be040846d433525d; Governance.sol blobs 79bf0203...,641c834f..., snapshot 633b7d2d... diferentes. Accounts.sol e LockedGold.sol não existem nos caminhos/árvore da phase1 examinados, mas existem na phase2. 50 DOCUMENTED_CANDIDATE seguem hipóteses lexicais. | Nomes iguais em Accounts IDs 1–7 não provam ABI, target de compilação ou atribuição do run; ReserveHarness inclui import ausente e applyHarness altera fontes. |
| **P20 BentoBox** | Patch do AGENTE-07 reproduzido em scratch sobre pacote pinned e cinco Solidity mudados; runner original continua sem prova de identidade, MAX_INT ausente em source isolada. | Não autorizar migration nem alterações no catálogo. |
| **P11 Keep** | Dependências npm e hashes foram recuperados; closure import textual expandida. | SHA da auditoria e compilação solc/ABI exatos seguem não comprovados. |

**Parecer:** fechamento documental/whitespace do PR #41 OK; nenhuma evidência nova que autorize promover CVL2 ou reproduzir prova não vacuosa. Permanecem P8 22+1 com alerta matemático de axiomas, P9 50 candidaturas estritamente documentais e bloqueios P20/P11. Não rodados CVL1, CVL2 nem Prover durante esta auditoria. PR #41 segue Draft, intacto.

**AGENTE-06 — RODADA 5 — QUALIDADE CVL2.**
