Agora você deve implementar a carga do CSV durante a inicialização da aplicação.

Antes de implementar, consulte no Context7 a abordagem atualmente recomendada pelo FastAPI 0.141.1 para lifecycle e lifespan.

Não utilize APIs antigas de startup se a documentação atual recomendar lifespan.

O dataset padrão do projeto está versionado em:

docs/Movielist.csv

A aplicação deve conseguir localizar e utilizar esse arquivo automaticamente quando nenhuma configuração adicional for fornecida.

O caminho padrão não deve depender de forma frágil do current working directory. Resolva o caminho de maneira consistente com a estrutura do projeto, de forma que a aplicação funcione ao ser executada localmente, pelos testes e dentro da imagem Docker.

Ao mesmo tempo, o caminho do CSV deve ser configurável.

Os testes e a avaliação devem conseguir inicializar a mesma aplicação utilizando outro arquivo CSV sem:

- alterar código;
- substituir docs/Movielist.csv;
- modificar estado global.

Utilize um mecanismo de configuração simples e explícito.

Se for utilizada uma variável de ambiente, prefira um nome claro, como MOVIELIST_CSV_PATH, mas utilize somente esse nome se ele fizer sentido com a configuração real implementada.

Use o módulo csv da biblioteca padrão do Python.

Não use pandas.

A importação deve:

- validar que o arquivo existe;
- validar a presença das colunas esperadas;
- tratar whitespace de forma segura;
- converter year explicitamente;
- interpretar winner de maneira consistente;
- persistir os filmes;
- persistir e associar os produtores;
- executar toda a carga dentro de uma única transação;
- impedir que o banco fique parcialmente preenchido quando ocorrer um erro.

Se o arquivo for inválido, a aplicação deve falhar durante o startup/lifespan com uma mensagem clara, em vez de iniciar utilizando dados incompletos.

Não implemente nenhuma lógica baseada em:

- títulos específicos;
- nomes específicos de produtores;
- anos específicos;
- resultados conhecidos de docs/Movielist.csv.

O arquivo padrão deve ser apenas uma entrada para a aplicação, não parte da regra de negócio.

Também garanta que múltiplas instâncias da aplicação utilizadas pelos testes possam carregar datasets diferentes de forma isolada.

Depois valide que:

- iniciar a aplicação sem configuração adicional utiliza docs/Movielist.csv;
- o schema é criado;
- os registros são importados;
- outro CSV pode ser informado pela configuração;
- uma aplicação criada com outro CSV não altera a configuração de outra instância;
- erro durante a importação não deixa carga parcial.

Execute as verificações de qualidade relevantes após a implementação.