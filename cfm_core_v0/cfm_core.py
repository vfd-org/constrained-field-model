#!/usr/bin/env python3
"""
CFM Core v0 Implementation

A pure numeric dynamical system representing early CFM field dynamics.

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

from .config import CFMCoreConfig
from .state import CFMCoreState


def _clamp01(value: float) -> float:
    """Clamp a value to [0, 1]."""
    return max(0.0, min(1.0, value))


class CFMCore:
    """
    CFM Core v0 - A pure numeric field dynamics system.

    Implements bounded numeric diagnostics based on coupled oscillator
    dynamics with phi/psi scaling.

    The core maintains internal state representing:
    - Coherence: Field coherence level
    - Instability: Inverse stability indicator
    - Energy: Normalized energy level
    - Phase: Oscillation phase position

    All outputs are guaranteed to be in [0, 1] and deterministic.

    Safety Guarantees:
    - No identity fields or derivation
    - No semantic processing
    - No control signal generation
    - Bounded, deterministic outputs
    """

    def __init__(
        self,
        config: Optional[CFMCoreConfig] = None,
        initial_state: Optional[CFMCoreState] = None,
    ):
        """
        Initialize CFM Core v0.

        Args:
            config: Configuration parameters (uses defaults if None)
            initial_state: Initial state (uses defaults if None)
        """
        self.config = config or CFMCoreConfig()
        self._state = initial_state.copy() if initial_state else CFMCoreState()

    def step(
        self,
        human_messages: Optional[List[str]] = None,
        external_events: Optional[Dict[str, Any]] = None,
        dt: float = 1.0,
    ) -> Dict[str, Any]:
        """
        Execute one CFM core step.

        Updates internal state according to phi/psi-based dynamics and
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
        stability = 1.0 - self._state.instability
        intensity = self._state.energy
        alignment = _clamp01((coherence + stability) / 2.0)

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
            # No identity / semantic / control fields
        }

    def _update_state(self, dt: float) -> None:
        """
        Update internal state using phi/psi-based dynamics.

        Args:
            dt: Time delta (already clamped)
        """
        # Increment counters
        self._state.time += dt
        self._state.step_count += 1

        # Phase evolution (wraps at 1.0)
        phase_delta = dt * self.config.omega_base
        self._state.phase = (self._state.phase + phase_delta) % 1.0

        # Energy dynamics: relaxation toward attractor
        # dE/dt = (E_target - E) / tau_energy
        energy_delta = dt * (
            self.config.energy_target - self._state.energy
        ) / (self.config.tau_energy * PHI)
        self._state.energy = _clamp01(self._state.energy + energy_delta)

        # Instability dynamics: driven oscillation with decay
        # dI/dt = (I_base * sin(2*pi * phase) - I) / tau_instability
        phase_angle = 2.0 * PI * self._state.phase
        instability_drive = self.config.instability_base * math.sin(phase_angle)
        instability_delta = dt * (
            instability_drive - self._state.instability
        ) / (self.config.tau_instability / PSI)
        self._state.instability = _clamp01(
            self._state.instability + instability_delta
        )

        # Coherence dynamics: coupled to energy and stability
        # C = (1 - I) * E^(1/phi)
        energy_factor = math.pow(
            max(0.0, self._state.energy), 1.0 / PHI
        )
        target_coherence = (1.0 - self._state.instability) * energy_factor

        # Smooth transition toward target
        coherence_delta = dt * (
            target_coherence - self._state.coherence
        ) / PHI
        self._state.coherence = _clamp01(
            self._state.coherence + coherence_delta
        )

    def reset(self, initial_state: Optional[CFMCoreState] = None) -> None:
        """
        Reset the core to initial state.

        Args:
            initial_state: State to reset to (uses defaults if None)
        """
        self._state = initial_state.copy() if initial_state else CFMCoreState()

    def get_state(self) -> CFMCoreState:
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
        }

    def verify_identity_safety(self) -> bool:
        """
        Verify the core maintains identity safety.

        The CFM Core v0 has no identity by design.

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
