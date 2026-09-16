Agora você deve revisar e finalizar o tratamento do campo producers do CSV.

Antes de escrever ou alterar a regra, analise os formatos que realmente aparecem no arquivo:

docs/Movielist.csv

Existem casos com:

- um único produtor;
- produtores separados por "and";
- produtores separados por vírgula;
- combinações de vírgula com "and";
- vírgula antes do último produtor.

Implemente uma solução pequena, explícita e suficiente para os formatos observados no dataset.

Isole essa responsabilidade para evitar que parsing de strings fique espalhado pela aplicação.

A regra deve:

- preservar o nome original de cada produtor;
- remover somente whitespace acidental;
- evitar produtores duplicados causados apenas por espaços;
- não alterar capitalização;
- não fazer normalizações agressivas;
- não tentar corrigir nomes;
- não tentar implementar um parser linguístico genérico.

A implementação não deve depender da lista conhecida de produtores de docs/Movielist.csv.

Ela deve funcionar com outros datasets que respeitem os mesmos formatos de separação.

Se houver alguma ambiguidade real nos dados e for necessário assumir uma regra, registre essa decisão de forma curta em .ai/decisions.md.

Não crie testes unitários para o parser.

O desafio exige somente testes de integração, portanto esses comportamentos serão exercitados posteriormente através de CSVs sintéticos carregados pela aplicação completa.

Depois da implementação:

- inicialize a aplicação com docs/Movielist.csv;
- confirme que filmes com múltiplos produtores geram as associações esperadas;
- confirme que nomes não ficam com whitespace residual;
- confirme que o mesmo produtor pode ser associado a diferentes filmes sem ser duplicado por erro de parsing;
- execute Ruff;
- execute a verificação de formatação;
- execute mypy;
- execute os testes de integração existentes, caso já existam.

Não adicione abstrações adicionais sem uma necessidade concreta.