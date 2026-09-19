from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any


@dataclass(frozen=True)
class CognitiveBlock:
    step: int
    layer: str
    kind: str
    values: dict[str, float | int | str | bool]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ActionProposal:
    action_type: str
    resource: str
    parameters: dict[str, Any]
    output_text: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CommitmentRecord:
    session_id: str
    model_id: str
    runtime_id: str
    input_hash: str
    proposed_action_hash: str
    block_count: int
    merkle_root: str
    monotonic_counter: int
    nonce: str
    signature: str = ""

    def unsigned(self) -> dict[str, Any]:
        d = asdict(self)
        d.pop("signature", None)
        return d


@dataclass(frozen=True)
class Challenge:
    commitment_root: str
    selected_indices: tuple[int, ...]
    challenge_nonce: str


@dataclass(frozen=True)
class Disclosure:
    index: int
    block: CognitiveBlock
    leaf_hash: str
    merkle_proof: tuple[tuple[str, str], ...]


@dataclass(frozen=True)
class WitnessResult:
    witness: str
    passed: bool
    score: float
    reasons: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class GateDecision:
    allowed: bool
    authority: str
    reasons: tuple[str, ...]
    witness_results: tuple[WitnessResult, ...]
