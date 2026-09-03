---
name: Reproducibility Issue
about: Report a failure to reproduce published results
title: "[REPRO] "
labels: reproducibility, needs-triage
assignees: ''
---

## 📋 Reproduction Failure Details

### Target Result
- **Component**: [e.g., eval/run_injection_benchmark.py]
- **Claim/Paper Section**: [e.g., "Table 2: ASR 0.0%"]
- **Expected Value**: [e.g., 0.0]
- **Observed Value**: [e.g., 0.02]

### Environment
- **Commit SHA**: 
- **Evidence Package DOI**: 
- **OS/Python/GPU**: 
- **Install Command**: 

### Reproduction Attempt
```bash
# Exact commands run
python scripts/reproduce_offline.sh --verify
```

### Output
```
# Paste full output including errors
```

## 🔍 Investigation
- [ ] Verified evidence package integrity (`sha256sum`)
- [ ] Verified exact dependency versions (`pip freeze`)
- [ ] Tried Docker reproduction (if available)
- [ ] Checked for non-determinism sources (RNG seeds, timestamps)

## 📊 Statistical Considerations
- Sample size in reproduction:
- Confidence interval overlap:
- Multiple comparison correction applied:

## 📝 Additional Context
Any clues, hypotheses, or partial successes.

## ✅ Checklist
- [ ] Using tagged release (not `main`)
- [ ] Evidence package from Zenodo (not local)
- [ ] Exact dependency versions installed
- [ ] Sufficient compute resources allocated
