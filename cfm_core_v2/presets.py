#!/usr/bin/env python3
"""
CFM Core v2 Presets

Named preset configurations for CFM Core v2, providing tuned parameter sets
for specific behavioral profiles.

Available Presets:
- CFM_V2_PRESET_BASELINE: Default configuration (reference)
- CFM_V2_PRESET_HIGH_STABILITY: Emphasizes stability, reduced oscillation
- CFM_V2_PRESET_HIGH_RESONANCE: Strong cross-channel coupling
- CFM_V2_PRESET_PULSED_ACTIVITY: More frequent instability pulses

Usage:
    from cfm_core_v2 import CFMCoreV2
    from cfm_core_v2.presets import CFM_V2_PRESET_HIGH_STABILITY

    core = CFMCoreV2(CFM_V2_PRESET_HIGH_STABILITY)
"""

import sys
import os

# Add parent directory for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cfm_consts import PHI, PSI

from .config import CFMCoreV2Config


# =============================================================================
# PRESET: BASELINE
# =============================================================================

CFM_V2_PRESET_BASELINE = CFMCoreV2Config()
"""Baseline preset - default CFM Core v2 configuration."""


# =============================================================================
# PRESET: HIGH STABILITY
# =============================================================================

CFM_V2_PRESET_HIGH_STABILITY = CFMCoreV2Config(
    stability_target=1.0 / PHI + 0.2,
    stability_coherence_coupling=min(1.0, (1.0 / PHI) * 1.5),
    instability_base=1.0 / (3.0 * PHI),
    pulse_threshold_low=1.0 / PHI,
    pulse_threshold_medium=1.0 / PHI + 0.2,
    pulse_threshold_high=1.0 - 1.0 / (2.0 * PHI ** 2),
    envelope_decay=1.0 / (PHI ** 2),
    tau_very_slow=PHI ** 4,
    alignment_lock_strength=1.0 / PHI + 0.1,
)
"""High Stability preset - emphasizes stability and reduces oscillation."""


# =============================================================================
# PRESET: HIGH RESONANCE
# =============================================================================

CFM_V2_PRESET_HIGH_RESONANCE = CFMCoreV2Config(
    resonance_coupling=1.0 / PHI,
    coherence_energy_coupling=1.0 / PHI,
    stability_coherence_coupling=1.0 - 1.0 / (PHI ** 2),
    alignment_stability_coupling=1.0 - 1.0 / (PHI ** 2),
    alignment_lock_strength=1.0 / PHI,
    basin_radius=1.0 / (PHI ** 3),
    basin_strength_inner=1.0 / PHI,
    basin_strength_outer=1.0 / (PHI ** 2),
)
"""High Resonance preset - emphasizes cross-channel coupling and resonance."""


# =============================================================================
# PRESET: PULSED ACTIVITY
# =============================================================================

CFM_V2_PRESET_PULSED_ACTIVITY = CFMCoreV2Config(
    instability_base=1.0 / PHI,
    pulse_threshold_low=1.0 / (PHI ** 3),
    pulse_threshold_medium=1.0 / (PHI ** 2),
    pulse_threshold_high=1.0 / PHI,
    energy_dissipation=1.0 / PHI,
    envelope_decay=1.0 / (PHI ** 2),
    tau_very_fast=1.0 / (PHI ** 3),
    tau_fast=1.0 / (PHI ** 2),
    basin_radius=1.0 / PHI,
    basin_strength_inner=1.0 / (PHI ** 3),
)
"""Pulsed Activity preset - more frequent and prominent instability pulses."""


# =============================================================================
# PRESET REGISTRY
# =============================================================================

CFM_V2_PRESETS = {
    "baseline": CFM_V2_PRESET_BASELINE,
    "high_stability": CFM_V2_PRESET_HIGH_STABILITY,
    "high_resonance": CFM_V2_PRESET_HIGH_RESONANCE,
    "pulsed_activity": CFM_V2_PRESET_PULSED_ACTIVITY,
}
"""Registry of all CFM v2 presets by name."""


def get_preset(name: str) -> CFMCoreV2Config:
    """
    Get a preset configuration by name.

    Args:
        name: Preset name (baseline, high_stability, high_resonance, pulsed_activity)

    Returns:
        CFMCoreV2Config instance for the requested preset

    Raises:
        ValueError: If preset name is unknown
    """
    name_lower = name.lower().replace("-", "_").replace(" ", "_")
    if name_lower not in CFM_V2_PRESETS:
        valid = ", ".join(CFM_V2_PRESETS.keys())
        raise ValueError(f"Unknown preset '{name}'. Valid presets: {valid}")
    return CFM_V2_PRESETS[name_lower]


def list_presets() -> list:
    """List all available preset names."""
    return list(CFM_V2_PRESETS.keys())


__all__ = [
    "CFM_V2_PRESET_BASELINE",
    "CFM_V2_PRESET_HIGH_STABILITY",
    "CFM_V2_PRESET_HIGH_RESONANCE",
    "CFM_V2_PRESET_PULSED_ACTIVITY",
    "CFM_V2_PRESETS",
    "get_preset",
    "list_presets",
]
