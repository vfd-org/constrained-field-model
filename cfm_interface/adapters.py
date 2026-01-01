#!/usr/bin/env python3
"""
CFM Core Adapter

Provides a safe adapter layer between CFM cores and external tools.
"""

import copy
import math
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List

from .protocols import CFMCoreProtocol
from .config import CFMCoreInterfaceConfig


@dataclass
class CFMCoreAdapter:
    """
    Adapter that wraps a CFMCoreProtocol implementation and provides
    safe, normalized access to its outputs.
    """

    core: CFMCoreProtocol
    config: CFMCoreInterfaceConfig = field(
        default_factory=CFMCoreInterfaceConfig
    )

    _call_count: int = field(default=0, init=False)
    _error_count: int = field(default=0, init=False)
    _last_error: Optional[str] = field(default=None, init=False)

    def step(
        self,
        human_messages: Optional[List[str]] = None,
        external_events: Optional[Dict[str, Any]] = None,
        dt: float = 1.0,
    ) -> Dict[str, Any]:
        """Call the CFM core safely and normalize its outputs."""
        self._call_count += 1
        clamped_dt = max(0.0, min(dt, self.config.max_dt))

        raw_output: Dict[str, Any] = {}
        error_occurred = False
        error_message = None

        try:
            result = self.core.step(
                human_messages=human_messages,
                external_events=external_events,
                dt=clamped_dt,
            )
            if isinstance(result, dict):
                raw_output = result
            else:
                error_occurred = True
                error_message = f"Core returned non-dict: {type(result)}"
        except Exception as e:
            error_occurred = True
            error_message = str(e)

        if error_occurred:
            self._error_count += 1
            self._last_error = error_message

        numeric_state = self._extract_numeric_state(raw_output)

        return {
            "raw": self._safe_copy(raw_output),
            "numeric_state": numeric_state,
            "metadata": {
                "call_count": self._call_count,
                "error_count": self._error_count,
                "last_error": self._last_error if error_occurred else None,
                "dt_clamped": clamped_dt != dt,
                "dt_used": clamped_dt,
            },
        }

    def _extract_numeric_state(self, raw_output: Dict[str, Any]) -> Dict[str, float]:
        """Extract and normalize numeric state from raw core output."""
        numeric_state: Dict[str, float] = {}
        for key in self.config.numeric_keys:
            value = raw_output.get(key, 0.0)
            numeric_state[key] = self._normalize_value(value)
        return numeric_state

    def _normalize_value(self, value: Any) -> float:
        """Normalize a value to float in [0,1]."""
        try:
            v = float(value)
            if math.isnan(v) or math.isinf(v):
                return 0.0
            return max(0.0, min(1.0, v))
        except (TypeError, ValueError):
            return 0.0

    def _safe_copy(self, obj: Any) -> Any:
        """Create a safe, JSON-serializable copy of an object."""
        try:
            return copy.deepcopy(obj)
        except Exception:
            return self._make_serializable(obj)

    def _make_serializable(self, obj: Any) -> Any:
        """Recursively convert an object to JSON-serializable form."""
        if obj is None:
            return None
        elif isinstance(obj, (bool, int, float, str)):
            if isinstance(obj, float) and (math.isnan(obj) or math.isinf(obj)):
                return str(obj)
            return obj
        elif isinstance(obj, dict):
            return {str(k): self._make_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [self._make_serializable(v) for v in obj]
        else:
            return str(obj)

    def get_status(self) -> Dict[str, Any]:
        """Get adapter status for diagnostics."""
        return {
            "call_count": self._call_count,
            "error_count": self._error_count,
            "last_error": self._last_error,
            "config_enabled": self.config.enabled,
            "config_max_dt": self.config.max_dt,
        }

    def reset(self) -> None:
        """Reset adapter state."""
        self._call_count = 0
        self._error_count = 0
        self._last_error = None
