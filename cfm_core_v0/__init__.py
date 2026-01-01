#!/usr/bin/env python3
"""
CFM Core v0 Package

A pure numeric dynamical system implementing early CFM field dynamics.

This package provides:
- CFMCore: The main core implementation
- CFMCoreConfig: Configuration dataclass
- CFMCoreState: Internal state dataclass

Usage:
    from cfm_core_v0 import CFMCore, CFMCoreConfig, CFMCoreState

    config = CFMCoreConfig()
    core = CFMCore(config)
    result = core.step(dt=0.1)

Safety Guarantees:
- All outputs bounded in [0, 1]
- No identity fields or derivation
- No semantic processing
- No control signal generation
- Fully deterministic
"""

from .config import CFMCoreConfig
from .state import CFMCoreState
from .cfm_core import CFMCore

__all__ = [
    "CFMCore",
    "CFMCoreConfig",
    "CFMCoreState",
]

__version__ = "0.1.0"
