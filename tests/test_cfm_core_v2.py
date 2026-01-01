#!/usr/bin/env python3
"""
Tests for CFM Core v2

Comprehensive test suite covering multi-channel architecture,
attractor basin dynamics, and five-tier timescale hierarchy.
"""

import json
import math
import sys
import os
import unittest

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cfm_core_v2 import CFMCoreV2, CFMCoreV2Config, CFMCoreV2State
from cfm_interface.adapters import CFMCoreAdapter
from cfm_interface.config import CFMCoreInterfaceConfig
from cfm_interface.protocols import CFMCoreProtocol
from cfm_consts import PHI, PSI


class TestCFMCoreV2Config(unittest.TestCase):
    """Tests for CFMCoreV2Config."""

    def test_default_values(self):
        """Test that default values are derived from phi/psi."""
        config = CFMCoreV2Config()
        self.assertAlmostEqual(config.tau_very_slow, PHI ** 3, places=10)
        self.assertAlmostEqual(config.tau_slow, PHI ** 2, places=10)
        self.assertAlmostEqual(config.tau_medium, PHI, places=10)
        self.assertAlmostEqual(config.tau_fast, 1.0 / PHI, places=10)
        self.assertAlmostEqual(config.tau_very_fast, 1.0 / (PHI ** 2), places=10)

    def test_timescale_hierarchy(self):
        """Test timescale hierarchy is properly ordered."""
        config = CFMCoreV2Config()
        self.assertGreater(config.tau_very_slow, config.tau_slow)
        self.assertGreater(config.tau_slow, config.tau_medium)
        self.assertGreater(config.tau_medium, config.tau_fast)
        self.assertGreater(config.tau_fast, config.tau_very_fast)

    def test_to_dict(self):
        """Test conversion to dictionary."""
        config = CFMCoreV2Config()
        d = config.to_dict()
        self.assertIn("tau_very_slow", d)
        self.assertIn("basin_center_c", d)
        self.assertIn("coherence_energy_coupling", d)


class TestCFMCoreV2State(unittest.TestCase):
    """Tests for CFMCoreV2State."""

    def test_default_values(self):
        """Test default state values are in valid ranges."""
        state = CFMCoreV2State()
        self.assertTrue(0.0 <= state.coherence_slow <= 1.0)
        self.assertTrue(0.0 <= state.coherence_fast <= 1.0)
        self.assertTrue(0.0 <= state.energy_potential <= 1.0)
        self.assertTrue(0.0 <= state.energy_flux <= 1.0)
        self.assertTrue(0.0 <= state.stability_envelope <= 1.0)
        self.assertTrue(0.0 <= state.instability_pulse <= 1.0)
        self.assertTrue(0.0 <= state.phase_global < 1.0)
        self.assertTrue(0.0 <= state.phase_local < 1.0)
        self.assertTrue(0.0 <= state.alignment_field <= 1.0)
        self.assertTrue(0.0 <= state.alignment_direction <= 1.0)
        self.assertTrue(0.0 <= state.resonance_index <= 1.0)

    def test_copy(self):
        """Test state copy is independent."""
        state1 = CFMCoreV2State(coherence_slow=0.5, energy_potential=0.7)
        state2 = state1.copy()
        state2.coherence_slow = 0.9
        self.assertEqual(state1.coherence_slow, 0.5)

    def test_validate(self):
        """Test validation method."""
        state = CFMCoreV2State()
        self.assertTrue(state.validate())

    def test_channel_getters(self):
        """Test channel getter methods."""
        state = CFMCoreV2State(coherence_slow=0.5, coherence_fast=0.6)
        coherence = state.get_channel_coherence()
        self.assertEqual(coherence["slow"], 0.5)
        self.assertEqual(coherence["fast"], 0.6)

    def test_distance_to_basin(self):
        """Test basin distance calculation."""
        state = CFMCoreV2State()
        distance = state.get_distance_to_basin()
        self.assertLess(distance, 0.1)  # Default state near basin


class TestCFMCoreV2Initialization(unittest.TestCase):
    """Tests for CFMCoreV2 initialization."""

    def test_default_initialization(self):
        """Test core can be created with defaults."""
        core = CFMCoreV2()
        self.assertIsNotNone(core.config)
        self.assertIsNotNone(core._state)

    def test_implements_protocol(self):
        """Test that CFMCoreV2 implements CFMCoreProtocol."""
        core = CFMCoreV2()
        self.assertIsInstance(core, CFMCoreProtocol)


class TestCFMCoreV2Step(unittest.TestCase):
    """Tests for CFMCoreV2 step behavior."""

    def setUp(self):
        self.core = CFMCoreV2()

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

    def test_outputs_bounded_1000_steps(self):
        """Test outputs remain in [0, 1] after 1000 steps."""
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
        """Test that v2 includes version metadata."""
        result = self.core.step(dt=0.1)
        self.assertEqual(result.get("cfm_version"), 2)

    def test_v2_specific_metadata(self):
        """Test v2-specific metadata in output."""
        result = self.core.step(dt=0.1)
        self.assertIn("cfm_resonance_index", result)
        self.assertIn("cfm_basin_distance", result)


class TestCFMCoreV2Determinism(unittest.TestCase):
    """Tests for CFMCoreV2 determinism."""

    def test_identical_sequences(self):
        """Test that two cores with same config produce identical sequences."""
        config = CFMCoreV2Config()
        state = CFMCoreV2State()
        core1 = CFMCoreV2(config, state.copy())
        core2 = CFMCoreV2(config, state.copy())

        for i in range(100):
            result1 = core1.step(dt=0.1)
            result2 = core2.step(dt=0.1)
            self.assertEqual(result1["coherence"], result2["coherence"],
                           f"Coherence mismatch at step {i}")

    def test_reset_reproduces_sequence(self):
        """Test that reset allows reproducing the same sequence."""
        core = CFMCoreV2()
        results1 = [core.step(dt=0.1) for _ in range(50)]
        core.reset()
        results2 = [core.step(dt=0.1) for _ in range(50)]
        for i, (r1, r2) in enumerate(zip(results1, results2)):
            self.assertEqual(r1["coherence"], r2["coherence"],
                           f"Coherence mismatch at step {i}")


class TestCFMCoreV2AdapterIntegration(unittest.TestCase):
    """Tests for CFMCoreV2 with CFMCoreAdapter."""

    def test_adapter_wraps_core(self):
        """Test that adapter can wrap CFMCoreV2."""
        core = CFMCoreV2()
        adapter_config = CFMCoreInterfaceConfig(enabled=True)
        adapter = CFMCoreAdapter(core=core, config=adapter_config)
        self.assertIsNotNone(adapter)

    def test_adapter_numeric_state_bounded(self):
        """Test that adapter output numeric_state is bounded."""
        core = CFMCoreV2()
        adapter_config = CFMCoreInterfaceConfig(enabled=True)
        adapter = CFMCoreAdapter(core=core, config=adapter_config)

        for _ in range(100):
            result = adapter.step(dt=0.1)
            for key in ["coherence", "stability", "intensity", "alignment"]:
                self.assertGreaterEqual(result["numeric_state"][key], 0.0)
                self.assertLessEqual(result["numeric_state"][key], 1.0)

    def test_adapter_json_serializable(self):
        """Test that adapter output is JSON serializable."""
        core = CFMCoreV2()
        adapter_config = CFMCoreInterfaceConfig(enabled=True)
        adapter = CFMCoreAdapter(core=core, config=adapter_config)

        for _ in range(20):
            result = adapter.step(dt=0.1)
            try:
                json_str = json.dumps(result)
                self.assertIsInstance(json_str, str)
            except (TypeError, ValueError) as e:
                self.fail(f"Output not JSON serializable: {e}")


class TestCFMCoreV2Safety(unittest.TestCase):
    """Tests for CFMCoreV2 safety invariants."""

    def test_verify_identity_safety(self):
        """Test identity safety verification."""
        core = CFMCoreV2()
        self.assertTrue(core.verify_identity_safety())

    def test_verify_state_bounds(self):
        """Test state bounds verification."""
        core = CFMCoreV2()
        for _ in range(100):
            core.step(dt=0.1)
            self.assertTrue(core.verify_state_bounds())

    def test_all_state_variables_bounded(self):
        """Test all 11 state variables remain bounded after many steps."""
        core = CFMCoreV2()
        for i in range(500):
            core.step(dt=0.1)
            state = core.get_state()
            self.assertTrue(0.0 <= state.coherence_slow <= 1.0)
            self.assertTrue(0.0 <= state.coherence_fast <= 1.0)
            self.assertTrue(0.0 <= state.energy_potential <= 1.0)
            self.assertTrue(0.0 <= state.energy_flux <= 1.0)
            self.assertTrue(0.0 <= state.stability_envelope <= 1.0)
            self.assertTrue(0.0 <= state.instability_pulse <= 1.0)
            self.assertTrue(0.0 <= state.alignment_field <= 1.0)
            self.assertTrue(0.0 <= state.alignment_direction <= 1.0)
            self.assertTrue(0.0 <= state.resonance_index <= 1.0)
            self.assertTrue(0.0 <= state.phase_global < 1.0)
            self.assertTrue(0.0 <= state.phase_local < 1.0)


class TestCFMCoreV2Dynamics(unittest.TestCase):
    """Tests for CFMCoreV2-specific dynamics behavior."""

    def test_phase_wrapping(self):
        """Test that phase variables wrap correctly."""
        core = CFMCoreV2()
        for _ in range(1000):
            core.step(dt=0.1)
        state = core.get_state()
        self.assertTrue(0.0 <= state.phase_global < 1.0)
        self.assertTrue(0.0 <= state.phase_local < 1.0)

    def test_basin_attraction(self):
        """Test that state converges toward basin center."""
        state = CFMCoreV2State(coherence_slow=0.1, energy_potential=0.9, stability_envelope=0.2)
        core = CFMCoreV2(initial_state=state)
        initial_distance = state.get_distance_to_basin()
        for _ in range(500):
            core.step(dt=0.1)
        final_distance = core.get_state().get_distance_to_basin()
        self.assertLess(final_distance, initial_distance)

    def test_resonance_index_variation(self):
        """Test that resonance index shows variation."""
        core = CFMCoreV2()
        resonance_values = []
        for _ in range(200):
            core.step(dt=0.1)
            resonance_values.append(core.get_state().resonance_index)
        self.assertGreater(max(resonance_values) - min(resonance_values), 0.001)

    def test_long_run_stability(self):
        """Test that v2 remains stable over long runs."""
        core = CFMCoreV2()
        for i in range(2000):
            result = core.step(dt=0.1)
            for key in ["coherence", "stability", "intensity", "alignment"]:
                self.assertGreaterEqual(result[key], 0.0)
                self.assertLessEqual(result[key], 1.0)
                self.assertFalse(math.isnan(result[key]))
                self.assertFalse(math.isinf(result[key]))


class TestCFMCoreV2StatusMethods(unittest.TestCase):
    """Tests for CFMCoreV2 status and channel methods."""

    def test_get_status(self):
        """Test get_status returns complete information."""
        core = CFMCoreV2()
        core.step(dt=0.1)
        status = core.get_status()
        self.assertIn("state", status)
        self.assertIn("config", status)
        self.assertIn("version", status)
        self.assertEqual(status["version"], 2)

    def test_get_channel_states(self):
        """Test get_channel_states returns all channels."""
        core = CFMCoreV2()
        core.step(dt=0.1)
        channels = core.get_channel_states()
        self.assertIn("coherence", channels)
        self.assertIn("energy", channels)
        self.assertIn("stability", channels)
        self.assertIn("phase", channels)
        self.assertIn("alignment", channels)
        self.assertIn("resonance", channels)


if __name__ == "__main__":
    unittest.main(verbosity=2)
