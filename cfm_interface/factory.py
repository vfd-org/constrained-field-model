#!/usr/bin/env python3
"""
CFM Core Factory

Factory function for creating CFM core instances by type name.
"""

import sys
import os
from typing import Any, Dict, Optional, List

# Add parent directory for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .protocols import CFMCoreProtocol


# Available CFM core types
CFM_CORE_TYPES = {
    "cfm": "cfm_core_v0.CFMCore",
    "cfm_v0": "cfm_core_v0.CFMCore",
    "cfm_v1": "cfm_core_v1.CFMCoreV1",
    "cfm_v2": "cfm_core_v2.CFMCoreV2",
}


def list_core_types() -> List[str]:
    """List available CFM core types."""
    return list(CFM_CORE_TYPES.keys())


def create_cfm_core(
    core_type: str = "cfm_v2",
    config: Optional[Any] = None,
    preset: Optional[str] = None,
) -> CFMCoreProtocol:
    """
    Create a CFM core instance by type name.

    Args:
        core_type: Type of core to create. One of:
            - "cfm" or "cfm_v0": CFM Core v0 (basic)
            - "cfm_v1": CFM Core v1 (enhanced slow/fast separation)
            - "cfm_v2": CFM Core v2 (multi-channel, default)
        config: Optional configuration object for the core
        preset: Optional preset name (for v2 only): baseline, high_stability,
                high_resonance, pulsed_activity

    Returns:
        CFMCoreProtocol implementation

    Raises:
        ValueError: If core_type is unknown
    """
    core_type_lower = core_type.lower()

    if core_type_lower not in CFM_CORE_TYPES:
        valid = ", ".join(CFM_CORE_TYPES.keys())
        raise ValueError(f"Unknown core type '{core_type}'. Valid types: {valid}")

    # Create based on type
    if core_type_lower in ("cfm", "cfm_v0"):
        from cfm_core_v0 import CFMCore, CFMCoreConfig
        if config is None:
            config = CFMCoreConfig()
        return CFMCore(config=config)

    elif core_type_lower == "cfm_v1":
        from cfm_core_v1 import CFMCoreV1, CFMCoreV1Config
        if config is None:
            config = CFMCoreV1Config()
        return CFMCoreV1(config=config)

    elif core_type_lower == "cfm_v2":
        from cfm_core_v2 import CFMCoreV2, CFMCoreV2Config, get_preset
        if preset is not None:
            config = get_preset(preset)
        elif config is None:
            config = CFMCoreV2Config()
        return CFMCoreV2(config=config)

    else:
        raise ValueError(f"Unknown core type: {core_type}")
