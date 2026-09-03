# Contributing to oreilly-agentic-ai-bootcamp

Thank you for contributing to oreilly-agentic-ai-bootcamp! This repository targets **O'Reilly Live Bootcamp** and maintains high standards for reproducibility, scientific rigor, and venue alignment.

## 📋 Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Types of Contributions](#types-of-contributions)
- [Development Setup](#development-setup)
- [Research Standards](#research-standards)
- [Pull Request Process](#pull-request-process)
- [Evidence Requirements](#evidence-requirements)

## 📜 Code of Conduct
This project follows the [Contributor Covenant](CODE_OF_CONDUCT.md). By participating, you agree to uphold this code.

## 🤔 Types of Contributions

### 🔬 Research Contributions
- **New experiments** targeting the venue scope
- **Statistical improvements** to existing analyses (pre-registered plans required)
- **Replication studies** with independent evidence packages
- **Adversarial extensions** with seeded, deterministic attack vectors

### 🛠️ Engineering Contributions
- Bug fixes with regression tests
- Performance optimizations (with benchmarks)
- CI/CD improvements
- Dependency updates (security patches prioritized)

### 📚 Documentation
- Venue-specific reproduction guides
- Statistical method explanations
- API documentation with examples

## 🛠️ Development Setup

```bash
# Clone & enter
git clone https://github.com/radanliev/oreilly-agentic-ai-bootcamp.git
cd oreilly-agentic-ai-bootcamp

# Create environment
python -m venv .venv
source .venv/bin/activate

# Install with dev dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Verify setup
python -m pytest tests/ -q
```

## 🔬 Research Standards

### Evidence Requirements
All research contributions **must** include:

1. **Frozen Evidence Package** (JSON, SHA-256 sealed)
   ```json
   {
     "repo": "oreilly-agentic-ai-bootcamp",
     "commit_sha": "abc123...",
     "evidence_hash": "sha256:...",
     "zenodo_doi": "10.5281/zenodo.XXXXXXX",
     "claims": [...],
     "statistical_analysis": {...}
   }
   ```

2. **Pre-registered Analysis Plan** (for statistical claims)
   - Hypotheses, endpoints, corrections specified *before* data collection
   - Stored in `docs/analysis-plans/`

3. **Reproducibility Artifacts**
   - `requirements.lock` (exact versions)
   - `conda-lock.yml` or Dockerfile
   - Compute requirements (GPU-hours, memory)

### Statistical Rigor
- Multiple comparison correction (Benjamini-Hochberg or Bonferroni)
- Effect sizes with confidence intervals
- Power analysis for sample sizes
- Sensitivity analyses for key assumptions

### Venue Alignment
Each repo maintains venue-specific alignment docs:
- Target venue requirements (page limits, anonymity, artifact eval)
- Claim-to-evidence mapping
- Reviewer anticipation (common objections addressed)

## 🧪 Testing Requirements

```bash
# Run full test suite
pytest -xvs --cov=oreilly_agentic_ai_bootcamp --cov-report=term-missing

# Run specific tests
pytest tests/ -xvs

# Benchmark performance
pytest tests/benchmarks/ --benchmark-only
```

**Minimum Requirements for PR:**
- ✅ All existing tests pass
- ✅ New tests for new functionality (≥90% coverage)
- ✅ Statistical tests for any claim changes
- ✅ No new `ruff`/`mypy` errors

## 🔀 Pull Request Process

### 1. Preparation
```bash
# Create feature branch from main
git checkout main && git pull
git checkout -b feat/your-contribution

# Make changes with evidence
# ... your work ...

# Run full validation
pre-commit run --all-files
pytest --cov=oreilly_agentic_ai_bootcamp
```

### 2. Commit Convention
Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body with evidence references]

[optional footer: Closes #XXX, Evidence: zenodo.XXXXXXX]
```

**Types:** `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`, `evidence`, `stats`

**Examples:**
```
evidence(oreilly-agentic-ai-bootcamp): add frozen evidence for O'Reilly Live Bootcamp submission v3
stats(oreilly-agentic-ai-bootcamp): update power analysis for battery (n=200)
feat(oreilly-agentic-ai-bootcamp): add new detection rule for injection variant
fix(oreilly-agentic-ai-bootcamp): resolve eBPF map collision in capture_admission
```

### 3. PR Requirements Checklist
- [ ] **Evidence package** uploaded to Zenodo (draft DOI in PR description)
- [ ] **Analysis plan** pre-registered (if statistical claims)
- [ ] **Tests** added/updated with ≥90% coverage
- [ ] **Documentation** updated (README, venue alignment, CHANGELOG.md)
- [ ] **CHANGELOG.md** updated under `## Unreleased`
- [ ] **CI passes** on all supported Python versions

### 4. Review Process
1. **Automated checks** (CI, pre-commit, coverage)
2. **Maintainer review** (code quality, research standards)
3. **Statistical review** (for evidence/stats changes)
4. **Venue alignment review** (for demo-level changes)
5. **Merge** (squash commits, preserve evidence trail)

---

## 🙋 Getting Help

- 💬 **Discussions**: [GitHub Discussions](https://github.com/radanliev/oreilly-agentic-ai-bootcamp/discussions)
- 🐛 **Issues**: [Bug Reports](https://github.com/radanliev/oreilly-agentic-ai-bootcamp/issues/new?template=bug_report.md)
- 📧 **Security**: security@radanliev.com (for responsible disclosure)
- 📚 **Docs**: [Documentation](https://radanliev.github.io/oreilly-agentic-ai-bootcamp/)

Thank you for advancing agentic AI security science! 🔬🛡️
