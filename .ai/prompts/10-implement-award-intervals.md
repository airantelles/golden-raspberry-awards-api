Agora você deve implementar a regra principal de cálculo dos intervalos entre prêmios.

Considere somente filmes vencedores.

Para cada produtor, ordene suas vitórias cronologicamente e calcule somente intervalos entre vitórias consecutivas.

Por exemplo, se um produtor venceu em 2000, 2002 e 2010, os pares válidos são:

- 2000 → 2002;
- 2002 → 2010.

Não considere 2000 → 2010 como um intervalo consecutivo.

Implemente essa regra utilizando uma window function LAG no SQLAlchemy.

Antes de escrever a consulta, consulte no Context7 a forma atual do SQLAlchemy 2.0.54 para utilizar:

- lag();
- over();
- partition_by;
- order_by.

A partir dos intervalos gerados, encontre:

- o menor intervalo global;
- o maior intervalo global.

Retorne todos os registros empatados em cada extremo.

A implementação deve tratar corretamente:

- produtor com uma única vitória;
- produtor com três ou mais vitórias;
- duas vitórias do mesmo produtor no mesmo ano;
- múltiplos vencedores no mesmo ano;
- intervalo zero;
- empate no menor intervalo;
- empate no maior intervalo;
- ausência total de produtores com duas vitórias.

Quando não houver nenhum intervalo válido, a camada de domínio/query deve produzir coleções vazias para min e max.

A ordenação final deve ser determinística.

Prefira uma consulta legível a micro-otimizações sem necessidade.

Não implemente ainda o endpoint HTTP.

Mantenha essa regra independente de FastAPI.