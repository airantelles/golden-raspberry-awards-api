Agora você deve analisar o teste técnico antes de implementar qualquer funcionalidade.

Leia integralmente o PDF da avaliação e o Movielist.csv disponíveis no projeto.

Use também a skill architecture-review.

A solução será implementada em Python utilizando FastAPI, SQLAlchemy e SQLite em memória.

Analise o problema considerando especialmente que outros arquivos CSV serão utilizados durante a avaliação.

Defina e justifique de forma objetiva:

- estrutura dos módulos;
- mecanismo de criação da aplicação;
- configuração do caminho do CSV;
- como testes poderão inicializar a mesma aplicação com outro CSV;
- lifecycle de criação do banco;
- momento da importação dos dados;
- estratégia transacional para a importação;
- modelagem de Movie;
- modelagem de Producer;
- relação entre filmes e produtores;
- se studios deve ou não ser normalizado;
- como interpretar winner;
- como calcular intervalos entre prêmios consecutivos;
- como lidar com produtores com mais de duas vitórias;
- como lidar com múltiplos vencedores no mesmo ano;
- como lidar com intervalo zero;
- como lidar com empates no menor intervalo;
- como lidar com empates no maior intervalo;
- comportamento quando nenhum produtor possuir duas vitórias;
- ordenação determinística da resposta;
- estratégia dos testes de integração.

A solução deve permanecer pequena e adequada ao tamanho do problema.

Não implemente código nesta etapa.

Quando uma decisão depender do comportamento atual de FastAPI ou SQLAlchemy, consulte o Context7.

Ao final, registre somente as decisões fechadas e suas justificativas resumidas em .ai/decisions.md.