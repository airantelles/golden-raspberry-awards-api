Agora você deve criar uma skill específica deste repositório para revisar decisões arquiteturais.

Crie a skill architecture-review dentro de .agents/skills, seguindo o formato atualmente suportado pelo Codex para skills de projeto.

A skill deve ser pensada para uma aplicação pequena que está sendo avaliada em um teste técnico para uma posição de especialista.

Ela deve analisar principalmente:

- acoplamento;
- testabilidade;
- configuração;
- lifecycle da aplicação;
- persistência;
- isolamento entre componentes;
- tratamento de recursos;
- decisões que possam dificultar testes com outros datasets;
- complexidade desnecessária.

Ela não deve incentivar automaticamente:

- Clean Architecture;
- repository pattern;
- service layer;
- CQRS;
- interfaces sem necessidade;
- abstrações criadas apenas para seguir um padrão arquitetural.

Quando duas soluções forem igualmente corretas para este contexto, a skill deve favorecer a mais simples.

Quando uma recomendação depender do comportamento atual de FastAPI, SQLAlchemy, Pydantic ou outra biblioteca externa, a skill deve orientar o agente a consultar o Context7 antes de concluir.

Mantenha a skill pequena e específica.

Não copie documentação de frameworks para dentro dela.

Depois de criar a skill, valide o formato do SKILL.md.