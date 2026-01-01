#!/usr/bin/env python3
"""
CFM Interface Package

Provides the interface layer for CFM core integration:
- CFMCoreProtocol: Protocol defining the CFM core interface
- CFMCoreAdapter: Safe adapter wrapping CFM cores
- CFMCoreInterfaceConfig: Configuration for the interface
- create_cfm_core: Factory function for creating CFM cores
"""

from .protocols import CFMCoreProtocol
from .adapters import CFMCoreAdapter
from .config import CFMCoreInterfaceConfig
from .factory import create_cfm_core, list_core_types

__all__ = [
    "CFMCoreProtocol",
    "CFMCoreAdapter",
    "CFMCoreInterfaceConfig",
    "create_cfm_core",
    "list_core_types",
]
