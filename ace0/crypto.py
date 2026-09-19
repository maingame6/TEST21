from __future__ import annotations

import hashlib
import hmac
import json
from dataclasses import dataclass
from typing import Any, Iterable


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def hash_object(value: Any) -> str:
    return sha256(canonical_json(value))


def hash_pair(left: str, right: str) -> str:
    return sha256(bytes.fromhex(left) + bytes.fromhex(right))


def merkle_root(leaves: Iterable[str]) -> str:
    level = list(leaves)
    if not level:
        return sha256(b"")
    while len(level) > 1:
        if len(level) % 2:
            level.append(level[-1])
        level = [hash_pair(level[i], level[i + 1]) for i in range(0, len(level), 2)]
    return level[0]


def merkle_proof(leaves: list[str], index: int) -> list[tuple[str, str]]:
    if not (0 <= index < len(leaves)):
        raise IndexError(index)
    proof: list[tuple[str, str]] = []
    idx = index
    level = list(leaves)
    while len(level) > 1:
        if len(level) % 2:
            level.append(level[-1])
        sibling = idx ^ 1
        proof.append(("left" if sibling < idx else "right", level[sibling]))
        next_level = [hash_pair(level[i], level[i + 1]) for i in range(0, len(level), 2)]
        idx //= 2
        level = next_level
    return proof


def verify_merkle_proof(leaf_hash: str, proof: list[tuple[str, str]], root: str) -> bool:
    current = leaf_hash
    for side, sibling in proof:
        current = hash_pair(sibling, current) if side == "left" else hash_pair(current, sibling)
    return hmac.compare_digest(current, root)


@dataclass(frozen=True)
class SoftwareRootOfTrust:
    """Simulation only. Replace with TPM/OpenTitan/Caliptra-backed signing in ACE-1+."""

    key: bytes
    key_id: str = "ace0-software-root"

    def sign(self, payload: Any) -> str:
        return hmac.new(self.key, canonical_json(payload), hashlib.sha256).hexdigest()

    def verify(self, payload: Any, signature: str) -> bool:
        expected = self.sign(payload)
        return hmac.compare_digest(expected, signature)
