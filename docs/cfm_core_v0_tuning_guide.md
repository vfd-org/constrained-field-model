# CFM Core v0 Tuning Guide

**Version:** 1.0
**Last Updated:** 2025-12-05

---

## Overview

This guide explains how to tune CFM Core v0's configuration parameters to achieve different dynamic behaviors. CFM Core v0 is a **pure numeric dynamical system** that produces bounded outputs in [0, 1] based on φ/ψ-coupled oscillator dynamics.

All tuning affects only the numeric behavior — no semantic, identity, or control aspects are modified.

---

## Default Configuration

The default configuration uses φ (golden ratio) and ψ (1/φ) derived values:

| Parameter | Default | Value |
|-----------|---------|-------|
| `tau_energy` | φ | ≈ 1.618 |
| `tau_instability` | φ² | ≈ 2.618 |
| `omega_base` | 1/φ | ≈ 0.618 |
| `energy_target` | 1/φ | ≈ 0.618 |
| `instability_base` | 1/(2φ) | ≈ 0.309 |
| `max_dt` | 1.0 | 1.0 |

These defaults produce smooth, stable dynamics with natural φ-proportioned relationships.

---

## Parameter Effects

### `tau_energy` — Energy Relaxation Time Constant

Controls how quickly energy converges to its target attractor.

| Value | Effect |
|-------|--------|
| **Smaller** (< 1.0) | Faster energy convergence, more responsive |
| **Default** (φ) | Balanced response, φ-natural decay |
| **Larger** (> 2.0) | Slower energy convergence, more inertia |

**Tuning Guidance:**
- Use smaller values (0.5–1.0) for faster-responding systems
- Use larger values (2.0–5.0) for smoother, more damped behavior
- Minimum practical value: ~0.1 (very fast response)

**Example:**
```python
from cfm_core_v0 import CFMCore, CFMCoreConfig

# Fast-responding energy dynamics
config = CFMCoreConfig(tau_energy=0.5)
core = CFMCore(config)
```

---

### `tau_instability` — Instability Relaxation Time Constant

Controls how quickly instability oscillations decay.

| Value | Effect |
|-------|--------|
| **Smaller** (< φ) | Faster instability decay, more stable |
| **Default** (φ²) | Natural oscillation decay |
| **Larger** (> 3.0) | Slower decay, sustained oscillations |

**Tuning Guidance:**
- Use smaller values (0.5–1.5) for quickly damped oscillations
- Use larger values (3.0–6.0) for more sustained instability variations
- This parameter interacts with ψ in the dynamics (τ_instability/ψ)

**Example:**
```python
# Quickly damped instability
config = CFMCoreConfig(tau_instability=1.0)
core = CFMCore(config)

# Sustained oscillations
config = CFMCoreConfig(tau_instability=5.0)
core = CFMCore(config)
```

---

### `omega_base` — Base Phase Frequency

Controls the fundamental oscillation frequency of the phase variable.

| Value | Effect |
|-------|--------|
| **Smaller** (< 0.3) | Slower oscillation, longer periods |
| **Default** (1/φ) | Natural φ-period oscillation |
| **Larger** (> 1.0) | Faster oscillation, shorter periods |

**Tuning Guidance:**
- Phase wraps at 1.0, so frequency determines cycle time
- With dt=0.1, default ω_base produces ~16 steps per cycle
- Use smaller values (0.1–0.3) for slow, smooth variations
- Use larger values (1.0–2.0) for rapid cycling

**Example:**
```python
# Slow oscillation (longer periods)
config = CFMCoreConfig(omega_base=0.2)
core = CFMCore(config)

# Fast oscillation (shorter periods)
config = CFMCoreConfig(omega_base=1.5)
core = CFMCore(config)
```

**Relationship to dt:**
- Period (in steps) ≈ 1 / (ω_base × dt)
- For dt=0.1 and ω_base=0.618: period ≈ 16 steps

---

### `energy_target` — Energy Attractor Value

Sets the target value that energy converges toward.

| Value | Range | Effect |
|-------|-------|--------|
| **Lower** | 0.3–0.5 | Lower mean energy, lower intensity output |
| **Default** | 1/φ ≈ 0.618 | Moderate energy level |
| **Higher** | 0.7–0.9 | Higher mean energy, higher intensity output |

**Tuning Guidance:**
- This directly affects the `intensity` output (intensity = energy)
- Also indirectly affects `coherence` (coherence ∝ energy^(1/φ))
- Valid range: [0, 1] (clamped if outside)

**Example:**
```python
# Low energy system
config = CFMCoreConfig(energy_target=0.4)
core = CFMCore(config)

# High energy system
config = CFMCoreConfig(energy_target=0.85)
core = CFMCore(config)
```

---

### `instability_base` — Base Instability Amplitude

Controls the amplitude of instability oscillations.

| Value | Range | Effect |
|-------|-------|--------|
| **Lower** | 0.1–0.2 | Smaller instability variations, more stable |
| **Default** | 1/(2φ) ≈ 0.309 | Moderate oscillation amplitude |
| **Higher** | 0.4–0.5 | Larger instability variations, less stable |

**Tuning Guidance:**
- Instability is driven by `instability_base × sin(2π × phase)`
- Higher values produce larger stability variations
- Stability output = 1 - instability, so high instability = low stability
- Valid range: [0, 0.5] (clamped if outside)

**Example:**
```python
# Very stable (small oscillations)
config = CFMCoreConfig(instability_base=0.1)
core = CFMCore(config)

# More variable (larger oscillations)
config = CFMCoreConfig(instability_base=0.45)
core = CFMCore(config)
```

---

### `max_dt` — Maximum Time Step

Limits the maximum allowed dt value passed to step().

| Value | Effect |
|-------|--------|
| **Smaller** (< 0.5) | Stricter limit, prevents large jumps |
| **Default** (1.0) | Allows moderate time steps |
| **Larger** (> 1.0) | Allows larger time steps |

**Tuning Guidance:**
- Primarily a safety parameter to prevent numerical instability
- For fine-grained dynamics, use smaller max_dt
- Values > 2.0 may cause visible discrete jumps

---

## Tuning Recipes

### Recipe 1: High Stability System

For a system with minimal instability variations and smooth outputs:

```python
config = CFMCoreConfig(
    tau_energy=2.0,            # Slower energy response
    tau_instability=1.0,       # Fast instability decay
    omega_base=0.3,            # Slow oscillation
    energy_target=0.7,         # Moderate-high energy
    instability_base=0.15,     # Small oscillations
)
core = CFMCore(config)
```

**Expected behavior:**
- Stability remains high (0.85–0.95)
- Coherence remains high (0.7–0.85)
- Smooth, slowly-varying outputs

---

### Recipe 2: Dynamic Oscillator

For a system with pronounced oscillations:

```python
config = CFMCoreConfig(
    tau_energy=1.0,            # Responsive energy
    tau_instability=4.0,       # Sustained instability
    omega_base=1.0,            # Faster oscillation
    energy_target=0.618,       # Default energy
    instability_base=0.4,      # Larger amplitude
)
core = CFMCore(config)
```

**Expected behavior:**
- Visible stability oscillations
- Coherence varies with stability
- More dynamic, varied outputs

---

### Recipe 3: Low Energy / Subdued System

For a lower-energy system:

```python
config = CFMCoreConfig(
    tau_energy=3.0,            # Very slow energy
    tau_instability=2.618,     # Default
    omega_base=0.618,          # Default
    energy_target=0.35,        # Low energy target
    instability_base=0.2,      # Moderate stability
)
core = CFMCore(config)
```

**Expected behavior:**
- Lower mean intensity (0.3–0.4)
- Lower mean coherence
- Subdued overall dynamics

---

### Recipe 4: Fast Response System

For a system that responds quickly to time steps:

```python
config = CFMCoreConfig(
    tau_energy=0.3,            # Very fast energy
    tau_instability=0.5,       # Very fast decay
    omega_base=0.618,          # Default frequency
    energy_target=0.618,       # Default energy
    instability_base=0.309,    # Default amplitude
)
core = CFMCore(config)
```

**Expected behavior:**
- Quick convergence to attractors
- Rapidly damped oscillations
- Fast response to dt changes

---

## Using Custom Initial State

Beyond configuration, you can also set custom initial state:

```python
from cfm_core_v0 import CFMCore, CFMCoreConfig, CFMCoreState

config = CFMCoreConfig()
initial_state = CFMCoreState(
    coherence=0.8,      # Start with high coherence
    instability=0.1,    # Start with low instability
    energy=0.9,         # Start with high energy
    phase=0.0,          # Start at phase 0
)

core = CFMCore(config, initial_state=initial_state)
```

This is useful for:
- Starting from specific known states
- Resuming from saved state
- Testing specific scenarios

---

## Comparing Configurations

Use the CLI tools to compare different configurations:

```bash
# Run the default CFM core
python tools/cfm_local_loop.py --steps 100 --core-type=cfm --output-json default.json

# Modify config, then run again
python tools/cfm_local_loop.py --steps 100 --core-type=cfm --output-json modified.json

# Extract fingerprints and compare
python tools/cfm_fingerprint.py --input default.json --output fp1.json
python tools/cfm_fingerprint.py --input modified.json --output fp2.json
python tools/cfm_fingerprint.py --compare fp1.json fp2.json
```

Or programmatically:

```python
from cfm_core_v0 import CFMCore, CFMCoreConfig

# Create two cores with different configs
config_a = CFMCoreConfig(tau_energy=1.0)
config_b = CFMCoreConfig(tau_energy=3.0)

core_a = CFMCore(config_a)
core_b = CFMCore(config_b)

# Run and compare
for step in range(20):
    result_a = core_a.step(dt=0.1)
    result_b = core_b.step(dt=0.1)

    diff = abs(result_a["intensity"] - result_b["intensity"])
    print(f"Step {step}: intensity diff = {diff:.4f}")
```

---

## Interpreting Statistics

When analyzing tuned core outputs, look for:

### Mean Values

| Metric | Healthy Range | Notes |
|--------|---------------|-------|
| coherence | 0.4–0.8 | Higher with high energy, low instability |
| stability | 0.6–0.9 | 1 - mean(instability) |
| intensity | near energy_target | Should converge toward target |
| alignment | 0.5–0.8 | Average of coherence and stability |

### Min/Max Spread

| Spread | Indicates |
|--------|-----------|
| Narrow (< 0.1) | Very stable, possibly static |
| Moderate (0.1–0.3) | Normal dynamic range |
| Wide (> 0.3) | High variability, may indicate stress |

---

## Bounds Verification

All CFM Core v0 outputs are guaranteed in [0, 1] regardless of configuration. If you observe values outside this range, there is a bug.

Use the `verify_state_bounds()` method to check internal state:

```python
core = CFMCore(config)
for _ in range(100):
    core.step(dt=0.1)

is_valid = core.verify_state_bounds()
print(f"State valid: {is_valid}")
```

---

## Related Documentation

- [CFM Core v0 Specification](cfm_core_v0_spec.md) — Technical specification
- [CFM Core v1 Specification](cfm_core_v1_spec.md) — Next version design

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-12-05 | Initial tuning guide |
