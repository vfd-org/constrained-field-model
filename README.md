# CFM Core

A bounded deterministic numeric dynamical substrate using phi/psi-based update equations.

## What CFM Core IS

- A deterministic dynamical system producing bounded numeric outputs in [0, 1]
- A mathematical model using phi (golden ratio), psi, and related constants
- A reproducible substrate for field-theoretic numeric computation
- Fully deterministic given initial state and timestep sequence

## What CFM Core is NOT

- A cognitive system, "mind," or sentience model
- A processor of semantic content or language
- An identity holder, accessor, or generator
- A control signal generator or decision maker

## Installation

```bash
# Clone the repository
git clone [https://github.com/cfm-project/cfm-core.git](https://github.com/vfd-org/constrained-field-model.git)
cd constrained-field-model

# Install in development mode
pip install -e .

# Or install with dev dependencies
pip install -e ".[dev]"
```

Requires Python 3.8+. No external dependencies for core functionality.

## Quick Start

```python
from cfm_interface import create_cfm_core

# Create a CFM core (v2 by default)
core = create_cfm_core("cfm_v2")

# Run simulation steps
for step in range(100):
    result = core.step(dt=0.1)
    # All outputs guaranteed in [0, 1]
    print(f"coherence={result['coherence']:.3f} stability={result['stability']:.3f}")
```

## Core Versions

| Version | Description | State Variables |
|---------|-------------|-----------------|
| v0 | Basic coupled oscillator | 4 (coherence, instability, energy, phase) |
| v1 | Slow/fast variable separation | 8 (adds coherence_baseline, alignment_phase) |
| v2 | Multi-channel architecture | 11 (five-tier timescale hierarchy) |

All versions produce the same four output fields: `coherence`, `stability`, `intensity`, `alignment`.

## CLI Tools

### Running Simulations

```bash
# Run 2000 steps with v2 core, output to JSON
cfm-loop --steps 2000 --core-type cfm_v2 --output-json out.json

# Or run directly
python tools/cfm_local_loop.py --steps 2000 --output-json out.json
```

### Fingerprint Extraction

```bash
# Extract behavioral fingerprint
cfm-fingerprint --input out.json --output fingerprint.json

# Compare two fingerprints for regression detection
cfm-fingerprint --compare fp1.json fp2.json
```

### Reference Scenario Runs

```bash
# Generate canonical reference run for regression testing
python tools/cfm_reference_runs.py --scenario baseline_quiet --output-json baseline.json

# Available scenarios:
#   baseline_quiet      2,000 steps, dt=0.1, no perturbations
#   baseline_long       20,000 steps, dt=0.1, no perturbations
#   mild_perturbation   5,000 steps, small bounded pulses
#   high_variability    10,000 steps, dt jitter + perturbation pulses
```

### Log Analysis

```bash
# Analyze a run output
python tools/cfm_log_analyzer.py --input out.json

# Analyze multiple runs with summary
python tools/cfm_log_analyzer.py --input run1.json run2.json --summary
```

## Reproducibility Workflow

Generate deterministic reference runs for regression testing:

```bash
# 1. Generate reference run with fixed seed
python tools/cfm_reference_runs.py \
    --scenario baseline_quiet \
    --core-type cfm_v2 \
    --seed 42 \
    --output-json reference_baseline.json

# 2. Extract fingerprint
cfm-fingerprint --input reference_baseline.json --output reference_fp.json

# 3. After code changes, regenerate and compare
python tools/cfm_reference_runs.py \
    --scenario baseline_quiet \
    --core-type cfm_v2 \
    --seed 42 \
    --output-json new_baseline.json

cfm-fingerprint --input new_baseline.json --output new_fp.json
cfm-fingerprint --compare reference_fp.json new_fp.json
```

Identical seeds produce identical trajectories. Any difference indicates behavioral change.

## Output Format

All CFM cores produce a dictionary with these guaranteed fields:

| Field | Type | Range | Description |
|-------|------|-------|-------------|
| `coherence` | float | [0, 1] | Field coherence level |
| `stability` | float | [0, 1] | Stability indicator |
| `intensity` | float | [0, 1] | Energy/activation level |
| `alignment` | float | [0, 1] | Resonance/alignment indicator |

Additional metadata fields (e.g., `cfm_version`, `cfm_step`, `cfm_time`) may be included.

## Safety Guarantees

All CFM cores guarantee:

- **Bounded outputs**: All values in [0, 1], always
- **No NaN/Inf**: Safe arithmetic operations only
- **Deterministic**: Same inputs produce identical outputs
- **No identity content**: No identity fields or derivation
- **No semantic processing**: Pure numeric dynamics

## Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Or with unittest
python -m unittest discover -s tests -p "test_*.py" -v
```

## Project Structure

```
cfm-core/
├── cfm_consts.py           # Mathematical constants (phi, psi, pi)
├── cfm_core_v0/            # CFM Core v0 implementation
├── cfm_core_v1/            # CFM Core v1 implementation
├── cfm_core_v2/            # CFM Core v2 implementation
├── cfm_interface/          # Unified interface layer
│   ├── protocols.py        # CFMCoreProtocol definition
│   ├── adapters.py         # CFMCoreAdapter
│   └── factory.py          # Core factory function
├── tools/                  # CLI tools
│   ├── cfm_local_loop.py   # Simulation runner
│   ├── cfm_fingerprint.py  # Fingerprint extraction
│   ├── cfm_reference_runs.py  # Reference scenario generator
│   └── cfm_log_analyzer.py # Run output analyzer
├── tests/                  # Test suite
└── docs/                   # Specifications and analysis
```

## Documentation

See the `docs/` directory for detailed specifications:

- CFM Core v0/v1/v2 specifications
- Behavioral analysis documents
- Parameter tuning guides

## License

MIT License - See [LICENSE](LICENSE) for details.

## Contact

Vibrational Field Dynamics Institute
Email: contact@vibrationalfielddynamics.org
Twitter/X: [@vfd_org](https://twitter.com/vfd_org)
