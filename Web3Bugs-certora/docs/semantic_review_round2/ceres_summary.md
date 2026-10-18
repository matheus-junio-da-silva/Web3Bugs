# CERES — Auditoria semântica independente, Project 18 OpenZeppelin

**Snapshot auditado:** `Web3Bugs-certora` da `main@80f551f23bbd86d7901c6a28e7f44c68aebae8fd`, após merge do PR #16. **Escopo entregue:** 181 linhas em [ceres_review.csv](ceres_review.csv), IDs 1–181 sem omissões.

## Método e limites

Reconstrução independente baseada nas 181 declarações copiadas, respectivos corpos originais em `contracts/18/specs`, pré-condições `require`, filtros, helpers/ghosts copiados em `N.spec`, referências e estados Solidity da matriz preexistente, justificativas individuais `N.md` e transcrição paginada do relatório de 13 páginas. A matriz anterior é tratada como **índice de navegação**, nunca como evidência de verdade do Bug Label. Cada linha enumera suas próprias condições, contraexemplo lógico e eventuais limitações. Contagens de assertions usam remoção de comentários e corpo CVL original.

**Limite de profundidade:** não se reexecutou Certora, não se obteve harness sintético do relatório, nem se comprovou a suficiência dos modelos ghost/external summaries. A inspeção do PDF histórico depende da transcrição de `reports/18.md`: símbolos gráficos individuais de prova não foram revalidados visualmente. `CONFIRMED` indica coerência semântica/documental condicional, **não resultado de prover**. `INCONCLUSIVE` abrange equivalência de harnesses, contratos executáveis, assumptions ou predicados não justificados. P0/P1/P2 são prioridades da **correção documental**, não severidade de exploit.

## Resultado

- Instâncias: **181**; CVL ativo original: **168**; expansão 13 Initializable por dois contextos, não provas extras.
- Decisões: **63 CONFIRMED**, **24 CORRECTION_REQUIRED**, **94 INCONCLUSIVE**.
- Correções por prioridade: {'P1': 23, 'P0': 1}.
- Fonte: **69 complete / 112 incomplete** segundo definição estreita de fechamento local. Não converter 'complete' em replay CVL ou soundness.
- Result/outcome mantidos conservadoramente: 177 NOT_STATED/NOT_STATED; 4 VIOLATED/FINDING de revisões históricas, não da versão corrigida.
- Nenhum arquivo de catálogo, CVL, Solidity ou PDF histórico foi editado por este programa.

## Questões críticas, com evidência por ID

1. **#149 e #150 (P1, inconclusivos):** `reinitializeRule` exige `n > initBefore` apenas em caminhos onde `reinitialize` retorna normalmente (sem @withrevert). Isso pode ser condição de segurança válida, mas não demonstra liveness ou atualização de versão sem harness histórico.
2. **#174 (P0):** `executeRevertsEffectCheck` assume pending && !ready e conclui apenas `lastReverted => pending && !ready`; isso não obriga o revert. Não confundir com #172 (`assert lastReverted`). Proposta de label: UNMAPPED.
3. **#13, #14, #51, #71, #76–78, #83–89, #95, #100, #108, #128 e #130:** existem duas ou três assertions ativas nas regras, enquanto a coluna anterior `Assertion/invariant` destaca apenas a primeira. O N.md pode mencionar os ramos em linhas de fonte, mas a descrição singular de predicado efetivo é incompleta. Corrigir a documentação/índice, não a CVL.
4. **#79 e #80:** mint/burn com unidades delegadas pode legitimamente modificar votos delegados; a interpretação universal de que `totalVotes` não muda precisa de precondições explícitas sobre ghost/delegação. Proposta cautelosa: UNMAPPED até validação do ghost.
5. **#110:** proibição indistinta de execução e cancelamento antes do prazo contrasta com fluxos de Governor que permitem cancelamento antecipado sob condições. Não classificar toda falsificação como bug no Solidity.
6. **#30–31:** a conversão `to_mathint(balanceOf + amount)` envolve soma Solidity/CVL prévia. Demonstrar satisfatibilidade do `require` e semantics de overflow antes de concluir que esses checks observam falha real.
7. **#166 e #171:** divergência entre `schedule(... bytes32 ...)` na declaração CVL e `schedule(... bytes ...)` Solidity. A linha continua incomplete; não modernizar assinatura silenciosamente.
8. **#122, #123, #124, #126:** PDF p.2 associa nominalmente as quatro regras a violações em revisões históricas do quorum. A versão corrigida não herda automaticamente esses contraexemplos.
9. **#159 e #160:** RulesInProgress não são verificações finais; a primeira testa bound depois de castVote (não é tautologia só porque usa igual precondition) e a segunda depende de helper não importado.
10. **#181:** `assert false` é regra de sanidade e deve permanecer UNMAPPED; uma violação alcançável é comportamento esperado do diagnóstico.

## Matriz de decisões por família

| Spec | IDs | Confirmed | Correction required | Inconclusive |
|---|---|---:|---:|---:|
| `AccessControl.spec` | 1–4 | 2 | 0 | 2 |
| `ERC1155.spec` | 5–45 | 36 | 3 | 2 |
| `ERC1155Burnable.spec` | 46–51 | 5 | 1 | 0 |
| `ERC1155Pausable.spec` | 52–59 | 8 | 0 | 0 |
| `ERC1155Supply.spec` | 60–63 | 0 | 0 | 4 |
| `ERC20FlashMint.spec` | 64–64 | 0 | 0 | 1 |
| `ERC20Votes.spec` | 65–80 | 0 | 6 | 10 |
| `ERC20Wrapper.spec` | 81–89 | 0 | 7 | 2 |
| `ERC721Votes.spec` | 90–100 | 0 | 2 | 9 |
| `GovernorBase.spec` | 101–113 | 0 | 2 | 11 |
| `GovernorCountingSimple.spec` | 114–121 | 0 | 0 | 8 |
| `GovernorPreventLateQuorum.spec` | 122–132 | 0 | 2 | 9 |
| `Initializable.spec` | 133–158 | 0 | 0 | 26 |
| `RulesInProgress.spec` | 159–160 | 0 | 0 | 2 |
| `TimelockController.spec` | 161–180 | 11 | 1 | 8 |
| `sanity.spec` | 181–181 | 1 | 0 | 0 |

## Índice completo de decisões, IDs 1–181

Cada posição mostra `#ID:DECISÃO`; o CSV contém as 181 justificativas, precondições, assertions, Solidity, evidence PDF, labels, resultados e contraexemplos. Para evitar confundir triagem automatizada com prova formal, as decisões INCONCLUSIVE não recebem conformidade fictícia.

**AccessControl.spec**: 1:I · 2:I · 3:C · 4:C

**ERC1155.spec**: 5:C · 6:C · 7:C · 8:C · 9:C · 10:C · 11:C · 12:C · 13:R · 14:R · 15:C · 16:C · 17:C · 18:C · 19:C · 20:C · 21:C · 22:C · 23:C · 24:C · 25:C · 26:C · 27:C · 28:C · 29:C · 30:I · 31:I · 32:C · 33:C · 34:C · 35:C · 36:C · 37:C · 38:C · 39:C · 40:C · 41:C · 42:C · 43:C · 44:C · 45:R

**ERC1155Burnable.spec**: 46:C · 47:C · 48:C · 49:C · 50:C · 51:R

**ERC1155Pausable.spec**: 52:C · 53:C · 54:C · 55:C · 56:C · 57:C · 58:C · 59:C

**ERC1155Supply.spec**: 60:I · 61:I · 62:I · 63:I

**ERC20FlashMint.spec**: 64:I

**ERC20Votes.spec**: 65:I · 66:I · 67:I · 68:I · 69:I · 70:I · 71:R · 72:I · 73:I · 74:I · 75:I · 76:R · 77:R · 78:R · 79:R · 80:R

**ERC20Wrapper.spec**: 81:I · 82:I · 83:R · 84:R · 85:R · 86:R · 87:R · 88:R · 89:R

**ERC721Votes.spec**: 90:I · 91:I · 92:I · 93:I · 94:I · 95:R · 96:I · 97:I · 98:I · 99:I · 100:R

**GovernorBase.spec**: 101:I · 102:I · 103:I · 104:I · 105:I · 106:I · 107:I · 108:R · 109:I · 110:R · 111:I · 112:I · 113:I

**GovernorCountingSimple.spec**: 114:I · 115:I · 116:I · 117:I · 118:I · 119:I · 120:I · 121:I

**GovernorPreventLateQuorum.spec**: 122:I · 123:I · 124:I · 125:I · 126:I · 127:I · 128:R · 129:I · 130:R · 131:I · 132:I

**Initializable.spec**: 133:I · 134:I · 135:I · 136:I · 137:I · 138:I · 139:I · 140:I · 141:I · 142:I · 143:I · 144:I · 145:I · 146:I · 147:I · 148:I · 149:I · 150:I · 151:I · 152:I · 153:I · 154:I · 155:I · 156:I · 157:I · 158:I

**RulesInProgress.spec**: 159:I · 160:I

**TimelockController.spec**: 161:C · 162:I · 163:C · 164:I · 165:C · 166:I · 167:C · 168:C · 169:C · 170:I · 171:I · 172:C · 173:C · 174:R · 175:C · 176:I · 177:I · 178:I · 179:C · 180:C

**sanity.spec**: 181:C

Legenda: C = CONFIRMED; R = CORRECTION_REQUIRED; I = INCONCLUSIVE.

## Revalidação e ações

- Conferir as 181 linhas do CSV, a identidade dos IDs e a preservação literal de todos os corpos CVL contra o snapshot fonte.
- Conferir no PDF gráfico os símbolos/assumptions de cada regra aplicável a cada target antes de eventualmente substituir NOT_STATED por VERIFIED.
- Recuperar Governor/Initializable/ERC20Votes/ERC721Votes/ERC1155Supply harnesses, configurações do Prover e mutações exatamente datadas; não equiparar mocks atuais.
- Reavaliar individualmente sugestões de UNMAPPED conforme `docs/standard.md`; Bug Label em property denota *modelo do detector*, nunca achado explotável automático.
- Não alterar o dataset histórico; mudanças propostas ficam apenas nesta revisão separada. Não fazer merge automático.

### Reprodução do inventário

```text
csv rows=181; original unique spec declaration=168; status complete=69 incomplete=112
decision counts={'INCONCLUSIVE': 94, 'CONFIRMED': 63, 'CORRECTION_REQUIRED': 24}
source report SHA-256 (documentação de proveniência): 4a35df36c47e6e7e2b4333cb3890bc2a8cbca569e32b2fc6f24820b8a56cbc37
```

## Verificações independentes adicionais

- Extração linha a linha: 181/181 property bodies aparecem literalmente nos 17 arquivos spec históricos; todos os incomplete têm arquivo N.txt.
- Comparação literal de todas as seções N.sol: **887/887 excertos** iguais às linhas Solidity de 29 arquivos históricos; zero erros.
- Reconstrução recursiva separada dos imports Solidity, começando dos entrypoints de cada uma das **16 famílias**, produziu a mesma closure documentada sem imports locais ausentes. Isso NÃO prova que ABI/harness originais eram compiláveis.
- PDF original preservado: SHA-256 **4a35df36c47e6e7e2b4333cb3890bc2a8cbca569e32b2fc6f24820b8a56cbc37**; nenhuma modificação em fonte.
- Validação do snapshot atual: check_specs.py exit 0 (**1222 examples; 1227 relations**), check_contests_csv.py exit 0, check_contracts.py exit 0.
- Verificação semântica não incluiu Prover/solc original nem inspeção gráfica dos símbolos no PDF; falsos negativos/positivos por assumptions/vacuidade continuam possíveis.
