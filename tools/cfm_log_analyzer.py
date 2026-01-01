#!/usr/bin/env python3
"""
CFM Log Analyzer

A read-only CLI tool for analyzing JSON run outputs from CFM cores.
Computes statistics, validates bounds, detects anomalies, and prints concise reports.

Usage:
    python tools/cfm_log_analyzer.py --input out.json
    python tools/cfm_log_analyzer.py --input out.json --output report.txt
    python tools/cfm_log_analyzer.py --input out.json --format json
    python tools/cfm_log_analyzer.py --input run1.json run2.json --summary

Features:
    - Computes min/mean/max/std for coherence, stability, intensity, alignment
    - Detects NaN/Inf values
    - Validates [0,1] boundedness
    - Identifies any core-specific fields present
    - Summarizes multiple runs
"""

import argparse
import json
import math
import sys
import os
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple


# ==============================================================================
# STATISTICS
# ==============================================================================

def compute_stats(values: List[float]) -> Dict[str, Any]:
    """
    Compute statistics for a list of numeric values.

    Returns dict with mean, std, min, max, and anomaly counts.
    """
    if not values:
        return {
            "count": 0,
            "mean": None,
            "std": None,
            "min": None,
            "max": None,
            "nan_count": 0,
            "inf_count": 0,
            "below_zero": 0,
            "above_one": 0,
        }

    # Separate valid values from anomalies
    valid = []
    nan_count = 0
    inf_count = 0
    below_zero = 0
    above_one = 0

    for v in values:
        if not isinstance(v, (int, float)):
            continue

        if math.isnan(v):
            nan_count += 1
        elif math.isinf(v):
            inf_count += 1
        else:
            valid.append(v)
            if v < 0.0:
                below_zero += 1
            elif v > 1.0:
                above_one += 1

    if not valid:
        return {
            "count": len(values),
            "mean": None,
            "std": None,
            "min": None,
            "max": None,
            "nan_count": nan_count,
            "inf_count": inf_count,
            "below_zero": below_zero,
            "above_one": above_one,
        }

    n = len(valid)
    mean = sum(valid) / n
    variance = sum((v - mean) ** 2 for v in valid) / n if n > 1 else 0.0
    std = math.sqrt(variance)

    return {
        "count": len(values),
        "mean": mean,
        "std": std,
        "min": min(valid),
        "max": max(valid),
        "nan_count": nan_count,
        "inf_count": inf_count,
        "below_zero": below_zero,
        "above_one": above_one,
    }


# ==============================================================================
# ANALYZER
# ==============================================================================

def analyze_run(run_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze a single CFM run and return a comprehensive report.

    Args:
        run_data: Parsed JSON from a CFM run output

    Returns:
        Dict containing analysis results
    """
    metadata = run_data.get("metadata", {})
    trajectories = run_data.get("trajectories", {})
    final_state = run_data.get("final_state", {})
    validation = run_data.get("validation", {})

    # Standard metrics
    common_metrics = ["coherence", "stability", "intensity", "alignment"]
    stats = {}

    for metric in common_metrics:
        if metric in trajectories:
            stats[metric] = compute_stats(trajectories[metric])

    # Detect core-specific fields (any trajectory key not in common_metrics)
    core_specific_stats = {}
    for key in trajectories:
        if key not in common_metrics:
            core_specific_stats[key] = compute_stats(trajectories[key])

    # Aggregate validation
    total_nan = sum(s.get("nan_count", 0) for s in stats.values())
    total_inf = sum(s.get("inf_count", 0) for s in stats.values())
    total_below_zero = sum(s.get("below_zero", 0) for s in stats.values())
    total_above_one = sum(s.get("above_one", 0) for s in stats.values())
    all_bounded = total_nan == 0 and total_inf == 0 and total_below_zero == 0 and total_above_one == 0

    return {
        "metadata": {
            "core_type": metadata.get("core_type", "unknown"),
            "scenario": metadata.get("scenario", "unknown"),
            "num_steps": metadata.get("num_steps", 0),
            "dt": metadata.get("dt", 0.0),
            "seed": metadata.get("seed", 0),
            "timestamp": metadata.get("timestamp", ""),
        },
        "common_metrics": stats,
        "core_specific_metrics": core_specific_stats,
        "final_state": final_state,
        "validation": {
            "total_nan": total_nan,
            "total_inf": total_inf,
            "total_below_zero": total_below_zero,
            "total_above_one": total_above_one,
            "all_bounded": all_bounded,
            "source_validation": validation,
        },
        "analysis_timestamp": datetime.now().isoformat(),
    }


def format_text_report(analysis: Dict[str, Any], filename: str = "") -> str:
    """Format analysis as human-readable text report."""
    lines = []
    lines.append("=" * 60)
    lines.append("CFM LOG ANALYSIS REPORT")
    lines.append("=" * 60)

    if filename:
        lines.append(f"File: {filename}")
    lines.append(f"Analysis time: {analysis['analysis_timestamp']}")
    lines.append("")

    # Metadata
    meta = analysis["metadata"]
    lines.append("METADATA")
    lines.append("-" * 40)
    lines.append(f"  Core type:    {meta['core_type']}")
    lines.append(f"  Scenario:     {meta['scenario']}")
    lines.append(f"  Steps:        {meta['num_steps']}")
    lines.append(f"  dt:           {meta['dt']}")
    lines.append(f"  Seed:         {meta['seed']}")
    lines.append(f"  Timestamp:    {meta['timestamp']}")
    lines.append("")

    # Common metrics
    lines.append("COMMON METRICS (coherence, stability, intensity, alignment)")
    lines.append("-" * 40)
    lines.append(f"{'Metric':<12} {'Mean':>10} {'Std':>10} {'Min':>10} {'Max':>10}")
    lines.append("-" * 54)

    for metric, stats in analysis["common_metrics"].items():
        if stats["mean"] is not None:
            lines.append(
                f"{metric:<12} {stats['mean']:>10.6f} {stats['std']:>10.6f} "
                f"{stats['min']:>10.6f} {stats['max']:>10.6f}"
            )
        else:
            lines.append(f"{metric:<12} {'N/A':>10} {'N/A':>10} {'N/A':>10} {'N/A':>10}")
    lines.append("")

    # Core-specific metrics (if any)
    if analysis["core_specific_metrics"]:
        lines.append("CORE-SPECIFIC METRICS")
        lines.append("-" * 40)
        lines.append(f"{'Metric':<12} {'Mean':>10} {'Std':>10} {'Min':>10} {'Max':>10}")
        lines.append("-" * 54)
        for metric, stats in analysis["core_specific_metrics"].items():
            if stats["mean"] is not None:
                lines.append(
                    f"{metric:<12} {stats['mean']:>10.6f} {stats['std']:>10.6f} "
                    f"{stats['min']:>10.6f} {stats['max']:>10.6f}"
                )
            else:
                lines.append(f"{metric:<12} {'N/A':>10} {'N/A':>10} {'N/A':>10} {'N/A':>10}")
        lines.append("")

    # Final state
    if analysis["final_state"]:
        lines.append("FINAL STATE")
        lines.append("-" * 40)
        for key, value in analysis["final_state"].items():
            if isinstance(value, float):
                lines.append(f"  {key}: {value:.6f}")
            else:
                lines.append(f"  {key}: {value}")
        lines.append("")

    # Validation
    val = analysis["validation"]
    lines.append("VALIDATION")
    lines.append("-" * 40)
    status = "PASS" if val["all_bounded"] else "FAIL"
    lines.append(f"  Bounded [0,1]: {status}")
    lines.append(f"  NaN values:    {val['total_nan']}")
    lines.append(f"  Inf values:    {val['total_inf']}")
    lines.append(f"  Below 0:       {val['total_below_zero']}")
    lines.append(f"  Above 1:       {val['total_above_one']}")
    lines.append("")
    lines.append("=" * 60)

    return "\n".join(lines)


def format_summary(analyses: List[Tuple[str, Dict[str, Any]]]) -> str:
    """Format a summary of multiple analyses."""
    lines = []
    lines.append("=" * 70)
    lines.append("CFM MULTI-RUN SUMMARY")
    lines.append("=" * 70)
    lines.append(f"Total files analyzed: {len(analyses)}")
    lines.append("")

    # Header
    lines.append(f"{'File':<30} {'Core':<8} {'Steps':>8} {'Bounded':>8}")
    lines.append("-" * 70)

    pass_count = 0
    for filename, analysis in analyses:
        short_name = os.path.basename(filename)[:28]
        core_type = analysis["metadata"]["core_type"][:6]
        steps = analysis["metadata"]["num_steps"]
        bounded = "PASS" if analysis["validation"]["all_bounded"] else "FAIL"
        if bounded == "PASS":
            pass_count += 1
        lines.append(f"{short_name:<30} {core_type:<8} {steps:>8} {bounded:>8}")

    lines.append("")
    lines.append(f"Passed: {pass_count}/{len(analyses)}")
    lines.append("=" * 70)

    return "\n".join(lines)


# ==============================================================================
# CLI INTERFACE
# ==============================================================================

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="CFM Log Analyzer - Analyze JSON run outputs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tools/cfm_log_analyzer.py --input out.json
  python tools/cfm_log_analyzer.py --input out.json --format json
  python tools/cfm_log_analyzer.py --input run1.json run2.json --summary
  python tools/cfm_log_analyzer.py --input out.json --output report.txt
        """
    )

    parser.add_argument(
        "--input",
        type=str,
        nargs="+",
        required=True,
        help="Input JSON file(s) to analyze",
    )

    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output file for report (stdout if not specified)",
    )

    parser.add_argument(
        "--format",
        type=str,
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )

    parser.add_argument(
        "--summary",
        action="store_true",
        help="Print summary of multiple files (instead of full reports)",
    )

    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress progress messages",
    )

    args = parser.parse_args()
    verbose = not args.quiet

    analyses = []

    for input_file in args.input:
        if verbose and len(args.input) > 1:
            print(f"Analyzing: {input_file}", file=sys.stderr)

        try:
            with open(input_file, "r") as f:
                run_data = json.load(f)
        except FileNotFoundError:
            print(f"Error: File not found: {input_file}", file=sys.stderr)
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in {input_file}: {e}", file=sys.stderr)
            sys.exit(1)

        analysis = analyze_run(run_data)
        analyses.append((input_file, analysis))

    # Format output
    if args.summary and len(analyses) > 1:
        output = format_summary(analyses)
    elif args.format == "json":
        if len(analyses) == 1:
            output = json.dumps(analyses[0][1], indent=2)
        else:
            output = json.dumps([a[1] for a in analyses], indent=2)
    else:
        reports = [format_text_report(a, f) for f, a in analyses]
        output = "\n\n".join(reports)

    # Write output
    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        if verbose:
            print(f"Report saved to: {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
