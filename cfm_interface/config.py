#!/usr/bin/env python3
"""
CFM Core Interface Configuration

Provides configuration flags for CFM core integration.
"""

from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class CFMCoreInterfaceConfig:
    """
    Configuration for CFM core interface.

    Attributes:
        enabled: Whether CFM core integration is enabled (default: False)
        use_mock_core: If enabled but no real core, use mock (default: True)
        max_dt: Maximum time delta to clamp dt values (default: 1.0)
        fail_closed: If True, errors in core return safe defaults (default: True)
        numeric_keys: Keys to extract from core output for numeric_state
    """

    enabled: bool = False
    use_mock_core: bool = True
    max_dt: float = 1.0
    fail_closed: bool = True
    numeric_keys: tuple = field(
        default_factory=lambda: ("coherence", "stability", "intensity", "alignment")
    )

    def __post_init__(self):
        """Validate configuration after initialization."""
        if self.max_dt <= 0:
            self.max_dt = 1.0
        if not isinstance(self.numeric_keys, tuple):
            self.numeric_keys = tuple(self.numeric_keys)
