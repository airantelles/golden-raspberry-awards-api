---
name: python-review
description: Review Python changes in this Golden Raspberry API as a specialist pull-request reviewer, finding concrete correctness, lifecycle, persistence, and maintainability problems.
---

# Python review

Review the changed code and the minimum relevant surrounding code as a Python
specialist. Report only findings with a concrete failure mode, incorrect
behaviour, or material maintenance/testing cost; do not propose a change just
for style or personal preference.

Prioritize bugs and correctness, non-idiomatic Python that risks errors,
inadequate typing, resource ownership and cleanup, exception handling, and
incorrect application lifecycle. Inspect SQLAlchemy sessions, SQLite
connections, transaction and rollback boundaries, and any global mutable state
especially carefully.

For this application, verify that importing, querying, and tests work with a
replacement CSV dataset rather than depending on `docs/Movielist.csv` or its
contents. Flag unnecessary dependencies, abstractions that do not solve a
present problem, and designs that make the required integration tests harder.
Do not require enterprise patterns, layers, or abstractions without a
demonstrable benefit in this small application.

Read `.ai/decisions.md` before recommending a change to a recorded
architectural decision. When a conclusion depends on the current API or
semantics of FastAPI, SQLAlchemy, Pydantic, pytest, HTTPX, SQLite, or another
library, consult Context7 before recommending the change.

For each finding, state its severity, exact location, failure scenario, and
smallest justified fix. If no meaningful issues are found, say so explicitly.
