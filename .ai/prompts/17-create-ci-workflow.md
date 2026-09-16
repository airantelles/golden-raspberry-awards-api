Agora você deve adicionar uma CI simples usando GitHub Actions.

Não crie pipeline de deploy.

O objetivo da CI é reproduzir as verificações que já existem localmente.

Configure o workflow para executar em:

- pull requests;
- pushes para a branch principal.

A CI deve utilizar Python 3.13 e uv 0.12.15.

Utilize o uv.lock em modo frozen.

Execute:

- instalação das dependências;
- Ruff;
- verificação de formatação;
- mypy;
- todos os testes de integração.

Não configure banco externo ou qualquer outro serviço porque a aplicação utiliza SQLite em memória.

Utilize versões atuais e estáveis das actions oficiais.

Quando existir suporte apropriado, configure cache do uv seguindo as práticas atuais.

Não coloque CONTEXT7_API_KEY ou qualquer outro secret na CI porque o Context7 não é necessário para executar a aplicação nem os testes.

A CI não deve modificar o lockfile.

Depois valide a sintaxe do workflow e, quando possível, reproduza localmente os mesmos comandos executados na pipeline.