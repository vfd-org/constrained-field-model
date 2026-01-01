#!/usr/bin/env python3
"""
Tests for CFM Core v1

Comprehensive test suite covering:
1. Initialization - Config, State, Core creation
2. Step behaviour - Bounded outputs, no NaN/Inf
3. Determinism - Identical sequences for identical inputs
4. Adapter integration - Works with CFMCoreAdapter
5. Safety invariants
6. v1-specific dynamics (slow/fast separation, lock-in)
"""

import json
import math
import sys
import os
import unittest

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cfm_core_v1 import CFMCoreV1, CFMCoreV1Config, CFMCoreV1State
from cfm_interface.adapters import CFMCoreAdapter
from cfm_interface.config import CFMCoreInterfaceConfig
from cfm_interface.protocols import CFMCoreProtocol
from cfm_consts import PHI, PSI


class TestCFMCoreV1Config(unittest.TestCase):
    """Tests for CFMCoreV1Config."""

    def test_default_values(self):
        """Test that default values are derived from phi/psi."""
        config = CFMCoreV1Config()
        self.assertAlmostEqual(config.tau_coherence, PHI * PHI, places=10)
        self.assertAlmostEqual(config.tau_energy, PHI, places=10)
        self.assertAlmostEqual(config.tau_instability, 1.0 / PHI, places=10)
        self.assertAlmostEqual(config.omega_phase, 1.0 / PHI, places=10)
        self.assertEqual(config.max_dt, 1.0)

    def test_slow_fast_separation(self):
        """Test that slow time constants are larger than fast ones."""
        config = CFMCoreV1Config()
        # Slow time constants should be larger (slower evolution)
        self.assertGreater(config.tau_coherence, config.tau_instability)
        self.assertGreater(config.tau_energy, config.tau_instability)

    def test_to_dict(self):
        """Test conversion to dictionary."""
        config = CFMCoreV1Config()
        d = config.to_dict()
        self.assertIn("tau_coherence", d)
        self.assertIn("tau_energy", d)
        self.assertIn("alignment_lock_strength", d)
        self.assertIn("coherence_decay_rate", d)


class TestCFMCoreV1State(unittest.TestCase):
    """Tests for CFMCoreV1State."""

    def test_default_values(self):
        """Test default state values are in valid ranges."""
        state = CFMCoreV1State()
        self.assertTrue(0.0 <= state.coherence <= 1.0)
        self.assertTrue(0.0 <= state.coherence_baseline <= 1.0)
        self.assertTrue(0.0 <= state.energy <= 1.0)
        self.assertTrue(0.0 <= state.instability <= 1.0)
        self.assertTrue(0.0 <= state.phase < 1.0)
        self.assertTrue(0.0 <= state.alignment_phase < 1.0)

    def test_copy(self):
        """Test state copy is independent."""
        state1 = CFMCoreV1State(coherence=0.5, energy=0.7)
        state2 = state1.copy()
        state2.coherence = 0.9
        self.assertEqual(state1.coherence, 0.5)

    def test_validate(self):
        """Test validation method."""
        state = CFMCoreV1State()
        self.assertTrue(state.validate())

    def test_from_dict(self):
        """Test state creation from dictionary."""
        data = {
            "coherence": 0.6,
            "coherence_baseline": 0.7,
            "energy": 0.5,
            "instability": 0.1,
            "phase": 0.25,
            "alignment_phase": 0.3,
            "time": 10.0,
            "step_count": 100,
        }
        state = CFMCoreV1State.from_dict(data)
        self.assertEqual(state.coherence, 0.6)
        self.assertEqual(state.energy, 0.5)
        self.assertEqual(state.step_count, 100)


class TestCFMCoreV1Initialization(unittest.TestCase):
    """Tests for CFMCoreV1 initialization."""

    def test_default_initialization(self):
        """Test core can be created with defaults."""
        core = CFMCoreV1()
        self.assertIsNotNone(core.config)
        self.assertIsNotNone(core._state)

    def test_implements_protocol(self):
        """Test that CFMCoreV1 implements CFMCoreProtocol."""
        core = CFMCoreV1()
        self.assertIsInstance(core, CFMCoreProtocol)

    def test_custom_config(self):
        """Test initialization with custom config."""
        config = CFMCoreV1Config(tau_coherence=5.0, tau_energy=3.0)
        core = CFMCoreV1(config=config)
        self.assertEqual(core.config.tau_coherence, 5.0)
        self.assertEqual(core.config.tau_energy, 3.0)


class TestCFMCoreV1Step(unittest.TestCase):
    """Tests for CFMCoreV1 step behaviour."""

    def setUp(self):
        self.core = CFMCoreV1()

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

    def test_version_in_output(self):
        """Test that v1 includes version metadata."""
        result = self.core.step(dt=0.1)
        self.assertEqual(result.get("cfm_version"), 1)

    def test_v1_specific_metadata(self):
        """Test v1-specific metadata in output."""
        result = self.core.step(dt=0.1)
        self.assertIn("cfm_time", result)
        self.assertIn("cfm_step", result)
        self.assertIn("cfm_phase", result)


class TestCFMCoreV1Determinism(unittest.TestCase):
    """Tests for CFMCoreV1 determinism."""

    def test_identical_sequences(self):
        """Test that two cores with same config produce identical sequences."""
        config = CFMCoreV1Config()
        state = CFMCoreV1State()
        core1 = CFMCoreV1(config, state.copy())
        core2 = CFMCoreV1(config, state.copy())

        for i in range(100):
            result1 = core1.step(dt=0.1)
            result2 = core2.step(dt=0.1)
            self.assertEqual(result1["coherence"], result2["coherence"],
                           f"Coherence mismatch at step {i}")
            self.assertEqual(result1["stability"], result2["stability"],
                           f"Stability mismatch at step {i}")

    def test_reset_reproduces_sequence(self):
        """Test that reset allows reproducing the same sequence."""
        core = CFMCoreV1()
        results1 = [core.step(dt=0.1) for _ in range(50)]
        core.reset()
        results2 = [core.step(dt=0.1) for _ in range(50)]
        for i, (r1, r2) in enumerate(zip(results1, results2)):
            self.assertEqual(r1["coherence"], r2["coherence"],
                           f"Coherence mismatch at step {i}")


class TestCFMCoreV1AdapterIntegration(unittest.TestCase):
    """Tests for CFMCoreV1 with CFMCoreAdapter."""

    def test_adapter_wraps_core(self):
        """Test that adapter can wrap CFMCoreV1."""
        core = CFMCoreV1()
        adapter_config = CFMCoreInterfaceConfig(enabled=True)
        adapter = CFMCoreAdapter(core=core, config=adapter_config)
        self.assertIsNotNone(adapter)

    def test_adapter_step_returns_bundle(self):
        """Test that adapter step returns expected bundle structure."""
        core = CFMCoreV1()
        adapter_config = CFMCoreInterfaceConfig(enabled=True)
        adapter = CFMCoreAdapter(core=core, config=adapter_config)
        result = adapter.step(dt=0.1)
        self.assertIn("raw", result)
        self.assertIn("numeric_state", result)
        self.assertIn("metadata", result)

    def test_adapter_numeric_state_bounded(self):
        """Test that adapter output numeric_state is bounded."""
        core = CFMCoreV1()
        adapter_config = CFMCoreInterfaceConfig(enabled=True)
        adapter = CFMCoreAdapter(core=core, config=adapter_config)

        for _ in range(100):
            result = adapter.step(dt=0.1)
            for key in ["coherence", "stability", "intensity", "alignment"]:
                self.assertGreaterEqual(result["numeric_state"][key], 0.0)
                self.assertLessEqual(result["numeric_state"][key], 1.0)

    def test_adapter_json_serializable(self):
        """Test that adapter output is JSON serializable."""
        core = CFMCoreV1()
        adapter_config = CFMCoreInterfaceConfig(enabled=True)
        adapter = CFMCoreAdapter(core=core, config=adapter_config)

        for _ in range(20):
            result = adapter.step(dt=0.1)
            try:
                json_str = json.dumps(result)
                self.assertIsInstance(json_str, str)
            except (TypeError, ValueError) as e:
                self.fail(f"Output not JSON serializable: {e}")


class TestCFMCoreV1Safety(unittest.TestCase):
    """Tests for CFMCoreV1 safety invariants."""

    def test_verify_identity_safety(self):
        """Test identity safety verification."""
        core = CFMCoreV1()
        self.assertTrue(core.verify_identity_safety())

    def test_verify_state_bounds(self):
        """Test state bounds verification."""
        core = CFMCoreV1()
        for _ in range(100):
            core.step(dt=0.1)
            self.assertTrue(core.verify_state_bounds())

    def test_all_state_variables_bounded(self):
        """Test all state variables remain bounded after many steps."""
        core = CFMCoreV1()
        for i in range(500):
            core.step(dt=0.1)
            state = core.get_state()
            self.assertTrue(0.0 <= state.coherence <= 1.0, f"Step {i}: coherence OOB")
            self.assertTrue(0.0 <= state.coherence_baseline <= 1.0, f"Step {i}: coherence_baseline OOB")
            self.assertTrue(0.0 <= state.energy <= 1.0, f"Step {i}: energy OOB")
            self.assertTrue(0.0 <= state.instability <= 1.0, f"Step {i}: instability OOB")
            self.assertTrue(0.0 <= state.phase < 1.0, f"Step {i}: phase OOB")
            self.assertTrue(0.0 <= state.alignment_phase < 1.0, f"Step {i}: alignment_phase OOB")


class TestCFMCoreV1Dynamics(unittest.TestCase):
    """Tests for CFMCoreV1-specific dynamics behavior."""

    def test_phase_wrapping(self):
        """Test that phase variables wrap correctly."""
        core = CFMCoreV1()
        for _ in range(1000):
            core.step(dt=0.1)
        state = core.get_state()
        self.assertTrue(0.0 <= state.phase < 1.0)
        self.assertTrue(0.0 <= state.alignment_phase < 1.0)

    def test_coherence_baseline_drift(self):
        """Test that coherence baseline slowly drifts toward target."""
        config = CFMCoreV1Config()
        state = CFMCoreV1State(coherence_baseline=0.3)
        core = CFMCoreV1(config, state)

        initial_baseline = state.coherence_baseline
        for _ in range(500):
            core.step(dt=0.1)
        final_baseline = core.get_state().coherence_baseline

        # Should have moved toward target (which is ~0.718)
        self.assertGreater(final_baseline, initial_baseline)

    def test_slow_fast_variable_separation(self):
        """Test that fast variables change more rapidly than slow ones."""
        core = CFMCoreV1()

        # Run a few steps and capture state deltas
        state1 = core.get_state()
        for _ in range(10):
            core.step(dt=0.1)
        state2 = core.get_state()

        # Phase (fast) should have changed more than coherence_baseline (very slow)
        phase_delta = abs(state2.phase - state1.phase)
        baseline_delta = abs(state2.coherence_baseline - state1.coherence_baseline)

        # Phase wraps so this test accounts for that
        if phase_delta > 0.5:
            phase_delta = 1.0 - phase_delta

        # Phase should have moved significantly more than baseline
        self.assertGreater(phase_delta * 10, baseline_delta)

    def test_long_run_stability(self):
        """Test that v1 remains stable over long runs."""
        core = CFMCoreV1()
        for i in range(2000):
            result = core.step(dt=0.1)
            for key in ["coherence", "stability", "intensity", "alignment"]:
                self.assertGreaterEqual(result[key], 0.0)
                self.assertLessEqual(result[key], 1.0)
                self.assertFalse(math.isnan(result[key]))
                self.assertFalse(math.isinf(result[key]))


class TestCFMCoreV1StatusMethods(unittest.TestCase):
    """Tests for CFMCoreV1 status methods."""

    def test_get_status(self):
        """Test get_status returns complete information."""
        core = CFMCoreV1()
        core.step(dt=0.1)
        status = core.get_status()
        self.assertIn("state", status)
        self.assertIn("config", status)
        self.assertIn("version", status)
        self.assertEqual(status["version"], 1)

    def test_get_state_returns_copy(self):
        """Test get_state returns a copy, not the internal state."""
        core = CFMCoreV1()
        core.step(dt=0.1)
        state1 = core.get_state()
        state1.coherence = 0.999
        state2 = core.get_state()
        # Should not have affected internal state
        self.assertNotEqual(state2.coherence, 0.999)


if __name__ == "__main__":
    unittest.main(verbosity=2)
