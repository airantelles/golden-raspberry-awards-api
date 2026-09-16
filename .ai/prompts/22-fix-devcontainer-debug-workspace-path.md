Agora você deve corrigir a configuração de debug do VS Code utilizada dentro do Dev Container.

Ao executar "API: Debug" pelo Run and Debug do VS Code, ocorreu o seguinte erro:

The terminal process failed to launch: Starting directory (cwd) "${containerWorkspaceFolder}" does not exist.

Revise:

- .vscode/launch.json;
- .devcontainer/devcontainer.json.

A configuração atual utiliza ${containerWorkspaceFolder} dentro de .vscode/launch.json.

Essa variável é válida no contexto de configuração do Dev Container, mas não está sendo expandida corretamente pelo launch.json.

Corrija as configurações de debug para utilizar as variáveis atualmente suportadas pelo VS Code nesse contexto.

Use ${workspaceFolder} dentro de .vscode/launch.json para representar a raiz do workspace aberto no container.

Ajuste todas as referências necessárias, incluindo:

- python;
- cwd;
- PYTHONPATH.

A configuração "API: Debug" deve continuar:

- utilizando debugpy;
- executando o módulo uvicorn;
- utilizando app.main:app;
- utilizando src como app-dir;
- escutando em 0.0.0.0;
- utilizando a porta 8000;
- utilizando o terminal integrado;
- permitindo breakpoints no código da aplicação;
- utilizando o Python da .venv criada por uv;
- sem utilizar --reload.

A configuração "Tests: Debug" também deve continuar:

- utilizando debugpy;
- executando pytest;
- utilizando a .venv do projeto;
- permitindo breakpoints nos testes e na aplicação;
- utilizando src no PYTHONPATH quando necessário.

Não remova ou altere a configuração correta existente no devcontainer.json apenas porque ela utiliza ${containerWorkspaceFolder}. Nesse arquivo essa variável pode continuar sendo utilizada quando for suportada pelo Dev Containers.

Confirme também que o Dev Container já instala a extensão oficial:

ms-python.debugpy

Não adicione outra extensão de debugger se ela já estiver presente.

Depois da alteração:

- valide a sintaxe de .vscode/launch.json;
- confirme que nenhum ${containerWorkspaceFolder} permanece dentro de .vscode/launch.json;
- confirme que ${workspaceFolder}/.venv/bin/python existe quando o workspace está aberto no Dev Container;
- confirme que src/app/main.py existe relativamente a ${workspaceFolder};
- execute uv sync --frozen;
- execute make check, caso o Makefile já esteja disponível;
- não altere código da aplicação ou regra de negócio.

Ao finalizar, informe resumidamente:

- qual era a causa do erro;
- quais variáveis foram substituídas;
- como validar "API: Debug" e "Tests: Debug" pelo VS Code.

Não faça commit nem push automaticamente.