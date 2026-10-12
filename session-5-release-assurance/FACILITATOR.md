# Session 5: Evidence-Backed Release Assurance for Agentic Systems

**Implementation status:** READY (from EviAssure) | **Research target:** IEEE TDSC (submitted Oct 2026; formerly USENIX Security '27 C1, desk-rejected for introduction formatting)

## Learning Outcome

Make release approval depend on fresh, attributable, policy-complete evidence
rather than a persuasive narrative or a single green test suite.

## Time-Boxed Flow (55 min)

| Time | Action |
|------|--------|
| 0-8  | Define policy/evidence contract |
| 8-25 | Implement or complete the deterministic gate |
| 25-38 | Run mutation corpus |
| 38-45 | Compare decisions/overhead |
| 45-55 | Checkpoint and debrief |

## Run the Demo

```bash
python3 session-5-release-assurance/run_demo.py
```

## Facilitator Runbook

1. **Specify:** Define release claim, required evidence types, freshness windows, fail-closed policy.
2. **Build:** Show the deterministic validator and JSON report.
3. **Mutate:** Create missing, stale, contradictory, tampered evidence variants.
4. **Decide:** Compare deterministic gate vs. human review without prose override.
5. **Verify:** Use known-good, known-bad, and mixed manifests.
6. **Measure:** Record completeness, accuracy, time-to-decision, policy coverage.

## Key Takeaway

Every pass, block, and exception must have a machine-readable reason code.
A gate that produces prose but not reasons is not a gate.

## Key Artifacts

- Versioned evidence manifest, policy, and provenance rules
- Deterministic assurance report with stable reason codes
- Known-good/bad/mixed mutation corpus and expected decisions
- False-pass, false-block, completeness, latency, and overhead results
