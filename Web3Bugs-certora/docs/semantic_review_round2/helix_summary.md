# HELIX — auditoria semântica independente, rodada 2

Data: 2026-10-18. Fonte catalogada: `matheus-junio-da-silva/Web3Bugs`, branch `main` consultada via GitHub. Artefato: [`helix_review.csv`](helix_review.csv) (exatamente **184** decisões).

## Totais e critério

| Escopo | Decisões | CONFIRMED | CORRECTION_REQUIRED | INCONCLUSIVE |
|---|---:|---:|---:|---:|
| Furucombo #129–266 | 138 | 132 | 6 | 0 |
| Radicle Drips #1–46 | 46 | 15 | 3 | 28 |
| **Total** | **184** | **147** | **9** | **28** |

`CONFIRMED` significa consistência documental verificada da **assertion, categoria, incompletude e resultado historicamente alegado**, **não** Prover rerun ou ABI compilada. `CORRECTION_REQUIRED` exige melhoria concreta no catálogo; `INCONCLUSIVE` é reservado aos targets sem harness/ABI recriável, mesmo quando a intenção CVL ou inexistência de prova histórica é clara. `NOT_STATED` significa que não há prova individual atribuível: não equivale a `VERIFIED`.

## Procedimento e limitações

1. Inspecionadas as seis rules ativas de `contracts/10/specs/proxy.spec` (#27–32), seu `arbitrary(method f)`, getters, precondições e drivers `_runHandler.sh`/`applyHarnesses.sh`; verificados os nomes dos **23** handlers contra a árvore atual de `contracts/10/contracts/handlers/`. Os **15** handlers nominais preservados e os **8** ausentes não são equiparados a `ProxyHarness`. Registrei o critério de resultado individual por target e PDF p.26–31.
2. Para Radicle, reconstruídos os **46** predicados das seis specs originais, sem equiparar os nomes homônimos de `Splits.spec` e `Splits2.spec`; cruzados com `DripsHub.sol`, `Drips.sol`, `Reserve.sol` e `Splits.sol`. O relatório oficial atesta **somente `Splits.sol`** (commit `6fe9d38`), sob loop unrolling até duas iterações e limites de `2^128` para certas somas. <https://certora.cdn.prismic.io/certora/ac54e881-b3ec-407a-a52b-ca17fc2c0240_Formal_Verification_Report_of_Radicle_Drips_Contracts.pdf>.
3. O snapshot ZIP inicialmente disponibilizado foi examinado, mas corresponde a árvore antiga (HEAD local `4a1bea89d88aa3b6aa165e8d81b8dd523c7afb82`), **sem Projects 10 e 23**. Para esses projetos foram consultados os arquivos atuais no GitHub. Não houve replay Certora nem checkout integral atualizado: isso limita a certeza quanto a versões efetivamente compiladas e ABI pós-Perl.
4. O PDF de Radicle foi inspecionado na fonte oficial (páginas 1–6), incluindo a tabela de regras. O PDF binário de Furucombo não pôde ser lido diretamente nesta execução; referências de página/coluna #27–32 foram confrontadas com a transcrição paginada do repositório e com revisão publicada, **não representam verificação visual independente do binário**. Não há bases suficientes para afirmar sucesso de qualquer um dos 138 jobs individualizados.

## Achados por prioridade

### P0 — Furucombo: `HBProtocol` e injeção de getters (6 decisões de correção)

**Exemplos 165–170**: `HBProtocol.sol` declara `contract HBProtocol is HMaker`, enquanto `_runHandler.sh` injeta `getSlot`, `getStackLengthSlot`, `getStackLength`, `getSender`, `getCubeCounter` apenas ao localizar textualmente a herança `is HandlerBase ... {` no **handler_file** selecionado. `HMaker.sol` importado não é processado como arquivo de destino desse Perl. Logo o handler HBProtocol não ganha por esse passo os getters exigidos por #27–32. Corrigir em cada `N.md` e `N.txt` a justificativa de incompletude com este desencaixe concreto. A ressalva genérica de 'getter/harness incompatibility' não basta. Não substituir a fonte por um patch inventado.

### P1 — Radicle: classificação estrita de oráculos e target

- **Exemplo 27 (`integrityOfCollect`)**: propor `S3-1` em lugar de `S6-4`. A assert ativa é `collectableAfter == 0`; o erro diretamente falsificador é a falta de limpeza do saldo armazenado por `_collect`, isto é, **missing state update**, e não arbitrariamente um erro de cálculo.
- **Exemplo 28 (`revertCharacteristicsOfCollect`)**: propor `SC` em lugar de `L8`. A regra `assert !lastReverted` não identifica especificamente um low-level call ou biblioteca como causa de reversão, exigido para `L8` em `docs/standard.md`; requer categorização semanticamente vinculada à chamada `collect`.
- **Exemplo 46 (`Splits2.revertCharacteristicsOfSplit`)**: propor `SC` em lugar de `L8` pelo mesmo critério. Não atribuir status `VERIFIED` com base em `Splits.spec` e seu próprio histórico.
- **Exemplos 1–24 e 42–45**: decisão `INCONCLUSIVE` sobre a relação CVL/ABI efetiva. `DripsHubHarness`, `UpdateReceiverStatesHarness`, `ReserveHarness`, `SlotTester` e wrappers de `Splits2` não foram reconstruídos. Conservar seus Result/Outcome `NOT_STATED`, mesmo quando o PDF contém propriedade homônima de outro target.

### P1 — Interpretação histórica individual de Furucombo

As seis rules não têm filtro `!isHandler()`, ao contrário de outras rules de `proxy.spec`, de modo que as 138 combinações são **aplicáveis em princípio**. Todavia o sucesso de uma proof do ProxyHarness não é prova do handler. Cada run altera `currentContract`, universo de métodos `f`, possíveis callbacks/summaries, imports, instrumentação, getters e ABI. Foram identificados oito targets Solidity ausentes, cinco também sem driver específico, além de imports `@openzeppelin` não vendorizados e da substituição `SafeERC20.sol → ERC20.sol`. Os **138 resultados individuais** permanecem `NOT_STATED / NOT_STATED`; símbolos `🔎` ou texto `None` na tabela não certificam sucesso. Não confundir a regra `noOverwrite` com o finding histórico de corrupção de **memória**, pois a assertion consulta **storage** por `getSlot`.

### P2 — Clareza e limitações adicionais

- #27 Furucombo: a afirmação sobre crescimento da stack depende da semântica de `uint256` de `stackLengthBefore + 1000000`. Não há precondição explícita de margem numérica nessa regra (diferentemente de `noOverwrite`); registrar o edge case como **não resolvido**, sem afirmar bug de overflow provado.
- Radicle #36: regra `splitReceiverShouldGetMoneyUponSplit` é **VIOLATED / FINDING** no PDF oficial, devido a arredondamento inteiro para zero, `L2` condizente com `docs/standard.md`. Essa constatação não demonstra exploração arbitrária nem transfere o resultado a outro contrato.
- Radicle #38: `cannotFrontRunSplitGeneralCase` teve **timeout**, `NOT_STATED / INCONCLUSIVE`; as três variantes restritas #39–41 são **VERIFIED / NO_FINDING** separadamente, e nenhuma delas prova a variante geral.
- `UNMAPPED` permanece defensável para probes de `assert false` e inspeção irrestrita de quem altera um saldo. Uma igualdade pré/pós incondicional sem excluir escritores legítimos não é automaticamente uma vulnerabilidade.

## Evidência e referências

- CVL Furucombo: `https://github.com/matheus-junio-da-silva/Web3Bugs/blob/main/Web3Bugs-certora/contracts/10/specs/proxy.spec`. Driver: `https://github.com/matheus-junio-da-silva/Web3Bugs/blob/main/Web3Bugs-certora/contracts/10/specs/scripts/_runHandler.sh`. Solidity: `https://github.com/matheus-junio-da-silva/Web3Bugs/blob/main/Web3Bugs-certora/contracts/10/contracts/handlers/bprotocol/HBProtocol.sol` e `https://github.com/matheus-junio-da-silva/Web3Bugs/blob/main/Web3Bugs-certora/contracts/10/contracts/Storage.sol`.
- Leitura cruzada Ceres: <https://github.com/matheus-junio-da-silva/Web3Bugs/pull/8#issuecomment-6254000743>; as conclusões foram testadas contra o padrão Perl e a declaração original de herança, não adotadas como autoridade.
- CVL Radicle: `https://github.com/matheus-junio-da-silva/Web3Bugs/blob/main/Web3Bugs-certora/contracts/23/specs/`, Solidity: `https://github.com/matheus-junio-da-silva/Web3Bugs/blob/main/Web3Bugs-certora/contracts/23/src/`. PDF oficial: <https://certora.cdn.prismic.io/certora/ac54e881-b3ec-407a-a52b-ca17fc2c0240_Formal_Verification_Report_of_Radicle_Drips_Contracts.pdf>. Taxonomia: <https://github.com/matheus-junio-da-silva/Web3Bugs/blob/main/docs/standard.md>.

## Reprodutibilidade e encaminhamento

A matriz contém uma linha por par (`project_id`,`example_id`), predicado, guards, dependências, método/storage relevantes, hipótese falsificadora, label atual/proposto, resultado/outcome atuais/propostos, PDF e decisão/risco. Recomendo revisar primeiramente as seis correções P0 de HBProtocol, depois as três propostas taxonômicas P1 e os 28 registros inconclusivos até obter os harnesses/ABI e scripts originais. **Não foram alterados os catálogos originais e nenhum merge foi realizado.**
