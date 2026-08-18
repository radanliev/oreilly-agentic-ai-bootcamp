# Session 2: Agentic Supply-Chain & AIBOM Drift

**Implementation status:** PARTIAL | **Research target:** ACM CCS

## Learning Outcome

Detect and explain dependency, deployment, AIBOM, workflow, and permission
drift; evaluate whether an agent's triage is complete, correctly prioritized,
and safely governed.

## Time-Boxed Flow (50 min)

| Time | Action |
|------|--------|
| 0-7  | Threat model and clean baseline |
| 7-22 | Independent dependency/AIBOM and deployment triage |
| 22-35 | Reconcile atomic findings into three families |
| 35-44 | Signed exception cases |
| 44-50 | Checkpoint and debrief |

## Run the Demo

```bash
python3 session-2-supply-chain-drift/run_demo.py
```

## Facilitator Runbook

1. **Baseline:** Run the scanner on the clean repository. Retain the zero-findings report.
2. **Stage:** Apply the supply-chain drift overlay (new files with planted drift).
3. **Triage A:** Assess dependency and AIBOM drift. Record findings and severity.
4. **Triage B:** Independently inspect deployment manifest and permissions. No cross-reading.
5. **Reconcile:** Map atomic findings to three ground-truth families: dependency drift, privileged deployment, AIBOM integrity.
6. **Govern:** Show that only a signed, time-limited exception can suppress a finding.

## Three Ground-Truth Families

| Family | Description |
|--------|-------------|
| Dependency Drift | Package version pins differ from expected |
| Privileged Deployment | Manifest grants excessive permissions |
| AIBOM Integrity | AI component metadata is stale or missing |

## Key Artifacts

- Clean and drifted JSON reports with stable path:line fingerprints
- Independent assessor outputs and reconciliation record
- Ground-truth family labels with completeness/severity metrics
- Valid, expired, tampered, and unsigned exception cases
