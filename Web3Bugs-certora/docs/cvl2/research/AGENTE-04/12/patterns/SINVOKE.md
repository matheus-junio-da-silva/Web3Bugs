# SINVOKE — Trocar sinvoke para chamada direta mantendo parâmetros/estado.

- Official documentation (A1): https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html#invoke-sinvoke-and-call (acesso 2026-10-19).
- Aplicações reconhecidas nas 11 instâncias: incomplete/8, incomplete/9, complete/10, complete/11, complete/12, complete/13, complete/14, complete/15, complete/16, complete/17, complete/18.
- Cada dossiê identifica trechos reais; a anotação internal/external, receiver, casts e alvos requerem prova independente. Não executar migração in-place no arquivo original.

## Anotacao da contrarrevisao 2026-10-19
Propostas por ocorrencia literal nos dossies individuais. Verificar [A1](https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html) e [A2](https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html); nao alterar receiver, summaries, args, quantificadores, storage, revert ou condicoes antes de fechar ABI historica.
