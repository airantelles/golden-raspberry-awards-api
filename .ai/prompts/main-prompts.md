# Main development prompts

This is a concise record of the principal development interactions. It keeps
their purpose and scope without reproducing full conversations.

- Analyze the technical requirements and propose a small FastAPI solution for
  calculating producer award-win intervals from a CSV.
- Implement the application factory, CSV import, in-memory persistence, and
  the public producer-interval endpoint.
- Design integration datasets that cover the supplied dataset, alternate CSVs,
  consecutive wins, ties, and the absence of valid intervals.
- Review the architecture and Python implementation for correctness,
  lifecycle, persistence, and maintainability.
