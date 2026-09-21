Agora você deve otimizar a lógica responsável pelo cálculo dos menores e maiores intervalos entre vitórias dos produtores.

Após a entrega do teste foi recebida a seguinte observação:

"Lógica ineficiente: o sistema realiza 6+ loops em código para chegar ao resultado. Isto pode ser reduzido melhorando a filtragem e classificação dos dados."

Primeiro analise a implementação atual em:

src/app/intervals.py

e também:

src/app/api.py
src/app/models.py
tests/

Antes de modificar o código, identifique explicitamente quantas travessias dos dados são realizadas atualmente desde o resultado da consulta SQL até a resposta final.

A implementação atual não deve continuar trazendo todos os intervalos válidos para Python para depois:

- encontrar o mínimo;
- encontrar o máximo;
- filtrar novamente os mínimos;
- filtrar novamente os máximos;
- ordenar os mesmos dados em múltiplas passagens.

A responsabilidade de filtrar e classificar os dados deve ser movida para o banco sempre que isso produzir uma solução mais simples e eficiente.

A consulta deve continuar utilizando SQLAlchemy 2.0.54 e SQLite.

Consulte o Context7 para confirmar a API atual do SQLAlchemy utilizada para:

- CTEs ou subqueries;
- LAG;
- funções de agregação;
- UNION ALL, se utilizado;
- ordenação;
- aliases e labels.

Preserve a regra já implementada:

1. considere somente filmes vencedores;
2. agrupe as vitórias por produtor;
3. ordene cronologicamente as vitórias de cada produtor;
4. utilize somente pares consecutivos de vitórias;
5. calcule followingWin - previousWin;
6. encontre o menor intervalo global;
7. encontre o maior intervalo global;
8. retorne todos os produtores empatados no mínimo;
9. retorne todos os produtores empatados no máximo;
10. suporte intervalo zero;
11. quando não houver intervalos válidos, retorne min e max vazios;
12. mantenha ordenação determinística.

Não altere o contrato HTTP.

A resposta deve continuar no formato:

{
  "min": [
    {
      "producer": "...",
      "interval": 0,
      "previousWin": 0000,
      "followingWin": 0000
    }
  ],
  "max": [
    {
      "producer": "...",
      "interval": 0,
      "previousWin": 0000,
      "followingWin": 0000
    }
  ]
}

Evite resolver a observação apenas trocando vários loops explícitos por comprehensions ou funções diferentes.

A otimização deve reduzir efetivamente:

- quantidade de dados transferidos do SQLite para Python;
- número de travessias feitas em Python;
- trabalho repetido de filtragem;
- trabalho repetido de ordenação.

Prefira que o SQLite calcule os intervalos e determine quais registros pertencem aos extremos.

Uma abordagem aceitável, caso seja adequada após a análise, é estruturar a consulta em etapas SQL semelhantes a:

- conjunto de vitórias com LAG por produtor;
- conjunto dos intervalos válidos;
- cálculo do MIN e MAX globais;
- seleção somente das linhas cujo intervalo corresponde ao mínimo ou máximo.

Considere cuidadosamente o caso em que:

minimum == maximum

Nesse cenário, os mesmos intervalos devem aparecer corretamente tanto em min quanto em max.

Se utilizar uma única consulta para retornar mínimo e máximo, considere uma forma explícita de classificar cada linha como pertencente a "min" ou "max".

UNION ALL entre os dois conjuntos pode ser utilizada se tornar esse caso mais correto e legível.

Não force essa estrutura se existir uma solução SQLAlchemy mais simples e equivalente.

O resultado ideal deve exigir no máximo uma pequena passagem em Python para transformar/classificar as linhas retornadas pelo banco.

Evite criar um set contendo todos os intervalos apenas para depois descobrir seus extremos.

Também revise src/app/api.py.

Se existirem comprehensions ou transformações adicionais que realizem passagens desnecessárias sobre os mesmos resultados, simplifique-as quando isso puder ser feito sem prejudicar clareza ou tipagem.

Não faça micro-otimizações sem impacto real.

O foco é remover as múltiplas travessias sobre todos os intervalos e fazer a consulta retornar somente os dados relevantes.

Mantenha o código legível.

Não introduza:

- cache;
- processamento assíncrono;
- pandas;
- SQL bruto sem necessidade;
- stored procedures;
- novas dependências;
- abstrações genéricas;
- repository pattern apenas para esta otimização.

## Validação funcional

Todos os testes de integração existentes devem continuar passando.

Revise particularmente os cenários de:

- empate no menor intervalo;
- empate no maior intervalo;
- mínimo igual ao máximo;
- três ou mais vitórias do mesmo produtor;
- somente vitórias consecutivas;
- múltiplos vencedores no mesmo ano;
- intervalo zero;
- nenhum produtor recorrente;
- ordenação determinística;
- dataset padrão docs/Movielist.csv.

Se algum desses cenários ainda não estiver coberto por teste de integração, adicione o menor teste necessário.

Não crie testes unitários.

## Validação da otimização

Além da correção funcional, demonstre objetivamente que a implementação foi simplificada.

Ao finalizar, compare a implementação anterior com a nova e informe:

- quantas travessias relevantes eram feitas anteriormente em Python;
- quantas permanecem depois da alteração;
- se todos os intervalos ainda são materializados em Python;
- se mínimo e máximo agora são determinados pelo SQLite;
- quantas linhas aproximadamente chegam ao Python no dataset padrão antes e depois, se isso puder ser medido de forma simples;
- quantas consultas SQL são executadas para calcular o resultado.

Prefira uma única consulta SQL para obter os extremos, desde que isso não prejudique a correção ou legibilidade.

Não adicione instrumentação permanente apenas para produzir essa comparação.

Se for útil durante a análise, utilize temporariamente:

EXPLAIN QUERY PLAN

ou logging das queries SQL, mas não deixe debugging desnecessário na aplicação final.

Verifique também se os índices e chaves já existentes são adequados para os joins utilizados.

Não adicione índices sem demonstrar que são úteis para esta consulta.

Depois execute:

make check

e confirme:

- Ruff aprovado;
- formatação aprovada;
- mypy aprovado;
- todos os testes de integração aprovados.

Execute também a aplicação com docs/Movielist.csv e confirme que o endpoint continua retornando o resultado esperado.

Não altere logging, Docker, Dev Container, CI ou documentação sem necessidade direta para esta otimização.

Ao finalizar, apresente um resumo curto contendo:

- causa da ineficiência anterior;
- estrutura da nova consulta;
- quantidade de processamento removida do Python;
- tratamento do caso minimum == maximum;
- resultado dos testes;
- resultado das verificações de qualidade.

Não faça commit nem push automaticamente.