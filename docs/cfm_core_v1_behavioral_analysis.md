# CFM Core v1 Behavioral Analysis Guide

**Version:** 1.0
**Status:** Analysis Framework
**Last Updated:** 2025-12-05

---

## 1. Purpose

This document defines the methodology for extracting **long-run behavioral baselines** from CFM Core v1. The analysis results will:

1. Characterize v1's dynamic fingerprint
2. Enable comparison against mock cores and CFM v0
3. Guide parameter selection for CFM v2 implementation
4. Establish quantitative metrics for core behavior validation

---

## 2. Running Long-Duration Simulations

### 2.1 Recommended Run Lengths

| Run Type | Steps | Duration | Purpose |
|----------|-------|----------|---------|
| Quick validation | 100 | ~1 second | Sanity check, bounds verification |
| Short baseline | 1,000 | ~5 seconds | Initial trajectory characterization |
| Medium baseline | 5,000 | ~20 seconds | Regime identification |
| Long baseline | 10,000 | ~40 seconds | Convergence analysis |
| Extended baseline | 50,000 | ~3 minutes | Full dynamic fingerprint |
| Stress test | 100,000 | ~7 minutes | Long-term stability verification |

### 2.2 Using cfm_local_loop

```bash
# Quick validation run
python tools/cfm_local_loop.py --steps 100 --core-type=cfm_v1 --output-json quick.json

# Short baseline
python tools/cfm_local_loop.py --steps 1000 --core-type=cfm_v1 --output-json short.json

# Medium baseline (recommended starting point)
python tools/cfm_local_loop.py --steps 5000 --core-type=cfm_v1 --output-json medium.json

# Long baseline
python tools/cfm_local_loop.py --steps 10000 --core-type=cfm_v1 --output-json long.json

# Extended baseline (full fingerprint)
python tools/cfm_local_loop.py --steps 50000 --core-type=cfm_v1 --output-json extended.json
```

### 2.3 Using cfm_fingerprint

After generating JSON output, extract fingerprints with:

```bash
# Extract fingerprint
python tools/cfm_fingerprint.py --input medium.json --output fp_medium.json

# Compare two fingerprints
python tools/cfm_fingerprint.py --compare fp1.json fp2.json
```

---

## 3. Metrics to Extract

### 3.1 Stability Regime Durations

Measure time spent in different stability bands:

| Regime | Stability Range | Interpretation |
|--------|-----------------|----------------|
| High Stability | [0.85, 1.0] | Locked, minimal fluctuation |
| Stable | [0.70, 0.85) | Normal operating range |
| Transitional | [0.50, 0.70) | Active dynamics |
| Low Stability | [0.30, 0.50) | High variability |
| Unstable | [0.0, 0.30) | Instability-dominated |

**Metrics to compute:**
- Mean time in each regime (steps)
- Transition frequency between regimes
- Longest continuous stay in each regime
- Regime occupancy percentage

### 3.2 Coherence Drift and Convergence

Analyze coherence evolution over time:

**Drift Metrics:**
- Initial coherence value (step 0)
- Final coherence value (step N)
- Net drift: final - initial
- Drift rate: net_drift / N
- Drift direction: sign(net_drift)

**Convergence Metrics:**
- Convergence target (coherence_target from config ≈ 0.718)
- Distance to target: |coherence - target|
- Time to reach within ε of target
- Convergence stability: variance in final 10% of run

**Baseline Metrics:**
- coherence_baseline drift rate
- coherence_baseline final value
- Baseline-to-coherence gap: |coherence - coherence_baseline|

### 3.3 Alignment Lock-In Frequency

Measure alignment lock-in behavior:

**Lock-In Detection:**
- Lock-in threshold: alignment > 0.618 (φ⁻¹)
- Lock-in duration: consecutive steps above threshold
- Lock-in frequency: number of lock-in events per 1000 steps

**Lock-In Metrics:**
- Mean lock-in duration
- Max lock-in duration
- Lock-in entry rate (transitions into lock-in per 1000 steps)
- Lock-in exit rate (transitions out of lock-in per 1000 steps)
- Lock-in stability: variance during lock-in periods

### 3.4 Phase Dynamic Fingerprints

Analyze phase evolution patterns:

**Phase Metrics:**
- Phase velocity: Δphase / Δt (should be ≈ omega_phase)
- Phase variance: spread around expected trajectory
- Phase wrap frequency: number of 0→1 wraps per 1000 steps

**Alignment Phase Metrics:**
- Alignment phase velocity ratio: alignment_phase_velocity / phase_velocity
- Expected ratio: ψ (PSI ≈ 1.325)
- Phase coherence: correlation between phase and alignment_phase

### 3.5 Resonance Interaction Statistics

Cross-variable coupling analysis:

**Coupling Metrics:**
- Coherence-Stability correlation
- Coherence-Intensity correlation
- Stability-Alignment correlation
- Energy-Coherence coupling strength

**Lag Analysis:**
- Cross-correlation at different time lags
- Dominant lag for each variable pair
- Coupling direction (which variable leads)

---

## 4. The CFM v1 Fingerprint

The **CFM v1 Fingerprint** is a structured summary capturing the essential behavioral characteristics of a v1 run.

### 4.1 Fingerprint Schema

```json
{
  "fingerprint_version": "1.0",
  "core_type": "cfm_v1",
  "run_parameters": {
    "steps": 10000,
    "dt": 0.1,
    "config": { /* CFMCoreV1Config values */ }
  },
  "oscillation_ranges": {
    "coherence": { "min": 0.0, "max": 1.0, "mean": 0.0, "std": 0.0 },
    "stability": { "min": 0.0, "max": 1.0, "mean": 0.0, "std": 0.0 },
    "intensity": { "min": 0.0, "max": 1.0, "mean": 0.0, "std": 0.0 },
    "alignment": { "min": 0.0, "max": 1.0, "mean": 0.0, "std": 0.0 }
  },
  "dominant_frequency_bands": {
    "coherence_period": 0.0,
    "stability_period": 0.0,
    "intensity_period": 0.0,
    "alignment_period": 0.0,
    "phase_wrap_period": 0.0
  },
  "drift_envelopes": {
    "coherence_drift_rate": 0.0,
    "coherence_baseline_drift_rate": 0.0,
    "energy_drift_rate": 0.0,
    "alignment_drift_rate": 0.0
  },
  "transition_points": {
    "stability_regime_changes": 0,
    "alignment_lock_in_events": 0,
    "coherence_crossings": 0
  },
  "noise_profile": {
    "coherence_noise_amplitude": 0.0,
    "stability_noise_amplitude": 0.0,
    "intensity_noise_amplitude": 0.0,
    "alignment_noise_amplitude": 0.0,
    "high_frequency_content": 0.0
  }
}
```

### 4.2 Oscillation Ranges

For each output variable (coherence, stability, intensity, alignment):

| Metric | Description | Expected v1 Range |
|--------|-------------|-------------------|
| min | Minimum observed value | > 0.0 |
| max | Maximum observed value | < 1.0 |
| mean | Average value | ≈ φ⁻¹ (0.618) |
| std | Standard deviation | < 0.15 |
| range | max - min | < 0.5 |

### 4.3 Dominant Frequency Bands

Estimated periods for each variable's oscillation:

| Variable | Expected Period | Notes |
|----------|-----------------|-------|
| coherence | τ_coherence (φ² ≈ 2.62) | Slow variable |
| stability | τ_instability (φ⁻¹ ≈ 0.62) | Fast oscillation |
| intensity | Mixed | Coherence-coupled |
| alignment | τ_medium | Lock-in modulated |
| phase_wrap | 1/omega_phase | Direct from config |

### 4.4 Drift Envelopes

Long-term drift characteristics:

| Drift Metric | Expected Behavior | Healthy Range |
|--------------|-------------------|---------------|
| coherence_drift_rate | Toward coherence_target | < 0.01 per 100 steps |
| coherence_baseline_drift_rate | Very slow upward | < 0.001 per 100 steps |
| energy_drift_rate | Toward energy_target | < 0.01 per 100 steps |
| alignment_drift_rate | Stable with lock-in | < 0.005 per 100 steps |

### 4.5 Transition Points

Discrete events in the trajectory:

| Event Type | Detection Criterion |
|------------|---------------------|
| Stability regime change | Stability crosses threshold |
| Alignment lock-in event | Alignment crosses φ⁻¹ upward |
| Alignment lock-out event | Alignment crosses φ⁻¹ downward |
| Coherence crossing | Coherence crosses baseline |

### 4.6 Noise Profile

High-frequency variability characteristics:

| Metric | Description | Healthy Range |
|--------|-------------|---------------|
| noise_amplitude | RMS of high-pass filtered signal | < 0.05 |
| high_frequency_content | Power above Nyquist/4 | < 0.1 |

---

## 5. Anomaly Detection

### 5.1 Under-Damped Behavior

**Symptoms:**
- Oscillation amplitude grows over time
- Coherence overshoots target repeatedly
- Stability shows increasing variance
- Alignment exhibits ringing after lock-in

**Detection Criteria:**
```
under_damped = (
    oscillation_amplitude_trend > 0.01 per 1000 steps
    OR coherence_overshoot_count > 5 per 1000 steps
    OR stability_variance_trend > 0.001 per 1000 steps
)
```

**Implications for v2:**
- Increase damping coefficients
- Reduce coupling strengths
- Extend time constants

### 5.2 Over-Damped Behavior

**Symptoms:**
- Variables converge too quickly (within 100 steps)
- Little to no oscillation visible
- Alignment never achieves lock-in
- System appears "frozen" in steady state

**Detection Criteria:**
```
over_damped = (
    convergence_time < 100 steps
    AND oscillation_amplitude < 0.01
    AND alignment_lock_in_events < 1 per 5000 steps
)
```

**Implications for v2:**
- Reduce damping coefficients
- Increase coupling strengths
- Shorten time constants

### 5.3 Poor Separation of Timescales

**Symptoms:**
- Slow and fast variables evolve at similar rates
- coherence_baseline tracks coherence too closely
- Phase and alignment_phase have similar velocities
- No clear regime structure visible

**Detection Criteria:**
```
poor_timescale_separation = (
    |coherence_period / stability_period - φ²| > 0.5
    OR |coherence_baseline_drift_rate / coherence_drift_rate| > 0.5
    OR |alignment_phase_velocity / phase_velocity - ψ| > 0.2
)
```

**Implications for v2:**
- Increase τ_slow / τ_fast ratio
- Strengthen φ-derived separation
- Review time constant hierarchy

### 5.4 Weak Coherence Convergence

**Symptoms:**
- Coherence does not approach target
- Coherence exhibits random walk behavior
- Large gap between coherence and coherence_baseline
- Coherence variance increases over time

**Detection Criteria:**
```
weak_coherence_convergence = (
    |final_coherence - coherence_target| > 0.2
    OR coherence_variance_trend > 0
    OR |coherence - coherence_baseline| > 0.3 at end of run
)
```

**Implications for v2:**
- Strengthen basin attraction
- Adjust coherence_target
- Review energy-coherence coupling

### 5.5 Insufficient Alignment Stability

**Symptoms:**
- Alignment fluctuates rapidly even during lock-in
- Lock-in durations are very short (< 10 steps)
- Alignment never stabilizes above threshold
- High variance in alignment during stable coherence periods

**Detection Criteria:**
```
insufficient_alignment_stability = (
    mean_lock_in_duration < 10 steps
    OR alignment_variance_during_lock_in > 0.05
    OR max_alignment < alignment_threshold + 0.1
)
```

**Implications for v2:**
- Increase alignment_lock_strength
- Extend alignment time constant
- Strengthen coherence-stability coupling to alignment

### 5.6 Anomaly Summary Table

| Anomaly | Key Indicator | Severity | v2 Response |
|---------|---------------|----------|-------------|
| Under-damped | Growing oscillations | High | Increase damping |
| Over-damped | No oscillations | Medium | Reduce damping |
| Poor timescale separation | Similar evolution rates | High | Adjust τ ratios |
| Weak coherence convergence | Far from target | Medium | Strengthen attraction |
| Insufficient alignment stability | Short lock-ins | Medium | Increase lock strength |

---

## 6. Feeding Results into CFM v2

### 6.1 Parameter Selection Pipeline

```
┌─────────────────────────────────────────────────────────────────────┐
│                  v1 Analysis → v2 Parameter Pipeline                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   v1 Behavioral Analysis                                             │
│   ──────────────────────                                             │
│   • Run long-duration simulations                                    │
│   • Extract fingerprint metrics                                      │
│   • Identify anomalies                                               │
│                                                                      │
│                    ↓                                                 │
│                                                                      │
│   Metric Interpretation                                              │
│   ────────────────────                                               │
│   • Compare against expected ranges                                  │
│   • Identify behavioral gaps                                         │
│   • Quantify improvement targets                                     │
│                                                                      │
│                    ↓                                                 │
│                                                                      │
│   v2 Parameter Mapping                                               │
│   ────────────────────                                               │
│   • Map v1 observations to v2 parameters                             │
│   • Apply φ-derived scaling rules                                    │
│   • Set initial v2 configuration                                     │
│                                                                      │
│                    ↓                                                 │
│                                                                      │
│   v2 Implementation & Validation                                     │
│   ─────────────────────────────                                      │
│   • Implement v2 with derived parameters                             │
│   • Run comparative analysis                                         │
│   • Iterate on parameters if needed                                  │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### 6.2 Attractor Manifold Calibration

v1 behavioral analysis informs v2 attractor manifold design:

| v1 Observation | v2 Attractor Parameter |
|----------------|------------------------|
| Mean coherence at convergence | Basin center coherence (μ_basin.c) |
| Mean energy at convergence | Basin center energy (μ_basin.e) |
| Mean stability at convergence | Basin center stability (μ_basin.s) |
| Coherence oscillation range | Basin radius (r_basin) |
| Regime transition frequency | Basin attraction strength (k_attraction) |

### 6.3 Timescale Tuning

v1 period measurements inform v2 time constants:

| v1 Metric | v2 Parameter | Mapping Rule |
|-----------|--------------|--------------|
| coherence_period | τ_slow | Scale by φ if too fast |
| stability_period | τ_fast | Scale by φ⁻¹ if too slow |
| baseline_drift_rate | τ_very_slow | Inverse relationship |
| lock_in_duration | τ_medium | Direct relationship |

### 6.4 Cross-Channel Coupling Strengths

v1 correlation analysis informs v2 coupling:

| v1 Correlation | v2 Coupling Parameter |
|----------------|----------------------|
| Coherence-Stability | stability_coherence_coupling |
| Coherence-Intensity | intensity_coherence_coupling |
| Stability-Alignment | alignment_stability_coupling |
| Energy-Coherence | coherence_energy_coupling |

**Mapping Rule:**
```
v2_coupling = v1_correlation * φ * adjustment_factor

where adjustment_factor:
    = 1.0 if correlation is in healthy range
    = 1.5 if correlation is too weak (need stronger coupling)
    = 0.7 if correlation is too strong (reduce coupling)
```

---

## 7. Analysis Workflow Checklist

### 7.1 Initial Baseline

- [ ] Run 1,000 step validation
- [ ] Verify all outputs bounded [0, 1]
- [ ] Verify no NaN/Inf values
- [ ] Check basic trajectory shape

### 7.2 Fingerprint Extraction

- [ ] Run 10,000 step extended baseline
- [ ] Extract oscillation ranges
- [ ] Estimate dominant frequencies
- [ ] Compute drift envelopes
- [ ] Count transition points
- [ ] Characterize noise profile

### 7.3 Comparative Analysis

- [ ] Compare v1 vs v0 (10,000 steps)
- [ ] Compare v1 vs mock-deterministic
- [ ] Compare v1 vs mock-stress
- [ ] Document key differences

### 7.4 Anomaly Check

- [ ] Check for under-damped behavior
- [ ] Check for over-damped behavior
- [ ] Verify timescale separation
- [ ] Verify coherence convergence
- [ ] Verify alignment stability

### 7.5 v2 Preparation

- [ ] Document v1 fingerprint metrics
- [ ] Identify behavioral gaps
- [ ] Propose v2 parameter adjustments
- [ ] Update parameter map template

---

## 8. References

- [CFM Core v1 Specification](cfm_core_v1_spec.md)
- [CFM Core v2 Specification](cfm_core_v2_spec.md)
- [CFM Core v2 Parameter Map](cfm_core_v2_parameter_map.md)
