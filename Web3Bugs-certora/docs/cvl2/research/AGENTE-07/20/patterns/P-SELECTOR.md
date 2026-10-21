# P-SELECTOR — Method literals versus variáveis method

**AGENTE-07 Fase 1 — Nota de padrão. Não é patch CVL2 nem prova de aplicabilidade automática.**

## Evidência
IDs: A2-SELECTOR.
Referência: https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html

## Regra documental específica
Method literal em CVL2 usa sig:foo(types).selector; f.selector de parâmetro method é diferente.

## Plano conservador de mudança candidata
Verificar o segmento exato na propriedade: só prefixar sig: num method literal não já prefixado.

## Risco de alteração semântica
Adição espúria de sig: altera sintaxe/capacidade de selecionar funções e filtros.

## Gate de promoção
1. Exigir linha de CVL original, original source path e contexto de import/target no dossier da property.
2. Associar evidência A1/A2 a esse caso específico e reconstruir qualquer target/ABI original necessário.
3. Distinguir erro original / dependência ausente / CLI / incompatibilidade CVL1→CVL2.
4. Não executar script de migração ou compilar nesta fase; exigir autorização antes de testar e demonstrar preservação semântica.


## Evidence recheck — 2026-10-19
- Full-source verification was performed for all 37 extracted N.spec instances; refer to full_spec_audit.csv for exact file, byte SHA, line and candidate details.
- Simple token scanner occurrences in this project: 56 directly matching this pattern name (zero is not proof of absence; some pattern classifications are semantic rather than lexical).
- No generic Certora migration example is sufficient evidence for an automatic transformation; verify before/after for the actual original rule, ABI, receiver, summary, ghosts, storage and reverts. See official CVL2 migration and changes documentation.
