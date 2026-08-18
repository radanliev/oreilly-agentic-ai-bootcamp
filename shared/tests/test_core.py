"""
Core tests for the shared assurance library.

Run with: python3 -m pytest shared/tests/ -v
"""

import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from shared.assurance.crypto import (
    hash_sha256, canonical_json, build_merkle_tree, merkle_leaf_digest,
    generate_merkle_proof, verify_merkle_proof, generate_ed25519_keypair,
    sign_payload_ed25519, verify_signature_ed25519
)
from shared.assurance.evidence import create_evidence_pack, ExecutionTraceRecord
from shared.assurance.policy import ReleasePolicyEngine
from shared.benchmark.tamper_vectors import TAMPER_VECTORS


def test_hash_deterministic():
    assert hash_sha256("hello") == hash_sha256("hello")
    assert hash_sha256("hello") != hash_sha256("world")


def test_canonical_json_sorted():
    c = canonical_json({"b": 2, "a": 1})
    assert c == '{"a":1,"b":2}'


def test_merkle_tree_single_leaf():
    leaf = merkle_leaf_digest("test")
    root, levels = build_merkle_tree([leaf])
    assert root == leaf
    assert len(levels) == 1


def test_merkle_tree_multiple_leaves():
    leaves = [merkle_leaf_digest(f"leaf-{i}") for i in range(4)]
    root, levels = build_merkle_tree(leaves)
    assert len(root) == 64
    assert len(levels) > 1


def test_merkle_proof_verification():
    leaves = [merkle_leaf_digest(f"leaf-{i}") for i in range(8)]
    root, levels = build_merkle_tree(leaves)
    for i in range(8):
        proof = generate_merkle_proof(i, levels)
        assert verify_merkle_proof(leaves[i], proof, root)


def test_ed25519_sign_verify():
    priv, pub, kid = generate_ed25519_keypair()
    payload = {"msg": "test"}
    sig = sign_payload_ed25519(payload, priv)
    assert verify_signature_ed25519(payload, sig, pub)
    assert not verify_signature_ed25519({"msg": "tampered"}, sig, pub)


def test_evidence_pack_creation():
    bundle = create_evidence_pack(signed=True)
    assert bundle.signed is True
    assert bundle.verify() is True
    assert bundle.execution_traces_count == 3
    assert len(bundle.merkle_root) == 64


def test_evidence_pack_unsigned():
    bundle = create_evidence_pack(signed=False)
    assert bundle.signed is False
    assert bundle.verify() is False


def test_tamper_vectors_block_all():
    """All tamper vectors should be detected by the policy engine."""
    import yaml
    policy_path = Path(__file__).parent.parent / "governance" / "release_policy.yaml"
    engine = ReleasePolicyEngine.from_yaml(policy_path)
    good_bundle = create_evidence_pack(signed=True)
    good_dict = good_bundle.to_dict()

    blocked_count = 0
    for name, mutator in TAMPER_VECTORS.items():
        mutated = mutator(good_dict)
        passed, violations, _ = engine.evaluate(mutated)
        assert not passed, f"Tamper vector '{name}' was NOT blocked"
        blocked_count += 1

    assert blocked_count == len(TAMPER_VECTORS), f"Expected {len(TAMPER_VECTORS)} blocked, got {blocked_count}"
