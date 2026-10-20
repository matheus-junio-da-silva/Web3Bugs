# Incidente operacional — WSL/Remote Desktop Commander — 20/10/2026

**Status:** `INFRA_BLOCKED`; proibição operacional temporária de novos testes/alterações no filesystem comprometido. O dispositivo `DESKTOP-5E26TVU` responde como conectado, mas isso **não atesta** a integridade do volume.

## Evidência observada

- Agentes 01,02,03,05,06,07,08 reportaram na Rodada 6: `Bus error`, saída 135 de processos Python/CLI, `EROFS` (read-only filesystem), `Input/output error` em acesso a dados e/ou falha no setup de scratch.
- O coordenador tentou três comandos triviais via Remote Desktop Commander: `df -h /home/mat`, `python3 --version` e `ls -ld /tmp`. **Todos falharam antes de iniciar o processo, com `Error: spawn EIO`**. Não seria válido declarar `check_specs.py`, `git diff --check` ou `certoraRun` executados neste ambiente depois disso.
- Pelo GitHub, os oito commits da Rodada 6 têm workflow `validate: success` e arquivos somente no diretório documental do agente; CI GitHub é independente do filesystem local e **não valida semântica**.

## Conduta segura

1. **Não escrever no WSL afetado:** nada de `git reset`, `rebase`, `rm -rf`, reinstalação de solc, recuperação de packages, comandos de patch ou Prover. Esses comandos poderiam perder worktrees/cache, além de produzir logs inconfiáveis.
2. A recuperação do ambiente depende do **usuário que administra o computador**. Primeiro confirmar backups e a saúde/espaço da unidade Windows/WSL e preservar logs do problema. O administrador pode usar os recursos documentados do Windows/WSL para reiniciar o subsistema de modo controlado, após encerrar processos e confirmar que não há trabalhos em andamento; não executar reinicialização automaticamente desta conexão.
3. Depois da recuperação e **antes** de liberar qualquer compilação: confirmar que leitura e escrita em um **diretório temporário novo** funcionam; que Python e `git` executam; que worktrees de cada agente têm HEAD/caminhos esperados e estão limpas; executar `git status`, os três validadores do catálogo e `git diff --check BASE...HEAD` em ambiente estável.
4. Retomar somente um diagnóstico por vez, com `--compilation_steps_only`, limites de tempo/CPU, `HOME` scratch, credenciais não exportadas, source hashes e logs; não utilizar outputs pré-falha como se fossem pós-recuperação.
5. Enquanto isso, agentes continuam podendo pesquisar source/ABI/public GitHub em sessões independentes, publicar documentação na própria pasta via conector GitHub e realizar cross-review read-only. **Proibido inventar `exit 0` ou `COMPILE_ERROR` sem execução.**

## Gate para atualização de progresso

O painel Round 6 contabiliza **4 COMPILE_OK, 12 COMPILE_ERROR, 1370 NOT_RUN**, todos baseados nas observações de compilação pré-incidente ou no caso P15/36 efetivamente executado pelo AGENTE-04. Nenhum indicador pode aumentar por `SIGBUS`, `EROFS`, CLI `--version`, ABI Solidity ou CI estrutural.

**Ação humana necessária:** recuperação controlada do volume WSL/Remote Desktop Commander para permitir novos testes. Não exige acesso a tokens, chaves ou `.env`, nem compartilhar segredos com agentes.
