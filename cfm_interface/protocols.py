#!/usr/bin/env python3
"""
CFM Core Protocol Definition

Defines the protocol (interface contract) that any CFM core implementation
must satisfy.
"""

from typing import Protocol, List, Dict, Any, Optional, runtime_checkable


@runtime_checkable
class CFMCoreProtocol(Protocol):
    """
    Protocol defining the interface for CFM core implementations.

    Requirements:
    - step() must be a pure function of (internal_state, inputs)
    - All outputs must be JSON-serializable
    - Inputs MUST NOT be mutated
    """

    def step(
        self,
        human_messages: Optional[List[str]] = None,
        external_events: Optional[Dict[str, Any]] = None,
        dt: float = 1.0,
    ) -> Dict[str, Any]:
        """
        Execute one CFM core step.

        Args:
            human_messages: Optional list of input messages (ignored by CFM cores)
            external_events: Optional dict of external event data (ignored by CFM cores)
            dt: Time delta since last step (seconds)

        Returns:
            A JSON-serializable dict containing at minimum:
            - coherence: float in [0,1]
            - stability: float in [0,1]
            - intensity: float in [0,1]
            - alignment: float in [0,1]

        Contract:
            - MUST return a dict (never None, never raise for normal input)
            - MUST NOT mutate human_messages or external_events
            - MUST produce deterministic output for same input + internal state
        """
        ...
