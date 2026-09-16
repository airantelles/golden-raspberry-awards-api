---
name: integration-test-design
description: Design a small, high-value set of integration-test datasets for the Golden Raspberry producer-interval API, especially when validating replacement CSV inputs.
---

# Integration-test design

Design integration tests for the API contract, not unit tests for its internal
helpers. Use the real application lifecycle, its real CSV import path, a real
in-memory SQLite database, and HTTP requests to the public endpoint. Do not
mock the interval rule, importer, persistence layer, or HTTP boundary.

Keep the suite deliberately small. Prefer a few isolated, hand-sized CSV
datasets whose expected response can be checked exactly over large fixtures or
many overlapping tests. Each dataset must be self-contained so it also proves
the application works when the supplied CSV is replaced.

## Choose scenarios that break naive implementations

Cover these behaviours with the fewest datasets that make each failure
unambiguous:

- ties at both the minimum and maximum interval, with deterministic ordering;
- one producer with three or more wins, proving intervals use adjacent wins
  only, never arbitrary historical pairs;
- multiple producers on one winning film, including names joined by `and`,
  `&`, commas, and their practical combinations used by the importer;
- multiple winning films in a year, including two wins by the same producer in
  that year, so zero-length adjacent intervals are retained;
- non-winning rows between wins, which must not affect intervals;
- producers with one win only, and a dataset with no recurring producer, both
  of which must produce no interval records.

When combining behaviours in one fixture, retain enough distinct producer
names and years that the expected minimum and maximum sets still identify the
specific rule being tested. Do not combine cases if it obscures whether a
failure came from producer parsing, winner filtering, sorting, or interval
selection.

For every proposed dataset, record the CSV rows, the expected HTTP status and
full response body, and the incorrect shortcut it defeats. Assert complete
ordered `min` and `max` lists, including each producer name, interval,
previous year, and following year. This makes ordering and tie handling part of
the contract rather than an incidental implementation detail.

## Test execution constraints

Create the input file used by the real importer, configure the application to
use it and an in-memory SQLite database, then start and stop the application
through its normal test lifecycle. Make the HTTP request only after startup has
performed the import. Use a fresh application/database lifecycle per dataset
unless the application explicitly documents safe reset behaviour.

If the test setup depends on the current lifecycle semantics of pytest,
HTTPX, FastAPI, or `TestClient`, consult Context7 before choosing fixtures,
client construction, or startup/shutdown handling. Do not rely on memory of a
library's current API.

Avoid tests that call services, repositories, parsers, or calculation
functions directly. The objective is a compact set of integration tests that
detect incorrect behaviour under evaluation datasets, not exhaustive unit-level
coverage.
