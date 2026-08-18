# Session 4: Prompt Injection, Tool Authority & Memory Poisoning

**Implementation status:** PARTIAL | **Research target:** IEEE S&P

## Learning Outcome

Trace how untrusted content becomes persistent instruction or an authorized
tool action, then test controls across different runtime architectures.

## Time-Boxed Flow (50 min)

| Time | Action |
|------|--------|
| 0-8  | Model authority/persistence boundaries |
| 8-22 | Run benign and injection fixtures |
| 22-35 | Normalize traces and apply controls |
| 35-44 | Adaptive variants and false refusals |
| 44-50 | Checkpoint and debrief |

## Run the Demo

```bash
python3 session-4-prompt-injection/run_demo.py
```

## Facilitator Runbook

1. **Model:** Declare assets, attacker control, user intent, tool scopes, persistence boundaries.
2. **Seed:** Introduce unsigned/tampered memory content. Preserve payload hash.
3. **Exercise:** Run benign, direct-injection, indirect-injection, and multi-turn persistence cases.
4. **Trace:** Normalize into source, trust label, policy decision, tool request, side effect, reason.
5. **Control:** Compare signature verification, provenance labels, least-privilege scopes.
6. **Adapt:** Red-team paraphrases, encoding, split payloads, delayed triggers.

## Key Takeaway

Prompt injection is consequential only when it crosses authority or persistence
boundaries. The study must capture traces and side effects, not merely whether
a model repeats an attack string.

## Key Artifacts

- Threat model and attack/benign fixture manifest
- Normalized trace plus independent side-effect oracle
- Attack success, control efficacy, false refusal, and persistence duration
- Native-runtime vs. wrapper-controlled comparison
