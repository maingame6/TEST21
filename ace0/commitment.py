from __future__ import annotations

import secrets
from dataclasses import replace

from .crypto import SoftwareRootOfTrust, hash_object, merkle_proof, merkle_root
from .models import ActionProposal, CognitiveBlock, CommitmentRecord, Disclosure


class CognitiveCommitmentEngine:
    def __init__(self, root: SoftwareRootOfTrust):
        self.root = root
        self._counter = 0

    def commit(
        self,
        *,
        session_id: str,
        model_id: str,
        runtime_id: str,
        input_data: object,
        action: ActionProposal,
        blocks: list[CognitiveBlock],
    ) -> tuple[CommitmentRecord, list[str]]:
        self._counter += 1
        leaves = [hash_object(b.to_dict()) for b in blocks]
        record = CommitmentRecord(
            session_id=session_id,
            model_id=model_id,
            runtime_id=runtime_id,
            input_hash=hash_object(input_data),
            proposed_action_hash=hash_object(action.to_dict()),
            block_count=len(blocks),
            merkle_root=merkle_root(leaves),
            monotonic_counter=self._counter,
            nonce=secrets.token_hex(16),
        )
        signature = self.root.sign(record.unsigned())
        return replace(record, signature=signature), leaves

    def verify_record(self, record: CommitmentRecord) -> bool:
        return self.root.verify(record.unsigned(), record.signature)

    @staticmethod
    def disclose(blocks: list[CognitiveBlock], leaves: list[str], indices: tuple[int, ...]) -> tuple[Disclosure, ...]:
        return tuple(
            Disclosure(
                index=i,
                block=blocks[i],
                leaf_hash=leaves[i],
                merkle_proof=tuple(merkle_proof(leaves, i)),
            )
            for i in indices
        )
