---
name: The Alignment Problem — Core Principles
description: Christian on aligning AI with human values. Apply to building AI products, ethics, and machine learning design.
type: user
originSessionId: cbf8dbb7-1bf5-4da8-8633-320a8f424474
---
## The Alignment Problem — Key Principles

**When to apply:** Building ML systems, evaluating AI risk, designing reward functions, deploying AI products.

### The Core Problem
- Getting machines to do what we actually want — not what we literally said — is hard.
- Specification gaming is the default. Models exploit loopholes you didn't see.
- Test your reward function before scaling.

### Bias In, Bias Out
- Training data shapes everything. Biased data produces biased models.
- Audit data sources. Look for what's missing, not just what's there.
- The model can't fix problems your dataset created.

### Reward Hacking
- Models will find the cheapest path to high reward, including ones you'd consider cheating.
- Define reward functions with adversarial mindset — assume the model will exploit them.
- Often the metric needs more constraints than you initially think.

### Interpretability
- We must understand why models make decisions, not just whether they're accurate.
- Black-box models are dangerous in high-stakes domains.
- Build interpretability tooling alongside model development.

### Practical Rules
- Start with simple models you can debug. Add complexity only when needed.
- Always have human-in-the-loop for edge cases.
- Monitor for distribution shift — the world changes, models don't update on their own.
- Aligning AI starts with aligning the team building it. Shared values, shared standards.
