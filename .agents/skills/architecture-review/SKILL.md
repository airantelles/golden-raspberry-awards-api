---
name: architecture-review
description: Review architectural decisions in this small technical-test application, focusing on simplicity, isolation, lifecycle, configuration, persistence, and dataset-independent testing.
---

# Architecture review

Review the change in proportion to a small application evaluated as a specialist technical test. Assess whether it improves or weakens:

- coupling and component isolation;
- testability, including integration tests with replacement CSV datasets;
- configuration, application lifecycle, persistence, and resource cleanup;
- ownership and release of files, database sessions, connections, and similar resources;
- unnecessary complexity or indirection.

Read `.ai/decisions.md` before recommending a change to an architectural decision recorded there. Treat existing project constraints as intentional unless the evidence shows they cause a concrete problem.

Prefer the simplest solution when alternatives are equally correct in this context. Do not recommend Clean Architecture, repository or service layers, CQRS, interfaces, or other abstractions merely to conform to a pattern. Recommend an abstraction only when it resolves a specific present problem, and name that problem.

For recommendations that rely on current behavior of FastAPI, SQLAlchemy, Pydantic, or another external library, consult Context7 before reaching a conclusion. Do not copy framework documentation into the review.

State concrete findings, their practical impact, and the smallest justified change. If no meaningful architectural issue exists, say so rather than inventing one.
