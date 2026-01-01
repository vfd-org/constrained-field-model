#!/usr/bin/env python3
"""
CFM Core v0 Configuration

Configuration dataclass for the CFM Core v0 implementation.
All default values are derived from phi, psi, or simple fractions thereof.
"""

from dataclasses import dataclass, field
import sys
import os

# Add parent directory for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cfm_consts import PHI, PSI


@dataclass
class CFMCoreConfig:
    """
    Configuration for CFM Core v0.

    All parameters have defaults derived from mathematical constants
    (phi, psi, pi, e) or simple integers, ensuring mathematical purity.

    Attributes:
        tau_energy: Energy relaxation time constant (default: phi)
        tau_instability: Instability relaxation time constant (default: phi^2)
        omega_base: Base phase frequency (default: 1/phi)
        energy_target: Energy attractor value (default: 1/phi)
        instability_base: Base instability amplitude (default: 1/(2*phi))
        max_dt: Maximum allowed time step (default: 1.0)
    """

    # Time constants (phi-scaled)
    tau_energy: float = field(default_factory=lambda: PHI)
    tau_instability: float = field(default_factory=lambda: PHI * PHI)

    # Frequency and amplitude
    omega_base: float = field(default_factory=lambda: 1.0 / PHI)
    energy_target: float = field(default_factory=lambda: 1.0 / PHI)
    instability_base: float = field(default_factory=lambda: 1.0 / (2.0 * PHI))

    # Bounds
    max_dt: float = 1.0

    def __post_init__(self):
        """Validate configuration after initialization."""
        # Ensure positive time constants
        if self.tau_energy <= 0:
            self.tau_energy = PHI
        if self.tau_instability <= 0:
            self.tau_instability = PHI * PHI

        # Ensure omega_base is positive
        if self.omega_base <= 0:
            self.omega_base = 1.0 / PHI

        # Ensure energy_target is in [0, 1]
        self.energy_target = max(0.0, min(1.0, self.energy_target))

        # Ensure instability_base is in [0, 0.5]
        self.instability_base = max(0.0, min(0.5, self.instability_base))

        # Ensure max_dt is positive
        if self.max_dt <= 0:
            self.max_dt = 1.0

    def to_dict(self) -> dict:
        """
        Convert configuration to dictionary.

        Returns:
            Configuration as dict
        """
        return {
            "tau_energy": self.tau_energy,
            "tau_instability": self.tau_instability,
            "omega_base": self.omega_base,
            "energy_target": self.energy_target,
            "instability_base": self.instability_base,
            "max_dt": self.max_dt,
        }
