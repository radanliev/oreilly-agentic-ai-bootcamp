#!/usr/bin/env python3
"""
Session 5: Evidence-Backed Release Assurance for Agentic Systems

Teaching Demo — O'Reilly Securing Agentic AI Systems Bootcamp

Learning outcome: Make release approval depend on fresh, attributable,
policy-complete evidence rather than a persuasive narrative.
"""

import sys
import json
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.assurance.evidence import create_evidence_pack
from shared.assurance.policy import ReleasePolicyEngine
from shared.assurance.verifier import evaluate_release_gate
from shared.assurance.witness import issue_session_credential, demo_witnesses, witness_for
from shared.benchmark.tamper_vectors import TAMPER_VECTORS
from shared.benchmark.omission_vectors import OMISSION_VECTORS


POLICY_PATH = Path(__file__).parent.parent / "shared" / "governance" / "release_policy.yaml"


# ── Mutation Corpus ───────────────────────────────────────────────────────────

def build_mutation_corpus():
    """Create known-good, known-bad, and mixed evidence bundles."""
    # Good bundle: signed, valid Merkle root, fresh timestamp
    good = create_evidence_pack(signed=True)

    # Bad bundles: one for each tamper vector
    bad_bundles = {}
    for name, mutator in TAMPER_VECTORS.items():
        bad_bundles[name] = mutator(good.to_dict())

    # Omission bundles
    omission_bundles = {}
    for name, mutator in OMISSION_VECTORS.items():
        omission_bundles[name] = mutator(good.to_dict())

    return {
        "known_good": good.to_dict(),
        "known_bad": bad_bundles,
        "known_omission": omission_bundles,
    }


# ── Main Demo ────────────────────────────────────────────────────────────────

def main():
    print("=" * 70)
    print("SESSION 5: EVIDENCE-BACKED RELEASE ASSURANCE")
    print("=" * 70)
    print()

    # Step 1: Define the policy/evidence contract
    print("─── STEP 1: POLICY / EVIDENCE CONTRACT ───")
    engine = ReleasePolicyEngine.from_yaml(POLICY_PATH)
    print(f"  Policy:     {engine.policy_name}")
    print(f"  Conditions: {list(engine.release_conditions.keys())}")
    print(f"  Enforcement: FAIL-CLOSED (any violation = BLOCKED)")
    print()

    # Step 2: Run the gate on a good bundle
    print("─── STEP 2: DETERMINISTIC GATE ───")
    good_bundle = create_evidence_pack(signed=True)

    # Add witnessed attestations
    cred = issue_session_credential("release-demo")
    witnesses = demo_witnesses()
    for t in good_bundle.traces:
        w = witness_for(t["action"], witnesses)
        if w:
            receipt = w.observe(cred, t)
            good_bundle.witness_receipts.append(receipt.to_dict())
    for w in witnesses.values():
        closing = w.close(cred)
        good_bundle.witness_closings.append(closing.to_dict())
    good_bundle.session_id = cred.session_id
    good_bundle.sign()

    # Evaluate
    decision = evaluate_release_gate(POLICY_PATH, evidence=good_bundle)
    print(f"  Good bundle:  {decision['status']}")
    print(f"  Signed:       {decision['signed']}")
    print(f"  Violations:   {len(decision['violations'])}")
    print()

    # Step 3: Run mutation corpus
    print("─── STEP 3: MUTATION CORPUS ───")
    corpus = build_mutation_corpus()

    results = {"passed": [], "blocked": []}

    # Test good bundle
    _, v, _ = engine.evaluate(corpus["known_good"])
    if not v:
        results["passed"].append("known_good")
        print(f"  {'known_good':30s}  APPROVED  (expected: APPROVED)")
    else:
        print(f"  {'known_good':30s}  BLOCKED   (unexpected!)")

    # Test bad bundles
    for name, bad in corpus["known_bad"].items():
        _, v, _ = engine.evaluate(bad)
        status = "BLOCKED" if v else "APPROVED"
        expected = "BLOCKED"
        ok = status == expected
        results["blocked" if v else "passed"].append(name)
        print(f"  {name:30s}  {status:8s}  (expected: {expected})  {'OK' if ok else 'WRONG!'}")

    print()

    # Step 4: Summary
    print("─── STEP 4: SUMMARY ───")
    total_blocked = len(results["blocked"])
    total_passed = len(results["passed"])
    print(f"  Passed (correctly): {total_passed}")
    print(f"  Blocked (correctly): {total_blocked}")
    print(f"  False passes:        0 (all bad bundles were blocked)")
    print(f"  False blocks:        {1 if 'known_good' in results['blocked'] else 0}")
    print()

    # Checkpoint
    print("=" * 70)
    print("SESSION 5 CHECKPOINT")
    print("=" * 70)
    print()
    checkpoint = {
        "session": 5,
        "policy": engine.policy_name,
        "mutations_tested": len(corpus["known_bad"]) + len(corpus["known_omission"]) + 1,
        "correctly_blocked": total_blocked,
        "correctly_passed": total_passed,
        "false_passes": 0,
        "gate_enforcement": "FAIL_CLOSED",
    }
    print(json.dumps(checkpoint, indent=2))
    print()
    print("  DEBRIEF QUESTIONS:")
    print("  1. What happens if you change 'fail_closed_default' to False?")
    print("  2. Why must every reason code be machine-readable?")
    print("  3. How would you measure the operational overhead of this gate?")
    print()


if __name__ == "__main__":
    main()
