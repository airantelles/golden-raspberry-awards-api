Agora você deve ajustar a configuração criada na etapa anterior para refletir a localização definitiva do dataset padrão do projeto.

O arquivo CSV fornecido com o desafio será versionado no repositório exatamente em:

docs/Movielist.csv

O documento original da avaliação não será versionado e não deve ser adicionado ao repositório.

Revise o Dockerfile e o .dockerignore criados anteriormente e faça somente os ajustes necessários para garantir que:

- docs/Movielist.csv não seja excluído pelo .dockerignore;
- docs/Movielist.csv esteja disponível na imagem final da aplicação;
- a estrutura da imagem mantenha um caminho previsível para esse arquivo;
- o container possa utilizar esse arquivo como dataset padrão sem exigir volume externo;
- nenhuma referência ao PDF original da avaliação seja adicionada à imagem.

A aplicação ainda será implementada para permitir que outro CSV seja informado por configuração, então não crie nenhum acoplamento que impeça o uso de datasets alternativos.

Não implemente ainda a lógica de leitura do CSV, porque isso será feito em uma etapa posterior.

Também atualize o AGENTS.md com duas regras permanentes:

- docs/Movielist.csv faz parte da entrega e deve permanecer versionado;
- o documento original da avaliação não faz parte da entrega e não deve ser adicionado ao repositório.

Não altere outras decisões do Dockerfile ou do projeto que já foram validadas, a menos que sejam necessárias para suportar essa mudança.

Depois dos ajustes:

- faça novamente o build da imagem;
- confirme que docs/Movielist.csv existe dentro da imagem;
- confirme que Python continua na versão 3.13.15;
- confirme que python -c "import sqlite3; print(sqlite3.sqlite_version)" continua retornando exatamente 3.53.4.

Corrija somente problemas relacionados a essa alteração.