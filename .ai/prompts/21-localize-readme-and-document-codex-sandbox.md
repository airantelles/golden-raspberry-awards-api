Agora você deve revisar e padronizar toda a documentação principal do projeto.

O README.md deve ficar integralmente em português brasileiro.

Atualmente existem partes da documentação em inglês e outras em português.
Padronize o texto para PT-BR, preservando em inglês somente:

- nomes oficiais de ferramentas;
- nomes de arquivos;
- comandos;
- código;
- nomes de configurações;
- endpoints;
- variáveis de ambiente;
- termos técnicos que normalmente são utilizados em inglês na área.

Não traduza artificialmente termos como:

- FastAPI;
- SQLAlchemy;
- Dev Container;
- Docker;
- GitHub Actions;
- Codex;
- Context7;
- Ruff;
- mypy;
- pytest;
- uv;
- lifespan;
- debug;
- breakpoint;
- endpoint;
- commit;
- pull request.

Mantenha o README técnico, objetivo e orientado a quem está avaliando o projeto.

Não faça alterações no código da aplicação nesta etapa.

## Uso do Codex em sandbox

Adicione à documentação uma explicação curta sobre o ambiente utilizado para executar o Codex durante o desenvolvimento.

O Codex foi executado dentro de um sandbox baseado em Docker.

Durante o desenvolvimento ele foi utilizado em modo autônomo, também conhecido informalmente como "YOLO mode", permitindo executar comandos e modificar arquivos sem exigir confirmação manual a cada ação.

Essa execução ocorreu dentro do sandbox para limitar o escopo de acesso do agente ao ambiente isolado do projeto e reduzir o impacto potencial sobre o sistema host.

Não afirme que Docker ou o sandbox fornecem "segurança total".

Não faça alegações absolutas sobre segurança.

Explique apenas que o isolamento foi utilizado como uma camada de proteção e contenção do ambiente de execução.

A seção pode ter um nome como:

"Desenvolvimento assistido por IA"

ou:

"Uso de IA no desenvolvimento"

Dentro dela, explique de forma curta que foram utilizados:

- Codex como agente principal de desenvolvimento;
- Context7 MCP para consulta de documentação atualizada;
- skills específicas do projeto;
- sandbox Docker para execução isolada do agente.

Mencione que os principais prompts utilizados estão registrados em:

.ai/prompts/

e que as principais decisões técnicas estão em:

.ai/decisions.md

Não transforme essa seção em propaganda sobre IA.

O objetivo é demonstrar de forma transparente:

- como a IA foi utilizada;
- quais ferramentas foram utilizadas;
- como o agente foi isolado durante a execução;
- onde o histórico relevante pode ser consultado.

## README

Revise todas as seções existentes e traduza para português brasileiro, incluindo quando aplicável:

- Quick start;
- Objective;
- Stack and versions;
- Local execution;
- Requirements;
- Endpoint;
- Dataset and another CSV;
- Tests and quality checks;
- Using Docker;
- Using Dev Container;
- Technical decisions;
- AI development record;
- Evaluation notes;
- seção sobre Makefile, caso já exista;
- seção sobre debug no VS Code, caso já exista.

Utilize títulos naturais em português, por exemplo:

- Início rápido;
- Objetivo;
- Stack e versões;
- Execução local;
- Requisitos;
- Dataset e uso de outro CSV;
- Testes e verificações de qualidade;
- Usando Docker;
- Usando Dev Container;
- Decisões técnicas;
- Desenvolvimento assistido por IA;
- Notas para avaliação.

Não altere:

- comandos funcionais;
- paths;
- nomes das variáveis de ambiente;
- exemplos JSON;
- nomes dos endpoints;
- versões das dependências.

Revise também .ai/README.md e traduza para português brasileiro se ele ainda estiver em inglês ou misturando idiomas.

Mantenha o mesmo significado técnico.

## Validação

Depois das alterações:

- revise o README completo;
- confirme que não restaram parágrafos em inglês sem necessidade;
- confirme que todos os comandos documentados continuam corretos;
- confirme que nenhum secret ou credencial foi incluído;
- confirme que a descrição do sandbox não promete segurança absoluta;
- confirme que .ai/prompts e .ai/decisions.md estão corretamente referenciados;
- execute make check, caso o Makefile já tenha sido adicionado;
- caso contrário, execute as verificações equivalentes com uv;
- revise o git diff.

Não modifique código da aplicação, testes ou infraestrutura sem necessidade.

Ao finalizar, informe resumidamente:

- quais documentos foram traduzidos;
- onde foi documentado o uso do Codex;
- como foi descrito o sandbox;
- resultado das verificações executadas.

Não faça commit nem push automaticamente.