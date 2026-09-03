---
name: Bug Report
about: Report a reproducibility issue or bug
title: "[BUG] "
labels: bug, needs-triage
assignees: ''
---

## 🐛 Bug Description
A clear description of the issue. Which component(s) affected?

## 🔄 Steps to Reproduce
```bash
# Exact commands to reproduce
cd oreilly-agentic-ai-bootcamp
python -m module --args
```

## 🖥️ Environment
- **OS**: [e.g., Ubuntu 22.04, macOS 14.2]
- **Python**: [e.g., 3.11.4]
- **Version**: [e.g., 1.2.0]
- **Install Method**: [pip / source / docker]
- **GPU**: [e.g., A100 40GB / CPU only]

## 📊 Expected vs Actual Behavior
| Aspect | Expected | Actual |
|--------|----------|--------|
| Exit code | 0 | 1 |
| Output | ... | ... |
| Evidence hash | sha256:... | sha256:... |

## 🔬 Evidence Context
- **Commit SHA**: `git rev-parse HEAD`
- **Evidence Package**: [Zenodo DOI or local path]
- **Frozen Requirements**: `cat requirements.lock`

## 📝 Additional Context
- Error traceback (if any)
- Screenshots (if UI-related)
- Related issues/PRs

## ✅ Checklist
- [ ] Searched existing issues
- [ ] Using latest `main` branch
- [ ] Provided exact reproduction steps
- [ ] Included environment details
