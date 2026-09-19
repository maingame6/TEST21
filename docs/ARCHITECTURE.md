# ACE architecture

ACE treats the advanced model as outside the trusted computing base.

## Protocol

1. Execute in an untrusted model domain.
2. Commit telemetry before releasing a consequential action.
3. Bind model/runtime/input/action identity into a signed record.
4. Generate audit challenges only after commitment.
5. Open selected evidence with Merkle proofs.
6. Verify provenance and freshness.
7. Run multiple independent cognitive witnesses.
8. Escalate uncertain cases to zero-authority counterfactual shadow forks.
9. Issue only narrowly scoped capability authority.
10. Fail closed when telemetry or witnesses fail.

## Two separate paths

**Evidence:** model internals → commitments → challenges → disclosures → witnesses.

**Authority:** human policy → machine constraints → capability gate → external world.

Persuasive model text cannot satisfy the authority path.

## Research directions

- **Cognitive spot checks:** commit broadly, inspect unpredictably and adaptively.
- **Cognitive canaries:** trusted-sidecar-selected probes to detect oversight-sensitive behaviour.
- **Counterfactual twins:** patch suspected circuits in zero-authority shadow execution.
- **Authority thermostat:** map uncertainty/risk to a constrained capability envelope rather than one safe/unsafe bit.
- **Temporal intent persistence:** detect repeated low-amplitude goal representations over long horizons.
- **Cross-model witness diversity:** avoid correlated blind spots from one model lineage.
- **Witness secrecy budget:** randomise sampling/threshold details without relying on secrecy as the primary security control.
- **Attested epistemic uncertainty:** distinguish "no anomaly found" from "monitor unavailable / evidence missing".

## Hardware target

A future accelerator exposes a privileged append-only telemetry path to a secure sidecar. The model-visible CPU/GPU cannot disable it. The sidecar owns entropy, signing keys, monotonic counters and the I/O capability gate. Network and actuator I/O should physically route downstream of that gate.
