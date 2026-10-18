# FAROL — validação independente Project 18

**Data:** 2026-10-18. **Branch:** fix/semantic-p18-farol. **Base main:** 80f551f23bbd86d7901c6a28e7f44c68aebae8fd.

## Execuções locais reais

Ubuntu VM: Python 3 disponível como python3; o executável python não existia (primeira tentativa exit 127). Um symlink temporário /home/mat/farol-p18/bin/python → python3 foi criado FORA do checkout, com PATH configurado apenas durante os comandos exigidos. Os comandos abaixo são os comandos literais solicitados, executados com o alias Python 3:


### python scripts/check_specs.py . — exit 0

~~~text
Check passed! 1222 spec examples and 1227 Bug Label relationships are structurally consistent.
~~~

### python scripts/check_contests_csv.py . — exit 0

~~~text
Check passed!

	`./results/contests.csv` is consistant with `./reports`
~~~

### python scripts/check_contracts.py . — exit 0

~~~text
Check passed!

	`./contracts` is consistant with `./reports`
~~~

### git diff whitespace — exit 0

Comando na raiz da cópia Git real antes do commit: git -c core.whitespace=cr-at-eol diff --check origin/main. Após commit também será executado o comando exigido origin/main...HEAD.

## Reconciliação com main / fontes históricas

- 1222 exemplos e 1227 relacionamentos estruturais aprovados pelo validador. Mudanças específicas: 5 linhas do Project 18 no spec_buglabel.csv (Bug Label + Detection Intent), sem Result ou Outcome alterados.
- results/bugs.csv original e atual SHA256 c3507feeb4d743f6ee182a11ba68dcf6485865556817702d5cbc18eaf337189b.
- results/contests.csv original e atual SHA256 570d74bb8776030afc575dae0c2bb247bbe9ec46a29e40d4171e04f87f57aad8.
- resources/18/OZ-final-report.pdf original e atual SHA256 4a35df36c47e6e7e2b4333cb3890bc2a8cbca569e32b2fc6f24820b8a56cbc37.
- Project 18: 177 NOT_STATED/NOT_STATED, 4 VIOLATED/FINDING históricos. As entradas de quatro violações não foram modificadas.
- 24 declarações N.md receberam documentação; 19 registros multi-assert da matriz semântica foram atualizados; original CERES (PR #22) e todos os contratos históricos intactos.

## Publicação e CI

A verificação de diff origin/main...HEAD, commit SHA e evidência GitHub Actions (se houver) são registrados no PR e na complementação deste arquivo após a publicação. CI não deve ser alegado como PASS antes de observar o run.
