Agora você deve implementar a infraestrutura de persistência e os modelos do projeto.

Use SQLAlchemy 2.0.54 seguindo o estilo atual da API 2.x.

O banco deve ser SQLite realmente em memória.

Antes de configurar a engine, consulte no Context7 a documentação atual do SQLAlchemy sobre SQLite in-memory utilizado por múltiplas sessões ou conexões.

Confirme especificamente a configuração adequada envolvendo StaticPool e check_same_thread.

A infraestrutura deve permitir criar instâncias isoladas da aplicação e do banco durante os testes.

Evite:

- engine global difícil de substituir;
- Session global compartilhada de forma insegura;
- estado persistente entre testes.

Modele:

Movie:
- identificador;
- year;
- title;
- studios;
- winner.

Producer:
- identificador;
- name.

Crie uma relação muitos para muitos entre Movie e Producer.

Studios deve permanecer como texto, a menos que uma necessidade concreta da regra justifique normalização.

Não adicione Alembic. O banco é efêmero e deve ser criado do zero ao iniciar a aplicação.

Não implemente ainda:

- importação do CSV;
- parsing dos produtores;
- cálculo dos intervalos;
- endpoint final.

Depois valide programaticamente que o schema pode ser criado corretamente em uma base SQLite em memória.