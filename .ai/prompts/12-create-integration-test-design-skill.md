Agora você deve criar uma skill específica para desenhar os cenários dos testes de integração.

Crie a skill integration-test-design dentro de .agents/skills, seguindo o formato atual suportado pelo Codex.

O desafio exige somente testes de integração e informa que outros datasets serão usados durante a avaliação.

A skill deve priorizar datasets pequenos capazes de quebrar implementações ingênuas.

Ela deve considerar principalmente:

- empate no menor intervalo;
- empate no maior intervalo;
- produtor com três ou mais vitórias;
- vários produtores no mesmo filme;
- diferentes combinações no campo producers;
- múltiplos vencedores no mesmo ano;
- duas vitórias do mesmo produtor no mesmo ano;
- intervalo zero;
- produtor com apenas uma vitória;
- nenhum produtor recorrente;
- ordenação determinística;
- linhas não vencedoras entre vitórias;
- dados que revelem implementação incorreta baseada em pares não consecutivos.

Os testes propostos pela skill devem:

- utilizar a interface HTTP;
- executar o lifecycle real da aplicação;
- utilizar a importação real;
- utilizar SQLite em memória real;
- evitar mocks da regra principal;
- evitar testes unitários.

A skill deve buscar poucos cenários de alto valor em vez de criar dezenas de testes redundantes.

Quando algum detalhe depender do comportamento atual de pytest, HTTPX, FastAPI ou TestClient, oriente o uso do Context7.

Mantenha a skill pequena e focada.

Depois valide o SKILL.md criado.