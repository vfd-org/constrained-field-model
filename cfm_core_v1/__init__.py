#!/usr/bin/env python3
"""
CFM Core v1 Package

An enhanced numeric dynamical system implementing CFM field dynamics
with clearer slow/fast variable separation and more interpretable trajectories.

This package provides:
- CFMCoreV1: The main core implementation
- CFMCoreV1Config: Configuration dataclass
- CFMCoreV1State: Internal state dataclass

Changes from v0:
- Coherence has independent slow dynamics (drifts upward, decays on instability)
- Stability exhibits regime-like behavior (stable band vs transient excursions)
- Intensity correlates with coherence (baseline + activation patterns)
- Alignment has resonance-like dynamics with lock-in behavior

Usage:
    from cfm_core_v1 import CFMCoreV1, CFMCoreV1Config, CFMCoreV1State

    config = CFMCoreV1Config()
    core = CFMCoreV1(config)
    result = core.step(dt=0.1)

Safety Guarantees:
- All outputs bounded in [0, 1]
- No identity fields or derivation
- No semantic processing
- No control signal generation
- Fully deterministic
"""

from .config import CFMCoreV1Config
from .state import CFMCoreV1State
from .cfm_core import CFMCoreV1

__all__ = [
    "CFMCoreV1",
    "CFMCoreV1Config",
    "CFMCoreV1State",
]

__version__ = "1.0.0"
