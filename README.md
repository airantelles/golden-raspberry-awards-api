# Golden Raspberry Awards API

API que encontra, entre produtores de filmes vencedores do Golden Raspberry,
os menores e maiores intervalos entre duas vitórias consecutivas.

## Quick start

Após clonar o repositório, execute os comandos a partir de sua raiz. O dataset
padrão já está disponível em `docs/Movielist.csv`; nenhuma configuração
adicional é necessária.

```bash
uv sync --frozen
uv run uvicorn --app-dir src app.main:app --reload
```

Em outro terminal, com a API em execução:

```bash
curl http://127.0.0.1:8000/producers/intervals
uv run pytest
```

Pare o servidor com `Ctrl+C` quando terminar. A API inicia em
`http://127.0.0.1:8000` e importa o CSV automaticamente durante a
inicialização.

## Objective

O endpoint `GET /producers/intervals` calcula o intervalo em anos entre cada
par consecutivo de vitórias de um produtor. A resposta contém todos os pares
empatados no menor intervalo global e todos os pares empatados no maior
intervalo global.

## Stack and versions

| Component | Version |
| --- | --- |
| Python | 3.13.15 |
| FastAPI | 0.141.1 |
| SQLAlchemy | 2.0.54 |
| Pydantic | 2.13.5 |
| Uvicorn | 0.53.0 |
| uv | 0.12.15 |
| pytest | 9.1.1 |
| HTTPX | 0.28.1 |
| Ruff | 0.16.7 |
| mypy | 2.3.1 |
| SQLite (Docker and Dev Container) | 3.53.4 |

## Local execution

### Requirements

- Python 3.13.15
- [uv](https://docs.astral.sh/uv/) 0.12.15

Install all runtime and development dependencies from the lock file:

```bash
uv sync --frozen
```

Start the API from the repository root:

```bash
uv run uvicorn --app-dir src app.main:app --reload
```

The default server address is `http://127.0.0.1:8000`. The `--reload` option
is convenient for local development; remove it when automatic restart is not
needed.

### Endpoint

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/producers/intervals` | Returns the global minimum and maximum producer win intervals. |

Example request:

```bash
curl http://127.0.0.1:8000/producers/intervals
```

Example response for the versioned default dataset:

```json
{
  "min": [
    {
      "producer": "Joel Silver",
      "interval": 1,
      "previousWin": 1990,
      "followingWin": 1991
    }
  ],
  "max": [
    {
      "producer": "Matthew Vaughn",
      "interval": 13,
      "previousWin": 2002,
      "followingWin": 2015
    }
  ]
}
```

If no producer has at least two winning films, the endpoint returns HTTP 200
with empty lists:

```json
{"min": [], "max": []}
```

## Dataset and another CSV

The default dataset is versioned at `docs/Movielist.csv` and is imported during
application startup. No manual preparation, download, or copy of data is
needed after cloning the repository.

The CSV path is configurable through `MOVIELIST_CSV_PATH`. A compatible file
is UTF-8 (a BOM is accepted), uses `;` as delimiter, and has the columns
`year`, `title`, `studios`, `producers`, and `winner`. `year`, `title`,
`studios`, and `producers` must have values; `winner` accepts `yes` or an empty
value. Producers are separated by commas and by the isolated conjunction
`and`.

To run the API with another compatible dataset, set the path when starting the
server:

```bash
MOVIELIST_CSV_PATH=./path/to/another.csv uv run uvicorn --app-dir src app.main:app --reload
```

The test suite also creates synthetic CSV datasets. The implementation does
not depend on the specific values in `docs/Movielist.csv`.

## Tests and quality checks

The project contains integration tests only. They exercise the application
through its HTTP API and its real lifespan.

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run mypy .
```

## Using Docker

Build the production image and start the API with the dataset already included
in the image:

```bash
docker build --tag golden-raspberry-awards-api .
docker run --detach --name golden-raspberry-awards-api --publish 8000:8000 golden-raspberry-awards-api
curl http://127.0.0.1:8000/producers/intervals
```

Stop and remove the container when necessary:

```bash
docker rm --force golden-raspberry-awards-api
```

To use another compatible CSV in a container, mount that file and configure
the existing CSV-path setting. This override is optional; it is not needed for
the normal image execution.

```bash
docker run --detach --name golden-raspberry-awards-api-custom --publish 8000:8000 --volume "$(pwd)/path/to/another.csv:/app/data/Movielist.csv:ro" --env MOVIELIST_CSV_PATH=/app/data/Movielist.csv golden-raspberry-awards-api
curl http://127.0.0.1:8000/producers/intervals
docker rm --force golden-raspberry-awards-api-custom
```

## Using Dev Container

Open the repository in VS Code with the Dev Containers extension and select
**Reopen in Container**. The container provides Python 3.13.15, SQLite 3.53.4,
uv, the development dependencies, Ruff, mypy, pytest, and Node.js used by the
development tools. Dependencies are installed automatically when the container
is created.

## Technical decisions

- Each application instance owns an in-memory SQLite database, created at
  startup and disposed at shutdown. The application factory also lets tests
  create isolated instances with their own CSVs.
- The CSV path defaults to `docs/Movielist.csv` and can be configured with
  `MOVIELIST_CSV_PATH`. Loading happens in the FastAPI lifespan before the API
  accepts requests, and the import is one transaction.
- `Movie` and `Producer` use a many-to-many association because one winning
  movie can credit multiple producers. Studios remain raw text because they do
  not participate in this query.
- The query uses SQL `LAG` to compare adjacent wins for each producer. It keeps
  every tied minimum and maximum and sorts the response deterministically.
- The code intentionally has no service, repository, or similar extra layer:
  they would not add value for this small, single-query application.

Relevant decisions are recorded in [.ai/decisions.md](.ai/decisions.md).

## AI development record

The use of AI during development is documented in [.ai/README.md](.ai/README.md).
The main prompts are under [.ai/prompts](.ai/prompts), and relevant technical
decisions are in [.ai/decisions.md](.ai/decisions.md).

## Evaluation notes

- The database is in-memory SQLite; no external database installation is needed.
- The versioned default dataset is `docs/Movielist.csv` and is imported during
  application startup/lifespan.
- Another compatible CSV can be used without code changes through the documented
  path configuration.
- The project implements integration tests only; they exercise the application
  through the API and include alternate synthetic datasets.
- The API supports ties for both the minimum and maximum intervals.
- The repository contains a record of AI use in `.ai`.
