#!/usr/bin/env python3
"""
CFM Core v2 Configuration

Configuration dataclass for the CFM Core v2 implementation.
All default values are derived from phi, psi, or simple fractions thereof.

Key v2 configuration features:
- Five-tier timescale hierarchy (very slow to very fast)
- Attractor basin parameters
- Cross-channel coupling strengths
- Instability pulse thresholds
"""

from dataclasses import dataclass, field
import sys
import os

# Add parent directory for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cfm_consts import PHI, PSI, PI


@dataclass
class CFMCoreV2Config:
    """
    Configuration for CFM Core v2.

    All parameters have defaults derived from mathematical constants
    (phi, psi, pi, e) or simple integers, ensuring mathematical purity.

    The configuration implements the five-tier timescale hierarchy:
    - Very Slow (tau_vs): phi^3 ~ 4.24
    - Slow (tau_s): phi^2 ~ 2.62
    - Medium (tau_m): phi ~ 1.62
    - Fast (tau_f): 1/phi ~ 0.62
    - Very Fast (tau_vf): 1/phi^2 ~ 0.38
    """

    # Timescale constants (five-tier hierarchy)
    tau_very_slow: float = field(default_factory=lambda: PHI ** 3)  # ~4.24
    tau_slow: float = field(default_factory=lambda: PHI ** 2)  # ~2.62
    tau_medium: float = field(default_factory=lambda: PHI)  # ~1.62
    tau_fast: float = field(default_factory=lambda: 1.0 / PHI)  # ~0.62
    tau_very_fast: float = field(default_factory=lambda: 1.0 / (PHI ** 2))  # ~0.38

    # Phase frequencies
    omega_global: float = field(default_factory=lambda: 1.0 / PHI)
    omega_local: float = field(default_factory=lambda: PHI / (PHI ** 2))  # = 1/phi

    # Attractor basin parameters
    basin_center_c: float = field(default_factory=lambda: 1.0 / PHI)  # ~0.618
    basin_center_e: float = field(default_factory=lambda: 1.0 / PHI)  # ~0.618
    basin_center_s: float = field(default_factory=lambda: 1.0 - 1.0 / (PHI ** 2))  # ~0.618
    basin_radius: float = field(default_factory=lambda: 1.0 / (PHI ** 2))  # ~0.38
    basin_strength_inner: float = field(default_factory=lambda: 1.0 / (PHI ** 2))
    basin_strength_outer: float = field(default_factory=lambda: 1.0 / (PHI ** 3))

    # Target values
    coherence_target: float = field(default_factory=lambda: 1.0 / PHI + 0.1)  # ~0.718
    energy_target: float = field(default_factory=lambda: 1.0 / PHI)  # ~0.618
    stability_target: float = field(default_factory=lambda: 1.0 - 1.0 / (PHI ** 2))  # ~0.618
    alignment_target: float = field(default_factory=lambda: 1.0 / PHI)  # ~0.618

    # Coupling strengths
    coherence_energy_coupling: float = field(default_factory=lambda: 1.0 / (2.0 * PHI))
    stability_coherence_coupling: float = field(default_factory=lambda: 1.0 / PHI)
    alignment_stability_coupling: float = field(default_factory=lambda: 1.0 / PHI)
    resonance_coupling: float = field(default_factory=lambda: 1.0 / (PHI ** 2))

    # Instability parameters
    instability_base: float = field(default_factory=lambda: 1.0 / (2.0 * PHI))
    pulse_threshold_low: float = field(default_factory=lambda: 1.0 / (PHI ** 2))  # ~0.38
    pulse_threshold_medium: float = field(default_factory=lambda: 1.0 / PHI)  # ~0.62
    pulse_threshold_high: float = field(default_factory=lambda: 1.0 - 1.0 / (PHI ** 2))  # ~0.62

    # Damping and decay
    energy_dissipation: float = field(default_factory=lambda: 1.0 / (PHI ** 2))
    envelope_decay: float = field(default_factory=lambda: 1.0 / (PHI ** 3))
    flux_damping: float = field(default_factory=lambda: 1.0 / PHI)

    # Lock-in parameters
    alignment_lock_strength: float = field(default_factory=lambda: 1.0 / PHI)

    # Bounds
    max_dt: float = 1.0

    def __post_init__(self):
        """Validate configuration after initialization."""
        # Ensure positive time constants
        if self.tau_very_slow <= 0:
            self.tau_very_slow = PHI ** 3
        if self.tau_slow <= 0:
            self.tau_slow = PHI ** 2
        if self.tau_medium <= 0:
            self.tau_medium = PHI
        if self.tau_fast <= 0:
            self.tau_fast = 1.0 / PHI
        if self.tau_very_fast <= 0:
            self.tau_very_fast = 1.0 / (PHI ** 2)

        # Ensure positive frequencies
        if self.omega_global <= 0:
            self.omega_global = 1.0 / PHI
        if self.omega_local <= 0:
            self.omega_local = 1.0 / PHI

        # Ensure target values are in [0, 1]
        self.coherence_target = max(0.0, min(1.0, self.coherence_target))
        self.energy_target = max(0.0, min(1.0, self.energy_target))
        self.stability_target = max(0.0, min(1.0, self.stability_target))
        self.alignment_target = max(0.0, min(1.0, self.alignment_target))

        # Ensure basin parameters are valid
        self.basin_center_c = max(0.0, min(1.0, self.basin_center_c))
        self.basin_center_e = max(0.0, min(1.0, self.basin_center_e))
        self.basin_center_s = max(0.0, min(1.0, self.basin_center_s))
        self.basin_radius = max(0.01, min(0.5, self.basin_radius))

        # Ensure coupling strengths are in reasonable ranges
        self.coherence_energy_coupling = max(0.0, min(1.0, self.coherence_energy_coupling))
        self.stability_coherence_coupling = max(0.0, min(1.0, self.stability_coherence_coupling))
        self.alignment_stability_coupling = max(0.0, min(1.0, self.alignment_stability_coupling))
        self.resonance_coupling = max(0.0, min(1.0, self.resonance_coupling))

        # Ensure instability_base is in [0, 0.5]
        self.instability_base = max(0.0, min(0.5, self.instability_base))

        # Ensure pulse thresholds are ordered and in [0, 1]
        self.pulse_threshold_low = max(0.0, min(1.0, self.pulse_threshold_low))
        self.pulse_threshold_medium = max(self.pulse_threshold_low, min(1.0, self.pulse_threshold_medium))
        self.pulse_threshold_high = max(self.pulse_threshold_medium, min(1.0, self.pulse_threshold_high))

        # Ensure max_dt is positive
        if self.max_dt <= 0:
            self.max_dt = 1.0

    def to_dict(self) -> dict:
        """Convert configuration to dictionary."""
        return {
            # Timescale constants
            "tau_very_slow": self.tau_very_slow,
            "tau_slow": self.tau_slow,
            "tau_medium": self.tau_medium,
            "tau_fast": self.tau_fast,
            "tau_very_fast": self.tau_very_fast,
            # Phase frequencies
            "omega_global": self.omega_global,
            "omega_local": self.omega_local,
            # Basin parameters
            "basin_center_c": self.basin_center_c,
            "basin_center_e": self.basin_center_e,
            "basin_center_s": self.basin_center_s,
            "basin_radius": self.basin_radius,
            "basin_strength_inner": self.basin_strength_inner,
            "basin_strength_outer": self.basin_strength_outer,
            # Target values
            "coherence_target": self.coherence_target,
            "energy_target": self.energy_target,
            "stability_target": self.stability_target,
            "alignment_target": self.alignment_target,
            # Coupling strengths
            "coherence_energy_coupling": self.coherence_energy_coupling,
            "stability_coherence_coupling": self.stability_coherence_coupling,
            "alignment_stability_coupling": self.alignment_stability_coupling,
            "resonance_coupling": self.resonance_coupling,
            # Instability
            "instability_base": self.instability_base,
            "pulse_threshold_low": self.pulse_threshold_low,
            "pulse_threshold_medium": self.pulse_threshold_medium,
            "pulse_threshold_high": self.pulse_threshold_high,
            # Damping
            "energy_dissipation": self.energy_dissipation,
            "envelope_decay": self.envelope_decay,
            "flux_damping": self.flux_damping,
            # Lock-in
            "alignment_lock_strength": self.alignment_lock_strength,
            # Bounds
            "max_dt": self.max_dt,
        }
