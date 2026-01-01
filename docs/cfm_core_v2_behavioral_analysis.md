# CFM Core v2 Behavioral Analysis Guide

**Version:** 1.0
**Status:** Analysis Framework
**Last Updated:** 2025-12-05

---

## 1. Purpose

This document defines the methodology for extracting **long-run behavioral baselines** from CFM Core v2. Unlike v1's simpler architecture, v2 introduces a multi-channel structure with 11 internal state variables, requiring channel-aware analysis techniques.

The analysis results will:

1. Characterize v2's multi-channel dynamic fingerprint
2. Enable comparison against v0, v1, and mock cores
3. Validate the five-tier timescale hierarchy
4. Guide preset configuration selection
5. Identify healthy vs anomalous operational regimes

---

## 2. CFM v2 Architecture Summary

### 2.1 Five Channels

| Channel | Variables | Timescales | Purpose |
|---------|-----------|------------|---------|
| **Coherence** | `coherence_slow`, `coherence_fast` | τ_slow, τ_fast | Baseline coherence + fluctuations |
| **Energy** | `energy_potential`, `energy_flux` | τ_slow, τ_fast | Stored activation + flow rate |
| **Stability** | `stability_envelope`, `instability_pulse` | τ_slow, τ_fast | Stability boundary + pulse events |
| **Phase** | `phase_global`, `phase_local` | τ_fast, τ_very_fast | Global + local oscillation phases |
| **Alignment** | `alignment_field`, `alignment_direction` | τ_medium, τ_very_slow | Field strength + attractor direction |

Plus: `resonance_index` (τ_medium) — cross-channel coupling strength

### 2.2 Five-Tier Timescale Hierarchy

| Tier | Time Constant | Value | Variables |
|------|---------------|-------|-----------|
| Very Slow | τ_vs | φ³ ≈ 4.24 | alignment_direction |
| Slow | τ_s | φ² ≈ 2.62 | coherence_slow, energy_potential, stability_envelope |
| Medium | τ_m | φ ≈ 1.62 | alignment_field, resonance_index |
| Fast | τ_f | φ⁻¹ ≈ 0.62 | coherence_fast, energy_flux, instability_pulse, phase_global |
| Very Fast | τ_vf | φ⁻² ≈ 0.38 | phase_local |

### 2.3 Attractor Basin

The system has a 3D attractor basin in (coherence, energy, stability) space:

- **Basin Center**: (φ⁻¹, φ⁻¹, 1−φ⁻²) ≈ (0.618, 0.618, 0.618)
- **Basin Radius**: φ⁻² ≈ 0.38
- **Inner Zone**: Strong linear attraction
- **Outer Shell**: Weak attraction
- **Outside Basin**: No attraction

### 2.4 Instability Pulse System

Pulses are phase-driven events that cascade through channels:

| Pulse Level | Threshold | Effect |
|-------------|-----------|--------|
| Weak | > θ_low (≈0.38) | Only coherence_fast affected |
| Moderate | > θ_medium (≈0.62) | All fast channels affected |
| Strong | > θ_high (≈0.62) | All channels including slow |

---

## 3. Running v2 Simulations

### 3.1 Recommended Run Lengths

| Run Type | Steps | Approximate Time | Purpose |
|----------|-------|------------------|---------|
| Quick validation | 500 | ~2 seconds | Bounds check, basic trajectory |
| Short baseline | 2,000 | ~5 seconds | Initial channel characterization |
| Medium baseline | 5,000 | ~12 seconds | Regime identification, pulse analysis |
| Long baseline | 20,000 | ~45 seconds | Full timescale separation validation |
| Extended baseline | 50,000 | ~2 minutes | Complete fingerprint extraction |
| Stress test | 100,000 | ~4 minutes | Long-term stability verification |

**Note**: v2's slower timescales (τ_very_slow ≈ 4.24) require longer runs than v1 to observe full dynamics.

### 3.2 Using cfm_local_loop

```bash
# Quick validation
python tools/cfm_local_loop.py --steps 500 --core-type=cfm_v2 --output-json v2_quick.json

# Short baseline
python tools/cfm_local_loop.py --steps 2000 --core-type=cfm_v2 --output-json v2_short.json

# Medium baseline (recommended starting point)
python tools/cfm_local_loop.py --steps 5000 --core-type=cfm_v2 --output-json v2_medium.json

# Long baseline
python tools/cfm_local_loop.py --steps 20000 --core-type=cfm_v2 --output-json v2_long.json

# Extended baseline (full fingerprint)
python tools/cfm_local_loop.py --steps 50000 --core-type=cfm_v2 --output-json v2_extended.json
```

### 3.3 Using cfm_fingerprint

For fingerprint extraction and comparison:

```bash
# Extract fingerprint from run output
python tools/cfm_fingerprint.py --input v2_medium.json --output fp_v2.json

# Compare two fingerprints
python tools/cfm_fingerprint.py --compare fp_v1.json fp_v2.json
```

---

## 4. Channel-Aware Metrics

### 4.1 Coherence Channel Metrics

**Slow Variable (coherence_slow)**:
- Long-term drift rate toward `coherence_target`
- Basin occupancy: time spent within basin radius of center
- Convergence time to target
- Final value stability (variance in last 10% of run)

**Fast Variable (coherence_fast)**:
- Tracking fidelity: correlation with coherence_slow
- Phase-modulated oscillation amplitude
- Resonance-coupled variations

**Output Coherence** (blended):
- Mean and standard deviation
- Range (max - min)
- Stability-weighted blend behavior

| Metric | Expected Healthy Range | Warning Signs |
|--------|------------------------|---------------|
| coherence_slow drift rate | < 0.005/100 steps | > 0.02/100 steps |
| coherence_slow final | 0.6 - 0.8 | < 0.4 or > 0.95 |
| coherence_fast variance | 0.01 - 0.08 | < 0.001 or > 0.15 |
| output coherence mean | 0.5 - 0.8 | < 0.3 or > 0.95 |

### 4.2 Energy Channel Metrics

**Potential (energy_potential)**:
- Convergence to `energy_target`
- Dissipation rate effectiveness
- Coherence-coupling influence

**Flux (energy_flux)**:
- Phase-driven activation cycles
- Mean flux level during active periods
- Saturation frequency (time near max)

| Metric | Expected Healthy Range | Warning Signs |
|--------|------------------------|---------------|
| energy_potential final | 0.5 - 0.75 | < 0.3 or > 0.9 |
| energy_flux mean | 0.1 - 0.4 | > 0.6 (over-activation) |
| flux saturation time | < 5% | > 20% |
| potential-flux correlation | 0.2 - 0.6 | < 0.1 or > 0.8 |

### 4.3 Stability Channel Metrics

**Envelope (stability_envelope)**:
- Mean stability level
- Regime occupancy (time in each stability band)
- Recovery rate after instability events

**Instability Pulse**:
- Pulse frequency (events per 1000 steps)
- Mean pulse duration
- Peak amplitude distribution
- Recovery time after each pulse

| Regime | Stability Range | Target Occupancy |
|--------|-----------------|------------------|
| High Stability | [0.75, 1.0] | 40-60% |
| Active | [0.50, 0.75) | 25-35% |
| Transitional | [0.30, 0.50) | 10-20% |
| Recovery | [0.10, 0.30) | 5-10% |
| Unstable | [0.0, 0.10) | < 5% |

| Metric | Expected Healthy Range | Warning Signs |
|--------|------------------------|---------------|
| pulse frequency | 5-20 per 1000 steps | > 40 (chaotic) or 0 (frozen) |
| mean pulse duration | 10-50 steps | > 100 (stuck) or < 3 (erratic) |
| peak amplitude | 0.2 - 0.5 | > 0.8 (severe) |
| recovery time | 20-80 steps | > 200 (slow) |

### 4.4 Phase Channel Metrics

**Global Phase (phase_global)**:
- Phase velocity (should be ≈ ω_global / τ_fast)
- Wrap frequency (transitions from ~1.0 to ~0.0)
- Regularity (variance of wrap intervals)

**Local Phase (phase_local)**:
- Phase velocity ratio to global (expected: faster)
- Global-modulated behavior verification
- Coupling strength with global phase

| Metric | Expected Healthy Range | Warning Signs |
|--------|------------------------|---------------|
| global velocity | 0.05 - 0.15 per step | < 0.02 or > 0.25 |
| local/global velocity ratio | 1.2 - 2.0 | < 1.0 (hierarchy failure) |
| wrap regularity (std) | < 0.2 | > 0.5 (irregular) |
| global-local phase coherence | 0.3 - 0.7 | < 0.1 (decoupled) |

### 4.5 Alignment Channel Metrics

**Field (alignment_field)**:
- Lock-in frequency (entries above threshold)
- Lock-in dwell time (duration above threshold)
- Lock-in stability (variance during lock-in)
- Build-up rate (rise rate to lock-in)

**Direction (alignment_direction)**:
- Drift rate (should be very slow)
- Basin-center convergence
- Stability-modulated behavior

| Metric | Expected Healthy Range | Warning Signs |
|--------|------------------------|---------------|
| lock-in events | 3-15 per 1000 steps | 0 (never) or > 30 (too easy) |
| mean lock-in duration | 30-200 steps | < 10 (unstable) or > 500 (stuck) |
| lock-in percentage | 25-50% | < 10% or > 80% |
| direction drift | < 0.001/100 steps | > 0.01 (too fast) |

### 4.6 Resonance Index Metrics

The resonance_index captures cross-channel coupling strength:

- Mean level (overall coupling)
- Correlation with each channel
- Variation pattern (oscillatory vs stable)

| Metric | Expected Healthy Range | Warning Signs |
|--------|------------------------|---------------|
| mean resonance_index | 0.4 - 0.7 | < 0.2 (decoupled) or > 0.9 (over-coupled) |
| resonance-stability correlation | 0.3 - 0.6 | < 0.1 (independent) |
| resonance-alignment correlation | 0.2 - 0.5 | > 0.8 (locked together) |

---

## 5. The CFM v2 Fingerprint

### 5.1 Fingerprint Schema

```json
{
  "fingerprint_version": "2.0",
  "core_type": "cfm_v2",
  "run_parameters": {
    "steps": 20000,
    "dt": 0.1,
    "config_preset": "BASELINE"
  },

  "regime_occupancy": {
    "high_stability": { "percentage": 0.0, "mean_duration": 0, "transitions_in": 0 },
    "active": { "percentage": 0.0, "mean_duration": 0, "transitions_in": 0 },
    "transitional": { "percentage": 0.0, "mean_duration": 0, "transitions_in": 0 },
    "recovery": { "percentage": 0.0, "mean_duration": 0, "transitions_in": 0 },
    "unstable": { "percentage": 0.0, "mean_duration": 0, "transitions_in": 0 }
  },

  "pulse_signatures": {
    "total_events": 0,
    "frequency_per_1000": 0.0,
    "mean_amplitude": 0.0,
    "max_amplitude": 0.0,
    "mean_duration": 0,
    "recovery_time_mean": 0,
    "weak_count": 0,
    "moderate_count": 0,
    "strong_count": 0
  },

  "channel_envelopes": {
    "coherence": { "min": 0.0, "max": 1.0, "mean": 0.0, "std": 0.0, "final": 0.0 },
    "energy": { "min": 0.0, "max": 1.0, "mean": 0.0, "std": 0.0, "final": 0.0 },
    "stability": { "min": 0.0, "max": 1.0, "mean": 0.0, "std": 0.0, "final": 0.0 },
    "alignment": { "min": 0.0, "max": 1.0, "mean": 0.0, "std": 0.0, "final": 0.0 },
    "resonance_index": { "min": 0.0, "max": 1.0, "mean": 0.0, "std": 0.0, "final": 0.0 }
  },

  "cross_channel_correlations": {
    "coherence_stability": 0.0,
    "coherence_energy": 0.0,
    "stability_alignment": 0.0,
    "energy_stability": 0.0,
    "resonance_stability": 0.0,
    "resonance_alignment": 0.0,
    "phase_global_local": 0.0
  },

  "timescale_separation": {
    "slow_fast_ratio": 0.0,
    "medium_fast_ratio": 0.0,
    "very_slow_slow_ratio": 0.0,
    "hierarchy_intact": true
  },

  "lock_in_statistics": {
    "events": 0,
    "frequency_per_1000": 0.0,
    "mean_duration": 0,
    "max_duration": 0,
    "time_in_lock_in_percent": 0.0,
    "stability_during_lock_in": 0.0
  },

  "basin_dynamics": {
    "time_in_basin_percent": 0.0,
    "mean_distance_to_center": 0.0,
    "excursion_count": 0,
    "mean_excursion_duration": 0
  }
}
```

### 5.2 Regime Classification

| Regime | Characteristics | Healthy Duration |
|--------|-----------------|------------------|
| **High Stability** | stability > 0.75, low pulse activity, strong lock-in | 40-60% of time |
| **Active** | stability 0.50-0.75, moderate dynamics, some pulses | 25-35% of time |
| **Transitional** | stability 0.30-0.50, frequent channel coupling, building/decaying | 10-20% of time |
| **Recovery** | stability 0.10-0.30, post-pulse recovery, rebuilding coherence | 5-10% of time |
| **Unstable** | stability < 0.10, strong pulses, channel disruption | < 5% of time |

### 5.3 Pulse Signature Interpretation

| Signature Type | Characteristics | Indication |
|----------------|-----------------|------------|
| **Regular pulses** | Even spacing, consistent amplitude | Healthy rhythm |
| **Clustered pulses** | Groups followed by quiet periods | Bursty dynamics |
| **Escalating pulses** | Increasing amplitude over time | Potential instability |
| **Rare strong pulses** | Infrequent but high-amplitude | Punctuated equilibrium |
| **Continuous low pulses** | High frequency, low amplitude | Over-sensitive system |

---

## 6. Anomaly Detection

### 6.1 Overly Chaotic Regimes

**Symptoms:**
- Regime transition rate > 25/1000 steps
- Time in high_stability < 25%
- Basin occupancy < 30%
- Pulse frequency > 40/1000 steps
- High variance in all channels

**Detection Criteria:**
```
chaotic = (
    regime_transition_rate > 25/1000
    AND high_stability_occupancy < 0.25
    AND basin_occupancy < 0.30
)
```

**Response:**
- Use HIGH_STABILITY preset
- Increase basin_strength_inner
- Decrease instability_base
- Increase τ_slow variables

### 6.2 Overly Frozen Regimes

**Symptoms:**
- Regime transition rate < 2/1000 steps
- Time in single regime > 90%
- Near-zero variance in slow variables
- No lock-in events or continuous lock-in
- Pulse frequency < 1/1000 steps

**Detection Criteria:**
```
frozen = (
    regime_transition_rate < 2/1000
    AND single_regime_occupancy > 0.90
    AND coherence_slow_variance < 0.001
)
```

**Response:**
- Use PULSED_ACTIVITY preset
- Increase instability_base
- Decrease basin_strength parameters
- Reduce alignment_lock_strength

### 6.3 Timescale Separation Failures

**Symptoms:**
- Fast variables evolve at similar rate to slow variables
- phase_local not clearly faster than phase_global
- coherence_fast variance similar to coherence_slow
- alignment_direction changes as fast as alignment_field

**Detection Criteria:**
```
timescale_failure = (
    |coherence_fast_var / coherence_slow_var - φ²| > 1.0
    OR local_phase_velocity / global_phase_velocity < 1.2
    OR direction_change_rate > field_change_rate * 0.5
)
```

**Response:**
- Verify τ hierarchy in config
- Check that τ_very_slow > τ_slow > τ_medium > τ_fast > τ_very_fast
- Consider adjusting timescale ratios

### 6.4 Pulse-Recovery Mismatch

**Symptoms:**
- Pulses not followed by recovery period
- Stability doesn't decrease during pulses
- Recovery time exceeds 5× expected
- Pulse amplitude doesn't affect channel states

**Detection Criteria:**
```
pulse_recovery_mismatch = (
    mean_recovery_time > 5 * expected_recovery
    OR stability_during_pulse > stability_target * 0.9
    OR pulse_amplitude_effect < 0.1
)
```

**Response:**
- Check pulse_threshold values
- Verify envelope_decay rate
- Review pulse response cascade logic

### 6.5 Cross-Channel Decoupling

**Symptoms:**
- Low correlations between related channels
- resonance_index near constant
- Energy-coherence coupling < 0.2
- Stability-alignment coupling < 0.2

**Detection Criteria:**
```
decoupled = (
    coherence_energy_correlation < 0.2
    AND stability_alignment_correlation < 0.2
    AND resonance_variance < 0.01
)
```

**Response:**
- Use HIGH_RESONANCE preset
- Increase cross-channel coupling parameters
- Verify resonance_coupling value

### 6.6 Anomaly Summary Table

| Anomaly | Key Indicator | Severity | Recommended Preset |
|---------|---------------|----------|-------------------|
| Chaotic | High transition rate | High | HIGH_STABILITY |
| Frozen | Near-zero dynamics | Medium | PULSED_ACTIVITY |
| Timescale failure | Wrong speed ratios | High | BASELINE (check config) |
| Pulse-recovery mismatch | No recovery | Medium | Check thresholds |
| Decoupled | Low correlations | Medium | HIGH_RESONANCE |

---

## 7. Feeding Results into Parameter Selection

### 7.1 Preset Selection Guide

| Observation | Recommended Preset | Rationale |
|-------------|-------------------|-----------|
| Default starting point | BASELINE | Unchanged from defaults |
| Too much instability | HIGH_STABILITY | Stronger basin attraction |
| Channels feel independent | HIGH_RESONANCE | More coupling |
| System too static | PULSED_ACTIVITY | More frequent pulses |
| Unknown behavior | BASELINE | Safe starting point |

### 7.2 Filling the Parameter Map

After running v2 behavioral analysis:

1. **Run extended simulation** (50k+ steps)
2. **Extract fingerprint** using the schema above
3. **Compare to targets** in cfm_core_v2_parameter_map.md Section 3
4. **Identify gaps** between observed and target values
5. **Apply mapping rules** from Section 4 of parameter map
6. **Select or tune preset** based on anomaly detection

### 7.3 Iterative Tuning

```
1. Start with BASELINE preset
2. Run 10,000 step analysis
3. Extract fingerprint metrics
4. Check against healthy ranges (Section 4)
5. If anomalies detected:
   a. Select appropriate preset (Section 6)
   b. Re-run analysis
   c. Compare fingerprints
6. If targets still not met:
   a. Consider custom config based on mapping rules
   b. Iterate with smaller adjustments (φ⁻¹ factors)
```

---

## 8. Analysis Workflow Checklist

### 8.1 Quick Validation

- [ ] Run 500 steps with v2
- [ ] Verify all outputs in [0, 1]
- [ ] Verify no NaN/Inf values
- [ ] Check basic trajectory shapes for all channels

### 8.2 Channel Characterization

- [ ] Run 5,000 steps
- [ ] Extract mean/std for each output metric
- [ ] Verify slow variables evolve slower than fast
- [ ] Check phase wrapping behavior

### 8.3 Full Fingerprint Extraction

- [ ] Run 20,000+ steps
- [ ] Compute regime occupancy percentages
- [ ] Count and characterize pulse events
- [ ] Compute cross-channel correlations
- [ ] Verify basin dynamics
- [ ] Extract lock-in statistics

### 8.4 Comparative Analysis

- [ ] Compare v2 vs v1 (10,000 steps)
- [ ] Compare v2 vs v0 (10,000 steps)
- [ ] Document key behavioral differences
- [ ] Verify v2 shows multi-channel coupling

### 8.5 Anomaly Check

- [ ] Check for chaotic regime
- [ ] Check for frozen regime
- [ ] Verify timescale separation
- [ ] Verify pulse-recovery behavior
- [ ] Check cross-channel coupling

### 8.6 Preset Validation

- [ ] Run same analysis with each preset
- [ ] Verify presets produce distinct behaviors
- [ ] Confirm all presets maintain bounds
- [ ] Document preset characteristic differences

---

## 9. References

- [CFM Core v2 Specification](cfm_core_v2_spec.md)
- [CFM Core v2 Parameter Map](cfm_core_v2_parameter_map.md)
- [CFM Core v1 Behavioral Analysis Guide](cfm_core_v1_behavioral_analysis.md)
