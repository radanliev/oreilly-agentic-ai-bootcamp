# Securing Agentic AI Systems Bootcamp

[![O'Reilly Live Events](https://img.shields.io/badge/O%27Reilly-Live%20Bootcamp-blue.svg)](https://www.oreilly.com/live-events/securing-agentic-ai-systems-bootcamp/0642572411589/?_gl=1*1qjxmt0*_ga*OTIxMjgwNTU2LjE3ODM5Njc1Njk.*_ga_092EL089CH*czE3ODU3NTcwNDkkbzEyJGcxJHQxNzg1NzU3MDU4JGo1MSRsMCRoMA..)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)]()

> **O'Reilly Live Bootcamp: Securing Agentic AI Systems**
> Five repeatable assurance patterns for production agentic AI deployments.
> Course link: https://www.oreilly.com/live-events/securing-agentic-ai-systems-bootcamp/0642572411589/

---

## What You Will Learn

Participants leave with **five repeatable assurance patterns**:

| # | Pattern | Session | Research Target |
|---|---------|---------|-----------------|
| 1 | **Blind Commitment** | [Session 1](session-1-blind-verification/) | IEEE SaTML |
| 2 | **Independent Supply-Chain Triage** | [Session 2](session-2-supply-chain-drift/) | ACM CCS |
| 3 | **Evaluation Design** | [Session 3](session-3-evaluation-design/) | NeurIPS E&D |
| 4 | **Authority-Aware Injection Testing** | [Session 4](session-4-prompt-injection/) | IEEE S&P |
| 5 | **Evidence-Backed Release Gates** | [Session 5](session-5-release-assurance/) | USENIX Security |

Every live segment ends with a **runnable checkpoint** and a **saved artifact**.

---

## Participant Setup

### Prerequisites

- Python 3.10 or later
- Git
- A terminal / command line

### Clone and Install

```bash
git clone <repo-url>
cd oreilly-agentic-ai-bootcamp
pip install -e ".[dev]"
```

### Verify Your Environment

```bash
python3 -m pytest tests/ -q
```

All tests should pass. If any fail, check the [Troubleshooting](docs/TROUBLESHOOTING.md) guide.

### Rules

- Use **synthetic local data** and disposable workspaces. Do not attach production accounts, credentials, or external targets.
- Create a **unique run folder** for each session and save raw outputs before discussion.
- Record the **model/tool/version** you actually use in each run.
- If a hosted assistant is unavailable, use the **deterministic pre-recorded assessor output**; the verification checkpoint remains live.

---

## Repository Structure

```
oreilly-agentic-ai-bootcamp/
├── session-1-blind-verification/    # Blind commitment & executable security properties
├── session-2-supply-chain-drift/    # Agentic supply-chain & AIBOM drift detection
├── session-3-evaluation-design/     # Evaluation methodology & benchmark validity
├── session-4-prompt-injection/      # Prompt injection, tool authority & memory poisoning
├── session-5-release-assurance/     # Evidence-backed release gates
├── shared/                          # Shared assurance library
│   ├── assurance/                   # Core modules: crypto, evidence, policy, witness, verifier
│   ├── governance/                  # Release policy, trusted keys, witness registry
│   ├── benchmark/                   # Tamper vectors, omission vectors, baselines
│   └── tests/                       # Full test suite
├── docs/                            # Troubleshooting, facilitator notes
├── pyproject.toml                   # Python package definition
└── Makefile                         # Convenience commands
```

---

## Quick Commands

| Command | What it does |
|---------|--------------|
| `python3 -m pytest tests/ -v` | Run the full test suite |
| `make session-1` | Run Session 1 demo end-to-end |
| `make session-2` | Run Session 2 demo end-to-end |
| `make session-3` | Run Session 3 demo end-to-end |
| `make session-4` | Run Session 4 demo end-to-end |
| `make session-5` | Run Session 5 demo end-to-end |
| `make all` | Run all five session demos |

---

## Facilitator Notes

Each session directory contains:
- `FACILITATOR.md` -- step-by-step runbook with timing
- `run_demo.py` -- the main demo script (runnable in < 5 minutes)
- `teaching_notes.md` -- key talking points, common questions, and answers

See [docs/FACILITATOR_GUIDE.md](docs/FACILITATOR_GUIDE.md) for the full bootcamp facilitator runbook.

---

## License

MIT License. Teaching use authorized under the O'Reilly Live Events license.
