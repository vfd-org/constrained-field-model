#!/usr/bin/env python3
"""
CFM Core v1 Implementation

An enhanced numeric dynamical system representing CFM field dynamics.

Key improvements over v0:
- Clearer slow/fast variable separation
- Coherence has independent dynamics (drift up, decay on instability)
- Alignment has resonance-like lock-in behavior
- More interpretable trajectories

This implementation:
- Uses phi/psi-based update equations
- Maintains all outputs in [0, 1]
- Is fully deterministic
- Contains no identity, semantic, or control logic
"""

import math
from typing import Dict, Any, Optional, List
import sys
import os

# Add parent directory for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cfm_consts import PHI, PSI, PI

from .config import CFMCoreV1Config
from .state import CFMCoreV1State


def _clamp01(value: float) -> float:
    """Clamp a value to [0, 1]."""
    return max(0.0, min(1.0, value))


def _smooth_step(x: float, edge0: float = 0.0, edge1: float = 1.0) -> float:
    """
    Smooth step function (Hermite interpolation).
    Returns 0 for x <= edge0, 1 for x >= edge1, smooth transition between.
    """
    x = _clamp01((x - edge0) / (edge1 - edge0))
    return x * x * (3.0 - 2.0 * x)


class CFMCoreV1:
    """
    CFM Core v1 - An enhanced numeric field dynamics system.

    Provides bounded numeric diagnostics based on coupled dynamics
    with phi/psi scaling and slow/fast separation.

    Key behavioral improvements:
    - Coherence: Slow drift toward attractor, decay on instability
    - Stability: Regime-like behavior with stable bands
    - Intensity: Correlates with coherence, baseline + activation
    - Alignment: Resonance lock-in when conditions are favorable

    All outputs are guaranteed to be in [0, 1] and deterministic.

    Safety Guarantees:
    - No identity fields or derivation
    - No semantic processing
    - No control signal generation
    - Bounded, deterministic outputs
    """

    def __init__(
        self,
        config: Optional[CFMCoreV1Config] = None,
        initial_state: Optional[CFMCoreV1State] = None,
    ):
        """
        Initialize CFM Core v1.

        Args:
            config: Configuration parameters (uses defaults if None)
            initial_state: Initial state (uses defaults if None)
        """
        self.config = config or CFMCoreV1Config()
        self._state = initial_state.copy() if initial_state else CFMCoreV1State()

    def step(
        self,
        human_messages: Optional[List[str]] = None,
        external_events: Optional[Dict[str, Any]] = None,
        dt: float = 1.0,
    ) -> Dict[str, Any]:
        """
        Execute one CFM core step.

        Updates internal state according to v1 dynamics and
        returns bounded numeric diagnostics.

        Args:
            human_messages: Ignored (no semantic processing)
            external_events: Ignored (pure internal dynamics)
            dt: Time delta since last step (clamped to [0, max_dt])

        Returns:
            Dict with coherence, stability, intensity, alignment
            all bounded in [0, 1], plus metadata.

        Contract:
            - Returns a dict (never None, never raises)
            - Does not mutate inputs
            - No identity information in output
            - Deterministic for same state + dt
        """
        # Clamp dt to safe range
        dt = max(0.0, min(dt, self.config.max_dt))

        # Update internal state
        self._update_state(dt)

        # Compute output values
        coherence = self._state.coherence
        stability = self._compute_stability()
        intensity = self._compute_intensity()
        alignment = self._compute_alignment(coherence, stability)

        # Return protocol-compliant output
        return {
            # Required fields (all in [0, 1])
            "coherence": coherence,
            "stability": stability,
            "intensity": intensity,
            "alignment": alignment,
            # Metadata (safe to include)
            "cfm_time": self._state.time,
            "cfm_step": self._state.step_count,
            "cfm_phase": self._state.phase,
            "cfm_version": 1,
            # No identity / semantic / control fields
        }

    def _update_state(self, dt: float) -> None:
        """
        Update internal state using v1 dynamics.

        Implements slow/fast variable separation:
        - Fast: phase, instability (quick oscillations)
        - Slow: coherence, energy, coherence_baseline (gradual drift)

        Args:
            dt: Time delta (already clamped)
        """
        # Increment counters
        self._state.time += dt
        self._state.step_count += 1

        # === FAST VARIABLES ===

        # Phase evolution (fast, wraps at 1.0)
        phase_delta = dt * self.config.omega_phase
        self._state.phase = (self._state.phase + phase_delta) % 1.0

        # Alignment phase evolution (slightly different frequency for resonance patterns)
        alignment_phase_delta = dt * self.config.omega_phase * PSI
        self._state.alignment_phase = (
            self._state.alignment_phase + alignment_phase_delta
        ) % 1.0

        # Instability dynamics (fast, sinusoidal drive with decay)
        # Uses smoother dynamics than v0 for regime-like behavior
        phase_angle = 2.0 * PI * self._state.phase
        instability_drive = self.config.instability_base * (
            0.5 + 0.5 * math.sin(phase_angle)  # Always positive, smoother
        )

        # Instability decays toward drive value
        instability_delta = dt * (
            instability_drive - self._state.instability
        ) / self.config.tau_instability
        self._state.instability = _clamp01(
            self._state.instability + instability_delta
        )

        # === SLOW VARIABLES ===

        # Energy dynamics: slow relaxation toward attractor
        energy_delta = dt * (
            self.config.energy_target - self._state.energy
        ) / self.config.tau_energy
        self._state.energy = _clamp01(self._state.energy + energy_delta)

        # Coherence baseline: very slow drift toward target
        # This provides the "slowly-charging capacitor" behavior
        baseline_delta = dt * (
            self.config.coherence_target - self._state.coherence_baseline
        ) / (self.config.tau_coherence * PHI)
        self._state.coherence_baseline = _clamp01(
            self._state.coherence_baseline + baseline_delta
        )

        # Coherence dynamics: follows baseline but is affected by instability
        # Under stable conditions: drift upward toward baseline
        # Under instability: decay
        stability_factor = 1.0 - self._state.instability
        target_coherence = self._state.coherence_baseline * stability_factor

        # Energy also contributes to coherence (like v0, but slower)
        energy_contribution = math.pow(max(0.0, self._state.energy), 1.0 / PHI)
        target_coherence = _clamp01(target_coherence * energy_contribution)

        # Smooth transition toward target
        if target_coherence > self._state.coherence:
            # Building coherence (slow)
            coherence_delta = dt * (
                target_coherence - self._state.coherence
            ) / self.config.tau_coherence
        else:
            # Decaying coherence (faster, scaled by instability)
            decay_rate = self.config.coherence_decay_rate * (
                1.0 + self._state.instability
            )
            coherence_delta = dt * (
                target_coherence - self._state.coherence
            ) * decay_rate / self.config.tau_coherence

        self._state.coherence = _clamp01(
            self._state.coherence + coherence_delta
        )

    def _compute_stability(self) -> float:
        """
        Compute stability output with regime-like behavior.

        Returns:
            Stability value in [0, 1]
        """
        # Base stability is inverse of instability
        base_stability = 1.0 - self._state.instability

        # Apply smoothing to create regime-like behavior
        # High stability tends to stay high (stable band)
        # Low stability recovers gradually
        if base_stability > self.config.stability_baseline:
            # In stable regime: smooth toward baseline
            return _clamp01(
                base_stability * 0.9 + self.config.stability_baseline * 0.1
            )
        else:
            # Below baseline: full instability effect visible
            return _clamp01(base_stability)

    def _compute_intensity(self) -> float:
        """
        Compute intensity output with coherence correlation.

        Intensity = baseline (from energy) + coherence modulation

        Returns:
            Intensity value in [0, 1]
        """
        # Baseline from energy
        baseline = self._state.energy

        # Coherence modulation: higher coherence enables higher intensity
        coherence_boost = self._state.coherence * self.config.intensity_coherence_coupling

        # Small phase-locked variation for "activation" pattern
        phase_angle = 2.0 * PI * self._state.phase
        activation = 0.05 * (1.0 + math.sin(phase_angle * PHI)) * self._state.coherence

        return _clamp01(baseline + coherence_boost + activation)

    def _compute_alignment(self, coherence: float, stability: float) -> float:
        """
        Compute alignment output with resonance-like dynamics.

        Alignment exhibits lock-in behavior when coherence and stability are high.

        Args:
            coherence: Current coherence output
            stability: Current stability output

        Returns:
            Alignment value in [0, 1]
        """
        # Base alignment (like v0)
        base_alignment = (coherence + stability) / 2.0

        # Lock-in factor: how strongly conditions favor lock-in
        # High when both coherence and stability are high
        lock_in_potential = coherence * stability

        # Lock-in threshold: above this, alignment stabilizes
        threshold = self.config.alignment_lock_strength

        if lock_in_potential > threshold:
            # Lock-in regime: alignment tends toward high stable value
            # The stronger lock_in_potential, the more stable
            lock_strength = _smooth_step(lock_in_potential, threshold, 1.0)
            target = threshold + (1.0 - threshold) * lock_strength
            alignment = base_alignment * (1.0 - lock_strength) + target * lock_strength
        else:
            # Drift regime: alignment varies with phase
            phase_angle = 2.0 * PI * self._state.alignment_phase
            drift = 0.1 * math.sin(phase_angle) * (1.0 - lock_in_potential)
            alignment = base_alignment + drift

        return _clamp01(alignment)

    def reset(self, initial_state: Optional[CFMCoreV1State] = None) -> None:
        """
        Reset the core to initial state.

        Args:
            initial_state: State to reset to (uses defaults if None)
        """
        self._state = initial_state.copy() if initial_state else CFMCoreV1State()

    def get_state(self) -> CFMCoreV1State:
        """
        Get a copy of the current internal state.

        Returns:
            Copy of internal state
        """
        return self._state.copy()

    def get_status(self) -> Dict[str, Any]:
        """
        Get core status for diagnostics.

        Returns:
            Status dict
        """
        return {
            "state": self._state.to_dict(),
            "config": self.config.to_dict(),
            "version": 1,
        }

    def verify_identity_safety(self) -> bool:
        """
        Verify the core maintains identity safety.

        The CFM Core v1 has no identity by design.

        Returns:
            Always True
        """
        return True

    def verify_state_bounds(self) -> bool:
        """
        Verify all state variables are in valid ranges.

        Returns:
            True if all values are bounded correctly
        """
        return self._state.validate()
