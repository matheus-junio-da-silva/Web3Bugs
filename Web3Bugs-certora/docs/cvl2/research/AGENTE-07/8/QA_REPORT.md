# AGENTE-07 — QA Project 8

## Reconciliação contra baseline 2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3
- CSV canônico Git blob SHA: `97e20443586540034a4c0305ce1db19b0d2f8cb5`; referências de metadata: 42; exemplos únicos após chave canônica: **42**.
- Complete: **0**; incomplete: **42**; esperados 0/42.
- Diretórios de artefatos de `results/spec` consultados no GitHub: 0 `.spec` complete + 42 `.spec` incomplete, e 42 `N.txt` incomplete.
- Árvore documental publicada no PR #41 (draft); dossiês numerados sem lacunas para os IDs atribuídos, validados novamente após publicação.

## Riscos que impedem promoção para status definitivo
- O relatório matemático existente registra W1 na família rayMul (inputs x=1,y=0) e W2/W3 em accrueYieldCheck. Esses modelos podem tornar provas vacuamente verdadeiras. Não modificar axiomas sem autorização; não atribuir W2/W3 a outro source não coberto.
- Histórico auditado e módulos transitivos não reconstruídos com prova individual do blob/commit para cada incomplete. Manifesto registra BLOCKED_PROVENANCE, não recuperações fictícias.
- Alguns dossiês incluem um trecho de CVL limitado a ~2.100 caracteres como orientação documental; esse trecho NÃO deve substituir a declaração integral na `.spec` histórica. Revisão independente deve confirmar integralmente assertions, dependencies e bounds antes de Fase 2.
- IDs de padrões referidos nas hipóteses são candidatos sintáticos; `cvl1_cvl2_change_ids` do CSV aponta ao relatório individual, não representa mudança aprovada.

## Validações realmente realizadas
- Leitura via conector GitHub de HEADs Web3Bugs e PropertyGPT: conferidos contra os baselines fornecidos.
- Contagem dos nomes de `.spec`/`.txt` por diretório GitHub e confronto com CSV; deduplicação por (Project ID, Status, Example ID) feita em memória.
- Contraste de exemplos individuais com `.spec`, `.md` e `N.txt` do catálogo, sem reescrita das fontes.
- Exame de documentação oficial Certora CVL2 (link e seção em evidence_register.csv).
- NÃO executados nesta fase: validadores Python do repositório, `git diff --check` local, CVL1, CVL2, Prover, equivalência experimental. **Nenhum exit code é atribuído a comandos não rodados**.

## Encaminhamento
- Antes de qualquer Fase 2: fechamento do commit auditado, comparação ABI/harness, provabilidade dos axiomas e revisão humana de alterações candidatas. Nenhuma autorização de implementação inferida.
- SEM ALTERAÇÕES EM SPECS; SEM COMPILAÇÃO CVL2; SEM PROVER; SEM TESTE CVL1.

## QA complementar de referências CVL2
- `properties.csv` agora contém IDs P-... explícitos para cada dossiê com padrão detectado; IDs derivam das hipóteses documentadas, não representam alterações CVL2 aprovadas. Campo vazio significa sem padrão sinalizado nesta pesquisa, nunca compilação bem-sucedida.
