# validation_and_invariant_guidelines.md

## Purpose

This document defines **testing, validation, and invariant-checking principles** for this repository.

The goal is not conventional unit testing alone, but **physics-aware validation** of simulation code that may later be integrated into a larger system. Tests should increase confidence that results are:

* Physically consistent
* Analytically defensible
* Numerically stable
* Robust under parameter variation

---

## Validation Philosophy

Simulation validation in this project prioritizes:

1. **Invariants and conservation laws**
2. **Limiting and asymptotic behavior**
3. **Dimensional and scaling consistency**
4. **Regression protection against accidental model changes**

Passing tests does *not* imply the model is correct — but failing tests strongly suggests something is wrong.

---

## What Counts as an Invariant

An invariant is any quantity or relationship that should remain constant (or bounded in a known way) when assumptions are satisfied.

Examples:

* Conservation of energy, momentum, or particle number
* Constant total probability or mass
* Symmetry preservation (e.g., left/right, sign symmetry)
* Known steady-state equilibria
* Monotonic quantities (e.g., entropy production, dissipation)

Invariants may be:

* Exact
* Approximate (within tolerance)
* Regime-dependent (valid only under stated assumptions)

---

## Classes of Tests

### 1. Analytic / Hand-Checkable Tests

These tests compare simulation results against:

* Closed-form solutions
* Back-of-the-envelope estimates
* Published scaling laws

Guidelines:

* Use simplified parameter sets
* Prefer small problem sizes
* Make expected outcomes explicit in comments or docs

---

### 2. Invariant Tests

Invariant tests assert that quantities remain conserved or bounded over time or iterations.

Examples:

* Relative energy drift stays below a threshold
* Center-of-mass remains fixed when no external force is applied
* Magnetic mirror symmetry preserved in symmetric setups

Invariant violations should:

* Trigger clear failures
* Report magnitude and location of violation

---

### 3. Limiting-Case Tests

These tests push parameters toward known limits:

* Zero field / zero force
* Infinite stiffness / massless limits
* Very small or very large time steps

Expected behavior:

* Reduction to simpler dynamics
* Smooth convergence, not numerical explosions

---

### 4. Consistency and Regression Tests

These tests ensure that:

* Refactoring does not change numerical results unintentionally
* Outputs remain consistent across environments
* Results are reproducible given fixed seeds and parameters

Regression tests may compare:

* Scalar outputs
* Time series norms
* Integrated quantities

---

## Tolerances and Numerical Error

Because floating-point arithmetic is unavoidable:

* Use **relative tolerances** where possible
* Avoid strict equality for floats
* Document why a given tolerance is acceptable

Tolerance choices should be:

* Physically motivated
* Stable across machines

---

## Test Structure and Location

Recommended structure:

* Validation logic may live alongside code during development
* Reusable tests should migrate to a `tests/` directory
* Data used for validation should be stored or regenerated deterministically

Avoid:

* Hard-coded magic numbers without explanation
* Tests that silently pass despite large errors

---

## What Tests Should NOT Do

* Hide numerical instability
* Mask physically impossible behavior
* Depend on plotting or manual inspection
* Require GPUs or non-core dependencies

---

## Reporting Failures

When a validation test fails, it should:

* Identify the violated invariant or expectation
* Report relevant parameters
* Quantify the error (absolute and/or relative)

Silent failure or ambiguous output is unacceptable for validation work.

---

## Guiding Principle

> A good validation test makes it *easy to trust* correct results
> and *hard to ignore* incorrect ones.
