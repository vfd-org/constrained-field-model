#!/usr/bin/env python3
"""
CFM Core v0 State

State dataclass for the CFM Core v0 implementation.
Contains the internal continuous variables that evolve over time.
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
class CFMCoreState:
    """
    Internal state of CFM Core v0.

    All state variables are maintained in their valid ranges.
    This is a pure data container with no behavioral logic.

    Attributes:
        coherence: Field coherence level [0, 1]
        instability: Inverse stability indicator [0, 1]
        energy: Normalized energy level [0, 1]
        phase: Normalized phase position [0, 1) (wraps)
        time: Accumulated simulation time (>= 0)
        step_count: Number of steps executed (>= 0)
    """

    # Core field variables (all in [0, 1])
    coherence: float = field(default_factory=lambda: 1.0 / PHI)
    instability: float = field(default_factory=lambda: 1.0 / (PHI * PHI))
    energy: float = field(default_factory=lambda: 1.0 / PHI)
    phase: float = 0.0

    # Time tracking
    time: float = 0.0
    step_count: int = 0

    def __post_init__(self):
        """Validate state after initialization."""
        self.coherence = _clamp01(self.coherence)
        self.instability = _clamp01(self.instability)
        self.energy = _clamp01(self.energy)
        self.phase = self.phase % 1.0  # Wrap to [0, 1)
        self.time = max(0.0, self.time)
        self.step_count = max(0, self.step_count)

    def copy(self) -> "CFMCoreState":
        """
        Create a deep copy of the state.

        Returns:
            New CFMCoreState with same values
        """
        return CFMCoreState(
            coherence=self.coherence,
            instability=self.instability,
            energy=self.energy,
            phase=self.phase,
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
            "instability": self.instability,
            "energy": self.energy,
            "phase": self.phase,
            "time": self.time,
            "step_count": self.step_count,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CFMCoreState":
        """
        Create state from dictionary.

        Args:
            data: State data as dict

        Returns:
            New CFMCoreState
        """
        return cls(
            coherence=data.get("coherence", 1.0 / PHI),
            instability=data.get("instability", 1.0 / (PHI * PHI)),
            energy=data.get("energy", 1.0 / PHI),
            phase=data.get("phase", 0.0),
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
            and 0.0 <= self.instability <= 1.0
            and 0.0 <= self.energy <= 1.0
            and 0.0 <= self.phase < 1.0
            and self.time >= 0.0
            and self.step_count >= 0
        )
