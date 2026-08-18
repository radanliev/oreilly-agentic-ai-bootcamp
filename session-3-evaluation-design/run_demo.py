#!/usr/bin/env python3
"""
Session 3: Evaluation Design — Structure, Leakage, Saturation & Invariants

Teaching Demo — O'Reilly Securing Agentic AI Systems Bootcamp

Learning outcome: Treat evaluation design as the object of study, and show
when a benchmark can or cannot support the claim made for it.
"""

import sys
import json
import random
import hashlib
from pathlib import Path
from typing import Dict, Any, List

sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.assurance.crypto import hash_sha256


# ── Evaluation Conditions ────────────────────────────────────────────────────

def high_structure_predict(trace, ground_truth):
    """Agent with full structure (source refs, trust boundaries, confidence)."""
    # Simulates a well-structured prediction
    match = trace["action"] == ground_truth["action"]
    return {
        "trace_id": trace["trace_id"],
        "predicted": trace["action"],
        "confidence": 0.9 if match else 0.3,
        "localization": ground_truth["location"] if match else "unknown",
        "match": match,
    }


def low_structure_predict(trace, ground_truth):
    """Agent with minimal structure."""
    match = trace["action"] == ground_truth["action"]
    return {
        "trace_id": trace["trace_id"],
        "predicted": trace["action"],
        "confidence": 0.5,
        "localization": "unknown",
        "match": match,
    }


def random_predict(trace, ground_truth):
    """Random baseline."""
    match = random.random() < 0.33
    return {
        "trace_id": trace["trace_id"],
        "predicted": "random-guess",
        "confidence": 0.33,
        "localization": "unknown",
        "match": match,
    }


def hindsight_predict(trace, ground_truth):
    """Hindsight always gets it right."""
    return {
        "trace_id": trace["trace_id"],
        "predicted": ground_truth["action"],
        "confidence": 1.0,
        "localization": ground_truth["location"],
        "match": True,
    }


# ── Leakage Detection ────────────────────────────────────────────────────────

LEAKAGE_CHANNELS = {
    "filename_hints": {
        "present": True,
        "description": "Ground truth file named 'correct_answer.py' in fixtures",
        "severity": "high",
    },
    "prompt_leakage": {
        "present": False,
        "description": "Answer included in evaluation prompt",
        "severity": "critical",
    },
    "path_disclosure": {
        "present": True,
        "description": "File paths in training data match evaluation paths",
        "severity": "medium",
    },
}


def audit_leakage():
    """Audit for answer-bearing cues in evaluation design."""
    print("─── LEAKAGE AUDIT ───")
    channels_found = 0
    for name, info in LEAKAGE_CHANNELS.items():
        status = "PRESENT" if info["present"] else "absent"
        print(f"  [{info['severity'].upper():8s}] {name}: {status}")
        print(f"           {info['description']}")
        if info["present"]:
            channels_found += 1
    print(f"  Channels with leakage: {channels_found}/{len(LEAKAGE_CHANNELS)}")
    print()
    return channels_found


# ── Ablation Testing ─────────────────────────────────────────────────────────

def run_ablation(traces, ground_truth, condition_fn, ablation_name):
    """Run an ablation: disable one feature and measure impact."""
    results = [condition_fn(t, ground_truth[t["trace_id"]]) for t in traces]
    recall = sum(1 for r in results if r["match"]) / len(results) if results else 0
    return {
        "ablation": ablation_name,
        "recall": recall,
        "n": len(results),
    }


# ── Main Demo ────────────────────────────────────────────────────────────────

def main():
    random.seed(42)

    print("=" * 70)
    print("SESSION 3: EVALUATION DESIGN")
    print("=" * 70)
    print()

    # Step 1: Define claims
    print("─── STEP 1: CLAIM / NON-CLAIM ───")
    claim = "High-structure predictions achieve >0.75 recall on release-gate failures"
    non_claims = [
        "This benchmark measures general agent safety",
        "Results transfer to production deployments",
        "Low recall means the agent is broken",
    ]
    print(f"  CLAIM:     {claim}")
    print(f"  NON-CLAIMS:")
    for nc in non_claims:
        print(f"    - {nc}")
    print()

    # Generate test data
    actions = ["verify_user_token", "evaluate_rbac", "execute_db_query", "deploy_model"]
    traces = [{"trace_id": f"TR-{i:03d}", "action": actions[i % len(actions)]}
              for i in range(20)]
    ground_truth = {
        t["trace_id"]: {"action": t["action"], "location": f"module_{i % 4}.py"}
        for i, t in enumerate(traces)
    }

    # Step 2: Run conditions
    print("─── STEP 2: CONDITION MATRIX ───")
    conditions = {
        "high_structure": high_structure_predict,
        "low_structure": low_structure_predict,
        "random": random_predict,
        "hindsight": hindsight_predict,
    }

    results = {}
    for name, fn in conditions.items():
        preds = [fn(t, ground_truth[t["trace_id"]]) for t in traces]
        recall = sum(1 for p in preds if p["match"]) / len(preds)
        results[name] = {"recall": recall, "n": len(preds)}
        print(f"  {name:20s}  recall={recall:.2f}  n={len(preds)}")
    print()

    # Step 3: Leakage audit
    leakage_count = audit_leakage()

    # Step 4: Ablations
    print("─── STEP 3: ABLATIONS ───")
    ablations = [
        ("baseline", high_structure_predict),
        ("no_source_refs", low_structure_predict),
        ("random_control", random_predict),
    ]
    for name, fn in ablations:
        result = run_ablation(traces, ground_truth, fn, name)
        print(f"  {name:25s}  recall={result['recall']:.2f}")
    print()

    # Step 5: Saturation check
    print("─── STEP 4: SATURATION STRESS ───")
    sizes = [5, 10, 20, 50]
    for n in sizes:
        subset = traces[:n]
        preds = [high_structure_predict(t, ground_truth[t["trace_id"]]) for t in subset]
        recall = sum(1 for p in preds if p["match"]) / len(preds) if preds else 0
        print(f"  N={n:3d}  recall={recall:.2f}  {'SATURATED' if recall >= 0.95 else 'unsaturated'}")
    print()

    # Checkpoint
    print("=" * 70)
    print("SESSION 3 CHECKPOINT")
    print("=" * 70)
    print()
    checkpoint = {
        "session": 3,
        "claim": claim,
        "conditions": results,
        "leakage_channels": leakage_count,
        "ablation_count": len(ablations),
    }
    print(json.dumps(checkpoint, indent=2))
    print()
    print("  DEBRIEF QUESTIONS:")
    print("  1. Name one leakage channel found in the audit.")
    print("  2. Which ablation most changes the conclusion?")
    print("  3. What claim can this benchmark NOT support?")


if __name__ == "__main__":
    main()
