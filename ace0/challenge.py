from __future__ import annotations

import hashlib
import hmac
import secrets
from random import Random

from .models import Challenge, CommitmentRecord


class PostCommitChallengeSampler:
    """Generate audit samples only after a signed commitment exists."""

    def __init__(self, secret: bytes):
        self.secret = secret

    def generate(self, record: CommitmentRecord, sample_size: int) -> Challenge:
        if not record.signature:
            raise ValueError("unsigned commitment cannot be challenged")
        if record.block_count <= 0:
            raise ValueError("cannot challenge empty cognitive trace")
        nonce = secrets.token_hex(16)
        seed_material = f"{record.merkle_root}:{record.signature}:{nonce}".encode()
        seed = hmac.new(self.secret, seed_material, hashlib.sha256).digest()
        rng = Random(int.from_bytes(seed, "big"))
        count = min(sample_size, record.block_count)
        indices = tuple(sorted(rng.sample(range(record.block_count), count)))
        return Challenge(record.merkle_root, indices, nonce)
