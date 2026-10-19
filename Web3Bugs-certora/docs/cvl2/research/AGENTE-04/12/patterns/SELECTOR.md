# SELECTOR — Adicionar sig: só a literal de método.

- Official documentation (A1): https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html#method-literals-require-sig (acesso 2026-10-19).
- Aplicações reconhecidas nas 1 instâncias: complete/11.
- Cada dossiê identifica trechos reais; a anotação internal/external, receiver, casts e alvos requerem prova independente. Não executar migração in-place no arquivo original.

## Anotacao da contrarrevisao 2026-10-19
Propostas por ocorrencia literal nos dossies individuais. Verificar [A1](https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html) e [A2](https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html); nao alterar receiver, summaries, args, quantificadores, storage, revert ou condicoes antes de fechar ABI historica.
