Agora você deve melhorar a experiência de desenvolvimento do projeto em dois pontos:

1. permitir executar e debugar a API diretamente pelo Run and Debug do VS Code quando o projeto estiver aberto pelo Dev Container;
2. adicionar um Makefile com os comandos de desenvolvimento mais utilizados.

Antes de alterar os arquivos, revise a configuração atual do projeto, principalmente:

- .devcontainer/devcontainer.json;
- Dockerfile;
- pyproject.toml;
- README.md;
- src/app/main.py;
- comandos já utilizados pela CI.

Não altere a arquitetura ou a regra de negócio da aplicação.

## VS Code debugging

Atualmente o Dev Container já configura o interpretador Python da .venv, mas o projeto não possui uma configuração versionada de debug.

Crie uma configuração de debug em:

.vscode/launch.json

Consulte a documentação atual do VS Code Python Debugger antes de definir o formato da configuração.

Utilize a configuração atualmente recomendada para debug Python, incluindo a extensão oficial de debugger caso ela seja necessária no Dev Container.

Crie pelo menos uma configuração chamada de forma clara, como:

API: Debug

Ela deve iniciar a aplicação FastAPI utilizando Uvicorn e o entry point real do projeto:

app.main:app

A aplicação utiliza estrutura src/, portanto configure corretamente o app-dir, working directory ou PYTHONPATH conforme a abordagem mais adequada.

O debugger deve:

- utilizar o Python da .venv criada por uv;
- iniciar a aplicação na porta 8000;
- utilizar o terminal integrado do VS Code;
- permitir breakpoints no código em src/app;
- funcionar dentro do Dev Container;
- utilizar docs/Movielist.csv automaticamente quando nenhum CSV alternativo for configurado;
- respeitar MOVIELIST_CSV_PATH quando essa variável estiver definida.

Não utilize --reload na configuração principal de debug se isso criar subprocessos e tornar breakpoints menos previsíveis.

O objetivo da configuração de debug é depuração previsível, não hot reload.

Se for útil, crie também uma segunda configuração:

Tests: Debug

Ela deve executar pytest pelo debugger e permitir breakpoints durante os testes de integração.

Não crie configurações adicionais sem necessidade.

Revise também .devcontainer/devcontainer.json.

Se o VS Code Python Debugger atual utilizar uma extensão separada, adicione somente a extensão oficial necessária.

Mantenha as extensões já existentes de Python, Pylance e Ruff.

Configure também, somente se trouxer valor real, as opções do VS Code necessárias para:

- reconhecer pytest;
- reconhecer src como source root;
- continuar utilizando ${containerWorkspaceFolder}/.venv/bin/python como interpretador.

Evite criar settings apenas por conveniência estética.

Depois valide na medida do possível que a configuração referencia:

- o módulo correto;
- o workspace correto;
- a .venv correta;
- a porta correta;
- o entry point correto.

## Makefile

Crie um Makefile na raiz do projeto.

O Makefile deve funcionar como uma interface de conveniência para os comandos que o projeto já utiliza.

Ele não deve substituir pyproject.toml, uv.lock ou uv.

Use uv para executar todos os comandos Python.

Crie targets pequenos e previsíveis.

Inclua pelo menos:

help
sync
run
dev
test
lint
format
format-check
typecheck
check
docker-build
docker-run
docker-stop

O comportamento esperado é:

make help
    Exibe os targets disponíveis e uma descrição curta.

make sync
    Instala/sincroniza as dependências utilizando:
    uv sync --frozen

make run
    Inicia a API sem hot reload.

make dev
    Inicia a API com hot reload para desenvolvimento local.

make test
    Executa todos os testes de integração.

make lint
    Executa Ruff lint.

make format
    Formata o código utilizando Ruff.

make format-check
    Verifica a formatação sem modificar arquivos.

make typecheck
    Executa mypy.

make check
    Executa todas as verificações locais equivalentes às verificações de qualidade da CI:
    lint, format-check, typecheck e test.

make docker-build
    Faz o build da imagem de produção utilizando o nome já documentado pelo projeto.

make docker-run
    Inicia a imagem de produção publicando a porta 8000.

make docker-stop
    Para e remove o container iniciado pelo target docker-run sem falhar desnecessariamente se ele já estiver parado.

Declare corretamente os targets como .PHONY.

Não esconda erros dos comandos de lint, testes ou type checking.

Se qualquer uma dessas verificações falhar, o target correspondente deve retornar código de saída diferente de zero.

Evite lógica shell complexa dentro do Makefile.

Os comandos devem continuar sendo fáceis de entender para alguém que abrir o arquivo.

## Make dentro do Dev Container

O Makefile também deve funcionar dentro do Dev Container.

Revise o target development do Dockerfile.

Atualmente ferramentas utilizadas somente durante a compilação de outros stages não devem ser assumidas como disponíveis no target development.

Se GNU Make ainda não estiver disponível no ambiente de desenvolvimento, instale-o somente no target development.

Não adicione make à imagem final de runtime.

Mantenha a imagem de produção sem ferramentas de desenvolvimento desnecessárias.

Depois valide dentro do target development que:

make --version

funciona.

## README

Atualize o README somente no necessário para documentar essas duas melhorias.

Na seção do Dev Container, explique que depois de usar "Reopen in Container" o desenvolvedor pode abrir:

Run and Debug

e selecionar:

API: Debug

para iniciar a aplicação com breakpoints.

Se existir a configuração Tests: Debug, documente-a de forma curta.

Adicione também uma seção curta sobre o Makefile.

Explique que os comandos uv continuam sendo a interface canônica e que o Makefile fornece apenas atalhos de desenvolvimento.

Mostre pelo menos:

make help
make dev
make test
make check
make docker-build
make docker-run

Não remova os comandos uv existentes do README.

Um avaliador não deve ser obrigado a ter Make instalado para entender como executar o projeto fora do Dev Container.

## Validação

Depois das alterações:

- execute uv sync --frozen;
- execute make help;
- execute make lint;
- execute make format-check;
- execute make typecheck;
- execute make test;
- execute make check;
- faça o build do target development do Dockerfile;
- confirme make --version dentro dele;
- confirme Python 3.13.15;
- confirme SQLite 3.53.4;
- confirme que o target runtime continua sem depender de Make;
- faça o build da imagem de produção;
- confirme que a aplicação continua iniciando normalmente;
- revise .vscode/launch.json e confirme que os caminhos utilizados existem dentro do Dev Container;
- revise o git diff.

Faça somente alterações relacionadas à experiência de desenvolvimento descrita neste prompt.

Não altere regra de negócio, contratos HTTP, models, queries ou testes apenas por oportunidade de refatoração.

Ao finalizar, informe resumidamente:

- quais configurações de debug foram adicionadas;
- como iniciar o debugger no Dev Container;
- quais targets foram adicionados ao Makefile;
- se Make foi necessário no target development;
- resultado das verificações executadas.

Não faça commit nem push automaticamente.