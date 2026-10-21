# AGENTE-08 — Regras e riscos CVL1 → CVL2 (somente hipóteses)

**Fase 1: este documento não substitui os dossiês por exemplo.** Referência A1: [Migration Guide](https://docs.certora.com/en/latest/docs/cvl/cvl2/migration.html), seções Step 2–4, e [Changes Introduced in CVL 2](https://docs.certora.com/en/latest/docs/cvl/cvl2/changes.html), seções Superficial syntax / Methods / Integer types / Removed features. A2: [Methods Block](https://docs.certora.com/en/latest/docs/cvl/methods.html). Páginas consultadas em 2026-10-19; versões executadas: nenhuma.

## E-METHODS — assinatura, despacho e receptor
- CVL1 pode conter `methods { foo(uint256) returns uint256 envfree }`. Em CVL2, o formato candidato é `function foo(uint256) external returns(uint256) envfree;` **somente depois de confirmar no Solidity se a chamada é external, internal ou pública compilada nas duas modalidades**.
- Summaries CVL1 alcançavam todas as implementações da assinatura; CVL2 presume `currentContract`. A forma wildcard `function _.foo(uint256) external => NONDET;` pode ser necessária para manter escopo global, mas não deve ser usada sem correspondência comprovada. Contratos secundários `using ... as ...` exigem resolução específica.
- Risco: restringir o receiver pode tornar a regra vacuamente verdadeira, expandir summaries pode mascarar efeitos ou criar falsos contraexemplos. Alternativa conservadora: manter uma anotação de compatibilidade pendente e não produzir spec compilável na Fase 1.

## E-INV — chamadas, reverts e seleção de métodos
- Documentação A1 Step 2: `sinvoke f(...)` tem candidato `f(...)`; `invoke f(...)` tem candidato `f@withrevert(...)`. Não alterar a posição de `lastReverted`, guards ou storage inicial. Fonte precisa está no N.spec citado por cada dossiê.
- Se houver literal `f.selector == fn(uint).selector`, a documentação A1 exige `sig:fn(uint).selector` **para o literal**, não para `f.selector` (E-SELECTOR). A presença de `.selector` sozinha não prova incompatibilidade.
- Risco: passar a explorar caminhos com reverts antes ignorados ou vice-versa. Alternativa: esperar comparação formal de paths na fase posterior.

## E-SEMICOLON — declarações históricas
- CVL2 requer terminador `;` nos `import`, `using` e `use`. `invariant` com `filtered`/`preserved` pode dispensar semicolon conforme seção oficial. Não adicionar `;` cegamente após comentários ou blocos.

## E-MATH — tipos/quantificadores
- CVL2 diferencia `mathint` e inteiros de largura fixa. `assert_` pode gerar contraexemplo, `require_` pode eliminar casos e mascarar bugs (guia A1 Step 3). Nunca propor `require_` como atalho automático; recast só com argumento explícito, domínio e bounds preservados.

## Condição para fase posterior
Para cada transformação, reabrir o N.spec, sua original source range e N.txt; verificar harness ABI, scripts/flags e original Result; comparar mesmo alcance, preconditions, ghosts/hooks, quantificadores, storage e possíveis contraexemplos. Sem reconstrução do modelo original, marcar UNRESOLVED_CANDIDATE, mesmo se sintaxe parecer simples.

## Famílias Notional — casos a revisar individualmente
- **P13/8–17:** `Balances.spec` tem regras ainda vazias/aspiracionais e não possui target de verificação selecionado nos scripts, ver fonte [Balances.spec](https://github.com/matheus-junio-da-silva/Web3Bugs/blob/2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3/Web3Bugs-certora/contracts/13/certora/accountContext/Balances.spec). Nenhum syntactic fix cria uma ABI comprovada.
- **P13/39:** a fórmula de settlement usa comparação sobre estado inicial zero que contraria a explicação report-level. Não substituir por implicação intuitiva nem atribuir ✔ ao texto executável.
- **P13/1, 58:** `assert false` diagnostica alcançabilidade, não constitui propriedade de segurança verificada.
- **P13/7, 57:** implicações tautológicas documentadas devem permanecer distinguíveis por source e target.
- **P13 com target identificado:** scripts históricos e imports transitivos de OpenZeppelin 3.4, Compound, Chainlink e Notional precisam de origem exata, checksums e remappings. Não aplicar automaticamente semântica de bibliotecas contemporâneas.

<!-- AGENTE08-R2 -->
## Contrarrevisão P13: targets, imports e 7 versus 5 VERIFIED
O verify.sh original fixa solc7.5, @openzeppelin remapeado para Brownie OpenZeppelin/openzeppelin-contracts@3.4.0-solc-0.7, compound-finance como pacote Brownie e interfaces da árvore histórica. Fonte de destino e checksum das dependências carregadas pelo antigo auditor permanecem indisponíveis. scripts/applyHarness.sh altera Constants.sol de internal constant para public constant, afetando observabilidade do target.
As 48 regras com target definido/inferido dependem de imports transitivos ausentes; os dez exemplos #8-17 de Balances.spec não têm ABI histórica selecionada nos scripts. O PDF original Notional1Nov2021.pdf (páginas 13-16) contém indicadores de provas: docs/spec_catalog_project_13.md menciona sete regras VERIFIED, mas o CSV atual registra #32/#34 NOT_STATED e consequentemente cinco VERIFIED. Esta divergência permanece documentada, sem corrigir silenciosamente o catálogo. #1/#58 são diagnósticos, #7/#57 tautologias, #39 contém um ramo contraditório.
