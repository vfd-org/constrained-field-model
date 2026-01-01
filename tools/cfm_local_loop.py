#!/usr/bin/env python3
"""
CFM Local Loop

A CLI tool for running CFM cores locally and capturing trajectory data.
This is a standalone execution tool for CFM dynamical systems.

Usage:
    python tools/cfm_local_loop.py --steps 2000 --core-type cfm_v2 --output-json out.json
    python tools/cfm_local_loop.py --steps 1000 --core-type cfm_v1 --preset high_stability

Features:
- Runs CFM core v0, v1, or v2
- Captures full trajectory data
- Outputs JSON for analysis
- Supports v2 presets
"""

import argparse
import json
import sys
import os
from datetime import datetime
from typing import Dict, Any, List, Optional

# Add parent directory for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cfm_interface import create_cfm_core, list_core_types


def run_cfm_loop(
    core_type: str = "cfm_v2",
    preset: Optional[str] = None,
    num_steps: int = 1000,
    dt: float = 1.0,
    verbose: bool = False,
) -> Dict[str, Any]:
    """
    Run CFM core for specified number of steps.

    Args:
        core_type: Type of CFM core (cfm, cfm_v0, cfm_v1, cfm_v2)
        preset: Optional preset name for v2
        num_steps: Number of steps to run
        dt: Time delta per step
        verbose: Print progress

    Returns:
        Dict with metadata and trajectories
    """
    # Create core
    core = create_cfm_core(core_type=core_type, preset=preset)

    # Initialize trajectories
    trajectories: Dict[str, List[float]] = {
        "coherence": [],
        "stability": [],
        "intensity": [],
        "alignment": [],
    }

    # Run loop
    for step in range(num_steps):
        result = core.step(dt=dt)

        # Capture trajectory
        trajectories["coherence"].append(result.get("coherence", 0.0))
        trajectories["stability"].append(result.get("stability", 0.0))
        trajectories["intensity"].append(result.get("intensity", 0.0))
        trajectories["alignment"].append(result.get("alignment", 0.0))

        if verbose and (step + 1) % 100 == 0:
            print(f"Step {step + 1}/{num_steps}: "
                  f"C={result['coherence']:.4f} "
                  f"S={result['stability']:.4f} "
                  f"I={result['intensity']:.4f} "
                  f"A={result['alignment']:.4f}")

    # Build output
    return {
        "metadata": {
            "core_type": core_type,
            "preset": preset,
            "num_steps": num_steps,
            "dt": dt,
            "timestamp": datetime.now().isoformat(),
            "scenario": "local_loop",
        },
        "trajectories": trajectories,
        "final_state": {
            "coherence": trajectories["coherence"][-1] if trajectories["coherence"] else 0.0,
            "stability": trajectories["stability"][-1] if trajectories["stability"] else 0.0,
            "intensity": trajectories["intensity"][-1] if trajectories["intensity"] else 0.0,
            "alignment": trajectories["alignment"][-1] if trajectories["alignment"] else 0.0,
        },
    }


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="CFM Local Loop - Run CFM cores locally"
    )

    parser.add_argument(
        "--steps",
        type=int,
        default=1000,
        help="Number of steps to run (default: 1000)",
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
        "--dt",
        type=float,
        default=1.0,
        help="Time delta per step (default: 1.0)",
    )

    parser.add_argument(
        "--output-json",
        type=str,
        default=None,
        help="Output JSON file path",
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print progress during run",
    )

    args = parser.parse_args()

    # Run the loop
    print("=" * 60)
    print("CFM Local Loop")
    print("=" * 60)
    print(f"Core type: {args.core_type}")
    print(f"Preset: {args.preset or 'default'}")
    print(f"Steps: {args.steps}")
    print(f"dt: {args.dt}")
    print()

    result = run_cfm_loop(
        core_type=args.core_type,
        preset=args.preset,
        num_steps=args.steps,
        dt=args.dt,
        verbose=args.verbose,
    )

    # Print summary
    print()
    print("=" * 60)
    print("Final State:")
    print("=" * 60)
    for key, value in result["final_state"].items():
        print(f"  {key}: {value:.6f}")

    # Save to JSON if requested
    if args.output_json:
        with open(args.output_json, "w") as f:
            json.dump(result, f, indent=2)
        print(f"\nSaved output to: {args.output_json}")


if __name__ == "__main__":
    main()
