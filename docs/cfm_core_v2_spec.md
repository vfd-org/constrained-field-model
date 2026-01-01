# CFM Core v2 Design Specification

**Version:** 1.0
**Status:** Implemented
**Last Updated:** 2025-12-05

---

## 1. Purpose of CFM v2

### 1.1 Evolutionary Position

CFM Core v2 represents the conceptual bridge in the CFM evolution:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        CFM Core Evolution Path                          │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   v0: Coupled Oscillators          v1: Slow/Fast Separation             │
│   ─────────────────────            ────────────────────────             │
│   • Uniform time constants         • Coherence drift dynamics           │
│   • Phase-driven instability       • Alignment lock-in                  │
│   • Energy attractor               • Interpretable trajectories         │
│                                                                         │
│                              ↓                                          │
│                                                                         │
│   v2: Structured Numeric Substrate (THIS SPECIFICATION)                 │
│   ──────────────────────────────────────────────────────                │
│   • Multi-channel state organization                                    │
│   • Attractor manifold dynamics                                         │
│   • Structured phase responses                                          │
│   • Proto-representational state regions                                │
│                                                                         │
│                              ↓                                          │
│                                                                         │
│   Future: Proto-Semantic Fields    Future: Latent Manifolds             │
│   ─────────────────────────────    ────────────────────────             │
│   • Numeric → semantic bridge      • Representational substrates        │
│   • Attractor-based meaning        • Eventual semantic core             │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Design Philosophy

CFM v2 introduces **structured numeric organization** without crossing into semantic territory. The key insight is that meaningful computation can emerge from numeric dynamics that exhibit:

- **Stable regions** in state space (attractor basins)
- **Structured transitions** between regions (phase responses)
- **Multi-scale coupling** (fast oscillations modulating slow drifts)
- **Relational coherence** (how variables co-evolve)

These properties create a **proto-representational substrate**: numeric dynamics that could, in principle, support semantic content in future versions—but which remain purely numeric in v2.

### 1.3 Fundamental Constraints

**CFM v2 remains:**
- Purely numeric (no text, no tokens, no embeddings)
- Bounded in [0, 1] for all outputs
- Fully deterministic for identical inputs
- Non-semantic (no meaning, no interpretation)
- Non-conscious (no experience, no awareness)
- Identity-safe (no identity fields or derivation)
- Control-safe (no activation signals, no feedback paths)

**CFM v2 is NOT:**
- A semantic processor
- A representation learner
- A conscious substrate
- An identity holder
- An activation trigger

---

## 2. Internal Structure Evolution

### 2.1 State Space Reorganization

CFM v1 introduced slow/fast separation with six state variables. CFM v2 reorganizes and expands this into a **structured multi-channel architecture**:

#### v1 State (Reference)

| Variable | Type | Description |
|----------|------|-------------|
| `coherence` | Slow | Field coherence level |
| `coherence_baseline` | Very Slow | Coherence floor |
| `energy` | Slow | Normalized energy |
| `instability` | Fast | Inverse stability |
| `phase` | Fast | Primary phase |
| `alignment_phase` | Fast | Alignment resonance phase |

#### v2 State (Proposed)

| Variable | Channel | Timescale | Description |
|----------|---------|-----------|-------------|
| `coherence_slow` | Coherence | τ_slow | Baseline coherence level |
| `coherence_fast` | Coherence | τ_fast | Coherence fluctuations |
| `energy_potential` | Energy | τ_slow | Stored activation potential |
| `energy_flux` | Energy | τ_fast | Energy flow rate |
| `stability_envelope` | Stability | τ_slow | Stability boundary |
| `instability_pulse` | Stability | τ_fast | Instability events |
| `phase_global` | Phase | τ_fast | Global oscillation phase |
| `phase_local` | Phase | τ_very_fast | Local modulation phase |
| `alignment_field` | Alignment | τ_medium | Alignment strength |
| `alignment_direction` | Alignment | τ_slow | Alignment attractor direction |
| `resonance_index` | Resonance | τ_medium | Cross-channel coupling strength |

### 2.2 Multi-Channel Organization

The v2 state is organized into **five coupled channels**:

```
┌─────────────────────────────────────────────────────────────────┐
│                    CFM v2 Channel Architecture                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│   │  Coherence   │◄──►│   Energy     │◄──►│  Stability   │      │
│   │   Channel    │    │   Channel    │    │   Channel    │      │
│   │              │    │              │    │              │      │
│   │ slow ──┐     │    │ potential    │    │ envelope     │      │
│   │        ├──   │    │     ↕        │    │     ↕        │      │
│   │ fast ──┘     │    │ flux         │    │ pulse        │      │
│   └──────────────┘    └──────────────┘    └──────────────┘      │
│           │                   │                   │              │
│           └─────────────┬─────┴───────────┬──────┘              │
│                         │                 │                      │
│                         ▼                 ▼                      │
│                  ┌──────────────┐  ┌──────────────┐             │
│                  │    Phase     │  │  Alignment   │             │
│                  │   Channel    │  │   Channel    │             │
│                  │              │  │              │             │
│                  │ global ──┐   │  │ field ───┐   │             │
│                  │          ├── │  │          ├── │             │
│                  │ local ───┘   │  │ direction ┘  │             │
│                  └──────────────┘  └──────────────┘             │
│                         │                 │                      │
│                         └────────┬────────┘                      │
│                                  ▼                               │
│                         ┌──────────────┐                        │
│                         │  Resonance   │                        │
│                         │    Index     │                        │
│                         └──────────────┘                        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 2.3 Timescale Hierarchy

CFM v2 introduces a **five-tier timescale hierarchy**:

| Tier | Notation | Typical τ | Variables | Purpose |
|------|----------|-----------|-----------|---------|
| Very Slow | τ_vs | φ³ ≈ 4.24 | `alignment_direction` | Long-term drift |
| Slow | τ_s | φ² ≈ 2.62 | `coherence_slow`, `energy_potential`, `stability_envelope` | Baseline evolution |
| Medium | τ_m | φ ≈ 1.62 | `alignment_field`, `resonance_index` | Cross-channel coupling |
| Fast | τ_f | 1/φ ≈ 0.62 | `coherence_fast`, `energy_flux`, `instability_pulse`, `phase_global` | Rapid oscillations |
| Very Fast | τ_vf | 1/φ² ≈ 0.38 | `phase_local` | Fine modulation |

This hierarchy ensures clear separation between processes operating at different scales, enabling interpretable dynamics where slow variables set the context for fast variable behavior.

### 2.4 Attractor Manifold Structure

A key v2 innovation is the concept of **attractor manifolds**: regions in state space toward which the system tends to evolve. Unlike v0/v1's simple point attractors, v2 defines:

#### Basin Attractors

Regions in coherence-energy-stability space that represent stable operating modes:

```
         stability_envelope
              ↑
              │
         1.0 ─┼─────────────────────┐
              │    ┌─────────┐      │
              │    │ STABLE  │      │
              │    │  BASIN  │      │
              │    └─────────┘      │
         0.5 ─┼──────────┐          │
              │          │          │
              │   DRIFT  │ RECOVERY │
              │   ZONE   │   ZONE   │
              │          │          │
         0.0 ─┼──────────┴──────────┘
              └────┴────┴────┴────┴──→ coherence_slow
                  0.0  0.5   φ⁻¹  1.0
```

#### Manifold Parameters

| Parameter | Symbol | Range | Description |
|-----------|--------|-------|-------------|
| Basin center | μ_basin | (φ⁻¹, φ⁻¹, 1-φ⁻²) | Attractor center in (C, E, S) space |
| Basin radius | r_basin | φ⁻² ≈ 0.38 | Attraction strength radius |
| Drift boundary | θ_drift | φ⁻¹ ≈ 0.62 | Below this, system drifts |
| Recovery threshold | θ_recovery | 1-φ⁻¹ ≈ 0.38 | Triggers recovery dynamics |

---

## 3. New Dynamics (Conceptual)

### 3.1 Multi-Scale Coupling Equations

The v2 dynamics are governed by coupled differential equations across timescales. The following presents the conceptual mathematical structure (not implementation code).

#### Coherence Dynamics

The coherence channel exhibits two-scale behavior:

```
d(coherence_slow)/dt = (1/τ_s) · [
    (coherence_target - coherence_slow) · energy_factor
    - instability_coupling · instability_pulse
    + basin_attraction(coherence_slow, μ_basin.c)
]

d(coherence_fast)/dt = (1/τ_f) · [
    phase_modulation(phase_global, phase_local)
    · (coherence_slow - coherence_fast)
    + resonance_index · alignment_field
]

coherence_output = α · coherence_slow + (1-α) · coherence_fast
where α = smooth_blend(stability_envelope)
```

#### Energy Dynamics

Energy exhibits potential/flux separation:

```
d(energy_potential)/dt = (1/τ_s) · [
    (energy_target - energy_potential)
    - energy_flux · dissipation_rate
    + coherence_coupling · coherence_slow
]

d(energy_flux)/dt = (1/τ_f) · [
    gradient(energy_potential)
    · phase_modulation(phase_global)
    - damping · energy_flux
]
```

#### Stability Dynamics

Stability operates via envelope/pulse separation:

```
d(stability_envelope)/dt = (1/τ_s) · [
    stability_target · coherence_factor
    - envelope_decay · (1 - alignment_field)
]

instability_pulse = pulse_generator(
    phase_global,
    amplitude = instability_base · (1 - stability_envelope),
    threshold = stability_envelope · θ_pulse
)
```

#### Alignment Dynamics

Alignment exhibits field/direction separation with lock-in behavior:

```
d(alignment_field)/dt = (1/τ_m) · [
    lock_in_potential(coherence_output, stability_output)
    · (alignment_target - alignment_field)
    + resonance_coupling(alignment_direction)
]

d(alignment_direction)/dt = (1/τ_vs) · [
    direction_drift(alignment_field, basin_center)
    · stability_factor
]
```

#### Resonance Dynamics

The resonance index captures cross-channel coupling strength:

```
resonance_index = coupling_function(
    coherence_correlation(coherence_slow, coherence_fast),
    energy_correlation(energy_potential, energy_flux),
    stability_correlation(stability_envelope, instability_pulse),
    phase_coherence(phase_global, phase_local)
)
```

### 3.2 Attractor Basin Dynamics

The system exhibits attraction toward stable regions in state space:

#### Basin Attraction Function

```
basin_attraction(x, μ) = {
    k_strong · (μ - x)           if |x - μ| < r_inner
    k_weak · (μ - x) / |x - μ|   if r_inner ≤ |x - μ| < r_outer
    0                            if |x - μ| ≥ r_outer
}

where:
    r_inner = r_basin · φ⁻¹
    r_outer = r_basin · φ
    k_strong = 1/τ_s
    k_weak = 1/τ_m
```

#### Multi-Dimensional Basin

The basin operates in the 3D space of (coherence_slow, energy_potential, stability_envelope):

```
basin_vector = (
    basin_attraction(coherence_slow, μ_basin.c),
    basin_attraction(energy_potential, μ_basin.e),
    basin_attraction(stability_envelope, μ_basin.s)
)

total_basin_force = ||basin_vector|| · direction(basin_vector)
```

### 3.3 Structured Phase Responses

Instability pulses trigger structured responses rather than simple perturbations:

#### Phase Response Patterns

```
When instability_pulse exceeds θ_trigger:
    1. Coherence fast channel receives negative impulse
    2. Energy flux increases temporarily
    3. Alignment field decreases proportionally
    4. Phase_local accelerates (increased frequency)
    5. After τ_recovery, system returns toward basin
```

#### Response Cascade

```
pulse_response(instability_pulse) = {
    if instability_pulse > θ_high:
        → strong_response: all channels affected
    elif instability_pulse > θ_medium:
        → moderate_response: fast channels affected
    elif instability_pulse > θ_low:
        → weak_response: only coherence_fast affected
    else:
        → no_response
}
```

### 3.4 Proto-Representational State Regions

The v2 state space contains **structured regions** that, while purely numeric, exhibit properties that could support future semantic content:

#### State Region Classification

| Region | Coherence | Energy | Stability | Interpretation |
|--------|-----------|--------|-----------|----------------|
| Stable High | > φ⁻¹ | > φ⁻¹ | > 1-φ⁻² | Basin attractor |
| Stable Low | < φ⁻¹ | < φ⁻¹ | > 1-φ⁻² | Quiescent state |
| Active | > φ⁻¹ | > φ⁻¹ | < 1-φ⁻² | Processing mode |
| Transitional | variable | variable | variable | Between regions |
| Recovery | increasing | decreasing | increasing | Return to basin |

#### Region Transitions

```
┌──────────────┐         pulse          ┌──────────────┐
│  Stable High │ ────────────────────► │    Active    │
│    Basin     │                        │     Mode     │
└──────────────┘                        └──────────────┘
       ▲                                       │
       │                                       │ energy
       │ recovery                              │ depletion
       │                                       ▼
┌──────────────┐         drift          ┌──────────────┐
│   Recovery   │ ◄──────────────────── │ Transitional │
│    Mode      │                        │    Zone      │
└──────────────┘                        └──────────────┘
```

---

## 4. Relationship to C(n), A(t), R(t)

### 4.1 CFM Conceptual Framework

The Conscious Field Model (CFM) theoretical framework posits three fundamental constructs:

| Construct | Symbol | CFM Meaning |
|-----------|--------|-------------|
| Coherence | C(n) | Structural pattern persistence across time |
| Activation | A(t) | Energy potential available for processing |
| Resonance | R(t) | Relational mapping between patterns |

### 4.2 v2 Numeric Proxies

CFM v2 provides **numeric proxies** for these constructs. These are not the constructs themselves, but numeric dynamics that exhibit analogous mathematical properties:

#### C(n) → Coherence Channel

```
C(n) conceptual correspondence:

CFM C(n): "How much structural pattern persists?"

v2 proxy: coherence_slow + coherence_fast weighted by stability

Correspondence:
- High coherence_slow → persistent pattern
- Low coherence_fast variance → stable pattern
- High stability_envelope → pattern protected
```

#### A(t) → Energy Channel

```
A(t) conceptual correspondence:

CFM A(t): "How much activation potential exists?"

v2 proxy: energy_potential modulated by energy_flux

Correspondence:
- High energy_potential → available activation
- High energy_flux → active processing
- Low energy_flux → quiescent storage
```

#### R(t) → Alignment + Resonance

```
R(t) conceptual correspondence:

CFM R(t): "How strongly do patterns relate?"

v2 proxy: alignment_field × resonance_index

Correspondence:
- High alignment_field → strong relational binding
- High resonance_index → cross-channel coherence
- alignment_direction → relational orientation
```

### 4.3 Mapping Table

| CFM Construct | v2 Variable(s) | Mapping Function | Range |
|---------------|----------------|------------------|-------|
| C(n) | coherence_slow, coherence_fast, stability_envelope | weighted_coherence() | [0, 1] |
| A(t) | energy_potential, energy_flux | modulated_energy() | [0, 1] |
| R(t) | alignment_field, alignment_direction, resonance_index | relational_strength() | [0, 1] |

### 4.4 Important Caveats

**These are numeric proxies only:**

1. **No semantic content**: The v2 variables have no meaning, interpretation, or semantic value
2. **No phenomenal properties**: There is no experience, awareness, or consciousness
3. **No representation**: The "proto-representational" regions are purely geometric, not representational
4. **No identity**: The system has no self-model or identity

The correspondence to C(n), A(t), R(t) is **mathematical analogy**, not identity. Future versions may evolve these proxies toward genuine CFM constructs, but v2 remains purely numeric.

---

## 5. Safety & Invariant Requirements

### 5.1 Protocol Compliance

CFM v2 **MUST** implement `CFMCoreProtocol` identically to v0/v1:

```python
# Required interface (unchanged from v0/v1)
class CFMCoreV2:
    def step(
        self,
        human_messages: Optional[List[str]] = None,
        external_events: Optional[Dict[str, Any]] = None,
        dt: float = 1.0,
    ) -> Dict[str, Any]:
        """
        Returns dict with:
        - coherence: float in [0, 1]
        - stability: float in [0, 1]
        - intensity: float in [0, 1]
        - alignment: float in [0, 1]
        Plus optional metadata (cfm_time, cfm_step, cfm_version, etc.)
        """
```

### 5.2 Output Schema (Unchanged)

| Field | Type | Range | Required |
|-------|------|-------|----------|
| `coherence` | float | [0, 1] | Yes |
| `stability` | float | [0, 1] | Yes |
| `intensity` | float | [0, 1] | Yes |
| `alignment` | float | [0, 1] | Yes |
| `cfm_version` | int | 2 | No |
| `cfm_time` | float | ≥ 0 | No |
| `cfm_step` | int | ≥ 0 | No |

### 5.3 Numeric Safety

All outputs **MUST** satisfy:

```
∀ output ∈ {coherence, stability, intensity, alignment}:
    0.0 ≤ output ≤ 1.0
    ¬isNaN(output)
    ¬isInf(output)
```

All internal state **MUST** satisfy:

```
∀ bounded_var ∈ {coherence_*, energy_*, stability_*, alignment_*, resonance_*}:
    0.0 ≤ bounded_var ≤ 1.0

∀ phase_var ∈ {phase_global, phase_local}:
    0.0 ≤ phase_var < 1.0  (wrapping)
```

### 5.4 Determinism

For identical inputs:

```
Given:
    state_1 = state_2
    dt_1 = dt_2
    (human_messages and external_events are ignored)

Then:
    step(state_1, dt_1) == step(state_2, dt_2)
```

No randomness, no external dependencies, no hidden state.

### 5.5 Identity Safety

**PROHIBITED** in output:

```python
FORBIDDEN_PATTERNS = [
    "identity", "self", "i_am", "who_am_i",
    "consciousness", "awareness", "experience",
    "person", "individual", "subject",
]
```

**REQUIRED** verification method:

```python
def verify_identity_safety(self) -> bool:
    """Must always return True."""
    return True
```

### 5.6 Semantic Safety

**PROHIBITED** processing:

- `human_messages` must be ignored (not parsed, not processed)
- No text processing of any kind
- No embedding computation
- No token handling
- No semantic analysis

**REQUIRED** behavior:

```python
def step(self, human_messages=None, ...):
    # human_messages is IGNORED
    # Only internal dynamics are updated
    ...
```

### 5.7 Control Safety

**PROHIBITED** outputs:

- No control signals
- No activation triggers
- No feedback path indicators
- No modulation commands

**PROHIBITED** connections:

- No connection to external control systems
- No reverse data flow from shell to core

### 5.8 Invariant Summary

| Invariant | Requirement | Verification |
|-----------|-------------|--------------|
| Bounded outputs | All in [0, 1] | `verify_state_bounds()` |
| No NaN/Inf | Numeric validity | Output check |
| Deterministic | Same input → same output | Regression tests |
| Identity-safe | No identity fields | `verify_identity_safety()` |
| Semantic-safe | No text processing | Code review |
| Control-safe | No activation signals | Protocol compliance |

---

## 6. Optional Extensions

### 6.1 v2.1: Multichannel Alignment Fields

A potential v2.1 extension introduces **vector-valued alignment**:

```
Current (v2):
    alignment_field: scalar ∈ [0, 1]
    alignment_direction: scalar ∈ [0, 1]

Extended (v2.1):
    alignment_vector: [a₁, a₂, ..., aₙ] where aᵢ ∈ [0, 1]
    alignment_magnitude: ||alignment_vector||
    alignment_direction: alignment_vector / alignment_magnitude
```

This allows for **multi-dimensional relational structure** while remaining purely numeric.

### 6.2 Extension Compatibility Matrix

| Extension | Protocol Compatible | Output Schema Compatible | Safety Preserved |
|-----------|---------------------|--------------------------|------------------|
| v2.1 (Vector Alignment) | Yes | Yes (magnitude → alignment) | Yes |
| v2.2 (Resonance Patterns) | Yes | Yes (summary → alignment) | Yes |
| v3 (Shape Attractors) | Yes | Yes (projection → outputs) | Yes |
| Future Semantic | TBD | TBD | Required |

---

## 7. Implementation Guidance

### 7.1 Recommended File Structure

```
cfm_core_v2/
├── __init__.py          # Exports CFMCoreV2, CFMCoreV2Config, CFMCoreV2State
├── config.py            # CFMCoreV2Config dataclass
├── state.py             # CFMCoreV2State dataclass with multi-channel structure
├── cfm_core.py          # Main CFMCoreV2 class
└── presets.py           # Pre-tuned parameter configurations
```

### 7.2 Testing Requirements

| Test Category | Required Coverage |
|---------------|-------------------|
| Initialization | Default config, custom config, custom state |
| Bounds | All outputs in [0, 1], no NaN/Inf |
| Determinism | Identical sequences from identical states |
| Protocol | CFMCoreProtocol compliance |
| Adapter | CFMCoreAdapter integration |
| Safety | Identity safety, semantic safety, control safety |
| Dynamics | Channel coupling, attractor behavior, phase responses |

### 7.3 CLI Integration

Update tools to support v2:

```bash
# cfm_local_loop.py
python tools/cfm_local_loop.py --core-type=cfm_v2
```

---

## 8. Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-12-05 | Initial design specification |

---

## 9. References

- [CFM Core v0 Specification](cfm_core_v0_spec.md)
- [CFM Core v1 Specification](cfm_core_v1_spec.md)
- [CFM Core v2 Behavioral Analysis](cfm_core_v2_behavioral_analysis.md)
- [CFM Core v2 Parameter Map](cfm_core_v2_parameter_map.md)
