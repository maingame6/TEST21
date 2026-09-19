# Roadmap

## ACE-0 — protocol simulator
Merkle cognitive commitments, simulated root-of-trust signatures, post-commit sampling, proof verification, witness quorum, fail-closed authority gate, tamper tests.

## ACE-0.2 — real model internals
Target a small open-weight transformer. Add NNsight/TransformerLens hooks, SAE feature extraction, circuit-tracer adapter, planted hidden-objective model organisms, blind behavioural auditing, and metrics for detection/false positives/overhead.

## ACE-0.3 — causal witnesses
Frozen checkpoints, zero-authority shadow forks, activation patching/feature ablation, and causal-effect records.

## ACE-1 — two-machine authority gateway
Model host has no unrestricted network credentials; gateway mediates external effects; TPM/Keylime-style attestation; scoped capability tokens.

## ACE-2 — secure sidecar / FPGA
Independent RNG, monotonic counters, commitment hashing outside model-controlled software, hardware-bound signing key, DMA/IOMMU isolation, telemetry-loss watchdog.

## ACE-3 — accelerator-integrated cognitive telemetry
Privileged activation taps, append-only commitment stream, random projection/compression, challenge-response buffers, independently clocked audit path, and hardware I/O gating downstream of model compute.

## Success criterion
A claim such as "mechanism X contributes to concealment" must predict the result of a controlled intervention on X. Failed predictions count against the microscope.
