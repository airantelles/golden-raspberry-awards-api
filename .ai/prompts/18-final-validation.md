Agora você deve realizar a validação final da entrega.

Não adicione novas funcionalidades.

Não faça refatorações por preferência pessoal.

Primeiro revise os requisitos já registrados para o projeto e verifique requisito por requisito se a implementação atende ao comportamento esperado.

O documento original da avaliação não faz parte do repositório e não deve ser adicionado durante esta etapa.

O dataset padrão faz parte da entrega e deve estar exatamente em:

docs/Movielist.csv

Confirme especificamente:

- leitura do CSV durante a inicialização da aplicação;
- uso automático de docs/Movielist.csv quando nenhum outro caminho é configurado;
- possibilidade de utilizar outro CSV sem alterar o código;
- persistência dos dados em banco embarcado em memória;
- nenhuma dependência de banco externo;
- endpoint REST;
- comportamento compatível com nível 2 do Richardson Maturity Model;
- retorno do menor intervalo;
- retorno do maior intervalo;
- suporte a empates;
- cálculo somente entre prêmios consecutivos;
- comportamento com intervalo zero;
- comportamento quando não existem intervalos válidos;
- somente testes de integração;
- funcionamento com datasets diferentes;
- README com instruções completas;
- código adequado para publicação no Git;
- registro do uso de IA no repositório.

Depois execute uma validação técnica completa.

A partir de um estado limpo, sempre que possível:

1. valide que a versão de Python utilizada localmente pelo projeto é 3.13.15;

2. execute:

   uv sync --frozen

3. execute Ruff;

4. execute a verificação de formatação;

5. execute mypy;

6. execute todos os testes de integração;

7. execute a suíte de integração mais de uma vez para detectar estado compartilhado ou comportamento não determinístico;

8. faça o build do Dockerfile sem utilizar cache quando isso for razoável;

9. valide Python 3.13.15 dentro da imagem;

10. valide que:

    python -c "import sqlite3; print(sqlite3.sqlite_version)"

    retorna exatamente:

    3.53.4

11. confirme que docs/Movielist.csv existe dentro da imagem final;

12. inicie o container sem montar um CSV externo;

13. confirme que a aplicação consegue carregar docs/Movielist.csv dentro do container;

14. faça uma chamada HTTP real ao endpoint;

15. valide o status code;

16. valide o Content-Type;

17. valide o formato do JSON retornado;

18. finalize o container corretamente.

Também valide explicitamente o suporte a outro dataset.

Utilize um CSV sintético temporário e confirme que a configuração pública da aplicação permite substituir docs/Movielist.csv sem alterar o código.

Não altere nem sobrescreva docs/Movielist.csv para realizar essa verificação.

Revise também o repositório e confirme:

- docs/Movielist.csv está versionado;
- o arquivo está exatamente dentro de docs/;
- .gitignore não exclui docs/Movielist.csv;
- .dockerignore não exclui docs/Movielist.csv;
- o Dockerfile inclui o dataset padrão no runtime;
- o documento original da avaliação não está versionado;
- nenhum PDF local da avaliação foi adicionado acidentalmente;
- nenhum secret está versionado;
- .env está ignorado pelo Git;
- CONTEXT7_API_KEY não aparece com valor real em nenhum arquivo;
- não existem tokens ou credenciais versionados;
- não existem caminhos absolutos da máquina do desenvolvedor em arquivos versionados;
- o Dev Container está coerente com o Dockerfile;
- Python é 3.13.15 no ambiente esperado;
- SQLite é 3.53.4 no Docker e Dev Container;
- uv.lock está consistente com pyproject.toml;
- a CI utiliza o lockfile sem modificá-lo;
- nenhuma instalação externa é necessária para o banco;
- o banco utilizado pela aplicação é realmente em memória;
- não existem testes unitários contrariando a decisão do projeto;
- os testes de integração utilizam datasets alternativos além de docs/Movielist.csv;
- os testes não compartilham banco ou estado;
- a aplicação não contém valores hardcoded derivados do dataset original;
- .ai/prompts está presente;
- .ai/decisions.md está presente;
- .ai/README.md está presente;
- as skills estão presentes em .agents/skills;
- AGENTS.md está presente;
- README contém comandos corretos;
- README permite executar a aplicação sem configuração manual do CSV padrão;
- README explica como utilizar outro CSV;
- CI está coerente com os comandos documentados localmente;
- nenhuma dependência direta declarada está sem uso.

Verifique também o Git status.

Confirme que não existem arquivos locais que deveriam estar versionados e ficaram esquecidos.

Ao mesmo tempo, não adicione arquivos apenas porque estão presentes no diretório de trabalho.

Em especial, não adicione o documento original da avaliação.

Se alguma verificação falhar:

- identifique a causa;
- faça somente a correção necessária;
- execute novamente a verificação correspondente.

Não faça mudanças cosméticas nesta etapa.

Não adicione funcionalidades novas para resolver observações que não sejam requisitos ou bugs reais.

Ao final, entregue um resumo curto contendo:

- requisitos funcionais validados;
- resultado dos testes de integração;
- resultado do Ruff;
- resultado da verificação de formatação;
- resultado do mypy;
- resultado do build Docker;
- versão do Python dentro do container;
- versão do SQLite dentro do container;
- confirmação de presença de docs/Movielist.csv na imagem;
- confirmação de execução com o dataset padrão;
- confirmação de execução com um dataset alternativo;
- resultado da verificação de secrets;
- eventuais limitações reais restantes.

Não invente limitações nem melhorias futuras apenas para preencher o relatório.