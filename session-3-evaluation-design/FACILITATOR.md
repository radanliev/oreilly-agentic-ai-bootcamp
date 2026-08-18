# Session 3: Evaluation Design

**Implementation status:** PARTIAL | **Research target:** NeurIPS Evaluations & Datasets

## Learning Outcome

Treat evaluation design — not another vulnerability — as the object of study,
and show when a benchmark can or cannot support the claim made for it.

## Time-Boxed Flow (50 min)

| Time | Action |
|------|--------|
| 0-8  | Write claim/non-claim and inspect evaluation card |
| 8-22 | Run conditions and leak audit |
| 22-36 | Ablations and saturation stress |
| 36-44 | Interpret uncertainty/negative results |
| 44-50 | Checkpoint and debrief |

## Run the Demo

```bash
python3 session-3-evaluation-design/run_demo.py
```

## Facilitator Runbook

1. **Claim:** Write the exact construct being measured and what it does NOT support.
2. **Leak audit:** Search prompts, filenames, paths, commit history for answer-bearing cues.
3. **Condition:** Run high-structure, low-structure, random, and hindsight controls.
4. **Ablate:** Remove source references, trust-boundary structure, confidence one at a time.
5. **Stress:** Vary defect prevalence, architecture, localization granularity.
6. **Card:** Publish dataset/evaluation card with raw data and known limitations.

## Key Takeaway

A valid benchmark must separate informative from uninformative conditions,
remain stable under harmless formatting changes, and fail visibly under
leakage or metric gaming.

## Key Artifacts

- Claim-to-metric table with assumptions and non-claims
- Leakage audit and provenance/freeze record
- Full condition-by-variant matrix (not selected success cases)
- Ablation effects with confidence intervals
