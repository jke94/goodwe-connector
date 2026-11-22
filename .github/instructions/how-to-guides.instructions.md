---
applyTo: "{sample.py,goodwe_connector/**/*.py,tests/**/*.py}"
---

# How-To Guidance

When providing operational guidance or implementing a usage example:

- Start from `goodwe_config.json` at the repository root.
- Show runnable commands and valid Python usage.
- Use `pytest -q tests` for the test suite.
- Distinguish supported SEMS+ operations from older operations that have not
  been migrated.
