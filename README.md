# Golden Raspberry Awards API

API que identifica, entre os produtores de filmes vencedores do Golden
Raspberry, os menores e maiores intervalos entre duas vitórias consecutivas.

## Início rápido

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

Interrompa o servidor com `Ctrl+C` ao finalizar. A API inicia em
`http://127.0.0.1:8000` e importa o CSV automaticamente durante a
inicialização.

## Objetivo

O endpoint `GET /producers/intervals` calcula o intervalo em anos entre cada
par consecutivo de vitórias de um produtor. A resposta contém todos os pares
empatados no menor intervalo global e todos os pares empatados no maior
intervalo global.

## Stack e versões

| Componente | Versão |
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
| SQLite (Docker e Dev Container) | 3.53.4 |

## Execução local

### Requisitos

- Python 3.13.15
- [uv](https://docs.astral.sh/uv/) 0.12.15

Instale todas as dependências de runtime e desenvolvimento a partir do arquivo
de lock:

```bash
uv sync --frozen
```

Inicie a API a partir da raiz do repositório:

```bash
uv run uvicorn --app-dir src app.main:app --reload
```

O endereço padrão do servidor é `http://127.0.0.1:8000`. A opção `--reload` é
conveniente no desenvolvimento local; remova-a quando a reinicialização
automática não for necessária.

### Endpoint

| Método | Caminho | Descrição |
| --- | --- | --- |
| `GET` | `/producers/intervals` | Retorna os intervalos mínimo e máximo globais entre vitórias de produtores. |

Exemplo de requisição:

```bash
curl http://127.0.0.1:8000/producers/intervals
```

Exemplo de resposta para o dataset padrão versionado:

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

Se nenhum produtor tiver pelo menos dois filmes vencedores, o endpoint retorna
HTTP 200 com listas vazias:

```json
{"min": [], "max": []}
```

## Dataset e uso de outro CSV

O dataset padrão está versionado em `docs/Movielist.csv` e é importado durante
a inicialização da aplicação. Após clonar o repositório, não é necessário
preparar, baixar ou copiar dados manualmente.

O caminho do CSV é configurável por meio de `MOVIELIST_CSV_PATH`. Um arquivo
compatível usa UTF-8 (BOM é aceito), `;` como delimitador e as colunas `year`,
`title`, `studios`, `producers` e `winner`. `year`, `title`, `studios` e
`producers` devem ter valores; `winner` aceita `yes` ou valor vazio. Os
produtores são separados por vírgulas e pela conjunção isolada `and`.

Para executar a API com outro dataset compatível, defina o caminho ao iniciar o
servidor:

```bash
MOVIELIST_CSV_PATH=./path/to/another.csv uv run uvicorn --app-dir src app.main:app --reload
```

A suíte de testes também cria datasets CSV sintéticos. A implementação não
depende dos valores específicos de `docs/Movielist.csv`.

## Testes e verificações de qualidade

O projeto contém somente testes de integração. Eles exercitam a aplicação por
meio de sua API HTTP e de seu lifespan real.

```bash
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run mypy .
```

## Makefile

Os comandos `uv` continuam sendo a interface canônica para executar o projeto.
O Makefile oferece apenas atalhos convenientes de desenvolvimento; não
substitui `uv`, `pyproject.toml` nem `uv.lock`.

```bash
make help
make dev
make test
make check
make docker-build
make docker-run
```

## Usando Docker

Faça o build da imagem de produção e inicie a API com o dataset já incluído na
imagem:

```bash
docker build --tag golden-raspberry-awards-api .
docker run --detach --name golden-raspberry-awards-api --publish 8000:8000 golden-raspberry-awards-api
curl http://127.0.0.1:8000/producers/intervals
```

Interrompa e remova o container quando necessário:

```bash
docker rm --force golden-raspberry-awards-api
```

Para usar outro CSV compatível em um container, monte o arquivo e configure o
valor existente para o caminho do CSV. Essa substituição é opcional e não é
necessária para a execução normal da imagem.

```bash
docker run --detach --name golden-raspberry-awards-api-custom --publish 8000:8000 --volume "$(pwd)/path/to/another.csv:/app/data/Movielist.csv:ro" --env MOVIELIST_CSV_PATH=/app/data/Movielist.csv golden-raspberry-awards-api
curl http://127.0.0.1:8000/producers/intervals
docker rm --force golden-raspberry-awards-api-custom
```

## Usando Dev Container

Abra o repositório no VS Code com a extensão Dev Containers e selecione
**Reopen in Container**. O container fornece Python 3.13.15, SQLite 3.53.4,
uv, as dependências de desenvolvimento, Ruff, mypy, pytest e Node.js usado
pelas ferramentas de desenvolvimento. As dependências são instaladas
automaticamente quando o container é criado.

## Depuração no VS Code

Após reabrir o repositório, abra **Run and Debug** e selecione **API: Debug**
para iniciar a API na porta 8000 com breakpoints habilitados em `src/app`. A
configuração usa o ambiente Python próprio do Dev Container, carrega
`docs/Movielist.csv` por padrão e preserva um `MOVIELIST_CSV_PATH` configurado
anteriormente. Selecione **Tests: Debug** para executar os testes de integração
com breakpoints.

## Decisões técnicas

- Cada instância da aplicação possui um banco SQLite em memória, criado na
  inicialização e descartado no shutdown. A factory da aplicação também permite
  que os testes criem instâncias isoladas com seus próprios CSVs.
- O caminho do CSV usa `docs/Movielist.csv` por padrão e pode ser configurado
  com `MOVIELIST_CSV_PATH`. O carregamento ocorre no lifespan do FastAPI antes
  de a API aceitar requisições, e a importação é uma única transação.
- `Movie` e `Producer` usam uma associação muitos-para-muitos, pois um filme
  vencedor pode creditar vários produtores. Os estúdios permanecem como texto
  bruto porque não participam desta consulta.
- A consulta usa SQL `LAG` para comparar vitórias adjacentes de cada produtor.
  Ela preserva todos os empates nos intervalos mínimo e máximo e ordena a
  resposta de forma determinística.
- O código intencionalmente não possui uma camada extra de service, repository
  ou similar: ela não agregaria valor a esta aplicação pequena, com uma única
  consulta.

As decisões relevantes estão registradas em [.ai/decisions.md](.ai/decisions.md).

## Desenvolvimento assistido por IA

Codex foi utilizado como agente principal para análise, implementação e
revisão. O Context7 MCP foi usado para consultar documentação atualizada, e as
skills específicas do projeto apoiaram a revisão de arquitetura, o desenho de
testes de integração e a revisão de Python.

Durante o desenvolvimento, o Codex foi executado de forma autônoma
(informalmente, "YOLO mode") em um sandbox baseado em Docker. O isolamento
serviu como uma camada de proteção e contenção, limitando o escopo de acesso do
agente ao ambiente isolado do projeto e reduzindo o impacto potencial no sistema
host.

Os principais prompts estão em [.ai/prompts/](.ai/prompts/), e as principais
decisões técnicas estão em [.ai/decisions.md](.ai/decisions.md). O registro de
uso de IA também é detalhado em [.ai/README.md](.ai/README.md).

## Notas para avaliação

- O banco de dados é SQLite em memória; não é necessária instalação de banco
  de dados externo.
- O dataset padrão versionado é `docs/Movielist.csv` e é importado durante a
  inicialização/lifespan da aplicação.
- Outro CSV compatível pode ser usado sem alterações de código por meio da
  configuração de caminho documentada.
- O projeto implementa somente testes de integração; eles exercitam a aplicação
  pela API e incluem datasets sintéticos alternativos.
- A API suporta empates tanto para os intervalos mínimo quanto máximo.
- O repositório contém o registro do uso de IA em `.ai`.
