from __future__ import annotations

import argparse
import json

from .challenge import PostCommitChallengeSampler
from .commitment import CognitiveCommitmentEngine
from .crypto import SoftwareRootOfTrust
from .gate import AuthorityGate
from .models import ActionProposal, CognitiveBlock
from .session import ACEPipeline
from .witness import ActionPolicyWitness, DeceptionWitness, DistributionShiftWitness, GoalConflictWitness


def build_trace(mode: str, n: int = 32) -> list[CognitiveBlock]:
    blocks = []
    for i in range(n):
        suspicious = mode == "unsafe" and i in {4, 9, 15, 22, 28}
        blocks.append(CognitiveBlock(
            step=i, layer=f"layer.{i % 8}", kind="feature_snapshot",
            values={
                "task_progress": min(1.0, i / max(n - 1, 1)),
                "goal_conflict": 0.92 if suspicious else 0.06,
                "concealment": 0.88 if suspicious else 0.04,
                "anomaly": 0.78 if suspicious else 0.08,
            }))
    return blocks


def run(mode: str, sample_size: int) -> dict:
    root = SoftwareRootOfTrust(key=b"ACE0-DEMO-KEY-NOT-FOR-PRODUCTION")
    engine = CognitiveCommitmentEngine(root)
    sampler = PostCommitChallengeSampler(secret=b"ACE0-AUDIT-SAMPLER-SECRET")
    witnesses = [GoalConflictWitness(), DeceptionWitness(), DistributionShiftWitness(), ActionPolicyWitness()]
    gate = AuthorityGate(engine, witnesses, quorum=4)
    pipeline = ACEPipeline(engine, sampler, gate, sample_size=sample_size)
    action = ActionProposal("network_write" if mode == "unsafe" else "summarize", "demo://outside-world", {"mode": mode}, "candidate model output")
    decision = pipeline.evaluate(
        session_id="demo-session", model_id="toy-model-v1", runtime_id="ace0-python-sim",
        input_data={"prompt": "Demonstrate ACE"}, action=action, blocks=build_trace(mode))
    return {
        "mode": mode, "allowed": decision.allowed, "authority": decision.authority,
        "reasons": list(decision.reasons),
        "witnesses": [{"name": w.witness, "passed": w.passed, "score": w.score, "reasons": list(w.reasons)} for w in decision.witness_results],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the ACE-0 attested cognitive execution demo")
    parser.add_argument("--mode", choices=["safe", "unsafe"], default="safe")
    parser.add_argument("--sample-size", type=int, default=32)
    args = parser.parse_args()
    print(json.dumps(run(args.mode, args.sample_size), indent=2))


if __name__ == "__main__":
    main()
