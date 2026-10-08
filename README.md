<p align="center">
  <img src="https://raw.githubusercontent.com/radanliev/oreilly-agentic-ai-bootcamp/main/assets/logo.svg" alt="O'Reilly Bootcamp Logo" width="180">
</p>

<h1 align="center">Securing Agentic AI Systems Bootcamp</h1>
<p align="center">
  <strong>Five repeatable assurance patterns for production agentic AI deployments — hands-on labs from the O'Reilly Live Bootcamp.</strong>
</p>

<p align="center">
  <a href="https://github.com/radanliev/oreilly-agentic-ai-bootcamp/actions/workflows/ci.yml"><img src="https://img.shields.io/github/actions/workflow/status/radanliev/oreilly-agentic-ai-bootcamp/ci.yml?branch=main&label=Build&style=flat-square" alt="Build Status"></a>
  <a href="https://pypi.org/project/oreilly-agentic-ai-bootcamp/"><img src="https://img.shields.io/pypi/v/oreilly-agentic-ai-bootcamp?style=flat-square&label=PyPI" alt="PyPI Version"></a>
  <a href="https://pypi.org/project/oreilly-agentic-ai-bootcamp/"><img src="https://img.shields.io/pypi/pyversions/oreilly-agentic-ai-bootcamp?style=flat-square" alt="Python Versions"></a>
  <a href="https://github.com/radanliev/oreilly-agentic-ai-bootcamp/blob/main/LICENSE"><img src="https://img.shields.io/github/license/radanliev/oreilly-agentic-ai-bootcamp?style=flat-square" alt="License"></a>
  <a href="https://github.com/radanliev/oreilly-agentic-ai-bootcamp/stargazers"><img src="https://img.shields.io/github/stars/radanliev/oreilly-agentic-ai-bootcamp?style=flat-square" alt="Stars"></a>
  <a href="https://www.oreilly.com/live-events/securing-agentic-ai-systems-bootcamp/0642572411589/"><img src="https://img.shields.io/badge/O%27Reilly-Live%20Bootcamp-blue?style=flat-square" alt="O'Reilly Live Bootcamp"></a>
</p>

<p align="center">
  <a href="#-what-you-will-learn">Learn</a> •
  <a href="#-five-assurance-patterns">Patterns</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-session-details">Sessions</a> •
  <a href="#-repository-structure">Structure</a> •
  <a href="#-facilitator-guide">Facilitator</a> •
  <a href="#-rules-of-engagement">Rules</a> •
  <a href="#-citation">Citation</a> •
  <a href="#-contributing">Contributing</a> •
  <a href="#-license">License</a>
</p>

---

## 🎓 What You Will Learn

Participants leave with **five repeatable assurance patterns** — each grounded in peer-reviewed research targeting top-tier security/ML venues:

| # | Pattern | Session | Research Target | Core Idea |
|---|---------|---------|-----------------|-----------|
| **1** | **Blind Commitment** | [Session 1](session-1-blind-verification/) | IEEE SaTML 2027 | Commit to where defects live *before* reveal; test against executable checks |
| **2** | **Independent Supply-Chain Triage** | [Session 2](session-2-supply-chain-drift/) | ACM CCS 2026 | Fail-closed AIBOM drift detection across deps, containers, K8s, CI |
| **3** | **Evaluation Design** | [Session 3](session-3-evaluation-design/) | NeurIPS 2027 E&D | Executable invariants for leakage, saturation, IRT — with honest negative results |
| **4** | **Authority-Aware Injection Testing** | [Session 4](session-4-prompt-injection/) | IEEE S&P 2027 | Capability-based mediation for tool-using agents (Adaptive adversary A1–A6) |
| **5** | **Evidence-Backed Release Gates** | [Session 5](session-5-release-assurance/) | IEEE S&P 2027 Cycle 2 | Cryptographic attestation, fail-closed gates, witness protocol |

> **Every live segment ends with a runnable checkpoint and a saved artifact.**

---

## 🔑 Five Assurance Patterns Deep Dive

### Pattern 1: Blind Commitment (SaTML)
> **Flip the order:** Predict the security defect before you see it. Then test the prediction against executable checks.

- **Blind commitment** — cite files, trust boundaries, STRIDE labels on a clean system
- **Controlled reveal** — planted defect variants become visible
- **Executable score** — red→green invariant tests + localization metrics
- **Patch oracle** — unified diff must apply and re-verify

### Pattern 2: Independent Supply-Chain Triage (CCS)
> **Fail-closed enforcement** of the agentic AIBOM–privilege policy gap — pre-deploy multi-surface validation.

- 11 atomic findings across 5 surfaces (deps, containers, K8s, CI, AIBOM)
- HMAC-signed, time-limited exception governance
- Cryptographic waiver system (no unsigned exceptions)

### Pattern 3: Evaluation Design (NeurIPS)
> **Executable, fail-closed pre-publication gate** for evaluation suites — with honest labelling of what diagnostics can/cannot do.

- Corpus-level Jaccard leakage: fails (1/302 recovery)
- Per-item 3-gram containment: works but threshold doesn't transfer
- Saturation index: provably identical to mean accuracy on binary data
- IRT 2PL: descriptive only; proportion correct more reproducible
- Gate itself costs measurement precision (80.7% test info removed)

### Pattern 4: Authority-Aware Injection Testing (IEEE S&P)
> **Capability-based authority mediation** for tool-using agents.

- Live LLM-in-the-loop factorial across 3 model families
- Adaptive adversary suite (A1–A6) against shipped enforcement
- Dual SU metrics (ambient/interactive/attested)
- Explicit TCB (Trusted Computing Base)

### Pattern 5: Evidence-Backed Release Gates (IEEE S&P 2027 Cycle 2)
> **Cryptographic attestation, fail-closed gates, tamper-resilient audit.**

- SHA-256 Merkle tree attestation (RFC 6962 domain separation)
- Ed25519 evidence packaging with nonces/timestamps
- Witness protocol: sequence-bound receipts + signed closing counts
- 17 tamper vectors (16/17 blocked), 7 omission vectors (7/7 detected)

---

## ⚙️ Quick Start

### Prerequisites
- Python 3.10 or later
- Git
- Terminal / command line

### Clone and Install
```bash
git clone https://github.com/radanliev/oreilly-agentic-ai-bootcamp.git
cd oreilly-agentic-ai-bootcamp
pip install -e ".[dev]"
```

### Verify Your Environment
```bash
python3 -m pytest tests/ -q
# All tests should pass. If any fail, check docs/TROUBLESHOOTING.md
```

---

## 📚 Session Details

Each session directory contains:
- **`FACILITATOR.md`** — step-by-step runbook with timing
- **`run_demo.py`** — main demo script (runnable in < 5 minutes)
- **`teaching_notes.md`** — key talking points, common questions, answers

### Quick Commands

| Command | What it does |
|---------|--------------|
| `python3 -m pytest tests/ -v` | Run full test suite |
| `make session-1` | Run Session 1 demo end-to-end |
| `make session-2` | Run Session 2 demo end-to-end |
| `make session-3` | Run Session 3 demo end-to-end |
| `make session-4` | Run Session 4 demo end-to-end |
| `make session-5` | Run Session 5 demo end-to-end |
| `make all` | Run all five session demos |

### Session Overview

| Session | Directory | Demo Script | Facilitator Guide |
|---------|-----------|-------------|-------------------|
| 1 | `session-1-blind-verification/` | `run_demo.py` | `FACILITATOR.md` |
| 2 | `session-2-supply-chain-drift/` | `run_demo.py` | `FACILITATOR.md` |
| 3 | `session-3-evaluation-design/` | `run_demo.py` | `FACILITATOR.md` |
| 4 | `session-4-prompt-injection/` | `run_demo.py` | `FACILITATOR.md` |
| 5 | `session-5-release-assurance/` | `run_demo.py` | `FACILITATOR.md` |

---

## 📁 Repository Structure

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
│   ├── TROUBLESHOOTING.md
│   └── FACILITATOR_GUIDE.md
├── pyproject.toml                   # Python package definition
└── Makefile                         # Convenience commands
```

---

## 📋 Rules of Engagement

| Rule | Rationale |
|------|-----------|
| **Use synthetic local data and disposable workspaces** | No production accounts, credentials, or external targets |
| **Create a unique run folder for each session** | Save raw outputs before discussion |
| **Record the model/tool/version actually used** | Reproducibility |
| **If hosted assistant unavailable, use deterministic pre-recorded assessor output** | Verification checkpoint remains live |

---

## 📖 Citation

```bibtex
@misc{radanliev2025oreillybootcamp,
  title={Securing Agentic AI Systems Bootcamp: Five Repeatable Assurance Patterns for Production Deployments},
  author={Radanliev, Petar},
  year={2025},
  note={O'Reilly Live Bootcamp},
  url={https://github.com/radanliev/oreilly-agentic-ai-bootcamp}
}
```

**Course Link**: https://www.oreilly.com/live-events/securing-agentic-ai-systems-bootcamp/0642572411589/

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Core** | Python 3.10+ |
| **Shared Library** | `shared/assurance/`, `shared/governance/`, `shared/benchmark/` |
| **Testing** | pytest |
| **Packaging** | setuptools, pyproject.toml |
| **Build** | Makefile convenience commands |
| **CI/CD** | GitHub Actions |

---

## 🤝 Contributing

This bootcamp repository is designed for educational delivery. Contributions welcome for:

- 🐛 Fixing demo scripts or test failures
- 💡 Improving facilitator guides or teaching notes
- 🔀 Updating for new model/tool versions
- 📝 Adding troubleshooting entries

See [CONTRIBUTING.md](CONTRIBUTING.md) for workflow.

---

## 📄 License

**MIT License** — teaching use authorized under the O'Reilly Live Events license. See [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- **O'Reilly Live Events** for hosting the bootcamp
- **Oxford Lagrange** for compute credits
- **Participants** of the Securing Agentic AI Systems Bootcamp
- **Agentic AI Security research community** (demos 1–10) for underlying patterns

---

<p align="center">
  <strong>Five patterns. Five venues. One bootcamp. Production-ready assurance for agentic AI.</strong>
</p>

<p align="center">
  <a href="https://github.com/radanliev/oreilly-agentic-ai-bootcamp/stargazers">⭐ Star</a> •
  <a href="https://github.com/radanliev/oreilly-agentic-ai-bootcamp/fork">🍴 Fork</a> •
  <a href="https://github.com/radanliev/oreilly-agentic-ai-bootcamp/issues">🐛 Report Issue</a> •
  <a href="https://github.com/radanliev/oreilly-agentic-ai-bootcamp/discussions">💬 Discuss</a>
</p>