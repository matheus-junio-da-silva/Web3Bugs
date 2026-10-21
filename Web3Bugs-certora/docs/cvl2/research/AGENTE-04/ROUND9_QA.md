# AGENTE-04 — RODADA 9 — QA, contagem e gate

**Pré-condição de infraestrutura checada:** o WSL DESKTOP-5E26TVU respondeu com Linux, Python 3.14.4, Git 2.53.0, solc 0.8.10 e 0.6.12, capacidade e leitura/escrita em novo /tmp, checkouts antigos limpos e clone **isolado** clean na HEAD inicial \`06dca368f5f2324da45f156dd9bc206745f11af0\`. Nenhum checkout de colega alterado.

**CLI/execução:** \`certora-cli 8.19.0\` versão confirmada, \`--compilation_steps_only\`, timeout 65s, HOME isolado, credenciais não exportadas, inputs SHA, resultados em \`ROUND9_ATTEMPTS.json\`. Seis execuções (3 propriedades): quatro parser errors originais, uma falha import SOLC, **uma derivada compilation-only exit 0**. Apenas **três propriedades** originais com COMPILE_ERROR acumulado (P12/23 e /25; P15/36), **154 NOT_RUN**, zero originais COMPILE_OK, **uma derivada COMPILE_OK**, zero SEMANTIC_PROVEN, 0/3 projetos migrados.

**Integridade executada no clone:** 157 N.spec SHA256 recalculados + 157 source hashes recalculados, todos idênticos à matriz R8; 157 chaves distintas, P15=116/P12=26/P2=15; todos Bug Labels/Property/Target/Result/Detection Outcome reconciliados ao CSV original sem divergências. N.spec/código histórico permanece intacto. Os outputs stdout/stderr são preservados como strings JSON de bytes originais e acompanhados de sha256 por execução; logs auxiliares no /tmp são efêmeros.

## Comandos obrigatórios após HEAD final publicada

Os quatro comandos exigidos foram **efetivamente executados depois do primeiro commit R9 `acf48b1739e1a488baf146926a4a067b078c7f48`**, no worktree isolado sobre essa HEAD. Não inferidos da CI. CWD \`Web3Bugs-certora/\`: \`python3 scripts/check_specs.py .\`, \`python3 scripts/check_contests_csv.py .\`, \`python3 scripts/check_contracts.py .\`. CWD raiz Git: \`git -c core.whitespace=cr-at-eol diff --check 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3...HEAD\`. **RESULTADO OBSERVADO na HEAD `acf48b17`: os três scripts EXIT 0; `check_specs.py` confirmou 1386 exemplos e 1390 relações; diff exato BASE...HEAD EXIT 0; 250 arquivos no diff completo, todos na pasta AGENTE-04, worktree limpa.** Após publicar este adendo, os quatro checks devem ser repetidos na HEAD final e o resultado informado no comentário do PR. Se EIO/SIGBUS/EROFS reaparecer, suspender e registrar INFRA_BLOCKED. Um workflow GitHub SUCCESS não substitui esses comandos.

**Gate vermelho semântico:** envfree, receiver, globals, ABI histórica P12, summary externo Chainlink P2 e counterexamples não demonstrados; a compilação da derivada R9 não transforma Result histórico em resultado novo.

**AGENTE-04 — RODADA 9 / EVIDÊNCIAS, TESTES CONTROLADOS E CONTRARREVISÃO**
