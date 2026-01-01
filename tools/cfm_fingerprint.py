#!/usr/bin/env python3
"""
CFM Fingerprint Extractor

A CLI tool for computing compact numeric fingerprints from CFM reference runs.
Fingerprints provide a compressed summary of core behavior under specific scenarios,
enabling regression detection and cross-core comparison.

Usage:
    python tools/cfm_fingerprint.py --input out.json
    python tools/cfm_fingerprint.py --input out.json --output fingerprint.json
    python tools/cfm_fingerprint.py --compare fp1.json fp2.json
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

# Mathematical constants
PHI = 1.618033988749895
PHI_INV = 1.0 / PHI


def compute_stats(values: List[float]) -> Dict[str, float]:
    """Compute basic statistics for a list of values."""
    valid = [v for v in values if isinstance(v, (int, float)) and not (math.isnan(v) or math.isinf(v))]

    if not valid:
        return {"mean": 0.0, "std": 0.0, "min": 0.0, "max": 0.0, "range": 0.0}

    n = len(valid)
    mean = sum(valid) / n
    variance = sum((v - mean) ** 2 for v in valid) / n if n > 1 else 0.0
    std = math.sqrt(variance)

    return {
        "mean": mean,
        "std": std,
        "min": min(valid),
        "max": max(valid),
        "range": max(valid) - min(valid),
    }


def extract_common_fingerprint(trajectories: Dict[str, List]) -> Dict[str, Any]:
    """Extract common metrics fingerprint."""
    return {
        "coherence": compute_stats(trajectories.get("coherence", [])),
        "stability": compute_stats(trajectories.get("stability", [])),
        "intensity": compute_stats(trajectories.get("intensity", [])),
        "alignment": compute_stats(trajectories.get("alignment", [])),
    }


def extract_fingerprint(run_data: Dict[str, Any]) -> Dict[str, Any]:
    """Extract a complete fingerprint from a reference run."""
    metadata = run_data.get("metadata", {})
    trajectories = run_data.get("trajectories", {})
    core_type = metadata.get("core_type", "unknown")

    return {
        "core_type": core_type,
        "scenario": metadata.get("scenario", "unknown"),
        "num_steps": metadata.get("num_steps", 0),
        "timestamp": datetime.now().isoformat(),
        "source_timestamp": metadata.get("timestamp", ""),
        "common_metrics": extract_common_fingerprint(trajectories),
        "core_specific": {},  # CFM cores use common metrics
    }


def compare_values(val1: Any, val2: Any, path: str = "") -> List[Dict[str, Any]]:
    """Recursively compare two values and return differences."""
    differences = []

    if isinstance(val1, dict) and isinstance(val2, dict):
        all_keys = set(val1.keys()) | set(val2.keys())
        for key in sorted(all_keys):
            new_path = f"{path}.{key}" if path else key
            if key not in val1:
                differences.append({"path": new_path, "type": "missing_in_first", "value2": val2[key]})
            elif key not in val2:
                differences.append({"path": new_path, "type": "missing_in_second", "value1": val1[key]})
            else:
                differences.extend(compare_values(val1[key], val2[key], new_path))

    elif isinstance(val1, list) and isinstance(val2, list):
        if len(val1) != len(val2):
            differences.append({"path": path, "type": "length_mismatch", "len1": len(val1), "len2": len(val2)})
        else:
            for i, (v1, v2) in enumerate(zip(val1, val2)):
                differences.extend(compare_values(v1, v2, f"{path}[{i}]"))

    elif isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
        if abs(val1 - val2) > 1e-6:
            rel_diff = abs(val1 - val2) / max(abs(val1), abs(val2), 1e-10)
            differences.append({
                "path": path,
                "type": "numeric_difference",
                "value1": val1,
                "value2": val2,
                "abs_diff": abs(val1 - val2),
                "rel_diff": rel_diff,
            })

    elif val1 != val2:
        differences.append({"path": path, "type": "value_mismatch", "value1": val1, "value2": val2})

    return differences


def compare_fingerprints(fp1: Dict[str, Any], fp2: Dict[str, Any]) -> Dict[str, Any]:
    """Compare two fingerprints and return a comparison report."""
    core_type_match = fp1.get("core_type") == fp2.get("core_type")
    scenario_match = fp1.get("scenario") == fp2.get("scenario")

    common_diffs = compare_values(
        fp1.get("common_metrics", {}),
        fp2.get("common_metrics", {}),
        "common_metrics"
    )

    specific_diffs = compare_values(
        fp1.get("core_specific", {}),
        fp2.get("core_specific", {}),
        "core_specific"
    )

    significant_diffs = []
    for diff in common_diffs + specific_diffs:
        if diff["type"] == "numeric_difference" and diff["rel_diff"] > 0.05:
            significant_diffs.append(diff)
        elif diff["type"] != "numeric_difference":
            significant_diffs.append(diff)

    return {
        "fingerprint1": {
            "core_type": fp1.get("core_type"),
            "scenario": fp1.get("scenario"),
            "timestamp": fp1.get("timestamp"),
        },
        "fingerprint2": {
            "core_type": fp2.get("core_type"),
            "scenario": fp2.get("scenario"),
            "timestamp": fp2.get("timestamp"),
        },
        "core_type_match": core_type_match,
        "scenario_match": scenario_match,
        "total_differences": len(common_diffs) + len(specific_diffs),
        "significant_differences": len(significant_diffs),
        "all_differences": common_diffs + specific_diffs,
        "significant_diff_details": significant_diffs,
    }


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="CFM Fingerprint Extractor - Compute fingerprints from reference runs"
    )

    parser.add_argument("--input", type=str, help="Input reference run JSON file")
    parser.add_argument("--output", type=str, help="Output fingerprint JSON file")
    parser.add_argument(
        "--compare",
        type=str,
        nargs=2,
        metavar=("FP1", "FP2"),
        help="Compare two fingerprint files",
    )
    parser.add_argument("--quiet", action="store_true", help="Suppress progress output")

    args = parser.parse_args()
    verbose = not args.quiet

    # Compare mode
    if args.compare:
        with open(args.compare[0], "r") as f:
            fp1 = json.load(f)
        with open(args.compare[1], "r") as f:
            fp2 = json.load(f)

        comparison = compare_fingerprints(fp1, fp2)

        print("\n" + "=" * 60)
        print("FINGERPRINT COMPARISON")
        print("=" * 60)
        print(f"\nFingerprint 1: {args.compare[0]}")
        print(f"  Core: {comparison['fingerprint1']['core_type']}")
        print(f"  Scenario: {comparison['fingerprint1']['scenario']}")
        print(f"\nFingerprint 2: {args.compare[1]}")
        print(f"  Core: {comparison['fingerprint2']['core_type']}")
        print(f"  Scenario: {comparison['fingerprint2']['scenario']}")
        print(f"\nCore type match: {comparison['core_type_match']}")
        print(f"Scenario match: {comparison['scenario_match']}")
        print(f"\nTotal differences: {comparison['total_differences']}")
        print(f"Significant differences (>5% relative): {comparison['significant_differences']}")

        if comparison["significant_diff_details"]:
            print("\nSignificant differences:")
            for diff in comparison["significant_diff_details"][:10]:
                print(f"  {diff['path']}: {diff.get('value1', 'N/A')} -> {diff.get('value2', 'N/A')}")
                if "rel_diff" in diff:
                    print(f"    (relative diff: {diff['rel_diff']*100:.2f}%)")
        return

    # Single file mode
    if args.input:
        if verbose:
            print("=" * 60)
            print("CFM Fingerprint Extractor")
            print("=" * 60)
            print(f"Input: {args.input}")

        with open(args.input, "r") as f:
            run_data = json.load(f)

        fingerprint = extract_fingerprint(run_data)
        fingerprint["source_file"] = args.input

        if args.output:
            os.makedirs(os.path.dirname(args.output) if os.path.dirname(args.output) else ".", exist_ok=True)
            with open(args.output, "w") as f:
                json.dump(fingerprint, f, indent=2)
            if verbose:
                print(f"Saved fingerprint to {args.output}")
        else:
            print(json.dumps(fingerprint, indent=2))
        return

    parser.print_help()


if __name__ == "__main__":
    main()
