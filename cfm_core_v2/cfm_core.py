#!/usr/bin/env python3
"""
CFM Core v2 Implementation

An advanced numeric dynamical system with multi-channel architecture,
attractor manifold dynamics, and structured phase responses.

Key v2 Features:
- Multi-channel state organization (Coherence, Energy, Stability, Phase, Alignment)
- Five-tier timescale hierarchy (very slow to very fast)
- Attractor basin dynamics in 3D (coherence, energy, stability) space
- Structured instability pulse responses
- Cross-channel resonance coupling

Safety Guarantees:
- No identity fields or derivation
- No semantic processing
- No control signal generation
- Bounded, deterministic outputs
"""

import math
from typing import Dict, Any, Optional, List
import sys
import os

# Add parent directory for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cfm_consts import PHI, PSI, PI

from .config import CFMCoreV2Config
from .state import CFMCoreV2State


def _clamp01(value: float) -> float:
    """Clamp a value to [0, 1]."""
    return max(0.0, min(1.0, value))


def _smooth_step(x: float, edge0: float = 0.0, edge1: float = 1.0) -> float:
    """Smooth step function (Hermite interpolation)."""
    if edge1 == edge0:
        return 1.0 if x >= edge1 else 0.0
    x = _clamp01((x - edge0) / (edge1 - edge0))
    return x * x * (3.0 - 2.0 * x)


class CFMCoreV2:
    """
    CFM Core v2 - Multi-channel numeric field dynamics system.

    All outputs are guaranteed to be in [0, 1] and deterministic.
    """

    def __init__(
        self,
        config: Optional[CFMCoreV2Config] = None,
        initial_state: Optional[CFMCoreV2State] = None,
    ):
        """Initialize CFM Core v2."""
        self.config = config or CFMCoreV2Config()
        self._state = initial_state.copy() if initial_state else CFMCoreV2State()

    def step(
        self,
        human_messages: Optional[List[str]] = None,
        external_events: Optional[Dict[str, Any]] = None,
        dt: float = 1.0,
    ) -> Dict[str, Any]:
        """Execute one CFM core v2 step."""
        dt = max(0.0, min(dt, self.config.max_dt))
        self._update_state(dt)

        coherence = self._compute_coherence_output()
        stability = self._compute_stability_output()
        intensity = self._compute_intensity_output()
        alignment = self._compute_alignment_output()

        return {
            "coherence": coherence,
            "stability": stability,
            "intensity": intensity,
            "alignment": alignment,
            "cfm_time": self._state.time,
            "cfm_step": self._state.step_count,
            "cfm_phase": self._state.phase_global,
            "cfm_version": 2,
            "cfm_resonance_index": self._state.resonance_index,
            "cfm_basin_distance": self._state.get_distance_to_basin(
                self.config.basin_center_c,
                self.config.basin_center_e,
                self.config.basin_center_s,
            ),
        }

    def _update_state(self, dt: float) -> None:
        """Update internal state using v2 multi-channel dynamics."""
        self._state.time += dt
        self._state.step_count += 1

        prev_coherence_slow = self._state.coherence_slow
        prev_energy_potential = self._state.energy_potential
        prev_stability_envelope = self._state.stability_envelope

        # Very fast -> Fast -> Medium -> Slow -> Very slow
        self._update_phase_local(dt)
        self._update_phase_global(dt)
        self._update_instability_pulse(dt)
        self._update_coherence_fast(dt)
        self._update_energy_flux(dt)
        self._update_resonance_index(dt)
        self._update_alignment_field(dt)
        self._update_coherence_slow(dt, prev_stability_envelope)
        self._update_energy_potential(dt, prev_coherence_slow)
        self._update_stability_envelope(dt, prev_coherence_slow)
        self._update_alignment_direction(dt)
        self._apply_pulse_response()

    def _update_phase_global(self, dt: float) -> None:
        phase_delta = dt * self.config.omega_global / self.config.tau_fast
        self._state.phase_global = (self._state.phase_global + phase_delta) % 1.0

    def _update_phase_local(self, dt: float) -> None:
        modulation = 1.0 + 0.2 * math.sin(2.0 * PI * self._state.phase_global)
        phase_delta = dt * self.config.omega_local * modulation / self.config.tau_very_fast
        self._state.phase_local = (self._state.phase_local + phase_delta) % 1.0

    def _phase_modulation(self) -> float:
        global_contrib = 0.5 + 0.5 * math.sin(2.0 * PI * self._state.phase_global)
        local_contrib = 0.5 + 0.5 * math.sin(2.0 * PI * self._state.phase_local)
        return _clamp01(global_contrib * (1.0 / PHI) + local_contrib * (1.0 - 1.0 / PHI))

    def _update_instability_pulse(self, dt: float) -> None:
        base_amplitude = self.config.instability_base * (1.0 - self._state.stability_envelope)
        phase_angle = 2.0 * PI * self._state.phase_global
        pulse_drive = base_amplitude * (0.5 + 0.5 * math.sin(phase_angle))
        threshold = self._state.stability_envelope * self.config.pulse_threshold_low

        if pulse_drive > threshold:
            target_pulse = pulse_drive
        else:
            target_pulse = pulse_drive * 0.3

        pulse_delta = dt * (target_pulse - self._state.instability_pulse) / self.config.tau_fast
        self._state.instability_pulse = _clamp01(self._state.instability_pulse + pulse_delta)

    def _update_stability_envelope(self, dt: float, prev_coherence: float) -> None:
        coherence_factor = _smooth_step(prev_coherence, 0.3, 0.8)
        target = self.config.stability_target * coherence_factor
        alignment_decay = self.config.envelope_decay * (1.0 - self._state.alignment_field)
        basin_attraction = self._basin_attraction(
            self._state.stability_envelope,
            self.config.basin_center_s,
        )

        envelope_delta = dt * (
            (target - self._state.stability_envelope) / self.config.tau_slow
            - alignment_decay
            + basin_attraction
        )
        self._state.stability_envelope = _clamp01(self._state.stability_envelope + envelope_delta)

    def _update_coherence_slow(self, dt: float, prev_stability: float) -> None:
        energy_factor = _smooth_step(self._state.energy_potential, 0.2, 0.8)
        instability_effect = self.config.coherence_energy_coupling * self._state.instability_pulse
        basin_attraction = self._basin_attraction(
            self._state.coherence_slow,
            self.config.basin_center_c,
        )

        coherence_delta = dt * (
            (self.config.coherence_target - self._state.coherence_slow) * energy_factor
            - instability_effect
            + basin_attraction
        ) / self.config.tau_slow

        self._state.coherence_slow = _clamp01(self._state.coherence_slow + coherence_delta)

    def _update_coherence_fast(self, dt: float) -> None:
        phase_mod = self._phase_modulation()
        tracking_term = phase_mod * (self._state.coherence_slow - self._state.coherence_fast)
        resonance_term = self._state.resonance_index * self._state.alignment_field * 0.1
        coherence_delta = dt * (tracking_term + resonance_term) / self.config.tau_fast
        self._state.coherence_fast = _clamp01(self._state.coherence_fast + coherence_delta)

    def _update_energy_potential(self, dt: float, prev_coherence: float) -> None:
        dissipation = self._state.energy_flux * self.config.energy_dissipation
        coherence_input = self.config.coherence_energy_coupling * prev_coherence
        basin_attraction = self._basin_attraction(
            self._state.energy_potential,
            self.config.basin_center_e,
        )

        energy_delta = dt * (
            (self.config.energy_target - self._state.energy_potential)
            - dissipation
            + coherence_input
            + basin_attraction
        ) / self.config.tau_slow

        self._state.energy_potential = _clamp01(self._state.energy_potential + energy_delta)

    def _update_energy_flux(self, dt: float) -> None:
        gradient = abs(self._state.energy_potential - self.config.energy_target)
        phase_angle = 2.0 * PI * self._state.phase_global
        phase_mod = 0.5 + 0.5 * math.sin(phase_angle)
        target_flux = gradient * phase_mod
        damping = self.config.flux_damping * self._state.energy_flux
        flux_delta = dt * (target_flux - damping - self._state.energy_flux) / self.config.tau_fast
        self._state.energy_flux = _clamp01(self._state.energy_flux + flux_delta)

    def _update_alignment_field(self, dt: float) -> None:
        coherence_out = self._compute_coherence_output()
        stability_out = self._compute_stability_output()
        lock_in_potential = coherence_out * stability_out

        target_attraction = lock_in_potential * (
            self.config.alignment_target - self._state.alignment_field
        )

        direction_coupling = (
            self.config.resonance_coupling *
            (self._state.alignment_direction - 0.5) *
            self._state.resonance_index
        )

        field_delta = dt * (target_attraction + direction_coupling) / self.config.tau_medium
        self._state.alignment_field = _clamp01(self._state.alignment_field + field_delta)

    def _update_alignment_direction(self, dt: float) -> None:
        basin_center_direction = self.config.basin_center_c
        stability_factor = _smooth_step(self._state.stability_envelope, 0.3, 0.8)
        direction_drift = (basin_center_direction - self._state.alignment_direction) * stability_factor
        direction_delta = dt * direction_drift / self.config.tau_very_slow
        self._state.alignment_direction = _clamp01(self._state.alignment_direction + direction_delta)

    def _update_resonance_index(self, dt: float) -> None:
        if self._state.coherence_slow > 0.01:
            coherence_ratio = self._state.coherence_fast / self._state.coherence_slow
            coherence_correlation = 1.0 - abs(1.0 - coherence_ratio)
        else:
            coherence_correlation = 0.5

        if self._state.energy_potential > 0.01:
            energy_ratio = self._state.energy_flux / self._state.energy_potential
            energy_correlation = 1.0 - abs(0.5 - energy_ratio)
        else:
            energy_correlation = 0.5

        stability_correlation = 1.0 - self._state.instability_pulse * self._state.stability_envelope
        phase_diff = abs(self._state.phase_global - self._state.phase_local)
        phase_coherence = 1.0 - 2.0 * min(phase_diff, 1.0 - phase_diff)

        target_resonance = (
            coherence_correlation * (1.0 / PHI) +
            energy_correlation * (1.0 / (PHI ** 2)) +
            stability_correlation * (1.0 / (PHI ** 2)) +
            phase_coherence * (1.0 / (PHI ** 3))
        )

        target_resonance = _clamp01(target_resonance / (1.0 / PHI + 2.0 / (PHI ** 2) + 1.0 / (PHI ** 3)))
        resonance_delta = dt * (target_resonance - self._state.resonance_index) / self.config.tau_medium
        self._state.resonance_index = _clamp01(self._state.resonance_index + resonance_delta)

    def _basin_attraction(self, x: float, mu: float) -> float:
        """Compute basin attraction force."""
        distance = abs(x - mu)
        direction = 1.0 if mu > x else -1.0

        r_inner = self.config.basin_radius / PHI
        if distance < r_inner:
            return direction * self.config.basin_strength_inner * distance

        r_outer = self.config.basin_radius * PHI
        if distance < r_outer:
            return direction * self.config.basin_strength_outer

        return 0.0

    def _apply_pulse_response(self) -> None:
        """Apply structured pulse response based on instability level."""
        pulse = self._state.instability_pulse

        if pulse > self.config.pulse_threshold_high:
            self._state.coherence_fast = _clamp01(
                self._state.coherence_fast - 0.1 * (pulse - self.config.pulse_threshold_high)
            )
            self._state.energy_flux = _clamp01(
                self._state.energy_flux + 0.15 * (pulse - self.config.pulse_threshold_high)
            )
            self._state.alignment_field = _clamp01(
                self._state.alignment_field - 0.08 * (pulse - self.config.pulse_threshold_high)
            )
            self._state.coherence_slow = _clamp01(
                self._state.coherence_slow - 0.02 * (pulse - self.config.pulse_threshold_high)
            )

        elif pulse > self.config.pulse_threshold_medium:
            self._state.coherence_fast = _clamp01(
                self._state.coherence_fast - 0.05 * (pulse - self.config.pulse_threshold_medium)
            )
            self._state.energy_flux = _clamp01(
                self._state.energy_flux + 0.08 * (pulse - self.config.pulse_threshold_medium)
            )
            self._state.alignment_field = _clamp01(
                self._state.alignment_field - 0.03 * (pulse - self.config.pulse_threshold_medium)
            )

        elif pulse > self.config.pulse_threshold_low:
            self._state.coherence_fast = _clamp01(
                self._state.coherence_fast - 0.02 * (pulse - self.config.pulse_threshold_low)
            )

    def _compute_coherence_output(self) -> float:
        alpha = _smooth_step(self._state.stability_envelope, 0.3, 0.8)
        coherence = alpha * self._state.coherence_slow + (1.0 - alpha) * self._state.coherence_fast
        return _clamp01(coherence)

    def _compute_stability_output(self) -> float:
        base = self._state.stability_envelope
        pulse_effect = self._state.instability_pulse * (1.0 - self._state.stability_envelope)
        resonance_boost = self._state.resonance_index * 0.1
        stability = base - pulse_effect + resonance_boost
        return _clamp01(stability)

    def _compute_intensity_output(self) -> float:
        base = self._state.energy_potential
        flux_contrib = self._state.energy_flux * 0.3
        coherence_out = self._compute_coherence_output()
        coherence_boost = coherence_out * 0.2
        phase_angle = 2.0 * PI * self._state.phase_global
        phase_variation = 0.05 * (1.0 + math.sin(phase_angle * PHI)) * coherence_out
        intensity = base + flux_contrib + coherence_boost + phase_variation
        return _clamp01(intensity)

    def _compute_alignment_output(self) -> float:
        base = self._state.alignment_field
        direction_bias = (self._state.alignment_direction - 0.5) * 0.1
        resonance_boost = self._state.resonance_index * 0.15
        coherence_out = self._compute_coherence_output()
        stability_out = self._compute_stability_output()
        lock_in_potential = coherence_out * stability_out

        if lock_in_potential > self.config.alignment_lock_strength:
            lock_strength = _smooth_step(
                lock_in_potential,
                self.config.alignment_lock_strength,
                1.0
            )
            target = self.config.alignment_lock_strength + (1.0 - self.config.alignment_lock_strength) * lock_strength
            alignment = base * (1.0 - lock_strength) + target * lock_strength
        else:
            alignment = base + direction_bias + resonance_boost

        return _clamp01(alignment)

    def reset(self, initial_state: Optional[CFMCoreV2State] = None) -> None:
        """Reset the core to initial state."""
        self._state = initial_state.copy() if initial_state else CFMCoreV2State()

    def get_state(self) -> CFMCoreV2State:
        """Get a copy of the current internal state."""
        return self._state.copy()

    def get_status(self) -> Dict[str, Any]:
        """Get core status for diagnostics."""
        return {
            "state": self._state.to_dict(),
            "config": self.config.to_dict(),
            "version": 2,
            "channels": {
                "coherence": self._state.get_channel_coherence(),
                "energy": self._state.get_channel_energy(),
                "stability": self._state.get_channel_stability(),
                "phase": self._state.get_channel_phase(),
                "alignment": self._state.get_channel_alignment(),
            },
            "basin_distance": self._state.get_distance_to_basin(
                self.config.basin_center_c,
                self.config.basin_center_e,
                self.config.basin_center_s,
            ),
        }

    def verify_identity_safety(self) -> bool:
        """The CFM Core v2 has no identity by design."""
        return True

    def verify_state_bounds(self) -> bool:
        """Verify all state variables are in valid ranges."""
        return self._state.validate()

    def get_channel_states(self) -> Dict[str, Dict[str, float]]:
        """Get all channel states organized by channel."""
        return {
            "coherence": self._state.get_channel_coherence(),
            "energy": self._state.get_channel_energy(),
            "stability": self._state.get_channel_stability(),
            "phase": self._state.get_channel_phase(),
            "alignment": self._state.get_channel_alignment(),
            "resonance": {"index": self._state.resonance_index},
        }
