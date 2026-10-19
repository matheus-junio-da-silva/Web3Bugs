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
