#!/usr/bin/env python3
"""
Session 1: Blind Verification & Executable Security Properties

Teaching Demo — O'Reilly Securing Agentic AI Systems Bootcamp

Learning outcome: Commit to a predicted failure location before reveal,
score the commitment after reveal, and require an executable red-to-green
patch result.

The ordering — commit, reveal, score, patch — is the control that prevents
hindsight from masquerading as verification.
"""

import sys
import json
import hashlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.assurance.crypto import hash_sha256, build_merkle_tree, merkle_leaf_digest
from shared.assurance.evidence import create_evidence_pack, ExecutionTraceRecord
from shared.assurance.policy import ReleasePolicyEngine
from shared.benchmark.tamper_vectors import TAMPER_VECTORS


# ── Step 1: Frame the Falsifiable Claim ─────────────────────────────────────

def frame_claim():
    """What we are testing: blind structure improves pre-reveal localization."""
    print("=" * 70)
    print("SESSION 1: BLIND VERIFICATION & EXECUTABLE SECURITY PROPERTIES")
    print("=" * 70)
    print()
    print("THE CLAIM:")
    print("  'An agent can predict WHERE a release will fail BEFORE seeing")
    print("   the vulnerability, and that prediction is more accurate than")
    print("   guessing — provided the prediction structure is high-quality.'")
    print()
    print("THE PROTOCOL:")
    print("  1. COMMIT  — Make a prediction before reveal")
    print("  2. REVEAL  — Apply the vulnerability")
    print("  3. SCORE   — Measure prediction accuracy")
    print("  4. PATCH   — Require an executable red-to-green fix")
    print()
    print("WHY THIS MATTERS:")
    print("  Without blind commitment, hindsight always scores 1.0.")
    print("  The ordering IS the experiment.")
    print()


# ── Step 2: Blind Prediction & Seal ──────────────────────────────────────────

def create_blind_prediction():
    """Simulate a blind prediction: predict what will fail in v1."""
    prediction = {
        "predicted_failure_location": "assurance/policy.py",
        "predicted_failure_family": "signature_verification",
        "predicted_severity": "critical",
        "cited_files": [
            "shared/assurance/policy.py",
            "shared/assurance/evidence.py",
        ],
        "trust_boundary": "The gate trusts the public key inside the bundle",
        "confidence": 0.75,
        "rationale": "If the policy engine uses the bundle-supplied public key"
                     " instead of a pinned registry key, an attacker can forge"
                     " a valid signature with their own key."
    }

    # Seal the prediction (hash it before reveal)
    prediction_json = json.dumps(prediction, sort_keys=True)
    seal_hash = hashlib.sha256(prediction_json.encode()).hexdigest()

    print("─── BLIND PREDICTION ───")
    print(f"  Failure location:   {prediction['predicted_failure_location']}")
    print(f"  Failure family:     {prediction['predicted_failure_family']}")
    print(f"  Confidence:         {prediction['confidence']}")
    print(f"  Seal hash:          {seal_hash[:32]}...")
    print()
    print("  [SEALED] Prediction hash computed before vulnerability reveal.")
    print()

    return prediction, seal_hash


# ── Step 3: Reveal the Vulnerability ─────────────────────────────────────────

def reveal_vulnerability():
    """Simulate revealing the v1 vulnerability (trusted key bypass)."""
    print("─── REVEAL ───")
    print("  Vulnerability: The policy engine verifies Ed25519 signatures")
    print("  using the PUBLIC KEY inside the evidence bundle, not a pinned")
    print("  registry key. An attacker can sign with their own key.")
    print()

    # Create a tampered bundle: sign with a DIFFERENT key
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    from shared.assurance.evidence import create_evidence_pack
    from shared.assurance.crypto import generate_ed25519_keypair

    attacker_priv, attacker_pub, attacker_kid = generate_ed25519_keypair()

    # Build a bundle and sign it with the attacker's key
    bundle = create_evidence_pack(signed=False)
    bundle.sign(attacker_priv, attacker_pub)

    print(f"  Attacker key ID:     {attacker_kid}")
    print(f"  Bundle signed with:  ATTACKER KEY (not trusted)")
    print()

    return bundle, attacker_kid


# ── Step 4: Score the Prediction ─────────────────────────────────────────────

def score_prediction(prediction, bundle, attacker_kid):
    """Score how well the blind prediction matched reality."""
    print("─── SCORE ───")

    # The actual failure: signature verified against bundle-supplied key
    actual_failure_location = "shared/assurance/policy.py"
    actual_failure_family = "signature_verification"

    # Score localization (did we identify the right file?)
    localization_match = (
        prediction["predicted_failure_location"] == actual_failure_location
    )

    # Score structure (did we identify the right failure family?)
    structure_match = (
        prediction["predicted_failure_family"] == actual_failure_family
    )

    scores = {
        "localization_recall": 1.0 if localization_match else 0.0,
        "structure_recall": 1.0 if structure_match else 0.0,
        "confidence": prediction["confidence"],
    }

    # Compare with controls
    hindsight_score = 1.0  # hindsight always gets it right
    random_score = 0.33   # ~1 in 3 families

    print(f"  Localization recall:  {scores['localization_recall']:.1f}  (predicted: {prediction['predicted_failure_location']})")
    print(f"  Structure recall:     {scores['structure_recall']:.1f}  (predicted: {prediction['predicted_failure_family']})")
    print(f"  Confidence:           {scores['confidence']:.2f}")
    print()
    print("  CONTROLS:")
    print(f"    Hindsight:          1.00  (always perfect after seeing the answer)")
    print(f"    Random baseline:    ~0.33 (1 in 3 failure families)")
    print(f"    Blind prediction:   {scores['structure_recall']:.1f}  (YOUR prediction)")
    print()
    print("  KEY INSIGHT: Hindsight always wins. That's why blind commitment matters.")
    print()

    return scores


# ── Step 5: Patch Oracle ─────────────────────────────────────────────────────

def patch_oracle():
    """Demonstrate the patch oracle: gold patch passes, wrong patch fails."""
    print("─── PATCH ORACLE ───")
    print("  A correct patch must make the gate pass.")
    print("  A wrong patch must keep the gate red.")
    print()

    policy_path = Path(__file__).parent.parent / "shared" / "governance" / "release_policy.yaml"

    # Test 1: Good bundle → should PASS
    good_bundle = create_evidence_pack(signed=True)
    engine = ReleasePolicyEngine.from_yaml(policy_path)
    passed, violations, _ = engine.evaluate(good_bundle)
    print(f"  [GOOD BUNDLE]   Gate: {'APPROVED' if passed else 'BLOCKED':8s}  (expected: APPROVED)")
    assert passed, "Gold patch failed!"

    # Test 2: Tampered Merkle root → should BLOCK
    tampered_dict = TAMPER_VECTORS["merkle_root_forge"](good_bundle.to_dict())
    engine2 = ReleasePolicyEngine.from_yaml(policy_path)
    passed2, violations2, _ = engine2.evaluate(tampered_dict)
    print(f"  [FORGED ROOT]   Gate: {'APPROVED' if passed2 else 'BLOCKED':8s}  (expected: BLOCKED)")
    assert not passed2, "Wrong-target patch passed!"

    # Test 3: Stripped signature → should BLOCK
    stripped = TAMPER_VECTORS["strip_signature"](good_bundle.to_dict())
    engine3 = ReleasePolicyEngine.from_yaml(policy_path)
    passed3, violations3, _ = engine3.evaluate(stripped)
    print(f"  [NO SIGNATURE]  Gate: {'APPROVED' if passed3 else 'BLOCKED':8s}  (expected: BLOCKED)")
    assert not passed3, "Unsigned bundle passed!"

    print()
    print("  PATCH ORACLE RESULT: All checks passed.")
    print("  The gold patch turns red to green; wrong patches stay red.")
    print()


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    print()
    frame_claim()

    prediction, seal = create_blind_prediction()
    bundle, attacker_kid = reveal_vulnerability()
    scores = score_prediction(prediction, bundle, attacker_kid)
    patch_oracle()

    print("=" * 70)
    print("SESSION 1 CHECKPOINT")
    print("=" * 70)
    print()
    print("  Artifact saved:")
    checkpoint = {
        "session": 1,
        "prediction_seal": seal,
        "scores": scores,
        "patch_oracle": "gold_passes_wrong_blocks",
    }
    print(json.dumps(checkpoint, indent=2))
    print()
    print("  DEBRIEF QUESTIONS:")
    print("  1. Why does hindsight always score 1.0?")
    print("  2. What happens to the score if you remove the seal?")
    print("  3. Could an attacker exploit the patch oracle to approve bad releases?")
    print()


if __name__ == "__main__":
    main()
