Agora você deve corrigir o isolamento do ambiente virtual Python utilizado pelo Dev Container.

Ao abrir o projeto no Dev Container, o VS Code e a extensão Ruff apresentaram os seguintes erros:

Ignoring environment 'file:///workspaces/golden-raspberry-awards-api/.venv' with errors:
Python executable is a broken symlink

e:

Error while trying to find the Ruff binary:
spawn /workspaces/golden-raspberry-awards-api/.venv/bin/python ENOENT

Analise a causa antes de modificar os arquivos.

O workspace local é montado dentro do Dev Container. Portanto, uma .venv criada no host também aparece em:

${containerWorkspaceFolder}/.venv

Virtual environments Python não devem ser compartilhados dessa forma entre o host e o container, pois seus executáveis e symlinks podem apontar para caminhos disponíveis somente no ambiente onde a virtualenv foi criada.

Consulte a documentação atual do uv sobre desenvolvimento em containers e sobre UV_PROJECT_ENVIRONMENT antes de implementar a correção.

A solução deve garantir que:

- o ambiente Python local do host continue independente;
- o Dev Container tenha seu próprio ambiente virtual;
- abrir ou reconstruir o Dev Container não apague nem modifique a .venv do host;
- o ambiente do Dev Container não dependa de symlinks criados no host;
- uv continue sendo a ferramenta responsável pela instalação das dependências.

Prefira utilizar um ambiente exclusivo do container fora do workspace bind-mounted.

Utilize:

/home/developer/.venv

como ambiente virtual do projeto dentro do Dev Container, a menos que durante a análise exista uma razão concreta para utilizar outro caminho.

Configure o ambiente de desenvolvimento para que o uv utilize esse caminho através de:

UV_PROJECT_ENVIRONMENT=/home/developer/.venv

Essa configuração deve existir somente no ambiente de desenvolvimento/container e não deve alterar o comportamento:

- da execução local no host;
- da imagem runtime;
- da CI;
- dos testes executados fora do Dev Container.

Revise o target development do Dockerfile e .devcontainer/devcontainer.json e escolha o local correto para definir essa variável.

Não defina UV_PROJECT_ENVIRONMENT globalmente em stages do Dockerfile que possam afetar a imagem de produção.

## VS Code

Atualize a configuração do VS Code no Dev Container para utilizar:

/home/developer/.venv/bin/python

como interpretador Python.

Revise:

.devcontainer/devcontainer.json
.vscode/launch.json

A configuração:

API: Debug

deve utilizar o interpretador:

/home/developer/.venv/bin/python

A configuração:

Tests: Debug

também deve utilizar esse mesmo interpretador.

Mantenha:

${workspaceFolder}

para cwd e para referências ao código-fonte.

Não volte a utilizar ${containerWorkspaceFolder} dentro do launch.json para cwd.

A separação esperada é:

- interpretador Python: /home/developer/.venv/bin/python
- código do projeto: ${workspaceFolder}
- source path: ${workspaceFolder}/src

Configure também o Python extension do Dev Container para utilizar o interpretador container-local.

Não dependa de:

${containerWorkspaceFolder}/.venv/bin/python

porque essa localização pertence ao workspace bind-mounted e pode conter uma virtualenv criada no host.

## Ruff

Revise a integração do Ruff com o VS Code.

O Ruff CLI utilizado pelas verificações do projeto deve continuar sendo a versão instalada pelas dependências de desenvolvimento e executada através de uv/make.

Não é necessário alterar o comportamento da extensão Ruff se ela conseguir funcionar corretamente com o ambiente Python ativo.

Não adicione uma segunda instalação manual do Ruff.

Se alguma configuração explícita de interpreter do Ruff for realmente necessária, consulte primeiro a documentação atual da extensão e utilize o ambiente container-local.

## Criação do ambiente

O postCreateCommand deve continuar instalando as dependências de forma reproduzível utilizando:

uv sync --frozen

Com UV_PROJECT_ENVIRONMENT configurado corretamente, esse comando deve criar ou atualizar:

/home/developer/.venv

e não:

${workspaceFolder}/.venv

Não utilize:

rm -rf ${workspaceFolder}/.venv

ou qualquer outra abordagem que apague a virtualenv existente no workspace.

O workspace é um bind mount e isso poderia modificar arquivos da máquina host.

## Makefile

Revise os targets do Makefile.

Como eles utilizam uv, devem continuar funcionando normalmente dentro e fora do Dev Container.

Não hardcode /home/developer/.venv no Makefile.

O Makefile deve continuar portátil.

Dentro do Dev Container, UV_PROJECT_ENVIRONMENT deve fazer com que uv utilize automaticamente o ambiente correto.

## Validação

Depois das alterações, faça uma validação específica do Dev Container.

Confirme conceitualmente e, quando possível, executando no container que:

echo "$UV_PROJECT_ENVIRONMENT"

retorna:

/home/developer/.venv

Confirme:

test -x /home/developer/.venv/bin/python

e:

/home/developer/.venv/bin/python --version

deve retornar Python 3.13.15.

Confirme também:

uv run python --version

e:

uv run python -c "import sqlite3; print(sqlite3.sqlite_version)"

O resultado esperado é:

Python 3.13.15

e:

3.53.4

Confirme que:

uv run ruff --version
uv run pytest --version
uv run mypy --version

funcionam utilizando o ambiente do container.

Execute:

make check

e confirme que todas as verificações passam.

Valide também que:

- .vscode/launch.json não referencia mais ${workspaceFolder}/.venv/bin/python;
- .devcontainer/devcontainer.json não utiliza mais ${containerWorkspaceFolder}/.venv/bin/python como Python default;
- nenhuma configuração apaga .venv do workspace;
- o runtime Docker continua inalterado;
- a CI continua inalterada;
- a .venv local continua ignorada pelo Git.

Revise o README.

Se ele afirmar que o Dev Container utiliza a .venv do workspace, corrija somente essa informação.

Não é necessário documentar detalhes internos de UV_PROJECT_ENVIRONMENT se isso não ajudar o avaliador.

Não altere regra de negócio, API, models, queries ou testes.

Ao finalizar, informe resumidamente:

- qual era a causa do broken symlink;
- onde fica agora a virtualenv do Dev Container;
- como uv foi configurado para utilizá-la;
- quais configurações do VS Code foram ajustadas;
- resultado do make check;
- como validar API: Debug e Tests: Debug no VS Code.

Não faça commit nem push automaticamente.