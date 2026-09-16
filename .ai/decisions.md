# Technical decisions

## ADR-001 — Project-local Context7 MCP

- Status: accepted
- Date: 2026-09-16

Context7 is configured only in `.codex/config.toml`, using the fixed package version `@upstash/context7-mcp@4.1.1`. If authentication is needed, the server receives `CONTEXT7_API_KEY` from the local environment; no credential is stored in the repository.
