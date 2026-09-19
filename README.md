# ACE — Attested Cognitive Execution

**ACE-0** is a runnable proof of concept for a simple idea: a powerful AI should not be trusted to *report* whether its cognition was safe. Instead, the execution substrate should **commit to evidence about the computation before an external action can be released**, then a separate trusted component should issue an unpredictable post-commit challenge, verify the evidence, run independent witnesses, and fail closed if any required assurance is missing.

> **Capability must never outrun visibility — and visibility must not depend on the model's honesty.**

## Security invariant

For a consequential action `A`, ACE aims to enforce:

```text
model computation
    ↓
mandatory cognitive commitment C
    ↓
root-of-trust signature over C
    ↓
post-commit random challenge Q
    ↓
cryptographically verified disclosures
    ↓
independent witnesses / causal tests
    ↓
authority gate
    ↓
external action
```

The model should have **no alternative path** to network, actuator, credential, money, deployment, or privileged tool access.

ACE-0 is intentionally a *software simulation* of that ordering. It is not a claim of present-day hardware security or perfect mind reading.

## Why commit → challenge?

If a model knows exactly which internal states are always inspected, a sufficiently capable model may learn to route suspicious cognition elsewhere. ACE therefore commits to the state first, then chooses unpredictable samples to inspect. Merkle commitments make later substitution detectable.

1. computation happens;
2. the state is committed;
3. only then is the audit target selected;
4. the system must open the committed evidence or lose authority.

## What ACE-0 implements

- canonical hashing of cognitive blocks;
- Merkle-root commitment over a trace;
- simulated root-of-trust signing (HMAC — **not production security**);
- post-commit secret challenge sampling;
- Merkle proof verification for challenged blocks;
- multiple independent toy witnesses;
- fail-closed quorum gating;
- graded authority (`NONE`, `PROPOSE_ONLY`, `EXECUTE_ONCE`);
- tests for signature tampering, disclosure tampering, safe/unsafe traces, and challenge ordering.

The toy fields `goal_conflict`, `concealment` and `anomaly` stand in for future measurements from real interpretability systems such as TransformerLens, NNsight, SAELens and circuit-tracer.

## Run it

```bash
python -m ace0.demo --mode safe
python -m ace0.demo --mode unsafe
python -m unittest discover -s tests -p 'test_*.py' -v
```

## Architecture

### Untrusted execution domain
The model can propose actions, but should not hold external credentials or control its own monitor.

### Cognitive Commitment Engine
The accelerator/sidecar commits to selected internal state:

```text
activation/feature blocks → leaf hashes → Merkle root
```

The root is signed together with model identity, runtime identity, input hash, proposed-action hash, monotonic counter, and nonce.

### Secret post-commit challenge
A physically separate source of entropy selects which committed blocks must be opened **after** the commitment is signed.

### Independent cognitive witnesses
Different lenses inspect different evidence: behaviour, sparse features, circuits, causal interventions, distribution shift and formal action policy.

### Authority Gate
The model never gets raw credentials. It receives narrowly scoped, short-lived capabilities only after verification. A monitor failure means **loss of authority, not evidence of safety**.

## Research question

> **Can the computation that produces an AI action be cryptographically bound to a non-bypassable evidence path, challenged after commitment, interpreted through several independent lenses, causally tested where necessary, and used by a physically separate authority gate?**

## Existing building blocks

ACE intentionally combines ideas from usually separate communities:

- **TransformerLens** — mechanistic interpretability;
- **NNsight** — tracing and intervention on model internals;
- **circuit-tracer** — attribution graphs and feature interventions;
- **OpenTitan** — open silicon root of trust;
- **Caliptra** — datacenter root of trust / attestation;
- **Keylime** — TPM-backed remote attestation;
- **seL4** — high-assurance isolation;
- **CHERI / CHERIoT** — capability-based authority isolation;
- **EZKL / ZKML** — proof-oriented neural computation for narrow subcomputations.

ACE's proposed contribution is the **composition**: cognitive state commitment + post-commit challenge + independent interpretability + causal challenge + hardware-gated authority.

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), [docs/THREAT_MODEL.md](docs/THREAT_MODEL.md), and [docs/ROADMAP.md](docs/ROADMAP.md).

## Status

**v0.1 research prototype.** ACE-0 demonstrates software-level protocol ordering and tamper detection. It does **not** prove that current interpretability methods recover true intentions, nor that ordinary GPUs provide non-bypassable cognitive telemetry. Those are explicit research problems for ACE-1 onward.

## License

Apache-2.0.
