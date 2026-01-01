#!/usr/bin/env python3
"""
Tests for CFM Core v0

Comprehensive test suite covering:
1. Initialization - Config, State, Core creation
2. Step behaviour - Bounded outputs, no NaN/Inf
3. Determinism - Identical sequences for identical inputs
4. Adapter integration - Works with CFMCoreAdapter
5. Safety invariants
"""

import json
import math
import sys
import os
import unittest

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cfm_core_v0 import CFMCore, CFMCoreConfig, CFMCoreState
from cfm_interface.adapters import CFMCoreAdapter
from cfm_interface.config import CFMCoreInterfaceConfig
from cfm_interface.protocols import CFMCoreProtocol
from cfm_consts import PHI, PSI


class TestCFMCoreConfig(unittest.TestCase):
    """Tests for CFMCoreConfig."""

    def test_default_values(self):
        """Test that default values are derived from phi/psi."""
        config = CFMCoreConfig()
        self.assertAlmostEqual(config.tau_energy, PHI, places=10)
        self.assertAlmostEqual(config.tau_instability, PHI * PHI, places=10)
        self.assertAlmostEqual(config.omega_base, 1.0 / PHI, places=10)
        self.assertEqual(config.max_dt, 1.0)

    def test_to_dict(self):
        """Test conversion to dictionary."""
        config = CFMCoreConfig()
        d = config.to_dict()
        self.assertIn("tau_energy", d)
        self.assertIn("omega_base", d)


class TestCFMCoreState(unittest.TestCase):
    """Tests for CFMCoreState."""

    def test_default_values(self):
        """Test default state values are in valid ranges."""
        state = CFMCoreState()
        self.assertTrue(0.0 <= state.coherence <= 1.0)
        self.assertTrue(0.0 <= state.instability <= 1.0)
        self.assertTrue(0.0 <= state.energy <= 1.0)
        self.assertTrue(0.0 <= state.phase < 1.0)

    def test_copy(self):
        """Test state copy is independent."""
        state1 = CFMCoreState(coherence=0.5, energy=0.7)
        state2 = state1.copy()
        state2.coherence = 0.9
        self.assertEqual(state1.coherence, 0.5)

    def test_validate(self):
        """Test validation method."""
        state = CFMCoreState()
        self.assertTrue(state.validate())


class TestCFMCoreInitialization(unittest.TestCase):
    """Tests for CFMCore initialization."""

    def test_default_initialization(self):
        """Test core can be created with defaults."""
        core = CFMCore()
        self.assertIsNotNone(core.config)
        self.assertIsNotNone(core._state)

    def test_implements_protocol(self):
        """Test that CFMCore implements CFMCoreProtocol."""
        core = CFMCore()
        self.assertIsInstance(core, CFMCoreProtocol)


class TestCFMCoreStep(unittest.TestCase):
    """Tests for CFMCore step behaviour."""

    def setUp(self):
        self.core = CFMCore()

    def test_step_returns_dict(self):
        """Test that step returns a dictionary."""
        result = self.core.step(dt=0.1)
        self.assertIsInstance(result, dict)

    def test_step_has_required_keys(self):
        """Test that step result has all required keys."""
        result = self.core.step(dt=0.1)
        self.assertIn("coherence", result)
        self.assertIn("stability", result)
        self.assertIn("intensity", result)
        self.assertIn("alignment", result)

    def test_outputs_bounded_single_step(self):
        """Test outputs are in [0, 1] after one step."""
        result = self.core.step(dt=0.1)
        for key in ["coherence", "stability", "intensity", "alignment"]:
            self.assertGreaterEqual(result[key], 0.0, f"{key} below 0")
            self.assertLessEqual(result[key], 1.0, f"{key} above 1")

    def test_outputs_bounded_many_steps(self):
        """Test outputs remain in [0, 1] after many steps."""
        for i in range(1000):
            result = self.core.step(dt=0.1)
            for key in ["coherence", "stability", "intensity", "alignment"]:
                self.assertGreaterEqual(result[key], 0.0, f"Step {i}: {key} below 0")
                self.assertLessEqual(result[key], 1.0, f"Step {i}: {key} above 1")

    def test_no_nan_inf(self):
        """Test no NaN or Inf values appear."""
        for _ in range(500):
            result = self.core.step(dt=0.1)
            for key in ["coherence", "stability", "intensity", "alignment"]:
                self.assertFalse(math.isnan(result[key]), f"{key} is NaN")
                self.assertFalse(math.isinf(result[key]), f"{key} is Inf")


class TestCFMCoreDeterminism(unittest.TestCase):
    """Tests for CFMCore determinism."""

    def test_identical_sequences(self):
        """Test that two cores with same config produce identical sequences."""
        config = CFMCoreConfig()
        state = CFMCoreState()
        core1 = CFMCore(config, state.copy())
        core2 = CFMCore(config, state.copy())

        for i in range(100):
            result1 = core1.step(dt=0.1)
            result2 = core2.step(dt=0.1)
            self.assertEqual(result1["coherence"], result2["coherence"],
                           f"Coherence mismatch at step {i}")

    def test_reset_reproduces_sequence(self):
        """Test that reset allows reproducing the same sequence."""
        core = CFMCore()
        results1 = [core.step(dt=0.1) for _ in range(50)]
        core.reset()
        results2 = [core.step(dt=0.1) for _ in range(50)]
        for i, (r1, r2) in enumerate(zip(results1, results2)):
            self.assertEqual(r1["coherence"], r2["coherence"],
                           f"Coherence mismatch at step {i}")


class TestCFMCoreAdapterIntegration(unittest.TestCase):
    """Tests for CFMCore with CFMCoreAdapter."""

    def test_adapter_wraps_core(self):
        """Test that adapter can wrap CFMCore."""
        core = CFMCore()
        adapter_config = CFMCoreInterfaceConfig(enabled=True)
        adapter = CFMCoreAdapter(core=core, config=adapter_config)
        self.assertIsNotNone(adapter)

    def test_adapter_step_returns_bundle(self):
        """Test that adapter step returns expected bundle structure."""
        core = CFMCore()
        adapter_config = CFMCoreInterfaceConfig(enabled=True)
        adapter = CFMCoreAdapter(core=core, config=adapter_config)
        result = adapter.step(dt=0.1)
        self.assertIn("raw", result)
        self.assertIn("numeric_state", result)
        self.assertIn("metadata", result)

    def test_adapter_numeric_state_bounded(self):
        """Test that adapter output numeric_state is bounded."""
        core = CFMCore()
        adapter_config = CFMCoreInterfaceConfig(enabled=True)
        adapter = CFMCoreAdapter(core=core, config=adapter_config)

        for _ in range(100):
            result = adapter.step(dt=0.1)
            for key in ["coherence", "stability", "intensity", "alignment"]:
                self.assertGreaterEqual(result["numeric_state"][key], 0.0)
                self.assertLessEqual(result["numeric_state"][key], 1.0)

    def test_adapter_json_serializable(self):
        """Test that adapter output is JSON serializable."""
        core = CFMCore()
        adapter_config = CFMCoreInterfaceConfig(enabled=True)
        adapter = CFMCoreAdapter(core=core, config=adapter_config)

        for _ in range(20):
            result = adapter.step(dt=0.1)
            try:
                json_str = json.dumps(result)
                self.assertIsInstance(json_str, str)
            except (TypeError, ValueError) as e:
                self.fail(f"Output not JSON serializable: {e}")


class TestCFMCoreSafety(unittest.TestCase):
    """Tests for CFMCore safety invariants."""

    def test_verify_identity_safety(self):
        """Test identity safety verification."""
        core = CFMCore()
        self.assertTrue(core.verify_identity_safety())

    def test_verify_state_bounds(self):
        """Test state bounds verification."""
        core = CFMCore()
        for _ in range(100):
            core.step(dt=0.1)
            self.assertTrue(core.verify_state_bounds())


if __name__ == "__main__":
    unittest.main(verbosity=2)
