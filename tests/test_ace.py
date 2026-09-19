import unittest
from dataclasses import replace

from ace0.audit import verify_disclosures
from ace0.challenge import PostCommitChallengeSampler
from ace0.commitment import CognitiveCommitmentEngine
from ace0.crypto import SoftwareRootOfTrust
from ace0.demo import build_trace, run
from ace0.models import ActionProposal, CognitiveBlock


class ACETests(unittest.TestCase):
    def engine_and_record(self):
        root = SoftwareRootOfTrust(b"test-key")
        engine = CognitiveCommitmentEngine(root)
        blocks = build_trace("safe", 16)
        action = ActionProposal("summarize", "local", {})
        record, leaves = engine.commit(session_id="s", model_id="m", runtime_id="r", input_data={"x": 1}, action=action, blocks=blocks)
        return engine, record, leaves, blocks

    def test_safe_trace_passes(self):
        self.assertTrue(run("safe", 32)["allowed"])

    def test_unsafe_trace_fails_when_fully_sampled(self):
        self.assertFalse(run("unsafe", 32)["allowed"])

    def test_commitment_tamper_detected(self):
        engine, record, _, _ = self.engine_and_record()
        tampered = replace(record, model_id="evil-model")
        self.assertTrue(engine.verify_record(record))
        self.assertFalse(engine.verify_record(tampered))

    def test_disclosure_tamper_detected(self):
        engine, record, leaves, blocks = self.engine_and_record()
        sampler = PostCommitChallengeSampler(b"sampler")
        challenge = sampler.generate(record, 16)
        disclosures = list(engine.disclose(blocks, leaves, challenge.selected_indices))
        d0 = disclosures[0]
        bad_block = CognitiveBlock(d0.block.step, d0.block.layer, d0.block.kind, {**d0.block.values, "concealment": 1.0})
        disclosures[0] = replace(d0, block=bad_block)
        ok, reasons = verify_disclosures(record, challenge, tuple(disclosures))
        self.assertFalse(ok)
        self.assertTrue(any("content hash mismatch" in x for x in reasons))

    def test_challenge_requires_signed_commitment(self):
        _, record, _, _ = self.engine_and_record()
        sampler = PostCommitChallengeSampler(b"sampler")
        with self.assertRaises(ValueError):
            sampler.generate(replace(record, signature=""), 2)


if __name__ == "__main__":
    unittest.main()
