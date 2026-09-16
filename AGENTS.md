# Instruções do projeto

## Versões obrigatórias

- Python: 3.13.15
- FastAPI: 0.141.1; SQLAlchemy: 2.0.54; Pydantic: 2.13.5; Uvicorn: 0.53.0
- pytest: 9.1.1; HTTPX: 0.28.1; Ruff: 0.16.7; mypy: 2.3.1; uv: 0.12.15
- SQLite: 3.53.4 nos ambientes Docker e Dev Container.
- Não use versões alpha, beta ou release candidate.

## Desenvolvimento

- Consulte o Context7 antes de implementar decisões que dependam da API ou do comportamento atual de uma biblioteca.
- Não adicione dependências sem necessidade concreta. Evite overengineering, abstrações, camadas e patterns por convenção.
- Não use `async` apenas porque FastAPI o suporta.
- O desafio requer somente testes de integração; não crie testes unitários.
- A aplicação deve continuar funcionando quando o CSV de entrada for substituído.
- `docs/Movielist.csv` faz parte da entrega e deve permanecer versionado.
- O documento original da avaliação não faz parte da entrega e não deve ser adicionado ao repositório.
- Nunca versione segredos.
- Após mudanças relevantes, execute testes, lint, verificação de formatação e type checking.
- Antes de alterar uma decisão arquitetural registrada, revise `.ai/decisions.md`.
