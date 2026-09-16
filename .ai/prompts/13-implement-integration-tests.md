Agora você deve implementar os testes utilizando a skill integration-test-design.

Crie somente testes de integração.

Não crie testes unitários.

Cada teste deve exercitar a aplicação através da interface HTTP e deve utilizar:

- a aplicação real;
- o lifespan real;
- SQLite em memória real;
- schema real;
- importação real do CSV;
- parsing real dos produtores;
- consulta real dos intervalos.

Não faça mock de:

- banco;
- sessão;
- importer;
- parser de produtores;
- consulta dos intervalos;
- regra principal;
- lifecycle da aplicação.

Crie um teste de integração utilizando o dataset versionado em:

docs/Movielist.csv

Esse teste deve confirmar que a aplicação consegue inicializar utilizando o dataset padrão e que o endpoint retorna o resultado esperado para esse conjunto de dados.

Os valores esperados desse teste podem ser derivados do dataset, mas não devem ser utilizados em nenhuma parte da implementação da aplicação.

Além desse teste, crie datasets sintéticos pequenos e independentes para validar os demais comportamentos.

Não faça todos os testes dependerem de docs/Movielist.csv.

Os datasets sintéticos são obrigatórios porque a avaliação poderá utilizar outros arquivos de entrada.

Prefira gerar esses CSVs como fixtures temporárias durante os próprios testes quando isso deixar o cenário mais claro, em vez de adicionar muitos arquivos permanentes ao repositório.

Certifique-se de cobrir pelo menos:

- empate no menor intervalo;
- empate no maior intervalo;
- produtor com três ou mais vitórias;
- cálculo somente entre vitórias consecutivas;
- cenário em que considerar a primeira e a última vitória produziria um resultado incorreto;
- vários produtores no mesmo filme;
- produtores separados por "and";
- produtores separados por vírgula;
- combinação de vírgula com "and";
- duas vitórias do mesmo produtor no mesmo ano;
- intervalo zero;
- múltiplos vencedores no mesmo ano;
- produtor com apenas uma vitória;
- nenhum produtor com duas vitórias;
- linhas não vencedoras entre anos vencedores;
- ordenação determinística da resposta.

Cada teste deve criar uma aplicação apontando para seu próprio CSV quando utilizar um dataset sintético.

Nenhum teste deve:

- alterar docs/Movielist.csv;
- depender da ordem de execução;
- compartilhar banco com outro teste;
- depender de dados deixados por uma execução anterior.

Utilize a configuração pública da aplicação para substituir o caminho do CSV. Não altere variáveis globais internas apenas para facilitar o teste.

Quando algum detalhe depender do comportamento atual de pytest, HTTPX, FastAPI, TestClient ou lifespan, consulte o Context7 antes de implementar.

Depois execute a suíte diversas vezes para detectar:

- estado compartilhado;
- dependência da ordem dos testes;
- comportamento não determinístico;
- flakiness.

Execute também:

- Ruff;
- verificação de formatação;
- mypy.

Corrija qualquer problema encontrado antes de finalizar.