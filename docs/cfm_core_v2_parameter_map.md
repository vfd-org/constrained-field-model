# CFM Core v2 Parameter Map

**Version:** 1.1
**Status:** Updated with v2 Presets Section
**Last Updated:** 2025-12-05

---

## 1. Purpose

This document provides a structured template for mapping **observed CFM v1 behavioral metrics** to **CFM v2 parameter selections**. The tables and rules defined here will guide the implementation of v2 once v1 behavioral analysis is complete.

**Important:** The numeric values in this document are placeholders. They should be filled in after running the behavioral analysis pipeline described in [CFM Core v1 Behavioral Analysis Guide](cfm_core_v1_behavioral_analysis.md).

---

## 2. v1 Observed Metrics

### 2.1 Oscillation Ranges

| Metric | v1 Observed Min | v1 Observed Max | v1 Mean | v1 Std | Notes |
|--------|-----------------|-----------------|---------|--------|-------|
| coherence | _TBD_ | _TBD_ | _TBD_ | _TBD_ | |
| stability | _TBD_ | _TBD_ | _TBD_ | _TBD_ | |
| intensity | _TBD_ | _TBD_ | _TBD_ | _TBD_ | |
| alignment | _TBD_ | _TBD_ | _TBD_ | _TBD_ | |

### 2.2 Drift Characteristics

| Metric | v1 Drift Rate | v1 Convergence Time | v1 Final Value | Notes |
|--------|---------------|---------------------|----------------|-------|
| coherence | _TBD_ | _TBD_ steps | _TBD_ | |
| coherence_baseline | _TBD_ | _TBD_ steps | _TBD_ | |
| energy | _TBD_ | _TBD_ steps | _TBD_ | |
| alignment | _TBD_ | _TBD_ steps | _TBD_ | |

### 2.3 Regime Occupancy

| Regime | v1 Occupancy % | v1 Mean Duration | v1 Transition Rate | Notes |
|--------|----------------|------------------|-------------------|-------|
| High Stability [0.85, 1.0] | _TBD_ | _TBD_ steps | _TBD_ /1000 steps | |
| Stable [0.70, 0.85) | _TBD_ | _TBD_ steps | _TBD_ /1000 steps | |
| Transitional [0.50, 0.70) | _TBD_ | _TBD_ steps | _TBD_ /1000 steps | |
| Low Stability [0.30, 0.50) | _TBD_ | _TBD_ steps | _TBD_ /1000 steps | |
| Unstable [0.0, 0.30) | _TBD_ | _TBD_ steps | _TBD_ /1000 steps | |

### 2.4 Lock-In Statistics

| Metric | v1 Observed Value | Notes |
|--------|-------------------|-------|
| Lock-in events per 1000 steps | _TBD_ | |
| Mean lock-in duration | _TBD_ steps | |
| Max lock-in duration | _TBD_ steps | |
| Time in lock-in (%) | _TBD_ | |
| Lock-in stability (variance) | _TBD_ | |

### 2.5 Timescale Measurements

| Variable | v1 Observed Period | v1 Expected Period | Ratio | Notes |
|----------|-------------------|-------------------|-------|-------|
| coherence | _TBD_ | φ² ≈ 2.62 | _TBD_ | |
| stability | _TBD_ | φ⁻¹ ≈ 0.62 | _TBD_ | |
| phase_wrap | _TBD_ | 1/ω ≈ 1.62 | _TBD_ | |
| baseline_drift | _TBD_ | φ³ ≈ 4.24 | _TBD_ | |

### 2.6 Cross-Channel Correlations

| Variable Pair | v1 Correlation | Lag | Coupling Direction | Notes |
|---------------|----------------|-----|-------------------|-------|
| coherence ↔ stability | _TBD_ | _TBD_ | _TBD_ | |
| coherence ↔ intensity | _TBD_ | _TBD_ | _TBD_ | |
| stability ↔ alignment | _TBD_ | _TBD_ | _TBD_ | |
| energy ↔ coherence | _TBD_ | _TBD_ | _TBD_ | |
| phase ↔ alignment_phase | _TBD_ | _TBD_ | Expected: ψ | |

---

## 3. v2 Target Behaviors

### 3.1 Desired Oscillation Ranges

| Metric | v2 Target Min | v2 Target Max | v2 Target Mean | v2 Target Std |
|--------|---------------|---------------|----------------|---------------|
| coherence | > 0.1 | < 0.95 | ≈ φ⁻¹ | < 0.12 |
| stability | > 0.2 | < 0.98 | ≈ 1-φ⁻² | < 0.10 |
| intensity | > 0.1 | < 0.95 | ≈ φ⁻¹ | < 0.15 |
| alignment | > 0.2 | < 0.95 | ≈ φ⁻¹ | < 0.10 |

### 3.2 Desired Drift Characteristics

| Metric | v2 Target Drift Rate | v2 Target Convergence | v2 Target Final |
|--------|---------------------|----------------------|-----------------|
| coherence_slow | < 0.005/100 steps | < 2000 steps | ≈ coherence_target |
| coherence_fast | oscillatory | N/A | tracks slow |
| energy_potential | < 0.008/100 steps | < 1500 steps | ≈ energy_target |
| alignment_field | < 0.003/100 steps | variable | lock-in dependent |

### 3.3 Desired Regime Occupancy

| Regime | v2 Target Occupancy | Rationale |
|--------|---------------------|-----------|
| High Stability | 40-60% | Majority time in stable basin |
| Stable | 20-30% | Normal operating range |
| Transitional | 10-20% | Active dynamics |
| Low Stability | 5-10% | Brief excursions |
| Unstable | < 5% | Rare events only |

### 3.4 Desired Lock-In Behavior

| Metric | v2 Target | Rationale |
|--------|-----------|-----------|
| Lock-in events | 5-15 per 1000 steps | Regular but not constant |
| Mean duration | 50-200 steps | Sustained lock-in |
| Max duration | > 500 steps | Demonstrates stability |
| Time in lock-in | 30-50% | Significant but not dominant |

### 3.5 Desired Timescale Separation

| Tier | v2 Target τ | Separation Ratio | Variables |
|------|-------------|------------------|-----------|
| Very Slow | φ³ ≈ 4.24 | φ from Slow | alignment_direction |
| Slow | φ² ≈ 2.62 | φ² from Fast | coherence_slow, energy_potential, stability_envelope |
| Medium | φ ≈ 1.62 | φ from Fast | alignment_field, resonance_index |
| Fast | φ⁻¹ ≈ 0.62 | baseline | coherence_fast, energy_flux, instability_pulse, phase_global |
| Very Fast | φ⁻² ≈ 0.38 | φ⁻¹ from Fast | phase_local |

---

## 4. Parameter Mapping Rules

### 4.1 Coherence Parameters

| v1 Observation | Condition | v2 Parameter Adjustment |
|----------------|-----------|------------------------|
| Coherence drifts too slowly | drift_rate < 0.001/100 steps | Decrease τ_slow by factor φ⁻¹ |
| Coherence drifts too fast | drift_rate > 0.01/100 steps | Increase τ_slow by factor φ |
| Coherence oscillation too large | std > 0.15 | Increase damping, decrease coupling |
| Coherence oscillation too small | std < 0.02 | Decrease damping, increase coupling |
| Coherence doesn't converge | final_distance > 0.2 | Increase basin attraction strength |
| Coherence overshoots target | overshoot_count > 5/1000 | Increase damping coefficient |

### 4.2 Stability Parameters

| v1 Observation | Condition | v2 Parameter Adjustment |
|----------------|-----------|------------------------|
| Stability too constant | std < 0.03 | Increase instability_base |
| Stability too variable | std > 0.20 | Decrease instability_base |
| Rare high-stability regime | high_stab_occupancy < 30% | Increase stability_baseline |
| Too much instability | unstable_occupancy > 10% | Decrease instability_base, increase envelope recovery |
| Regime transitions too fast | transition_rate > 20/1000 | Increase τ_instability |
| Regime transitions too slow | transition_rate < 2/1000 | Decrease τ_instability |

### 4.3 Alignment Parameters

| v1 Observation | Condition | v2 Parameter Adjustment |
|----------------|-----------|------------------------|
| Lock-in never achieved | lock_in_events = 0 | Decrease alignment_lock_strength threshold |
| Lock-in too frequent | lock_in_events > 30/1000 | Increase alignment_lock_strength threshold |
| Lock-in duration too short | mean_duration < 20 steps | Increase lock_in stability factor |
| Lock-in duration too long | mean_duration > 500 steps | Decrease lock_in stability factor |
| Alignment collapses quickly | decay_rate > 0.1/step | Increase τ_alignment |
| Alignment too slow to build | rise_rate < 0.01/step | Decrease τ_alignment |

### 4.4 Energy Parameters

| v1 Observation | Condition | v2 Parameter Adjustment |
|----------------|-----------|------------------------|
| Energy converges too fast | convergence < 200 steps | Increase τ_energy |
| Energy converges too slow | convergence > 5000 steps | Decrease τ_energy |
| Energy-coherence coupling weak | correlation < 0.3 | Increase coherence_energy_coupling |
| Energy-coherence coupling strong | correlation > 0.8 | Decrease coherence_energy_coupling |

### 4.5 Phase Parameters

| v1 Observation | Condition | v2 Parameter Adjustment |
|----------------|-----------|------------------------|
| Phase velocity incorrect | |velocity - ω| > 0.1 | Adjust omega_phase |
| Phase-alignment phase ratio wrong | |ratio - ψ| > 0.2 | Adjust alignment_phase_velocity |
| Phase wrapping irregular | wrap_variance > 0.1 | Check numerical precision |

### 4.6 Cross-Channel Coupling

| v1 Observation | Condition | v2 Parameter Adjustment |
|----------------|-----------|------------------------|
| Coherence-stability decoupled | correlation < 0.2 | Increase stability_coherence_coupling |
| Coherence-stability over-coupled | correlation > 0.9 | Decrease stability_coherence_coupling |
| Poor resonance | resonance_index < 0.3 | Increase cross-channel coupling strengths |
| Excessive resonance | resonance_index > 0.9 | Decrease cross-channel coupling strengths |

---

## 5. Using Presets as Starting Points

CFM Core v2 provides named presets that serve as pre-tuned parameter configurations for common behavioral profiles. These presets can be used as starting points for further tuning.

### 5.1 Available Presets

| Preset | Primary Behavior | Use Case |
|--------|------------------|----------|
| `baseline` | Default φ-derived parameters | Reference configuration, general use |
| `high_stability` | Higher stability, reduced oscillation | Systems requiring stable convergence |
| `high_resonance` | Strong cross-channel coupling | Systems requiring coordinated dynamics |
| `pulsed_activity` | More frequent instability pulses | Systems requiring dynamic variability |

### 5.2 Preset Selection Guidelines

| v1 Observation | Recommended Preset |
|----------------|-------------------|
| High stability regime occupancy < 30% | `high_stability` |
| Stability variance > 0.15 | `high_stability` |
| Resonance index consistently < 0.4 | `high_resonance` |
| Channels appear decoupled (correlation < 0.3) | `high_resonance` |
| Intensity variance < 0.05 | `pulsed_activity` |
| System too predictable (low dynamism) | `pulsed_activity` |
| Balanced dynamics desired | `baseline` |

### 5.3 Preset-Based Tuning Workflow

```
1. Run v1 behavioral analysis
2. Identify primary behavioral issue (stability, resonance, dynamism)
3. Select appropriate preset as starting configuration
4. Run v2 with selected preset
5. Compare v2 behavior to targets
6. If further adjustment needed, modify individual parameters from preset base
```

### 5.4 Importing Presets

```python
from cfm_core_v2 import CFMCoreV2, get_preset, CFM_V2_PRESETS

# Using get_preset function
config = get_preset("high_stability")
core = CFMCoreV2(config)

# Using preset constants directly
from cfm_core_v2 import CFM_V2_PRESET_HIGH_RESONANCE
core = CFMCoreV2(CFM_V2_PRESET_HIGH_RESONANCE)

# Listing available presets
from cfm_core_v2 import list_presets
print(list_presets())  # ['baseline', 'high_stability', 'high_resonance', 'pulsed_activity']
```

### 5.5 Modifying Presets

Presets can be used as templates for custom configurations:

```python
from cfm_core_v2 import CFMCoreV2Config, CFM_V2_PRESET_HIGH_STABILITY
from cfm_consts import PHI

# Start from high_stability preset values and adjust
custom_config = CFMCoreV2Config(
    # Copy from high_stability
    stability_target=CFM_V2_PRESET_HIGH_STABILITY.stability_target,
    instability_base=CFM_V2_PRESET_HIGH_STABILITY.instability_base,
    # Custom adjustment
    resonance_coupling=1.0 / PHI,  # Increase resonance
)
```

---

## 6. φ-Derived Tuning Factors

### 6.1 Standard Adjustment Factors

| Factor Name | Value | Use Case |
|-------------|-------|----------|
| φ_boost | φ ≈ 1.618 | Increase time constant, strengthen effect |
| φ_reduce | φ⁻¹ ≈ 0.618 | Decrease time constant, weaken effect |
| φ²_boost | φ² ≈ 2.618 | Strong increase |
| φ²_reduce | φ⁻² ≈ 0.382 | Strong decrease |
| ψ_factor | ψ ≈ 1.325 | Phase relationship adjustments |

### 6.2 Adjustment Application

When an adjustment is needed:

```
new_parameter = old_parameter × adjustment_factor

Examples:
- τ_slow too fast: new_τ_slow = old_τ_slow × φ
- coupling too weak: new_coupling = old_coupling × φ
- damping insufficient: new_damping = old_damping × φ²
```

### 6.3 Iterative Refinement

```
1. Run v1 analysis, fill observed metrics tables
2. Compare observed vs target for each metric
3. Apply mapping rules to identify adjustments
4. Compute v2 parameters using adjustment factors
5. Implement v2 with derived parameters
6. Run v2 analysis
7. If targets not met, iterate (smaller adjustment factors)
```

---

## 7. Parameter Summary Tables

### 7.1 v2 Time Constants (To Be Derived)

| Parameter | v1 Equivalent | v1 Observed | v2 Target | Adjustment Factor | v2 Derived |
|-----------|---------------|-------------|-----------|-------------------|------------|
| τ_very_slow | τ_coherence × φ | _TBD_ | φ³ | _TBD_ | _TBD_ |
| τ_slow | τ_coherence | _TBD_ | φ² | _TBD_ | _TBD_ |
| τ_medium | new | N/A | φ | baseline | φ |
| τ_fast | τ_instability | _TBD_ | φ⁻¹ | _TBD_ | _TBD_ |
| τ_very_fast | new | N/A | φ⁻² | baseline | φ⁻² |

### 7.2 v2 Attractor Parameters (To Be Derived)

| Parameter | v1 Equivalent | v1 Observed | v2 Target | v2 Derived |
|-----------|---------------|-------------|-----------|------------|
| μ_basin.c | coherence_target | _TBD_ | ≈ 0.718 | _TBD_ |
| μ_basin.e | energy_target | _TBD_ | ≈ 0.618 | _TBD_ |
| μ_basin.s | stability_baseline | _TBD_ | ≈ 0.8 | _TBD_ |
| r_basin | coherence_range | _TBD_ | ≈ 0.38 | _TBD_ |
| k_attraction | N/A | N/A | _TBD_ | _TBD_ |

### 7.3 v2 Coupling Strengths (To Be Derived)

| Parameter | v1 Equivalent | v1 Observed Correlation | v2 Target | v2 Derived |
|-----------|---------------|------------------------|-----------|------------|
| coherence_stability_coupling | implicit | _TBD_ | 0.5-0.7 | _TBD_ |
| coherence_energy_coupling | implicit | _TBD_ | 0.4-0.6 | _TBD_ |
| stability_alignment_coupling | alignment_lock_strength | _TBD_ | 0.5-0.7 | _TBD_ |
| resonance_coupling | N/A | N/A | 0.3-0.5 | _TBD_ |

---

## 8. Analysis Workflow

### 8.1 Data Collection Checklist

- [ ] Run 10,000+ step v1 simulation
- [ ] Extract oscillation ranges for all metrics
- [ ] Compute drift rates and convergence times
- [ ] Measure regime occupancy percentages
- [ ] Count and characterize lock-in events
- [ ] Estimate dominant periods for each variable
- [ ] Compute cross-channel correlations

### 8.2 Table Population Checklist

- [ ] Fill Section 2.1 (Oscillation Ranges)
- [ ] Fill Section 2.2 (Drift Characteristics)
- [ ] Fill Section 2.3 (Regime Occupancy)
- [ ] Fill Section 2.4 (Lock-In Statistics)
- [ ] Fill Section 2.5 (Timescale Measurements)
- [ ] Fill Section 2.6 (Cross-Channel Correlations)

### 8.3 Parameter Derivation Checklist

- [ ] Apply mapping rules from Section 4
- [ ] Consider using presets from Section 5 as starting points
- [ ] Compute adjustment factors
- [ ] Fill Section 7.1 (Time Constants)
- [ ] Fill Section 7.2 (Attractor Parameters)
- [ ] Fill Section 7.3 (Coupling Strengths)
- [ ] Document any anomalies or special cases

### 8.4 Validation Checklist

- [ ] Verify all derived parameters are physically reasonable
- [ ] Check timescale hierarchy is preserved (τ_vs > τ_s > τ_m > τ_f > τ_vf)
- [ ] Confirm coupling strengths are in [0, 1]
- [ ] Ensure attractor parameters are consistent with CFM theory

---

## 9. References

- [CFM Core v1 Specification](cfm_core_v1_spec.md)
- [CFM Core v1 Behavioral Analysis Guide](cfm_core_v1_behavioral_analysis.md)
- [CFM Core v2 Specification](cfm_core_v2_spec.md)
- [CFM Core v2 Behavioral Analysis Guide](cfm_core_v2_behavioral_analysis.md)
