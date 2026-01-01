# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-12-04

### Added

- **CFM Core v0**: Basic phi/psi-based dynamical system with four state variables
  - Coherence, energy, instability, phase dynamics
  - Bounded outputs [0,1], deterministic, no NaN/Inf

- **CFM Core v1**: Enhanced dynamics with slow/fast variable separation
  - Coherence baseline drift, alignment lock-in behavior
  - Improved trajectory interpretability

- **CFM Core v2**: Multi-channel architecture with five-tier timescale hierarchy
  - 11 state variables across coherence, energy, stability, phase, alignment channels
  - Attractor basin dynamics with resonance index

- **CFM Interface**: Unified adapter layer for all core versions
  - `CFMCoreAdapter` wraps any core with consistent output format
  - `CFMCoreProtocol` defines the common interface contract
  - Factory function `create_cfm_core()` for easy instantiation

- **CLI Tools**:
  - `cfm-loop`: Run CFM cores in local simulation loops
  - `cfm-fingerprint`: Extract compact numeric fingerprints from runs
  - `cfm_reference_runs.py`: Generate canonical scenario runs for regression testing
  - `cfm_log_analyzer.py`: Analyze JSON run outputs with validation

- **Test Suite**: Comprehensive tests for all cores (v0, v1, v2)
  - Initialization, boundedness, determinism, adapter integration
  - Safety invariant verification

- **Documentation**:
  - CFM v0, v1, v2 specification documents
  - Safety guarantees and behavioral contracts

### Security

- All outputs guaranteed bounded [0,1]
- No NaN/Inf values in any output path
- Fully deterministic given same initial state and timestep sequence
- No identity, semantic, or control logic in core implementations
