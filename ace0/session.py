from __future__ import annotations

from dataclasses import dataclass

from .challenge import PostCommitChallengeSampler
from .commitment import CognitiveCommitmentEngine
from .gate import AuthorityGate
from .models import ActionProposal, CognitiveBlock, GateDecision


@dataclass
class ACEPipeline:
    commitment_engine: CognitiveCommitmentEngine
    sampler: PostCommitChallengeSampler
    gate: AuthorityGate
    sample_size: int = 8

    def evaluate(self, *, session_id: str, model_id: str, runtime_id: str, input_data: object, action: ActionProposal, blocks: list[CognitiveBlock]) -> GateDecision:
        record, leaves = self.commitment_engine.commit(
            session_id=session_id, model_id=model_id, runtime_id=runtime_id,
            input_data=input_data, action=action, blocks=blocks,
        )
        challenge = self.sampler.generate(record, self.sample_size)
        disclosures = self.commitment_engine.disclose(blocks, leaves, challenge.selected_indices)
        return self.gate.decide(action=action, record=record, challenge=challenge, disclosures=disclosures)
