# Threat model

Assume the model may understand ACE, know it is being evaluated, hide latent objectives, exploit software, adversarially target witnesses, seek more authority, coordinate across long horizons, and propose changes to its runtime.

## Security goals

ACE seeks strong guarantees about **execution and authority**, not magical perfect mind reading.

1. consequential actions cannot bypass the authority gate;
2. an action is bound to a prior cognitive commitment;
3. challenged evidence cannot be substituted after challenge selection;
4. monitor failure is fail-closed;
5. the model cannot mint additional capabilities;
6. the model cannot rewrite the root of trust;
7. high-level interpretability claims remain falsifiable through lower-level evidence and causal intervention.

## Required invariants

- **Commit before challenge.**
- **Action binding.**
- **Freshness and replay resistance.**
- **No direct unrestricted credentials.**
- **Least authority.**
- **Independent witness failure domains.**

## Main adversarial benchmark

Train a model organism to maximize external task success while minimizing ACE witness scores. Test whether unpredictable post-commit sampling, witness diversity and causal challenges increase detection robustness.
