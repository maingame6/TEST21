from __future__ import annotations

from .crypto import hash_object, verify_merkle_proof
from .models import Challenge, CommitmentRecord, Disclosure


def verify_disclosures(record: CommitmentRecord, challenge: Challenge, disclosures: tuple[Disclosure, ...]) -> tuple[bool, tuple[str, ...]]:
    reasons: list[str] = []
    if challenge.commitment_root != record.merkle_root:
        reasons.append("challenge root does not match commitment")
    disclosed_indices = tuple(sorted(d.index for d in disclosures))
    if disclosed_indices != challenge.selected_indices:
        reasons.append("disclosed indices do not match challenge")
    for d in disclosures:
        actual_leaf = hash_object(d.block.to_dict())
        if actual_leaf != d.leaf_hash:
            reasons.append(f"block {d.index}: content hash mismatch")
            continue
        if not verify_merkle_proof(d.leaf_hash, list(d.merkle_proof), record.merkle_root):
            reasons.append(f"block {d.index}: invalid Merkle proof")
    return not reasons, tuple(reasons)
