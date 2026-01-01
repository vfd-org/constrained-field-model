# CFM Core v0 Specification

**Version:** 0.1
**Status:** Implementation Spec
**Last Updated:** 2025-12-05

---

## Overview

CFM Core v0 is a **pure numeric dynamical system** that conforms to the `CFMCoreProtocol`. It represents an early implementation of Conscious Field Model (CFM) concepts as bounded numerical field dynamics, without any semantic processing, identity access, or cognitive functionality.

### What CFM Core v0 IS

- A deterministic dynamical system with coupled oscillators
- A producer of bounded numeric diagnostics in [0, 1]
- A mathematical model using φ, ψ, π, e-based update rules
- Fully compatible with `CFMCoreAdapter`

### What CFM Core v0 is NOT

- A cognitive system or "mind"
- A processor of semantic content or language
- An identity holder or accessor
- A control signal generator

---

## Conceptual Role

CFM Core v0 models early versions of field-theoretic quantities:

| Quantity | CFM Concept | Core Variable |
|----------|-------------|---------------|
| C(n) | Coherence field | `coherence` |
| A(t) | Activation/intensity | `intensity` |
| R(t) | Resonance/alignment | `alignment` |
| S(t) | Stability index | `stability` |

These are **purely numeric** representations with no semantic content. The dynamics are governed by coupled differential-like update equations using φ and ψ scaling.

---

## Internal State

The core maintains a `CFMCoreState` containing:

| Variable | Range | Description |
|----------|-------|-------------|
| `coherence` | [0, 1] | Field coherence level |
| `instability` | [0, 1] | Inverse stability indicator |
| `energy` | [0, 1] | Normalized energy level |
| `phase` | [0, 1] | Normalized phase position (wraps at 1.0) |
| `time` | ≥ 0 | Accumulated time |
| `step_count` | ≥ 0 | Step counter |

All state variables are maintained in their valid ranges at all times.

---

## Update Dynamics

### Core Update Equations

On each step with time delta `dt`:

```
# Phase evolution (wraps at 1.0)
phase' = (phase + dt * ω_base / φ) mod 1.0

# Energy dynamics (φ-attractor)
energy' = clamp01(energy + dt * (E_target - energy) / (φ * τ_energy))

# Instability dynamics (ψ-scaled)
instability' = clamp01(instability + dt * (I_base * sin(2π * phase) - instability) / (ψ * τ_inst))

# Coherence (coupled to energy and instability)
coherence' = clamp01((1 - instability) * energy^(1/φ))
```

Where:
- `ω_base = 1/φ` — base angular frequency
- `E_target` — energy attractor (default: 1/φ ≈ 0.618)
- `I_base = 1/(2φ)` — instability base amplitude
- `τ_energy`, `τ_inst` — time constants (φ-scaled)

### Output Mapping

The step output maps internal state to protocol fields:

| Output Field | Derivation |
|--------------|------------|
| `coherence` | Direct from state.coherence |
| `stability` | 1.0 - state.instability |
| `intensity` | state.energy |
| `alignment` | (coherence + stability) / 2 |

All outputs are guaranteed in [0, 1].

---

## Configuration

`CFMCoreConfig` parameters:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `tau_energy` | float | φ | Energy relaxation time constant |
| `tau_instability` | float | φ² | Instability relaxation time constant |
| `omega_base` | float | 1/φ | Base phase frequency |
| `energy_target` | float | 1/φ | Energy attractor value |
| `instability_base` | float | 1/(2φ) | Base instability amplitude |
| `max_dt` | float | 1.0 | Maximum allowed time step |

All defaults are derived from φ, ψ, or simple fractions thereof.

---

## Protocol Conformance

CFM Core v0 implements `CFMCoreProtocol`:

```python
def step(
    self,
    human_messages: Optional[List[str]] = None,
    external_events: Optional[Dict[str, Any]] = None,
    dt: float = 1.0,
) -> Dict[str, Any]:
    ...
```

### Input Handling

- `human_messages`: **Ignored** — CFM Core v0 has no semantic processing
- `external_events`: **Ignored** — CFM Core v0 uses only internal dynamics
- `dt`: Clamped to [0, max_dt] and used for state evolution

### Output Schema

Returns a dict matching the CFM Core interface:

```python
{
    "coherence": float,      # [0, 1]
    "stability": float,      # [0, 1]
    "intensity": float,      # [0, 1]
    "alignment": float,      # [0, 1]
    # Optional metadata
    "cfm_time": float,       # Internal time
    "cfm_step": int,         # Step count
    "cfm_phase": float,      # Phase position [0, 1]
}
```

---

## Safety Constraints

### Identity Safety

- **No identity fields**: The core does not contain or access identity information
- **No identity derivation**: Outputs are pure functions of numeric state
- **Protocol compliance**: `verify_identity_safety()` always returns `True`

### Control Safety

- **No control signals**: Outputs are diagnostic only
- **No activation logic**: No connection to external control systems
- **No feedback paths**: Core does not receive shell state

### Semantic Safety

- **No text processing**: `human_messages` is ignored
- **No embeddings**: Core uses only scalar float state
- **No token handling**: Pure numeric dynamics

### Numeric Safety

- **Bounded outputs**: All values in [0, 1] via clamping
- **No NaN/Inf**: Safe arithmetic operations only
- **Deterministic**: Same inputs produce same outputs

---

## Adapter Compatibility

CFM Core v0 is designed for direct use with `CFMCoreAdapter`:

```python
from cfm_core_v0 import CFMCore, CFMCoreConfig
from cfm_interface import CFMCoreAdapter, CFMCoreInterfaceConfig

config = CFMCoreConfig()
core = CFMCore(config)

adapter_config = CFMCoreInterfaceConfig(enabled=True)
adapter = CFMCoreAdapter(core=core, config=adapter_config)

# Use standalone
result = adapter.step(dt=0.1)
```

No special adapter modifications are required.

---

## Differences from Mock Cores

| Aspect | MockCFMCore | CFMCore v0 |
|--------|-------------|------------|
| Dynamics | Simple sine waves | Coupled oscillator system |
| State | Time only | Full state vector |
| Physics | No attractor | φ-attractor dynamics |
| Purpose | Testing | CFM foundation |
| Determinism | Time-based | Step-based |

---

## Future Evolution

CFM Core v0 is a foundation for future development:

- **v0.x**: May add additional state variables
- **v1.x**: Enhanced dynamics with more interpretable trajectories (see [CFM Core v1 Specification](cfm_core_v1_spec.md))
- **Beyond**: May connect to CFM formal equations

All future versions must maintain:
- Protocol conformance
- Safety constraints
- Bounded outputs
- Determinism

---

## References

- [CFM Core v0 Tuning Guide](cfm_core_v0_tuning_guide.md) — Parameter tuning guidance
- [CFM Core v1 Specification](cfm_core_v1_spec.md) — Next version design
- `cfm_interface/protocols.py` — Protocol source
- `cfm_consts.py` — Mathematical constants

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 0.1 | 2025-12-05 | Initial specification |
