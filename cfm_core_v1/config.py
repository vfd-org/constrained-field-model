#!/usr/bin/env python3
"""
CFM Core v1 Configuration

Configuration dataclass for the CFM Core v1 implementation.
All default values are derived from phi, psi, or simple fractions thereof.

Key differences from v0:
- Separate time constants for slow (coherence, energy) and fast (instability, phase) variables
- Coherence has independent attractor dynamics
- Alignment has resonance/lock-in parameters
"""

from dataclasses import dataclass, field
import sys
import os

# Add parent directory for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cfm_consts import PHI, PSI


@dataclass
class CFMCoreV1Config:
    """
    Configuration for CFM Core v1.

    All parameters have defaults derived from mathematical constants
    (phi, psi, pi, e) or simple integers, ensuring mathematical purity.

    The configuration introduces slow/fast variable separation:
    - Slow variables (coherence, energy): larger time constants
    - Fast variables (instability, phase): smaller time constants

    Attributes:
        # Slow variable time constants
        tau_coherence: Coherence evolution time constant (slow, default: phi^2)
        tau_energy: Energy relaxation time constant (slow, default: phi)

        # Fast variable time constants
        tau_instability: Instability decay time constant (fast, default: 1/phi)
        omega_phase: Phase evolution frequency (default: 1/phi)

        # Attractor values
        coherence_target: Coherence attractor under stable conditions (default: ~0.7)
        energy_target: Energy attractor value (default: 1/phi)
        stability_baseline: Baseline stability level (default: ~0.8)

        # Coupling parameters
        coherence_decay_rate: Rate of coherence decay under instability (default: 1/psi)
        alignment_lock_strength: Strength of alignment lock-in (default: 1/phi)
        intensity_coherence_coupling: How much coherence affects intensity (default: 1/(2*phi))

        # Instability dynamics
        instability_base: Base instability amplitude (default: 1/(2*phi))

        # Bounds
        max_dt: Maximum allowed time step (default: 1.0)
    """

    # Slow variable time constants (larger = slower evolution)
    tau_coherence: float = field(default_factory=lambda: PHI * PHI)
    tau_energy: float = field(default_factory=lambda: PHI)

    # Fast variable time constants (smaller = faster evolution)
    tau_instability: float = field(default_factory=lambda: 1.0 / PHI)
    omega_phase: float = field(default_factory=lambda: 1.0 / PHI)

    # Attractor values
    coherence_target: float = field(default_factory=lambda: 1.0 / PHI + 0.1)  # ~0.718
    energy_target: float = field(default_factory=lambda: 1.0 / PHI)  # ~0.618
    stability_baseline: float = field(default_factory=lambda: 1.0 - 1.0 / (PHI * PHI))  # ~0.8

    # Coupling parameters
    coherence_decay_rate: float = field(default_factory=lambda: 1.0 / PSI)
    alignment_lock_strength: float = field(default_factory=lambda: 1.0 / PHI)
    intensity_coherence_coupling: float = field(default_factory=lambda: 1.0 / (2.0 * PHI))

    # Instability dynamics
    instability_base: float = field(default_factory=lambda: 1.0 / (2.0 * PHI))

    # Bounds
    max_dt: float = 1.0

    def __post_init__(self):
        """Validate configuration after initialization."""
        # Ensure positive time constants
        if self.tau_coherence <= 0:
            self.tau_coherence = PHI * PHI
        if self.tau_energy <= 0:
            self.tau_energy = PHI
        if self.tau_instability <= 0:
            self.tau_instability = 1.0 / PHI

        # Ensure omega_phase is positive
        if self.omega_phase <= 0:
            self.omega_phase = 1.0 / PHI

        # Ensure attractor values are in [0, 1]
        self.coherence_target = max(0.0, min(1.0, self.coherence_target))
        self.energy_target = max(0.0, min(1.0, self.energy_target))
        self.stability_baseline = max(0.0, min(1.0, self.stability_baseline))

        # Ensure coupling parameters are in reasonable ranges
        self.coherence_decay_rate = max(0.0, min(2.0, self.coherence_decay_rate))
        self.alignment_lock_strength = max(0.0, min(1.0, self.alignment_lock_strength))
        self.intensity_coherence_coupling = max(0.0, min(0.5, self.intensity_coherence_coupling))

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
            "tau_coherence": self.tau_coherence,
            "tau_energy": self.tau_energy,
            "tau_instability": self.tau_instability,
            "omega_phase": self.omega_phase,
            "coherence_target": self.coherence_target,
            "energy_target": self.energy_target,
            "stability_baseline": self.stability_baseline,
            "coherence_decay_rate": self.coherence_decay_rate,
            "alignment_lock_strength": self.alignment_lock_strength,
            "intensity_coherence_coupling": self.intensity_coherence_coupling,
            "instability_base": self.instability_base,
            "max_dt": self.max_dt,
        }
