# Registro do desenvolvimento assistido por IA

Codex foi utilizado para análise, implementação e revisão. O Context7 MCP foi
usado para consultar documentação atualizada, e as skills `architecture-review`,
`integration-test-design` e `python-review` foram utilizadas durante o trabalho.

O Codex foi executado de forma autônoma (informalmente, "YOLO mode") em um
sandbox baseado em Docker. Esse isolamento foi utilizado como uma camada de
proteção e contenção do ambiente de execução, limitando o escopo de acesso do
agente ao projeto isolado e reduzindo o impacto potencial no sistema host.

Os principais prompts estão em [prompts/](prompts/). Eles registram as
interações centrais do desenvolvimento e não constituem necessariamente uma
transcrição literal de todas as mensagens trocadas.

[.ai/decisions.md](decisions.md) registra as decisões técnicas relevantes
tomadas durante o desenvolvimento.
