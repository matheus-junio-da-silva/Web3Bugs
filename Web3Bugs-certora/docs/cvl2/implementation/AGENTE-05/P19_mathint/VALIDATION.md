# Validação e reprodução — AGENTE-05 P19 / Phase 2

## Verificações observadas nesta retomada

- A terceira revisão [PR #44](https://github.com/matheus-junio-da-silva/Web3Bugs/pull/44#pullrequestreview-5577673176) foi lida integralmente antes do trabalho.
- Os dois arquivos originais foram obtidos da `main@2a03637b7639d0a5ad4b5c54cf8a0a5ba647b6a3` via GitHub. Em cada um, a transformação ocorreu **uma** vez e a comparação linha-a-linha retornou **uma linha alterada**; conteúdo restante preservado.
- Hashes originais: P19/1 `279c6c956d9084cb576f9e3f99dba63936d27b6e07401f9878751ac22808016a`; P19/2 `132af5147a37652fe4318fc3fda8b6148fe6da0cc3195397c86d1527677c3df7`. Hashes derivados: P19/1 `6dff6a352b42887fbf8c8679a16cb35c20489fefd668ce960146e701fe4ff4af`; P19/2 `cffd0de64eef3d466acbd706967e4729fd8aa8ad12e2e3376ba241eafa9adac3`. Coincidem com o experimento independente.
- Compilação independente do coordenador: **exit 0 em ambos**, `certora-cli 8.19.0`, `solc 0.8.7`, `--compilation_steps_only`, timeout 60s. Essa informação provém da revisão externa, não de uma execução deste agente.
- **Bloqueio de reexecução:** `DESKTOP-5E26TVU` não respondeu a vários comandos e pings e passou a **Offline**. Nesta retomada, NÃO foram observados stdout/stderr, duração nem exit code próprios da nova compilação; não foram gerados logs falsos. O ambiente local alternativo não forneceu uma CLI Certora operacional.

## Reproduzir com WSL autorizado (assim que disponível)

Executar os passos **separadamente** para `N=1` e `N=2` em checkout isolado. O comando abaixo executa apenas compilação, sem verificação formal. Não compartilhar credenciais. Em diretórios temporários vazios, copie apenas a spec derivada e `Dummy.sol`, valide `sha256sum`, execute:

```bash
N=1
REPO=/CAMINHO/DO/CHECKOUT/Web3Bugs-certora
TMP=$(mktemp -d)
cp "$REPO/results/cvl2/02_unresolved/19/$N.spec" "$TMP/property.spec"
cp "$REPO/contracts/19/spec/harnesses/Dummy.sol" "$TMP/Dummy.sol"
cd "$TMP"
sha256sum property.spec Dummy.sol
mkdir -p home
START=$(date +%s%N)
HOME="$PWD/home" XDG_CONFIG_HOME="$PWD/home/config" \
 timeout --signal=TERM --kill-after=5s 60s \
 /home/mat/certora-ac-audit/certora_venv/bin/certoraRun \
 Dummy.sol:Dummy --verify Dummy:property.spec \
 --compilation_steps_only \
 --solc /home/mat/.solc-select/artifacts/solc-0.8.7/solc-0.8.7 \
 > compilation.stdout.log 2> compilation.stderr.log
RC=$?
END=$(date +%s%N)
printf 'exit=%s duration_ms=%s\n' "$RC" "$(((END-START)/1000000))"
```

Executar em ambiente sem credenciais carregadas; **não** submeter job ao Prover. Uma execução `timeout` exit 124 deve ser classificada TIMEOUT, não COMPILE_OK. Sanitizar logs antes de publicá-los.

## Validadores e diff

Reexecutar com checkout disponível os três validadores `python3 scripts/check_specs.py .`, `python3 scripts/check_contests_csv.py .`, `python3 scripts/check_contracts.py .` a partir de `Web3Bugs-certora`; e `git diff --check <BASE>...HEAD`, incluindo a checagem de escopo. **Nenhum exit code fresco desses comandos foi obtido nesta retomada.** Os três validadores tiveram exit 0 na revisão documental anterior do PR #44, mas isso não substitui nova medição.

As duas specs derivadas preservam whitespace do arquivo original porque somente uma linha foi autorizada para edição. Com arquivos novos, `git diff --check` pode sinalizar trailing whitespace herdado; essa falha deverá ser registrada explicitamente, não corrigida alterando linhas não autorizadas ou escondida como PASS.

**Status 02_unresolved; SEM PROVER, CVL1, merge ou modificação adicional.**
