# Constrained Field Model (CFM)

**Constrained Field Model (CFM)** is an open-source mathematical framework for simulating
φ-scaled, constraint-driven field-state dynamics.

This repository provides a **deterministic, non-semantic computational substrate**
for studying how constrained fields evolve, stabilise, bifurcate, and interact
under coupled dynamics.

> ⚠️ **Non-goal notice**  
> This project does **not** implement:
> - agency
> - intelligence
> - language
> - cognition
> - identity
> - user-facing assistants or UIs  
>
> CFM is a **mathematical / dynamical core only**.

---

## Repository Scope

CFM is designed to answer **one narrow class of questions**:

> *How do constrained, multi-channel field states evolve over time under φ-scaled
coupling, damping, and coherence constraints?*

It is intended as a **research substrate** that can later be embedded into
higher-level systems — but makes **no claims** about emergent intelligence or consciousness.

---

## Repository Structure

```text
cfm-open/
├── cfm_consts.py            # Mathematical constants (φ, ψ, π)
├── cfm_core_v0/             # Core v0: basic coupled oscillators
├── cfm_core_v1/             # Core v1: slow / fast separation
├── cfm_core_v2/             # Core v2: multi-channel architecture
├── cfm_interface/           # Unified interface + adapters
├── tools/                   # CLI-style analysis tools
├── tests/                   # Test suite
├── docs/                    # Formal specs and behavioral analyses
├── README.md
├── LICENSE
└── pyproject.toml
Each cfm_core_v* version represents a strictly bounded evolution model with
well-defined state variables and update rules.

Installation
Clone the repository:

bash
Copy code
git clone https://github.com/vfd-org/constrained-field-model.git
cd constrained-field-model
Install dependencies (Python ≥3.9 recommended):

bash
Copy code
pip install -e .
If you prefer not to install in editable mode, you can run all tools directly
via python tools/....

Quick Start
Run a local field evolution loop using Core v2:

bash
Copy code
python tools/cfm_local_loop.py --steps 2000 --core-type cfm_v2
This will:

initialise a constrained multi-channel field

evolve it deterministically

emit state data for inspection

Fingerprint Extraction
Generate a structural fingerprint from an evolution trace:

bash
Copy code
python tools/cfm_fingerprint.py --input out.json
Fingerprints are structural descriptors, not semantic labels.

Design Principles
CFM is built around the following principles:

Deterministic dynamics
No stochastic sampling unless explicitly configured.

Constraint-first modeling
Field behavior is shaped by boundary and coupling constraints.

No semantic assumptions
States are numeric; interpretation is external.

Composable cores
Each core version is standalone and testable.

Failure is allowed
Divergence, instability, and collapse are valid outcomes.

Documentation
Formal specifications and behavioral analyses are provided in /docs, including:

Core v0–v2 mathematical definitions

Parameter maps

Stability and bifurcation behavior

Tuning guidance

These documents describe what the system does, not what it “means”.

Tests
Run the test suite:

bash
Copy code
pytest
All tests are deterministic and designed to validate:

state evolution correctness

constraint enforcement

interface compatibility

License
MIT License — see LICENSE.

Citation
If you use this work in research, please cite using CITATION.cff.

Status
This repository represents an initial open-source release of the CFM substrate.

Future work (if any) will focus on:

mathematical refinement

stability analysis

interface generalisation

No roadmap for higher-level systems is implied.

yaml
Copy code

---

## Why this README works (important)

- It **does not promise the future**
- It **cannot be read as “ARIA in disguise”**
- It **sets expectations correctly**
- It protects you from:
  - hype backlash
  - ontology arguments
  - identity projection
  - “where’s the AI?” noise

This is exactly how **foundational substrates** should be published.

---

### If you want next steps
I can:
- sanity-check `pyproject.toml` script entries
- tighten wording even further for academic audiences
- write a **one-paragraph announcement** that won’t trigger UI expectations
- help you decide whether to tag a `v0.1.0` release now or later

But for now:  
**Yes — you can paste this README in as-is and publish safely.**
