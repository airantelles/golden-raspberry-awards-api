Agora você deve criar uma skill para revisão especializada do código Python deste projeto.

Crie a skill python-review dentro de .agents/skills.

Ela deve revisar o código como um engenheiro especialista em Python faria durante um pull request.

A skill deve procurar principalmente:

- bugs;
- problemas de corretude;
- código não idiomático em Python;
- typing inadequado;
- gerenciamento incorreto de recursos;
- tratamento de exceções;
- lifecycle incorreto;
- problemas com sessões SQLAlchemy;
- problemas com conexões SQLite;
- problemas de transação;
- abstrações desnecessárias;
- dificuldade de teste;
- estado global;
- comportamento que dependa do CSV original;
- dependências sem necessidade;
- APIs de bibliotecas usadas incorretamente.

Ela não deve:

- sugerir mudanças apenas por preferência estética;
- exigir patterns sem uma necessidade concreta;
- transformar uma aplicação pequena em arquitetura corporativa;
- sugerir abstrações sem benefício demonstrável.

Quando uma conclusão depender da API atual de uma biblioteca, a skill deve orientar o agente a consultar o Context7 antes de recomendar alteração.

Mantenha a skill curta e orientada a problemas reais.

Depois valide o SKILL.md.