# AGENTE-06 — P17, commit auditado confirmado

- Relatório arquivado `reports/17.md` (PDF página 1) indica commit completo `f385d71983ae5c5799faae9b2dfea43e5cf75262`.
- Upstream [compound-finance/compound-protocol](https://github.com/compound-finance/compound-protocol/commit/f385d71983ae5c5799faae9b2dfea43e5cf75262); Git tree `d0691da015ec80a6957f1c881063478c52da94ed`.
- O report refere a linguagem histórica **Specify**, não CVL2. A existência de .cvl/.spclnk e o vínculo de bytes não autorizam parser moderno.
- Proveniência de arquivos conferida no repositório GitHub e contra o snapshot Web3Bugs `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`:

| Fonte | Blob auditado e arquivado |
|---|---|
| `contracts/CToken.sol` | `df653280f128ac8c1f2599272e311455b3135a0f` — correspondência exata |
| `contracts/CErc20.sol` | `b86ce526cfa126b638cc8927df500c6491e8ee3c` — correspondência exata |
| `spec/formal/borrowAndRepayFresh.cvl` | `bf48f8106272327fbdecab7f118647808277f4d6` — correspondência exata |
| `spec/formal/accrueInterest.cvl` | `184e0fb1ad0117e9bcc45aef3241a544cffaae8b` — correspondência exata |
| `spec/formal/mintAndRedeemFresh.cvl` | `379bcd70c9571bd7c2096a8ab8b953a72c241730` — correspondência exata |

## Limites
- Outros arquivos, mappings e wrappers sintéticos podem diferir. Em especial `interestRateModelGetBorrowRate()` não existe na ABI de CToken/CErc20Certora catalogada; isso permanece pendente para a propriedade incomplete #7.
- Não criar helper para suprir selector ausente; reconstrução exige evidência do harness usado.
- `source_commit_audited` da matriz registra o SHA do *source report*; a correspondência de 5 blobs não equivale a prova de execução de 41 specs.
- SEM ALTERAÇÕES EM SPECS; SEM COMPILAÇÃO CVL2; SEM PROVER; SEM TESTE CVL1.
