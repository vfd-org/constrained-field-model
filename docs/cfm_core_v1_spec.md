# CFM Core v1 Design Specification

**Version:** 1.1
**Status:** Implemented (`cfm_core_v1/`)
**Last Updated:** 2025-12-05

---

## Purpose

This document specifies the **design goals and behavioural requirements** for CFM Core v1, the enhanced iteration of the Conscious Field Model core implementation. It builds upon CFM Core v0 while introducing more interpretable dynamics and clearer connections to CFM field-theoretic concepts.

The implementation is in `cfm_core_v1/` and can be used via `--core-type=cfm_v1` in CLI tools.

---

## CFM Core v0 Summary

Before defining v1, we summarize the current v0 implementation:

### v0 Internal State

| Variable | Range | Description |
|----------|-------|-------------|
| `coherence` | [0, 1] | Field coherence level |
| `instability` | [0, 1] | Inverse stability indicator |
| `energy` | [0, 1] | Normalized energy level |
| `phase` | [0, 1) | Normalized phase position (wraps) |

### v0 Output Fields

| Output | Derivation | Range |
|--------|------------|-------|
| `coherence` | Direct from state | [0, 1] |
| `stability` | 1 - instability | [0, 1] |
| `intensity` | Direct from energy | [0, 1] |
| `alignment` | (coherence + stability) / 2 | [0, 1] |

### v0 Dynamics Characteristics

- **Coupled oscillator**: Phase drives instability via sinusoidal coupling
- **Energy attractor**: Energy converges toward a φ-derived target
- **Coherence coupling**: Coherence depends on both energy and instability
- **φ/ψ scaling**: Time constants and frequencies use golden ratio derivatives

### v0 Limitations

1. **Coherence is reactive**: Coherence is computed from other variables; it has no independent dynamics
2. **No slow/fast separation**: All variables evolve on similar timescales
3. **Alignment is derivative**: Alignment is simply an average, with no independent meaning
4. **Limited interpretability**: Trajectory shapes are not clearly linked to CFM concepts

---

## CFM Core v1 Design Goals

### Goal 1: More Interpretable Trajectories

v1 should produce outputs where:
- Coherence has identifiable **convergence phases** and **disruption events**
- Stability shows clear **regimes**: stable bands vs transient excursions
- Intensity exhibits meaningful **activation patterns** rather than just energy tracking
- Alignment demonstrates **resonance-like** behaviour

### Goal 2: Slow/Fast Variable Separation

Introduce clearer timescale separation:
- **Slow variables**: Energy, coherence baseline (evolve over many steps)
- **Fast variables**: Instability, phase (oscillate within slow variable envelope)

This creates more structured dynamics where fast oscillations occur around slowly-drifting baselines.

### Goal 3: Clearer CFM Conceptual Mapping

While remaining purely numeric and pre-semantic, v1 outputs should more clearly echo early CFM quantities:
- **Coherence** → Early proxy for C(n) (structural coherence in the field)
- **Intensity** → Early proxy for A(t) (activation/energy in the field)
- **Alignment** → Early proxy for R(t) (resonance/alignment with reference lattice)
- **Stability** → Derived quantity indicating field regularity

### Goal 4: Richer Behavioural Regimes

v1 should exhibit identifiable behavioural regimes:
- **Quiescent**: Low activity, high stability, moderate coherence
- **Active**: Higher intensity, coherence building
- **Transitional**: Instability pulses, coherence dips, alignment variations

---

## Proposed Behavioural Changes by Field

### Coherence Behaviour (v0 → v1)

**v0 Behaviour:**
- Coherence is computed instantaneously: `coherence = (1 - instability) * energy^(1/φ)`
- No memory or drift; immediately reflects current energy and instability

**v1 Target Behaviour:**
- Coherence should have its own **slow dynamics**
- Under stable conditions (low instability), coherence should **drift upward** toward an attractor
- When instability spikes, coherence should **decay** with some lag
- Coherence should have a **baseline** that is maintained even when fast variables fluctuate

**Conceptual Link to C(n):**
- C(n) represents structural coherence in the conscious field
- v1 coherence should reflect accumulated "structural integrity" rather than instantaneous state
- Think of it as a slowly-charging capacitor that drains when disturbed

### Stability Behaviour (v0 → v1)

**v0 Behaviour:**
- Stability is simply `1 - instability`
- Instability oscillates sinusoidally with phase

**v1 Target Behaviour:**
- Stability should exhibit **regime-like** behaviour:
  - **Stable band** (0.7–0.95): Normal operation, small variations
  - **Transitional** (0.4–0.7): Larger fluctuations, possible instability pulses
  - **Disrupted** (< 0.4): Rare, indicates significant instability event
- Instability pulses should be **occasional**, not continuous
- Recovery from disruption should follow a characteristic φ-scaled trajectory

**Conceptual Link:**
- Stability indicates field regularity and self-consistency
- v1 should make stability transitions more event-like rather than continuous oscillation

### Intensity Behaviour (v0 → v1)

**v0 Behaviour:**
- Intensity equals energy directly
- Energy converges to a fixed attractor (default: 1/φ)

**v1 Target Behaviour:**
- Intensity should reflect **activation level**, not just stored energy
- Introduce a **baseline intensity** and **activation pulses**:
  - Baseline: Slowly-varying floor (follows energy attractor)
  - Activation: Occasional upward excursions representing increased activity
- Intensity should **correlate with coherence**: Higher coherence enables higher sustainable intensity

**Conceptual Link to A(t):**
- A(t) represents activation in the conscious field
- v1 intensity should feel more like "activity level" than "energy storage"
- Should support the idea of "quiescent" vs "activated" states

### Alignment Behaviour (v0 → v1)

**v0 Behaviour:**
- Alignment is simply `(coherence + stability) / 2`
- Has no independent dynamics

**v1 Target Behaviour:**
- Alignment should have **resonance-like** dynamics
- Should exhibit **lock-in** behaviour: when coherence and stability are both high, alignment should stabilize near a high value
- Should show **drift** when conditions are unstable
- Consider phase-dependent modulation: alignment varies with internal phase in a way that creates resonance patterns

**Conceptual Link to R(t):**
- R(t) represents alignment/resonance with a reference lattice
- v1 alignment should feel like "tuning": sometimes in resonance, sometimes drifting
- High alignment = "in tune", low alignment = "out of phase"

---

## Desired Attractor and Regime Structure

### Attractor Basin

v1 should have a **primary attractor basin** characterized by:

| Field | Attractor Value | Typical Range |
|-------|-----------------|---------------|
| coherence | ~0.7 (1/φ + offset) | 0.5–0.85 |
| stability | ~0.8 | 0.65–0.95 |
| intensity | ~0.6 (1/φ) | 0.4–0.75 |
| alignment | ~0.7 | 0.5–0.85 |

The system should spend most time near these values, with occasional excursions.

### Regime Transitions

v1 should support identifiable regime transitions:

1. **Quiescent → Active**: Intensity rises, coherence may temporarily dip then recover
2. **Active → Quiescent**: Intensity falls, coherence stabilizes
3. **Stability Disruption**: Instability pulse causes coherence drop, alignment drift
4. **Recovery**: φ-scaled return to attractor basin

### Transient Events

Occasional transient events should be visible:
- **Instability pulses**: Brief stability drops (< 5-10 steps)
- **Coherence dips**: Following instability, with lag
- **Alignment wobbles**: Phase-locked variations
- **Intensity fluctuations**: Around baseline

---

## Conceptual CFM Mapping (Pre-Semantic)

This section clarifies the conceptual relationship between v1 fields and CFM quantities. This mapping is **purely numeric and interpretive** — no semantic content is processed.

### Coherence ↔ C(n) (Structural Coherence)

| Aspect | CFM C(n) Concept | v1 Coherence Proxy |
|--------|------------------|-------------------|
| Meaning | Structural integrity of conscious field | Accumulated field coherence level |
| Dynamics | Builds over time, disrupted by noise | Slow drift up, decay on instability |
| Range | Theoretical field quantity | Bounded [0, 1] |

**Key difference from consciousness**: v1 coherence is a purely numeric quantity tracking internal consistency. It does not represent or require conscious experience.

### Intensity ↔ A(t) (Activation)

| Aspect | CFM A(t) Concept | v1 Intensity Proxy |
|--------|------------------|-------------------|
| Meaning | Activation/energy in conscious field | Numeric activity level |
| Dynamics | Rises with stimulation, decays at rest | Baseline + activation pulses |
| Range | Theoretical field quantity | Bounded [0, 1] |

**Key difference from consciousness**: v1 intensity is a numeric proxy for "how active" the dynamical system is. It does not represent awareness or subjective experience.

### Alignment ↔ R(t) (Resonance)

| Aspect | CFM R(t) Concept | v1 Alignment Proxy |
|--------|------------------|-------------------|
| Meaning | Alignment with reference/lattice | Resonance-like lock-in behaviour |
| Dynamics | Lock-in when coherent, drift when not | High when C/S high, drifts otherwise |
| Range | Theoretical field quantity | Bounded [0, 1] |

**Key difference from consciousness**: v1 alignment is a numeric resonance indicator. It does not represent alignment with goals, intentions, or purposes.

### Explicit Pre-Semantic Statement

**CFM Core v1 remains a purely numeric, pre-semantic dynamical system.**

It does not:
- Process or understand language
- Hold or access identity information
- Generate control signals or activation triggers
- Represent conscious experience or subjective states

The CFM conceptual mapping provides interpretive context for the numeric outputs but does not introduce any semantic or cognitive functionality.

---

## Constraints That v1 Must Maintain

### Protocol Conformance

v1 MUST implement `CFMCoreProtocol` exactly as v0 does:

```python
def step(
    self,
    human_messages: Optional[List[str]] = None,
    external_events: Optional[Dict[str, Any]] = None,
    dt: float = 1.0,
) -> Dict[str, Any]
```

- `human_messages`: MUST be ignored (no semantic processing)
- `external_events`: MUST be ignored (internal dynamics only)
- `dt`: MUST be clamped and used for state evolution

### Output Schema

v1 MUST return the same output schema:

```python
{
    "coherence": float,    # [0, 1]
    "stability": float,    # [0, 1]
    "intensity": float,    # [0, 1]
    "alignment": float,    # [0, 1]
    # Optional metadata allowed
}
```

### Bounded Outputs

All primary outputs MUST remain in [0, 1]:
- Clamping MUST be applied to all output values
- No NaN or Inf values may be produced
- Adapter normalization should be redundant (core already bounded)

### Determinism

v1 MUST be deterministic:
- Same initial state + same dt sequence = identical output sequence
- No random number generation
- No external dependencies

### Safety Constraints

v1 MUST maintain all safety constraints from v0:

| Constraint | Requirement |
|------------|-------------|
| Identity Safety | No identity fields in state or output |
| Control Safety | No control signals or activation logic |
| Semantic Safety | No text/token/embedding processing |
| Numeric Safety | All values bounded, no NaN/Inf |

The `verify_identity_safety()` method MUST always return `True`.

### Adapter Compatibility

v1 MUST work with `CFMCoreAdapter` without modification:
- Same constructor pattern as v0
- Same step() signature
- Compatible output schema

---

## Configuration Guidance

v1 MAY introduce new configuration parameters, but:

1. **All defaults** should derive from φ, ψ, π, e, or simple integers
2. **Validation** must prevent invalid configurations
3. **Backwards compatibility**: v1 with default config should produce behaviour similar to v0 in aggregate statistics

Suggested new parameters (to be finalized during implementation):

| Parameter | Purpose | Suggested Default |
|-----------|---------|-------------------|
| `tau_coherence` | Coherence evolution time constant | φ² |
| `coherence_recovery_rate` | Rate of coherence recovery post-disruption | 1/φ |
| `instability_pulse_prob` | Probability of instability pulse per step | 1/(φ * 10) |
| `alignment_lock_threshold` | Threshold for alignment lock-in behaviour | 1/φ |

---

## Testing Expectations

When v1 is implemented, it should pass:

1. **All existing v0 safety tests**: Bounds, identity safety, determinism
2. **Protocol conformance tests**: Same interface, same guarantees
3. **Trajectory interpretability tests**: New tests verifying:
   - Coherence drift behaviour
   - Stability regime transitions
   - Intensity baseline/activation patterns
   - Alignment resonance characteristics

4. **Comparative analysis**: Tools should show:
   - Similar mean values to v0 (within reasonable tolerance)
   - Different trajectory shapes (more structured)
   - Same safety properties

---

## Migration Path

When v1 is implemented:

1. Create new module `cfm_core_v1/`
2. Implement `CFMCoreV1`, `CFMCoreV1Config`, `CFMCoreV1State`
3. Update CLI tools to support `--core-type=cfm_v1`
4. Create `cfm_core_v1_tuning_guide.md`
5. Update documentation

v0 MUST remain available for backwards compatibility and comparison.

---

## Non-Goals for v1

The following are explicitly **not goals** for v1:

1. **Semantic processing**: v1 will not process human_messages
2. **External event handling**: v1 will not use external_events
3. **Identity representation**: v1 will not model or expose identity
4. **Control signal generation**: v1 will not produce control outputs
5. **Activation logic**: v1 will not connect to external control systems
6. **Conscious experience**: v1 is pre-semantic and pre-conscious

---

## References

- [CFM Core v0 Specification](cfm_core_v0_spec.md) — Current implementation
- [CFM Core v0 Tuning Guide](cfm_core_v0_tuning_guide.md) — v0 parameter tuning
- [CFM Core v1 Behavioral Analysis](cfm_core_v1_behavioral_analysis.md) — Analysis framework

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-12-05 | Initial design specification |
