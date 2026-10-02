# Modificações em relação ao Web3Bugs

O `Web3Bugs-certora` mantém a estrutura e a taxonomia de labels do Web3Bugs, com as seguintes alterações deliberadas:

- **Todas as severidades são catalogadas**, e não apenas findings High.
- Em `results/bugs.csv`, a coluna **`Difficulty` foi substituída por `Severity`**.
- O campo `Severity` preserva a severidade informada pelo relatório de auditoria/verificação de origem.
- Os projetos-fonte são os projetos Certora coletados no [PropertyGPT](https://github.com/matheus-junio-da-silva/PropertyGPT).
- Os relatórios são mantidos em `reports/` somente em formato Markdown.

As demais convenções do Web3Bugs devem ser mantidas sempre que aplicáveis.
