#!/usr/bin/env python3
"""
CFM Core v1 State

State dataclass for the CFM Core v1 implementation.
Contains the internal continuous variables that evolve over time.

Key differences from v0:
- alignment_phase: Internal phase for resonance dynamics
- coherence_baseline: Slowly-drifting coherence floor
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
class CFMCoreV1State:
    """
    Internal state of CFM Core v1.

    All state variables are maintained in their valid ranges.
    This is a pure data container with no behavioral logic.

    State variables are organized into:
    - Slow variables: coherence, coherence_baseline, energy
    - Fast variables: instability, phase, alignment_phase

    Attributes:
        # Slow variables
        coherence: Field coherence level [0, 1]
        coherence_baseline: Slowly-drifting coherence floor [0, 1]
        energy: Normalized energy level [0, 1]

        # Fast variables
        instability: Inverse stability indicator [0, 1]
        phase: Primary phase position [0, 1) (wraps)
        alignment_phase: Secondary phase for alignment resonance [0, 1) (wraps)

        # Tracking
        time: Accumulated simulation time (>= 0)
        step_count: Number of steps executed (>= 0)
    """

    # Slow variables (all in [0, 1])
    coherence: float = field(default_factory=lambda: 1.0 / PHI)
    coherence_baseline: float = field(default_factory=lambda: 1.0 / PHI)
    energy: float = field(default_factory=lambda: 1.0 / PHI)

    # Fast variables
    instability: float = field(default_factory=lambda: 1.0 / (PHI * PHI))
    phase: float = 0.0
    alignment_phase: float = 0.0

    # Time tracking
    time: float = 0.0
    step_count: int = 0

    def __post_init__(self):
        """Validate state after initialization."""
        self.coherence = _clamp01(self.coherence)
        self.coherence_baseline = _clamp01(self.coherence_baseline)
        self.energy = _clamp01(self.energy)
        self.instability = _clamp01(self.instability)
        self.phase = self.phase % 1.0  # Wrap to [0, 1)
        self.alignment_phase = self.alignment_phase % 1.0  # Wrap to [0, 1)
        self.time = max(0.0, self.time)
        self.step_count = max(0, self.step_count)

    def copy(self) -> "CFMCoreV1State":
        """
        Create a deep copy of the state.

        Returns:
            New CFMCoreV1State with same values
        """
        return CFMCoreV1State(
            coherence=self.coherence,
            coherence_baseline=self.coherence_baseline,
            energy=self.energy,
            instability=self.instability,
            phase=self.phase,
            alignment_phase=self.alignment_phase,
            time=self.time,
            step_count=self.step_count,
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert state to dictionary.

        Returns:
            State as dict
        """
        return {
            "coherence": self.coherence,
            "coherence_baseline": self.coherence_baseline,
            "energy": self.energy,
            "instability": self.instability,
            "phase": self.phase,
            "alignment_phase": self.alignment_phase,
            "time": self.time,
            "step_count": self.step_count,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CFMCoreV1State":
        """
        Create state from dictionary.

        Args:
            data: State data as dict

        Returns:
            New CFMCoreV1State
        """
        return cls(
            coherence=data.get("coherence", 1.0 / PHI),
            coherence_baseline=data.get("coherence_baseline", 1.0 / PHI),
            energy=data.get("energy", 1.0 / PHI),
            instability=data.get("instability", 1.0 / (PHI * PHI)),
            phase=data.get("phase", 0.0),
            alignment_phase=data.get("alignment_phase", 0.0),
            time=data.get("time", 0.0),
            step_count=data.get("step_count", 0),
        )

    def validate(self) -> bool:
        """
        Check if state is valid.

        Returns:
            True if all values are in valid ranges
        """
        return (
            0.0 <= self.coherence <= 1.0
            and 0.0 <= self.coherence_baseline <= 1.0
            and 0.0 <= self.energy <= 1.0
            and 0.0 <= self.instability <= 1.0
            and 0.0 <= self.phase < 1.0
            and 0.0 <= self.alignment_phase < 1.0
            and self.time >= 0.0
            and self.step_count >= 0
        )
