Agora você deve criar o AGENTS.md deste repositório para manter as principais instruções de desenvolvimento disponíveis para as próximas sessões do Codex.

Mantenha o arquivo curto e útil. Ele não deve substituir o README nem documentar todo o projeto.

Registre as seguintes regras permanentes:

- o projeto deve usar Python 3.13.15;
- FastAPI deve ficar fixado em 0.141.1;
- SQLAlchemy deve ficar fixado em 2.0.54;
- SQLite deve ficar fixado em 3.53.4 nos ambientes Docker e Dev Container;
- Pydantic deve ficar fixado em 2.13.5;
- Uvicorn deve ficar fixado em 0.53.0;
- pytest deve ficar fixado em 9.1.1;
- HTTPX deve ficar fixado em 0.28.1;
- Ruff deve ficar fixado em 0.16.7;
- mypy deve ficar fixado em 2.3.1;
- uv deve ficar fixado em 0.12.15;
- quando alguma decisão depender da API ou do comportamento atual de uma biblioteca, consulte o Context7 antes de implementar;
- não use versões alpha, beta ou release candidate;
- não adicione dependências sem uma necessidade concreta;
- não faça overengineering;
- não crie abstrações, camadas ou patterns apenas por convenção;
- não use async apenas porque FastAPI suporta async;
- o desafio exige somente testes de integração, portanto não crie testes unitários;
- a aplicação deve funcionar corretamente quando o CSV de entrada for substituído;
- nenhum segredo pode ser versionado;
- após mudanças relevantes, execute testes, lint, verificação de formatação e type checking;
- antes de modificar decisões arquiteturais já registradas, revise .ai/decisions.md.

Consulte a documentação atual do Codex sobre AGENTS.md antes de criar o arquivo.

Não implemente nenhuma funcionalidade da aplicação neste passo.