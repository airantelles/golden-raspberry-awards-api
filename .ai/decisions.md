# Technical decisions

## ADR-001 — Project-local Context7 MCP

- Status: accepted
- Date: 2026-09-16

Context7 is configured only in `.codex/config.toml`, using the fixed package version `@upstash/context7-mcp@4.1.1`. If authentication is needed, the server receives `CONTEXT7_API_KEY` from the local environment; no credential is stored in the repository.

## ADR-002 — Aplicação, importação e cálculo dos intervalos

- Status: accepted
- Date: 2026-09-16

### Estrutura e ciclo de vida

- Os módulos serão `app` (factory e lifespan), `database` (Base, engine e fábrica de sessões), `models` (Movie, Producer e associação), `importer` (leitura/validação do CSV), `api` (rota e consulta) e `schemas` (resposta). Cada módulo possui uma responsabilidade presente; não haverá camadas de serviço, repositórios ou configurações genéricas.
- `create_app(csv_path: Path | None = None)` criará uma instância isolada. O argumento explícito tem precedência; sem ele, o caminho virá de `MOVIELIST_CSV_PATH`, com padrão para `docs/Movielist.csv`. Assim a execução normal é configurável e testes podem criar a mesma aplicação com qualquer fixture CSV, sem estado global.
- A factory criará um engine SQLite em memória próprio da instância, com pool/conexão apropriado para ser compartilhado entre a thread do `TestClient` e a aplicação. Engine e fábrica de sessões ficarão no estado da aplicação, não em variáveis globais.
- O lifespan criará o schema e importará os dados antes de aceitar requisições; no encerramento descartará o engine. Embora o protocolo de lifespan seja assíncrono, a importação, sessões e rota serão síncronas.

### Importação e persistência

- O importador lerá CSV UTF-8 (aceitando BOM), delimitado por `;`, por meio da biblioteca padrão. Validará o cabeçalho e os campos obrigatórios, reportando linha e causa em entradas inválidas.
- A criação das tabelas ocorre uma vez por instância, antes da carga. Todas as linhas, produtores e associações serão persistidos em uma única transação: qualquer erro desfaz toda a carga e impede uma aplicação parcialmente inicializada de atender requisições.
- `Movie` terá `id`, `year`, `title`, `studios` como texto bruto e `winner` booleano, além da relação com produtores. `Producer` terá `id` e `name` canônico único. A identidade será o nome após remover espaços externos e normalizar espaços internos, sem comparação aproximada, troca de caixa ou correção ortográfica.
- `movie_producers` será uma tabela de associação muitos-para-muitos com chaves estrangeiras e chave primária composta. Um produtor repetido na mesma célula será associado uma única vez ao filme.
- `studios` não será normalizado: não participa do requisito de consulta, e preservá-lo como texto evita uma entidade, parser e regras de identidade sem valor para este problema.
- A coluna `winner` será verdadeira somente para `yes`, sem distinção de maiúsculas/minúsculas e com espaços externos ignorados; valor vazio é falso. Outro valor não vazio é inválido, para evitar resultado silenciosamente incorreto.
- A lista de produtores de uma célula será separada por vírgulas e pela conjunção isolada `and` (incluindo a forma Oxford `, and`), com espaços normalizados. Esta é a convenção observada no CSV; o conteúdo restante do nome é preservado.

### Intervalos e resposta

- A única operação necessária será `GET /producers/intervals`, que representa a coleção calculada de intervalos dos produtores e retorna o formato `min`/`max` especificado. É uma rota HTTP simples, sem RPC ou estado de sessão, suficiente para o nível 2 de Richardson exigido.
- Cada filme vencedor atribui uma vitória a todos os seus produtores. Para cada produtor, as vitórias serão ordenadas por `(year, title, movie id)` e serão comparadas somente em pares adjacentes; o intervalo é `followingWin - previousWin`. Isso trata corretamente produtores com mais de duas vitórias, sem comparar indevidamente primeira e última vitória.
- Duas vitórias do mesmo produtor no mesmo ano são eventos distintos e geram intervalo zero. Vencedores diferentes no mesmo ano são creditados independentemente a seus respectivos produtores.
- `min` e `max` conterão todos os pares cujo intervalo seja, respectivamente, o menor e o maior valor global. Empates não serão descartados. Entradas idênticas na forma pública serão deduplicadas, pois o contrato não expõe a identidade do filme; um mesmo produtor pode aparecer mais de uma vez quando os pares tiverem anos distintos.
- Quando não houver produtor com ao menos duas vitórias, a resposta será HTTP 200 com `{"min": [], "max": []}`.
- A resposta será ordenada deterministicamente em cada lista por nome do produtor (casefold), nome original, `previousWin` e `followingWin`, depois de eliminar duplicatas. Isso torna a API estável mesmo sob empates.

### Testes

- Haverá somente testes de integração, exercitando a rota pública com `TestClient` dentro de seu context manager para executar o lifespan real. Cada teste passará um CSV temporário à factory, obtendo banco, schema e carga independentes.
- Os cenários cobrirão o CSV fornecido (mínimo Joel Silver: 1990–1991, 1; máximo Matthew Vaughn: 2002–2015, 13), mais de duas vitórias, múltiplos vencedores/intervalo zero, empates de mínimo e máximo, ausência de pares e troca de CSV. Asserções compararão o JSON completo e já ordenado.
