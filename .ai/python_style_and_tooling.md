# Python Style and Tooling (Authoritative)

## Purpose

This document is the **single source of truth for Python code generation and modification** in this repository.

It defines environment assumptions, tooling, file structure, style rules, and mandatory boilerplate to support a **simulation validation project** whose primary goal is correctness, transparency, and analytic testability.

This document governs **how Python code is written**. Project intent, validation philosophy, and physics priorities are defined in `system_prompt.md` and validation documents.

---

## Environment and Tooling

* **Python version**: >= 3.13
* **Virtual environment**: `.venv/` at repository root
* **Interpreter**: `.venv/bin/python`
* **Package manager**: `uv`

Rules:

* Required dependencies are declared in `pyproject.toml`
* Do **not** install packages or modify the environment
* If dependencies are missing or incompatible, report the issue instead of working around it

---

## Dependency Policy

### Core Libraries (assumed available)

* `numpy`
* `pandas`
* `matplotlib`

### Additional Dependencies

* Must be explicitly justified
* Must not be required for core validation logic
* Must not introduce GPU or platform-specific requirements

**All code must run correctly on CPU-only systems.**
GPU acceleration, if present, must be optional and non-default.

---

## Coding Style

* Follow **PEP 8**
* Use **type hints** for all function signatures
* Write concise docstrings for:

  * Modules
  * Classes
  * Public functions

Restrictions:

* Do **not** use `from __future__ import annotations`
* Avoid metaprogramming, decorators that obscure logic, and overly dynamic constructs

Clarity is preferred over brevity.

---

## Structural Expectations

* Favor small, well-named functions
* Avoid monolithic scripts when possible
* Group configuration parameters explicitly
* Preserve intermediate variables useful for diagnostics and validation

Code should be understandable when opened directly in **Spyder or VS Code**, without external context.

---

## Data, Output, and Reproducibility

* Simulation outputs belong in `data/`
* Do not embed generated data in source files
* Prefer deterministic execution where possible
* If randomness is used, expose seeds explicitly

Outputs should be easy to:

* Inspect numerically
* Compare across runs
* Use in invariant or regression tests

---

## Validation-Oriented Implementation Rules

When writing or modifying code:

* Expose physically meaningful intermediate quantities
* Make units and scaling explicit where practical
* Prefer readable equations over condensed vector tricks

Where appropriate:

* Enable invariant checks
* Support analytic or limiting-case comparisons
* Make it easy to log or export intermediate results

If a coding choice improves performance but obscures validation, **choose validation clarity instead**.

---

## Required File Header (Mandatory)

All new Python files **must** begin with a copyright and license header.

Rules:

* Do not remove or alter existing headers
* New files must include the canonical header template

Recommended practice:

* Store the canonical header text in a reusable file (e.g. `.ai/python_file_header.txt`)
* Paste it verbatim at the top of each new `.py` file

---

## Boilerplate Expectations

Python scripts should follow this general structure:

1. Copyright / license header
2. Module-level docstring describing purpose and assumptions
3. Imports (grouped and minimal)
4. Configuration section
5. Function and class definitions
6. `if __name__ == '__main__':` entry point

The goal is **repeatable, inspectable validation runs**, not production deployment.

---

## Final Principle

> Python code in this repository exists to make validation easier,
> not to maximize cleverness, abstraction, or raw performance.
