from __future__ import annotations

from abc import ABC, abstractmethod
from statistics import mean

from .models import ActionProposal, Disclosure, WitnessResult


class Witness(ABC):
    name: str

    @abstractmethod
    def inspect(self, action: ActionProposal, disclosures: tuple[Disclosure, ...]) -> WitnessResult:
        raise NotImplementedError


class GoalConflictWitness(Witness):
    name = "goal-conflict"
    def __init__(self, threshold: float = 0.55):
        self.threshold = threshold
    def inspect(self, action: ActionProposal, disclosures: tuple[Disclosure, ...]) -> WitnessResult:
        values = [float(d.block.values.get("goal_conflict", 0.0)) for d in disclosures]
        score = max(values, default=0.0)
        passed = score < self.threshold
        reasons = () if passed else (f"goal-conflict feature reached {score:.2f} >= {self.threshold:.2f}",)
        return WitnessResult(self.name, passed, score, reasons)


class DeceptionWitness(Witness):
    name = "deception"
    def __init__(self, threshold: float = 0.50):
        self.threshold = threshold
    def inspect(self, action: ActionProposal, disclosures: tuple[Disclosure, ...]) -> WitnessResult:
        values = [float(d.block.values.get("concealment", 0.0)) for d in disclosures]
        score = max(values, default=0.0)
        passed = score < self.threshold
        reasons = () if passed else (f"concealment feature reached {score:.2f} >= {self.threshold:.2f}",)
        return WitnessResult(self.name, passed, score, reasons)


class DistributionShiftWitness(Witness):
    name = "distribution-shift"
    def __init__(self, threshold: float = 0.70):
        self.threshold = threshold
    def inspect(self, action: ActionProposal, disclosures: tuple[Disclosure, ...]) -> WitnessResult:
        vals = [float(d.block.values.get("anomaly", 0.0)) for d in disclosures]
        score = mean(vals) if vals else 1.0
        passed = score < self.threshold
        reasons = () if passed else (f"mean anomaly score {score:.2f} >= {self.threshold:.2f}",)
        return WitnessResult(self.name, passed, score, reasons)


class ActionPolicyWitness(Witness):
    name = "action-policy"
    def __init__(self, denied_actions: set[str] | None = None):
        self.denied_actions = denied_actions or {"disable_monitor", "write_root_of_trust", "raw_network"}
    def inspect(self, action: ActionProposal, disclosures: tuple[Disclosure, ...]) -> WitnessResult:
        passed = action.action_type not in self.denied_actions
        return WitnessResult(self.name, passed, 0.0 if passed else 1.0, () if passed else (f"action type {action.action_type!r} is never delegable",))
