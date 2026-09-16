Agora você deve expor a consulta de intervalos através da API REST.

O serviço deve atender ao nível 2 do Richardson Maturity Model solicitado pelo desafio.

Crie somente o endpoint necessário para consultar os intervalos de prêmio por produtor.

Use GET e uma URI orientada ao recurso.

Não implemente HATEOAS.

A resposta JSON deve seguir exatamente o contrato do enunciado:

{
  "min": [...],
  "max": [...]
}

Cada item deve conter exatamente:

- producer;
- interval;
- previousWin;
- followingWin.

No código Python, mantenha atributos idiomáticos em snake_case, como:

- previous_win;
- following_win.

Use Pydantic 2.13.5 para serializar os nomes esperados pelo contrato JSON.

Antes de implementar aliases ou serialização, consulte no Context7 a abordagem atual recomendada pelo Pydantic 2.13.5.

Não exponha entidades SQLAlchemy diretamente como response model.

Quando não houver intervalos válidos, retorne:

{
  "min": [],
  "max": []
}

Não crie endpoints adicionais sem necessidade.

Depois:

- inicie a aplicação;
- faça uma chamada real ao endpoint;
- valide status code;
- valide Content-Type;
- valide o formato JSON;
- valide o resultado usando o CSV original.