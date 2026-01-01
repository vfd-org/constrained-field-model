#!/usr/bin/env python3
"""
CFM Core v2 Package

An advanced numeric dynamical system with multi-channel architecture,
attractor manifold dynamics, and structured phase responses.

This package provides:
- CFMCoreV2: The main core implementation
- CFMCoreV2Config: Configuration parameters
- CFMCoreV2State: Internal state dataclass

Key v2 Features:
- Multi-channel state organization (Coherence, Energy, Stability, Phase, Alignment)
- Five-tier timescale hierarchy (very slow to very fast)
- Attractor basin dynamics in 3D (coherence, energy, stability) space
- Structured instability pulse responses
- Cross-channel resonance coupling

All outputs remain bounded in [0, 1], deterministic, and protocol-compliant.

Safety Guarantees:
- No identity fields or derivation
- No semantic processing
- No control signal generation
- Bounded, deterministic outputs
"""

from .config import CFMCoreV2Config
from .state import CFMCoreV2State
from .cfm_core import CFMCoreV2
from .presets import (
    CFM_V2_PRESET_BASELINE,
    CFM_V2_PRESET_HIGH_STABILITY,
    CFM_V2_PRESET_HIGH_RESONANCE,
    CFM_V2_PRESET_PULSED_ACTIVITY,
    CFM_V2_PRESETS,
    get_preset,
    list_presets,
)

__all__ = [
    "CFMCoreV2",
    "CFMCoreV2Config",
    "CFMCoreV2State",
    "CFM_V2_PRESET_BASELINE",
    "CFM_V2_PRESET_HIGH_STABILITY",
    "CFM_V2_PRESET_HIGH_RESONANCE",
    "CFM_V2_PRESET_PULSED_ACTIVITY",
    "CFM_V2_PRESETS",
    "get_preset",
    "list_presets",
]

__version__ = "2.0.0"
