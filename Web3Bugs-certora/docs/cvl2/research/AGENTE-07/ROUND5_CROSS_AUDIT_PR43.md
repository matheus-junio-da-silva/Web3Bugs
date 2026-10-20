# Contrarrevisão independente somente leitura — PR #43

HEAD atual revisada: 96771fa27f90e56299bccc75a9729937ec4e77cc. PR https://github.com/matheus-junio-da-silva/Web3Bugs/pull/43. Worktree detached /home/mat/cvl2-agent07-round5-pr43-readonly; NÃO houve alteração, commit, push ou execução de scripts de harness nesta branch.

- 200 arquivos exclusivamente sob docs/cvl2/research/AGENTE-08; git diff --check BASE...HEAD exit 0.
- P14 34/34 UNRESOLVED_CANDIDATE e P5 17/17 UNRESOLVED_CANDIDATE, sem reintroduzir as 31 promoções Opyn.
- Opyn original complete/14/1.spec:10 conserva assert true; complete/14/25.spec:31–32 conserva sinvoke settleVault seguido por assert false; #19 vem de NoBankruptcy.spec e continua bloqueado. Não corrigir/assertar a semântica dos caminhos por conveniência.
- AGENTE-08 ROUND4_EVIDENCE_AND_GATES.md:11–16 relata applyHarnesses.sh histórico blob Git 70b2169 idêntico ao snapshot, quatro Solidity modificados em scratch, inclusos Controller/MarginPool/MarginCalculatorInterface/ERC20Upgradeable; alterações incluem cheapGetVault internal e getters públicos. Ainda NÃO reproduzi nem compilei a ABI em minha auditoria.
- P5 ROUND4_EVIDENCE_AND_GATES.md:18–24 relata lock e dois tarballs por SHA-1, patch com fuzz=0 em scratch, três hashes Bridge.sol distintos e fechamento textual de 40 Solidity, 64 imports, zero missing. CSV 5/ROUND4_IMPORT_CLOSURE.csv contém 40 linhas; isso NÃO implica compilação solc nem ABI histórica.
- Revisão é conferência independente da proveniência e das invariantes documentais críticas, NÃO análise exaustiva de 155 regras nem execução CVL.

**Decisão:** sem regressão documental detectada nas amostras e gates executados; PR #43 segue DRAFT, nenhuma promoção, Fase 2 requer ABI pós-patch e artefatos exatos do run do coordenador.

AGENTE-07 — RODADA 5 — QUALIDADE CVL2
