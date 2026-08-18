# Session 1: Blind Verification & Executable Security Properties

**Implementation status:** READY | **Research target:** IEEE SaTML

## Learning Outcome

Commit to a predicted failure location before reveal, score the commitment
after reveal, and require an executable red-to-green patch result.

## Time-Boxed Flow (50 min)

| Time | Action |
|------|--------|
| 0-5  | Frame the falsifiable claim and freeze the environment |
| 5-18 | Blind prediction and seal |
| 18-30 | Reveal and score |
| 30-43 | Patch oracle and negative control |
| 43-50 | Checkpoint and debrief |

## Run the Demo

```bash
python3 session-1-blind-verification/run_demo.py
```

## Facilitator Runbook

1. **Freeze:** Record commit, environment, model/tool version. Do NOT expose the defect.
2. **Commit:** Produce a schema-valid prediction with cited files, trust boundaries, failure family, confidence. Seal its hash.
3. **Reveal:** Apply the v1-vulnerability condition. Preserve the reveal event separately.
4. **Score:** Calculate localization/structure recall. Compare blind, hindsight, random controls.
5. **Patch:** Apply a candidate diff in a clean workspace. Gold patch must pass; wrong patch must stay red.
6. **Audit:** Package predictions, seals, ground truth, scores, and limitations without editing failed runs.

## Why This Matters

It turns an agent-security explanation into a falsifiable claim. The ordering
(commit → reveal → score → patch) prevents hindsight from masquerading as
verification.

## Key Artifacts

- Sealed pre-reveal prediction and independent reveal log
- Ground-truth file/failure-family mapping and scorer output
- High/low/random/hindsight conditions with uncertainty and exact tests
- Gold-patch success plus wrong-target negative control
