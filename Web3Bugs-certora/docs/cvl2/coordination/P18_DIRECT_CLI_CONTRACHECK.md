# Contraprova independente — OpenZeppelin P18/3 e P18/23

**Data:** 20/10/2026. **Contexto:** AGENTE-02 [PR #37](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/37) teve nove tentativas `certoraRun` bloqueadas pela exigência de token antes do parser. Este documento distingue a falha ambiental das incompatibilidades reais de CVL2. O coordenador executou o CLI diretamente num WSL autorizado, sem variáveis de credenciais e sem Prover.

## Execução reprodutível

Fonte imutável: Web3Bugs baseline `2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3`.
CLI observado: `/home/mat/certora-ac-audit/certora_venv/bin/certoraRun` **certora-cli 8.19.0**.
Compilador: `/home/mat/.solc-select/artifacts/solc-0.8.6/solc-0.8.6`.
Cópias temporárias das 2 specs e da árvore Solidity em `/tmp/cvl2-coord-r5-p18-{3,23}-20261020/`.
Cwd: cada diretório temporário. `HOME` temporário. `CERTORAKEY`, `CERTORA_TOKEN`, `CERTORA_API_KEY` removidas do subprocesso. `timeout --kill-after=5s 60s`.

```bash
certoraRun contracts/mocks/AccessControlMock.sol:AccessControlMock \
  --verify AccessControlMock:specs/property.spec \
  --compilation_steps_only --solc /home/mat/.solc-select/artifacts/solc-0.8.6/solc-0.8.6

certoraRun contracts/mocks/ERC1155Mock.sol:ERC1155Mock \
  --verify ERC1155Mock:specs/property.spec \
  --compilation_steps_only --solc /home/mat/.solc-select/artifacts/solc-0.8.6/solc-0.8.6
```

| Original | SHA-256 do original E da cópia | EXIT | Erro efetivamente observado |
| --- | --- | ---: | --- |
| `results/spec/complete/18/3.spec` | `5ca7758775888bd0f8275e7f00a41b3dd8056668bc647bb7478010b1dff702c2` | **1** | `property.spec:8:5` e `:9:5`: entrada de `methods` requer `function`; `:8:32` e `:9:52`: requer terminador `;` |
| `results/spec/complete/18/23.spec` | `3c2ac679b19f75c7777d3221c858337529a4646a18bcb194bf6a812d64ba16c9` | **1** | `property.spec:8:5` e `:9:5`: exige `function`; `:8:61` e `:9:64`: exige `;` |

Os dois arquivos fonte e suas cópias tiveram `sha256sum` idênticos, sem edição de sintaxe, requirements ou assertions. Ambos alcançaram o parser CVL2 e exibiram a mensagem concreta `Since CVL 2, methods block entries must begin with function`; **não houve bloqueio por token nesse caminho de execução**. Stdout/stderr integrais permanecem somente na máquina WSL nos diretórios temporários citados, não sendo parte da trilha arquivada neste PR (limitação de reprodutibilidade).

## Classificação e interpretação

- Contar ambos como `COMPILE_ERROR` real de CVL2, diferentemente das nove falhas de `CERTORAKEY` do agente, que são `PREFLIGHT_AUTH_BLOCKED` e **não são novas propriedades compiladas ou rejeitadas pelo parser**.
- Não converter automaticamente `methods` antigos para `function ... external;`: `public` no Solidity pode significar chamadas internas ou externas, e summaries dependem de receiver/dispatch.
- Mesmo se uma variante em scratch compilar futuramente, isso não equivale à spec CVL1 completa, mesma ABI/runner histórico, nem a resultado VERIFIED ou preservação de contraexemplos.
- PR #37 permanece documental em Draft; nenhuma spec derivada foi produzida para P18. Nenhum arquivo histórico foi modificado, nenhum Prover executado.
