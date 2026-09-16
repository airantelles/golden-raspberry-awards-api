Agora você deve configurar um Dev Container para permitir que o projeto seja aberto no VS Code com todo o ambiente de desenvolvimento pronto.

Reutilize o Dockerfile existente o máximo possível para evitar dois ambientes Python independentes.

O Dev Container deve possuir exatamente:

- Python 3.13.15;
- SQLite 3.53.4;
- uv 0.12.15;
- Node.js 24.21.0 LTS.

Node.js deve existir somente no ambiente de desenvolvimento porque será utilizado para ferramentas como o Context7 MCP.

Node.js não deve ser incluído na imagem final da aplicação.

Configure o Dev Container para:

- instalar as dependências de desenvolvimento utilizando uv.lock;
- expor a porta usada pela aplicação FastAPI;
- repassar CONTEXT7_API_KEY a partir do ambiente local sem gravar o valor no repositório;
- disponibilizar as extensões essenciais do VS Code para Python e Ruff;
- evitar uma lista desnecessariamente grande de extensões;
- utilizar um postCreateCommand reproduzível;
- abrir o workspace na raiz do projeto.

Consulte a documentação atual de Dev Containers quando houver dúvida sobre a sintaxe.

Depois valide, dentro do ambiente quando possível:

- python --version;
- python -c "import sqlite3; print(sqlite3.sqlite_version)";
- uv --version;
- node --version;
- npx --version;
- execução de Ruff;
- execução de mypy.

Não altere a regra da aplicação nesta etapa.