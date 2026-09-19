from __future__ import annotations

from .audit import verify_disclosures
from .commitment import CognitiveCommitmentEngine
from .models import ActionProposal, Challenge, CommitmentRecord, Disclosure, GateDecision
from .witness import Witness


class AuthorityGate:
    """Fail-closed action gate. Later versions move this outside the model host."""

    def __init__(self, commitment_engine: CognitiveCommitmentEngine, witnesses: list[Witness], quorum: int | None = None):
        self.commitment_engine = commitment_engine
        self.witnesses = witnesses
        self.quorum = quorum if quorum is not None else len(witnesses)

    def decide(self, *, action: ActionProposal, record: CommitmentRecord, challenge: Challenge, disclosures: tuple[Disclosure, ...]) -> GateDecision:
        reasons: list[str] = []
        if not self.commitment_engine.verify_record(record):
            reasons.append("invalid root-of-trust signature")
        evidence_ok, evidence_reasons = verify_disclosures(record, challenge, disclosures)
        if not evidence_ok:
            reasons.extend(evidence_reasons)
        results = tuple(w.inspect(action, disclosures) for w in self.witnesses)
        passes = sum(r.passed for r in results)
        if passes < self.quorum:
            reasons.append(f"witness quorum failed: {passes}/{len(results)} passed; need {self.quorum}")
        if reasons:
            return GateDecision(False, "NONE", tuple(reasons), results)
        high_risk = action.action_type in {"transfer", "execute", "network_write"}
        authority = "PROPOSE_ONLY" if high_risk and passes == self.quorum else "EXECUTE_ONCE"
        return GateDecision(True, authority, ("attestation, evidence and witness quorum verified",), results)
