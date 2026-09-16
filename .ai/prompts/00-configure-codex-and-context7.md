Agora você deve preparar este repositório para o desenvolvimento com Codex antes de implementar a aplicação.

Configure o Context7 como MCP somente para este projeto, usando a forma atualmente recomendada pelo Codex para configuração project-local.

O Context7 será utilizado durante o desenvolvimento para consultar documentação atualizada das bibliotecas e ferramentas usadas no projeto.

A versão do Context7 MCP deve ser fixada em 4.1.1.

Nenhuma API key ou outro segredo pode ser commitado.

Se o Context7 utilizar uma chave, ela deve ser obtida da variável de ambiente CONTEXT7_API_KEY.

Crie também:

- .env.example contendo apenas os nomes das variáveis que podem ser necessárias;
- uma regra no .gitignore garantindo que .env e arquivos equivalentes com secrets não sejam versionados;
- .ai/prompts para armazenar os principais prompts utilizados durante o desenvolvimento;
- .ai/README.md explicando resumidamente a finalidade desse diretório;
- .ai/decisions.md para registrar decisões técnicas relevantes que surgirem durante o projeto.

Consulte a documentação atual do Codex e do Context7 antes de definir o formato da configuração, em vez de assumir uma sintaxe antiga.

Neste momento não implemente a aplicação.

Depois de configurar, valide que a configuração do MCP está sintaticamente correta e informe resumidamente quais arquivos foram criados.