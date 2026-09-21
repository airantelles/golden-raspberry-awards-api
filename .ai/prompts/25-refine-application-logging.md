Agora você deve fazer uma revisão pontual da implementação de logging adicionada na etapa anterior.

Não refatore a aplicação inteira e não altere regra de negócio.

Revise apenas dois pontos:

1. LOG_LEVEL deve controlar prioritariamente os logs da aplicação sem tornar desnecessariamente verbosos os logs de bibliotecas de terceiros.

Verifique o uso atual de logging.basicConfig(level=...) e confirme se ele está alterando o root logger de forma mais ampla do que necessário.

Se houver uma solução pequena e idiomática para configurar os logs de app.* sem interferir nos loggers administrados pelo Uvicorn ou em outras bibliotecas, aplique-a.

Não introduza dependência externa ou framework de logging.

2. LOG_LEVEL=DEBUG deve produzir algum diagnóstico útil da aplicação.

Adicione somente logs DEBUG que tragam valor real para o endpoint principal, por exemplo:

- início do cálculo dos extremos dos produtores;
- quantidade de resultados mínimos e máximos encontrados.

Não registre:

- conteúdo completo da resposta;
- dados do CSV;
- uma linha por filme ou produtor;
- access logs HTTP já fornecidos pelo Uvicorn.

Mantenha:

- INFO para lifecycle e importação;
- DEBUG para detalhes internos de diagnóstico;
- ERROR/EXCEPTION para falhas.

Depois execute:

make check

Valide também manualmente a aplicação com:

LOG_LEVEL=INFO

e:

LOG_LEVEL=DEBUG

Confirme que DEBUG adiciona detalhes úteis sem gerar excesso de logs.

Não faça outras alterações.

Não faça commit nem push automaticamente.