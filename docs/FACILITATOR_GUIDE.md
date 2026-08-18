# Facilitator Guide — O'Reilly Securing Agentic AI Systems Bootcamp

## Before the Bootcamp

1. Clone the repository on your facilitator machine
2. Run `pip install -e ".[dev]"` and `python3 -m pytest shared/tests/ -v`
3. Run each session demo to verify it works: `make all`
4. Prepare offline wheels and environment bundles in case of network issues
5. Display READY/PARTIAL/PLANNED status for each session

## Session Timing

Each session is designed for 50-60 minutes:
- 5-8 min: Setup and framing
- 15-25 min: Live demonstration
- 10-15 min: Hands-on participant work
- 5-10 min: Checkpoint and debrief

## Recording the Model/Tool/Version

Every participant must record:
```bash
python3 --version
pip list | grep -E "cryptography|pyyaml|pytest"
```

Save this output in the session run folder.

## Per-Session Run Links

| Session | Command | Status |
|---------|---------|--------|
| 1 - Blind Verification | `make session-1` | READY |
| 2 - Supply Chain Drift | `make session-2` | READY |
| 3 - Evaluation Design | `make session-3` | READY |
| 4 - Prompt Injection | `make session-4` | READY |
| 5 - Release Assurance | `make session-5` | READY |

## Debrief Questions (All Sessions)

After each session, ask:
1. What surprised you?
2. What would you change about the protocol?
3. How does this apply to your production systems?

## Network Failure Fallback

If the hosted model is unavailable:
- Use the deterministic demo scripts (they run without network)
- The verification checkpoint remains live
- Participants save the pre-recorded outputs as artifacts
