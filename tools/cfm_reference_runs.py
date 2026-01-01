#!/usr/bin/env python3
"""
CFM Reference Runs

A CLI tool for generating canonical JSON runs for defined reference scenarios.
Produces reproducible outputs for regression testing and behavioral analysis.

Usage:
    python tools/cfm_reference_runs.py --scenario baseline_quiet --core-type cfm_v2 --output-json out.json
    python tools/cfm_reference_runs.py --scenario mild_perturbation --seed 42 --output-json perturb.json
    python tools/cfm_reference_runs.py --scenario high_variability --core-type cfm_v1 --output-json var.json

Scenarios:
    baseline_quiet:      2,000 steps, dt=0.1, no perturbations (default)
    baseline_long:       20,000 steps, dt=0.1, no perturbations
    mild_perturbation:   5,000 steps, small bounded external_events pulses at intervals
    high_variability:    10,000 steps, dt jitter + bounded perturbation pulses

All outputs are bounded [0,1], deterministic given seed, no NaN/Inf.
"""

import argparse
import json
import math
import sys
import os
from datetime import datetime
from typing import Dict, Any, List, Optional

# Add parent directory for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cfm_interface import create_cfm_core, list_core_types


# ==============================================================================
# SCENARIO DEFINITIONS
# ==============================================================================

SCENARIOS = {
    "baseline_quiet": {
        "description": "Mild baseline run with no perturbations",
        "steps": 2000,
        "dt": 0.1,
        "perturbation_interval": None,
        "perturbation_amplitude": 0.0,
        "dt_jitter": 0.0,
    },
    "baseline_long": {
        "description": "Extended baseline run for full dynamics observation",
        "steps": 20000,
        "dt": 0.1,
        "perturbation_interval": None,
        "perturbation_amplitude": 0.0,
        "dt_jitter": 0.0,
    },
    "mild_perturbation": {
        "description": "Small bounded external_events pulses at fixed intervals",
        "steps": 5000,
        "dt": 0.1,
        "perturbation_interval": 500,
        "perturbation_amplitude": 0.05,
        "dt_jitter": 0.0,
    },
    "high_variability": {
        "description": "dt jitter + bounded perturbation pulses",
        "steps": 10000,
        "dt": 0.1,
        "perturbation_interval": 200,
        "perturbation_amplitude": 0.1,
        "dt_jitter": 0.02,
    },
}


def list_scenarios() -> List[str]:
    """List available scenario names."""
    return list(SCENARIOS.keys())


# ==============================================================================
# DETERMINISTIC PSEUDO-RANDOM GENERATOR
# ==============================================================================

class DeterministicRNG:
    """
    Simple deterministic pseudo-random number generator.
    Uses a linear congruential generator for reproducibility without external deps.
    """

    def __init__(self, seed: int = 0):
        """Initialize with seed."""
        self._state = seed if seed != 0 else 1

    def next_float(self) -> float:
        """Return next float in [0, 1)."""
        # LCG parameters (same as MINSTD)
        self._state = (self._state * 48271) % 2147483647
        return self._state / 2147483647.0

    def next_in_range(self, low: float, high: float) -> float:
        """Return next float in [low, high)."""
        return low + self.next_float() * (high - low)


# ==============================================================================
# REFERENCE RUN GENERATOR
# ==============================================================================

def generate_reference_run(
    core_type: str = "cfm_v2",
    preset: Optional[str] = None,
    scenario: str = "baseline_quiet",
    steps: Optional[int] = None,
    dt: Optional[float] = None,
    seed: int = 0,
) -> Dict[str, Any]:
    """
    Generate a canonical reference run for a given scenario.

    Args:
        core_type: Type of CFM core (cfm_v0, cfm_v1, cfm_v2)
        preset: Optional preset name for v2
        scenario: Scenario name from SCENARIOS
        steps: Number of steps (overrides scenario default if provided)
        dt: Time delta (overrides scenario default if provided)
        seed: Random seed for deterministic perturbations

    Returns:
        Dict with metadata, trajectories, and validation info

    Raises:
        ValueError: If scenario is unknown
    """
    if scenario not in SCENARIOS:
        valid = ", ".join(SCENARIOS.keys())
        raise ValueError(f"Unknown scenario '{scenario}'. Valid: {valid}")

    scenario_config = SCENARIOS[scenario]

    # Use provided values or scenario defaults
    actual_steps = steps if steps is not None else scenario_config["steps"]
    actual_dt = dt if dt is not None else scenario_config["dt"]
    perturbation_interval = scenario_config["perturbation_interval"]
    perturbation_amplitude = scenario_config["perturbation_amplitude"]
    dt_jitter = scenario_config["dt_jitter"]

    # Create core
    core = create_cfm_core(core_type=core_type, preset=preset)

    # Initialize RNG for deterministic perturbations
    rng = DeterministicRNG(seed)

    # Initialize trajectories
    trajectories: Dict[str, List[float]] = {
        "coherence": [],
        "stability": [],
        "intensity": [],
        "alignment": [],
    }

    # Track step-level data for validation
    step_dts: List[float] = []
    perturbation_steps: List[int] = []

    # Validation counters
    nan_inf_count = 0
    out_of_bounds_count = 0

    # Run simulation
    for step in range(actual_steps):
        # Compute effective dt (with optional jitter)
        effective_dt = actual_dt
        if dt_jitter > 0:
            jitter = rng.next_in_range(-dt_jitter, dt_jitter)
            effective_dt = max(0.001, actual_dt + jitter)  # Keep positive
        step_dts.append(effective_dt)

        # Generate perturbation pulse if interval is set
        external_events = None
        if perturbation_interval and (step + 1) % perturbation_interval == 0:
            # Create bounded numeric perturbation (no identity/semantic content)
            pulse_value = rng.next_in_range(0.0, perturbation_amplitude)
            external_events = {
                "numeric_pulse": pulse_value,
                "step_triggered": step,
            }
            perturbation_steps.append(step)

        # Execute step
        # Note: CFM cores ignore external_events by design, but we pass them
        # to demonstrate the interface. The perturbation has no effect on
        # internal dynamics (cores are purely internal), but we record the
        # intent for reproducibility documentation.
        result = core.step(dt=effective_dt, external_events=external_events)

        # Capture trajectory values
        for key in ["coherence", "stability", "intensity", "alignment"]:
            value = result.get(key, 0.0)

            # Validate: check for NaN/Inf
            if math.isnan(value) or math.isinf(value):
                nan_inf_count += 1
                value = 0.0  # Replace with safe value

            # Validate: check bounds [0, 1]
            if value < 0.0 or value > 1.0:
                out_of_bounds_count += 1
                value = max(0.0, min(1.0, value))

            trajectories[key].append(value)

    # Build output
    return {
        "metadata": {
            "core_type": core_type,
            "preset": preset,
            "scenario": scenario,
            "scenario_description": scenario_config["description"],
            "num_steps": actual_steps,
            "dt": actual_dt,
            "dt_jitter": dt_jitter,
            "seed": seed,
            "perturbation_interval": perturbation_interval,
            "perturbation_amplitude": perturbation_amplitude,
            "perturbation_steps": perturbation_steps,
            "timestamp": datetime.now().isoformat(),
            "version": "0.1.0",
        },
        "trajectories": trajectories,
        "final_state": {
            "coherence": trajectories["coherence"][-1] if trajectories["coherence"] else 0.0,
            "stability": trajectories["stability"][-1] if trajectories["stability"] else 0.0,
            "intensity": trajectories["intensity"][-1] if trajectories["intensity"] else 0.0,
            "alignment": trajectories["alignment"][-1] if trajectories["alignment"] else 0.0,
        },
        "validation": {
            "nan_inf_count": nan_inf_count,
            "out_of_bounds_count": out_of_bounds_count,
            "all_bounded": nan_inf_count == 0 and out_of_bounds_count == 0,
            "deterministic": True,  # Always deterministic given same seed
        },
    }


# ==============================================================================
# CLI INTERFACE
# ==============================================================================

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="CFM Reference Runs - Generate canonical scenario runs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Scenarios:
  baseline_quiet      2,000 steps, dt=0.1, no perturbations (default)
  baseline_long       20,000 steps, dt=0.1, no perturbations
  mild_perturbation   5,000 steps, small bounded pulses at intervals
  high_variability    10,000 steps, dt jitter + bounded perturbation pulses

Examples:
  python tools/cfm_reference_runs.py --scenario baseline_quiet --output-json out.json
  python tools/cfm_reference_runs.py --scenario mild_perturbation --seed 42 --output-json mp.json
  python tools/cfm_reference_runs.py --scenario high_variability --core-type cfm_v1 --output-json hv.json
        """
    )

    parser.add_argument(
        "--scenario",
        type=str,
        default="baseline_quiet",
        choices=list_scenarios(),
        help="Scenario to run (default: baseline_quiet)",
    )

    parser.add_argument(
        "--core-type",
        type=str,
        default="cfm_v2",
        choices=list_core_types(),
        help="Type of CFM core to use (default: cfm_v2)",
    )

    parser.add_argument(
        "--preset",
        type=str,
        default=None,
        choices=["baseline", "high_stability", "high_resonance", "pulsed_activity"],
        help="Preset configuration for v2 (optional)",
    )

    parser.add_argument(
        "--steps",
        type=int,
        default=None,
        help="Number of steps (overrides scenario default)",
    )

    parser.add_argument(
        "--dt",
        type=float,
        default=None,
        help="Time delta per step (overrides scenario default)",
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=0,
        help="Random seed for deterministic perturbations (default: 0)",
    )

    parser.add_argument(
        "--output-json",
        type=str,
        required=True,
        help="Output JSON file path (required)",
    )

    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress progress output",
    )

    args = parser.parse_args()

    # Generate the run
    if not args.quiet:
        print("=" * 60)
        print("CFM Reference Runs")
        print("=" * 60)
        print(f"Scenario: {args.scenario}")
        print(f"Core type: {args.core_type}")
        print(f"Preset: {args.preset or 'default'}")
        print(f"Seed: {args.seed}")
        if args.steps:
            print(f"Steps (override): {args.steps}")
        if args.dt:
            print(f"dt (override): {args.dt}")
        print()

    result = generate_reference_run(
        core_type=args.core_type,
        preset=args.preset,
        scenario=args.scenario,
        steps=args.steps,
        dt=args.dt,
        seed=args.seed,
    )

    # Save to JSON
    with open(args.output_json, "w") as f:
        json.dump(result, f, indent=2)

    if not args.quiet:
        print()
        print("=" * 60)
        print("Run Complete")
        print("=" * 60)
        print(f"Steps: {result['metadata']['num_steps']}")
        print(f"Perturbations: {len(result['metadata']['perturbation_steps'])}")
        print()
        print("Final State:")
        for key, value in result["final_state"].items():
            print(f"  {key}: {value:.6f}")
        print()
        print("Validation:")
        print(f"  All bounded [0,1]: {result['validation']['all_bounded']}")
        print(f"  NaN/Inf count: {result['validation']['nan_inf_count']}")
        print(f"  Out of bounds count: {result['validation']['out_of_bounds_count']}")
        print()
        print(f"Saved to: {args.output_json}")


if __name__ == "__main__":
    main()
