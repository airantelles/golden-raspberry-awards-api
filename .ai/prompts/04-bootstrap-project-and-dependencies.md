Agora você deve criar a base executável do projeto seguindo as decisões já registradas.

Use uv como gerenciador de dependências e lockfile.

Configure exatamente estas versões:

- Python 3.13.15;
- FastAPI 0.141.1;
- SQLAlchemy 2.0.54;
- Pydantic 2.13.5;
- Uvicorn 0.53.0;
- pytest 9.1.1;
- HTTPX 0.28.1;
- Ruff 0.16.7;
- mypy 2.3.1;
- uv 0.12.15.

Não use versões alpha, beta, RC ou development release.

Crie:

- pyproject.toml;
- .python-version;
- uv.lock;
- estrutura inicial do pacote Python;
- uma aplicação FastAPI mínima que consiga iniciar;
- .gitignore adequado ao projeto.

Configure Ruff e mypy no próprio pyproject.toml.

Não adicione pandas ou outras bibliotecas para leitura do CSV. O módulo csv da stdlib será suficiente.

Não adicione pydantic-settings neste momento, a menos que exista uma necessidade concreta que não possa ser resolvida de forma simples sem ele. Caso considere necessário, explique antes de adicionar.

Use o Context7 para conferir as APIs atuais relevantes das bibliotecas.

Não implemente ainda:

- banco de dados;
- carga do CSV;
- parsing de produtores;
- regra dos intervalos.

Depois de criar a base:

- execute uv sync usando o lockfile;
- execute Ruff;
- execute a verificação de formatação;
- execute mypy;
- inicie a aplicação para verificar que ela sobe corretamente.

Corrija problemas encontrados antes de concluir esta etapa.