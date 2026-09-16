Agora você deve containerizar a aplicação.

Crie um Dockerfile adequado tanto para produzir a imagem final da API quanto para servir de base para o ambiente de desenvolvimento posteriormente.

A imagem deve usar exatamente Python 3.13.15.

O ambiente da aplicação dentro do container deve utilizar exatamente SQLite 3.53.4.

Como o módulo sqlite3 do Python depende da biblioteca SQLite nativa, não considere suficiente apenas instalar qualquer versão disponível no sistema operacional.

Implemente a construção da imagem de forma que o comando:

python -c "import sqlite3; print(sqlite3.sqlite_version)"

retorne exatamente:

3.53.4

Se for necessário compilar ou instalar a biblioteca SQLite 3.53.4 durante o build, faça isso de forma reproduzível e remova artefatos de compilação desnecessários da imagem final.

Use uv 0.12.15 e uv.lock para instalar as dependências.

A instalação da imagem final deve ser frozen e reproduzível.

Não inclua dependências de desenvolvimento na imagem final.

A imagem final deve:

- executar como usuário não-root;
- conter somente os arquivos necessários à execução;
- incluir o CSV padrão utilizado pela aplicação;
- não conter Node.js;
- não conter Codex;
- não conter Context7;
- não conter ferramentas de compilação que não sejam necessárias em runtime.

Use multi-stage build quando isso ajudar a manter a imagem final limpa.

Crie também um .dockerignore adequado.

Depois:

- faça o build da imagem;
- valide a versão do Python dentro dela;
- valide sqlite3.sqlite_version;
- inicie o container;
- confirme que a aplicação consegue subir.

Não implemente regra de negócio nesta etapa.