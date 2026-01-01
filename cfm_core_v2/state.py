#!/usr/bin/env python3
"""
CFM Core v2 State

State dataclass for the CFM Core v2 implementation.
Contains the 11 internal continuous variables organized into five channels.

Multi-Channel Architecture:
- Coherence Channel: coherence_slow, coherence_fast
- Energy Channel: energy_potential, energy_flux
- Stability Channel: stability_envelope, instability_pulse
- Phase Channel: phase_global, phase_local
- Alignment Channel: alignment_field, alignment_direction
- Resonance: resonance_index
"""

from dataclasses import dataclass, field
from typing import Dict, Any
import sys
import os

# Add parent directory for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cfm_consts import PHI


def _clamp01(value: float) -> float:
    """Clamp a value to [0, 1]."""
    return max(0.0, min(1.0, value))


@dataclass
class CFMCoreV2State:
    """
    Internal state of CFM Core v2.

    All state variables are maintained in their valid ranges.
    This is a pure data container with no behavioral logic.

    State variables are organized into five channels plus resonance.
    """

    # ===== Coherence Channel =====
    coherence_slow: float = field(default_factory=lambda: 1.0 / PHI)
    coherence_fast: float = field(default_factory=lambda: 1.0 / PHI)

    # ===== Energy Channel =====
    energy_potential: float = field(default_factory=lambda: 1.0 / PHI)
    energy_flux: float = field(default_factory=lambda: 1.0 / (PHI ** 2))

    # ===== Stability Channel =====
    stability_envelope: float = field(default_factory=lambda: 1.0 - 1.0 / (PHI ** 2))
    instability_pulse: float = field(default_factory=lambda: 1.0 / (PHI ** 2))

    # ===== Phase Channel =====
    phase_global: float = 0.0
    phase_local: float = 0.0

    # ===== Alignment Channel =====
    alignment_field: float = field(default_factory=lambda: 1.0 / PHI)
    alignment_direction: float = field(default_factory=lambda: 1.0 / PHI)

    # ===== Resonance =====
    resonance_index: float = field(default_factory=lambda: 1.0 / PHI)

    # ===== Time Tracking =====
    time: float = 0.0
    step_count: int = 0

    def __post_init__(self):
        """Validate state after initialization."""
        self.coherence_slow = _clamp01(self.coherence_slow)
        self.coherence_fast = _clamp01(self.coherence_fast)
        self.energy_potential = _clamp01(self.energy_potential)
        self.energy_flux = _clamp01(self.energy_flux)
        self.stability_envelope = _clamp01(self.stability_envelope)
        self.instability_pulse = _clamp01(self.instability_pulse)
        self.alignment_field = _clamp01(self.alignment_field)
        self.alignment_direction = _clamp01(self.alignment_direction)
        self.resonance_index = _clamp01(self.resonance_index)
        self.phase_global = self.phase_global % 1.0
        self.phase_local = self.phase_local % 1.0
        self.time = max(0.0, self.time)
        self.step_count = max(0, self.step_count)

    def copy(self) -> "CFMCoreV2State":
        """Create a deep copy of the state."""
        return CFMCoreV2State(
            coherence_slow=self.coherence_slow,
            coherence_fast=self.coherence_fast,
            energy_potential=self.energy_potential,
            energy_flux=self.energy_flux,
            stability_envelope=self.stability_envelope,
            instability_pulse=self.instability_pulse,
            phase_global=self.phase_global,
            phase_local=self.phase_local,
            alignment_field=self.alignment_field,
            alignment_direction=self.alignment_direction,
            resonance_index=self.resonance_index,
            time=self.time,
            step_count=self.step_count,
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert state to dictionary."""
        return {
            "coherence_slow": self.coherence_slow,
            "coherence_fast": self.coherence_fast,
            "energy_potential": self.energy_potential,
            "energy_flux": self.energy_flux,
            "stability_envelope": self.stability_envelope,
            "instability_pulse": self.instability_pulse,
            "phase_global": self.phase_global,
            "phase_local": self.phase_local,
            "alignment_field": self.alignment_field,
            "alignment_direction": self.alignment_direction,
            "resonance_index": self.resonance_index,
            "time": self.time,
            "step_count": self.step_count,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CFMCoreV2State":
        """Create state from dictionary."""
        return cls(
            coherence_slow=data.get("coherence_slow", 1.0 / PHI),
            coherence_fast=data.get("coherence_fast", 1.0 / PHI),
            energy_potential=data.get("energy_potential", 1.0 / PHI),
            energy_flux=data.get("energy_flux", 1.0 / (PHI ** 2)),
            stability_envelope=data.get("stability_envelope", 1.0 - 1.0 / (PHI ** 2)),
            instability_pulse=data.get("instability_pulse", 1.0 / (PHI ** 2)),
            phase_global=data.get("phase_global", 0.0),
            phase_local=data.get("phase_local", 0.0),
            alignment_field=data.get("alignment_field", 1.0 / PHI),
            alignment_direction=data.get("alignment_direction", 1.0 / PHI),
            resonance_index=data.get("resonance_index", 1.0 / PHI),
            time=data.get("time", 0.0),
            step_count=data.get("step_count", 0),
        )

    def validate(self) -> bool:
        """Check if state is valid."""
        bounded_valid = (
            0.0 <= self.coherence_slow <= 1.0
            and 0.0 <= self.coherence_fast <= 1.0
            and 0.0 <= self.energy_potential <= 1.0
            and 0.0 <= self.energy_flux <= 1.0
            and 0.0 <= self.stability_envelope <= 1.0
            and 0.0 <= self.instability_pulse <= 1.0
            and 0.0 <= self.alignment_field <= 1.0
            and 0.0 <= self.alignment_direction <= 1.0
            and 0.0 <= self.resonance_index <= 1.0
        )
        phase_valid = (
            0.0 <= self.phase_global < 1.0
            and 0.0 <= self.phase_local < 1.0
        )
        tracking_valid = self.time >= 0.0 and self.step_count >= 0
        return bounded_valid and phase_valid and tracking_valid

    def get_channel_coherence(self) -> Dict[str, float]:
        """Get coherence channel variables."""
        return {"slow": self.coherence_slow, "fast": self.coherence_fast}

    def get_channel_energy(self) -> Dict[str, float]:
        """Get energy channel variables."""
        return {"potential": self.energy_potential, "flux": self.energy_flux}

    def get_channel_stability(self) -> Dict[str, float]:
        """Get stability channel variables."""
        return {"envelope": self.stability_envelope, "pulse": self.instability_pulse}

    def get_channel_phase(self) -> Dict[str, float]:
        """Get phase channel variables."""
        return {"global": self.phase_global, "local": self.phase_local}

    def get_channel_alignment(self) -> Dict[str, float]:
        """Get alignment channel variables."""
        return {"field": self.alignment_field, "direction": self.alignment_direction}

    def get_distance_to_basin(
        self,
        basin_c: float = None,
        basin_e: float = None,
        basin_s: float = None,
    ) -> float:
        """Compute Euclidean distance to basin center in (C, E, S) space."""
        if basin_c is None:
            basin_c = 1.0 / PHI
        if basin_e is None:
            basin_e = 1.0 / PHI
        if basin_s is None:
            basin_s = 1.0 - 1.0 / (PHI ** 2)

        dc = self.coherence_slow - basin_c
        de = self.energy_potential - basin_e
        ds = self.stability_envelope - basin_s

        return (dc ** 2 + de ** 2 + ds ** 2) ** 0.5
