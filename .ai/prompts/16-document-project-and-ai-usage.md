Agora você deve finalizar a documentação do projeto.

Crie ou revise o README.md principal pensando principalmente em alguém que acabou de clonar o repositório para avaliar o teste técnico e precisa conseguir executar tudo com o mínimo de atrito.

O README deve ser objetivo, técnico e fácil de seguir.

O dataset padrão já está versionado em:

docs/Movielist.csv

Portanto, o fluxo principal de execução não deve exigir que o avaliador copie, baixe, monte ou configure manualmente um CSV.

No início do README, crie uma seção "Quick start" com o caminho mais curto possível para executar o projeto.

Essa seção deve permitir que alguém faça, em poucos comandos:

1. instale as dependências com uv;
2. inicie a API;
3. faça uma chamada ao endpoint principal;
4. execute os testes de integração.

Considere que docs/Movielist.csv já está disponível depois do clone.

Não exija variável de ambiente para o Quick Start.

Depois do Quick start, organize o restante da documentação em seções claras.

O README deve explicar:

- objetivo da aplicação;
- stack utilizada;
- versões principais utilizadas no projeto;
- requisitos para execução local;
- instalação das dependências com uv;
- execução local da aplicação;
- execução dos testes de integração;
- execução do Ruff;
- verificação de formatação;
- execução do mypy;
- execução com Docker;
- uso do Dev Container;
- endpoint disponível;
- exemplo de request;
- exemplo de response;
- decisões arquiteturais mais importantes;
- comportamento quando não existem intervalos válidos;
- premissas relevantes sobre o CSV;
- utilização do dataset padrão;
- como utilizar outro CSV sem alterar o código;
- onde está registrado o uso de inteligência artificial durante o desenvolvimento.

Crie uma seção "Using Docker" com comandos completos e copiáveis para:

- fazer o build da imagem;
- iniciar o container;
- mapear a porta da API;
- chamar o endpoint principal;
- parar/remover o container quando necessário.

O exemplo principal de Docker deve funcionar sem volume adicional porque docs/Movielist.csv já deve estar incluído na imagem.

Se a aplicação suportar substituir o CSV em runtime através de configuração ou volume, documente também um exemplo separado mostrando como executar o container com outro dataset.

Não torne esse override obrigatório para o fluxo normal.

Os comandos devem corresponder ao Dockerfile real do projeto.

Crie também uma seção "Using Dev Container".

Explique de forma simples que o avaliador pode abrir o repositório no VS Code com suporte a Dev Containers e utilizar "Reopen in Container".

Explique o que já estará disponível nesse ambiente, incluindo:

- Python 3.13.15;
- SQLite 3.53.4;
- uv;
- dependências de desenvolvimento;
- Ruff;
- mypy;
- pytest;
- Node.js utilizado pelas ferramentas de desenvolvimento.

Não transforme essa seção em um tutorial completo do VS Code.

Crie uma seção curta de arquitetura ou "Technical decisions" explicando apenas as decisões que ajudam o avaliador a entender a solução.

Inclua, quando corresponder à implementação real:

- SQLite em memória;
- application factory ou mecanismo equivalente de criação isolada da aplicação;
- caminho do CSV configurável;
- carregamento do CSV durante o lifespan da aplicação;
- importação transacional;
- relação muitos para muitos entre Movie e Producer;
- studios mantido como texto por não participar da consulta solicitada;
- uso de window function LAG para calcular vitórias consecutivas;
- tratamento de empates;
- resposta determinística;
- ausência proposital de camadas ou abstrações que não agregariam valor ao tamanho do projeto.

Não justifique excessivamente decisões óbvias.

Inclua uma seção explicando o dataset.

Deixe claro que:

- o dataset padrão está versionado em docs/Movielist.csv;
- ele é carregado automaticamente durante a inicialização da aplicação;
- nenhuma preparação manual dos dados é necessária para executar o projeto;
- o caminho do CSV continua configurável;
- outro dataset compatível pode ser utilizado sem alterar o código;
- os testes utilizam datasets sintéticos adicionais;
- a implementação não depende dos valores específicos de docs/Movielist.csv.

Documente como executar a aplicação utilizando outro CSV.

Use exatamente o mecanismo realmente implementado no projeto.

Por exemplo, se a implementação utilizar MOVIELIST_CSV_PATH, mostre um comando equivalente a:

MOVIELIST_CSV_PATH=/path/to/another.csv uv run fastapi dev

Não documente MOVIELIST_CSV_PATH se essa variável não existir de fato na aplicação.

Não invente opções de configuração somente para melhorar a documentação.

Crie ao final uma seção curta "Evaluation notes" para facilitar a validação do teste.

Nessa seção, destaque explicitamente que:

- o banco utilizado é SQLite em memória;
- nenhuma instalação externa de banco de dados é necessária;
- o dataset padrão está disponível em docs/Movielist.csv;
- o CSV é importado durante o startup/lifespan da aplicação;
- outro dataset pode ser utilizado sem alterar o código;
- o projeto implementa somente testes de integração;
- os testes exercitam a aplicação através da API;
- os testes incluem datasets sintéticos alternativos;
- a aplicação suporta empates no menor e no maior intervalo;
- o projeto contém registro do uso de IA.

Não use essa seção para fazer marketing sobre o projeto. Ela deve funcionar somente como checklist técnico para o avaliador.

Também documente os comandos de qualidade:

- uv run ruff check .;
- uv run ruff format --check .;
- uv run mypy .;
- uv run pytest.

Se os comandos reais do projeto forem diferentes, utilize os comandos que realmente funcionam no repositório em vez de copiar estes cegamente.

Todos os comandos presentes no README devem ser executáveis e devem corresponder à configuração real do projeto.

Antes de finalizar o README, execute os principais comandos documentados para confirmar que eles funcionam.

Depois revise também .ai/README.md.

Esse arquivo deve explicar de forma resumida que o projeto utilizou:

- Codex para análise, implementação e revisão;
- Context7 MCP para consulta de documentação atualizada;
- a skill architecture-review;
- a skill integration-test-design;
- a skill python-review.

Explique que .ai/prompts contém os principais prompts utilizados durante o desenvolvimento e que eles representam o registro das principais interações, não necessariamente uma transcrição literal de todas as mensagens trocadas.

Explique também que .ai/decisions.md registra decisões técnicas relevantes tomadas durante o desenvolvimento.

O documento original da avaliação não faz parte do repositório e não deve ser mencionado como um arquivo necessário para executar o projeto.

Não adicione, copie ou reproduza o documento original da avaliação na documentação.

Não duplique o conteúdo completo dos prompts dentro da documentação.

Não inclua:

- CONTEXT7_API_KEY;
- tokens;
- secrets;
- credenciais;
- caminhos absolutos específicos da máquina do desenvolvedor;
- nomes de usuários locais;
- informações que não sejam necessárias para executar ou avaliar o projeto.

Não escreva texto de marketing.

Não transforme o README em documentação extensa da implementação interna.

O objetivo final é que um avaliador consiga, apenas lendo o README:

1. entender rapidamente o que a aplicação faz;
2. instalar as dependências;
3. iniciar a API utilizando docs/Movielist.csv automaticamente;
4. chamar o endpoint;
5. executar os testes;
6. executar as verificações de qualidade;
7. rodar o projeto com Docker sem precisar montar o dataset padrão;
8. utilizar o Dev Container;
9. executar a aplicação com outro CSV se desejar;
10. entender as principais decisões técnicas;
11. localizar o registro de uso de IA.

Ao terminar, revise o README inteiro como se você fosse um avaliador que acabou de clonar o repositório.

Se algum passo depender de conhecimento que não esteja documentado, ajuste a documentação.

Por fim, execute novamente os comandos essenciais descritos no README e confirme que a documentação corresponde ao comportamento real do projeto.