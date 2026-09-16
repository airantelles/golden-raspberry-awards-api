Agora você deve revisar toda a implementação como se estivesse analisando um pull request submetido por um candidato a uma posição de especialista Python.

Use as skills:

- architecture-review;
- python-review.

Primeiro faça a revisão sem alterar o código.

Separe claramente:

- problemas reais;
- riscos relevantes;
- sugestões opcionais.

Não trate preferências pessoais como problemas.

Revise especialmente:

- independência em relação ao CSV original;
- parsing de produtores;
- cálculo apenas entre vitórias consecutivas;
- empate no mínimo;
- empate no máximo;
- intervalo zero;
- ausência de intervalos;
- ordenação determinística;
- SQLite em memória;
- SQLite 3.53.4 nos containers;
- StaticPool;
- check_same_thread;
- lifecycle das sessões;
- transações;
- isolamento dos testes;
- FastAPI lifespan;
- contrato JSON;
- aliases Pydantic;
- typing;
- tratamento de erros;
- dependências desnecessárias;
- Dockerfile;
- execução como usuário não-root;
- Dev Container;
- secrets;
- configuração do Context7;
- AGENTS.md;
- skills.

Quando alguma conclusão depender do comportamento atual de uma biblioteca, consulte o Context7 antes de recomendar uma alteração.

Depois da revisão, corrija somente os problemas que tenham benefício concreto.

Não faça refatorações cosméticas amplas.

Por fim execute:

- uv sync --frozen;
- Ruff;
- verificação de formatação;
- mypy;
- todos os testes de integração.

Se alguma etapa falhar, corrija o problema e execute novamente.

Registre em .ai/decisions.md somente decisões novas que realmente tenham sido tomadas durante essa revisão.