Agora você deve corrigir a falha encontrada na execução real da CI no GitHub Actions.

A pipeline falhou ainda durante o setup do job com o seguinte erro:

Error: Unable to resolve action `astral-sh/setup-uv@v10`, unable to find version `v10`

Revise o workflow existente em .github/workflows e identifique onde astral-sh/setup-uv está sendo referenciado.

O projeto deve continuar utilizando:

- Python 3.13.15;
- uv 0.12.15;
- uv.lock em modo frozen;
- cache do uv quando suportado;
- Ruff;
- verificação de formatação;
- mypy;
- testes de integração.

Não altere essas versões ou as verificações da pipeline apenas para corrigir o erro.

Antes de modificar o workflow, consulte a documentação e o repositório oficial atual do astral-sh/setup-uv e confirme qual é a release estável válida atualmente.

Não assuma que um major alias como @v10 existe apenas porque existe uma release 10.x.

Prefira fixar a GitHub Action de forma reproduzível e segura.

Se a documentação oficial recomendar ou demonstrar pin por commit SHA, utilize o SHA correspondente à release estável escolhida e deixe um comentário ao lado indicando a versão legível da action, por exemplo:

uses: owner/action@<commit-sha> # vX.Y.Z

A versão da GitHub Action e a versão do uv são coisas diferentes.

Mantenha uv explicitamente fixado em:

0.12.15

Revise também as outras actions utilizadas no mesmo workflow.

Não faça upgrades ou alterações nelas sem necessidade, mas verifique se alguma outra referência possui o mesmo tipo de problema de versão inexistente.

Faça somente mudanças relacionadas à correção e confiabilidade da CI.

Depois da alteração:

- revise a sintaxe completa do YAML;
- confirme que o workflow continua executando em pull requests e pushes para a branch principal;
- confirme que uv.lock continua sendo utilizado sem atualização;
- confirme que nenhuma etapa executa uv lock ou modifica o lockfile;
- confirme que nenhuma secret ou CONTEXT7_API_KEY foi adicionada à pipeline;
- execute localmente, na medida do possível, os mesmos comandos utilizados pela CI:
  - uv sync --frozen;
  - uv run ruff check .;
  - uv run ruff format --check .;
  - uv run mypy .;
  - uv run pytest;
- verifique o git diff e garanta que somente os arquivos necessários para corrigir a CI foram modificados.

Não altere código da aplicação, testes, Dockerfile, Dev Container ou documentação se isso não for necessário para resolver essa falha.

Ao finalizar, informe resumidamente:

- qual era a causa da falha;
- qual versão da action setup-uv foi utilizada;
- como ela foi fixada no workflow;
- se todos os comandos locais equivalentes à CI passaram.

Não faça commit nem push automaticamente.