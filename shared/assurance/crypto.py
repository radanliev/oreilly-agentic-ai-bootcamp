"""
Cryptographic primitives for the bootcamp: SHA-256 hashing, Merkle trees, Ed25519 signing.

Simplified for teaching — same algorithms as the production EviAssure system.
"""

import hmac
import hashlib
import json
import base64
from typing import List, Dict, Any, Tuple

from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization


def hash_sha256(data: str | bytes) -> str:
    """Compute SHA-256 digest."""
    if isinstance(data, str):
        data = data.encode('utf-8')
    return hashlib.sha256(data).hexdigest()


def canonical_json(data: Dict[str, Any]) -> str:
    """Produce deterministic, key-sorted JSON string."""
    return json.dumps(data, sort_keys=True, separators=(',', ':'))


# --- Merkle Tree (RFC 6962 domain separation) ---

LEAF_PREFIX = b"\x00"
NODE_PREFIX = b"\x01"


def merkle_leaf_digest(leaf_content: str | bytes) -> str:
    """SHA-256(0x00 || content) — Merkle leaf digest."""
    if isinstance(leaf_content, str):
        leaf_content = leaf_content.encode("utf-8")
    return hashlib.sha256(LEAF_PREFIX + leaf_content).hexdigest()


def merkle_node_digest(left_hex: str, right_hex: str) -> str:
    """SHA-256(0x01 || left || right) — internal node digest."""
    return hashlib.sha256(
        NODE_PREFIX + bytes.fromhex(left_hex) + bytes.fromhex(right_hex)
    ).hexdigest()


def build_merkle_tree(leaf_digests: List[str]) -> Tuple[str, List[List[str]]]:
    """Build a Merkle tree from leaf digests. Returns (root, levels)."""
    if not leaf_digests:
        return merkle_leaf_digest("EMPTY_TREE"), [[merkle_leaf_digest("EMPTY_TREE")]]

    current_level = list(leaf_digests)
    levels = [current_level]

    while len(current_level) > 1:
        next_level = []
        for i in range(0, len(current_level), 2):
            left = current_level[i]
            right = current_level[i + 1] if i + 1 < len(current_level) else left
            next_level.append(merkle_node_digest(left, right))
        levels.append(next_level)
        current_level = next_level

    return current_level[0], levels


def generate_merkle_proof(index: int, levels: List[List[str]]) -> List[Dict[str, str]]:
    """Generate inclusion proof for leaf at `index`."""
    proof = []
    curr_idx = index
    for level in levels[:-1]:
        is_right = (curr_idx % 2 == 1)
        sibling_idx = curr_idx - 1 if is_right else curr_idx + 1
        sibling_hash = level[sibling_idx] if sibling_idx < len(level) else level[curr_idx]
        proof.append({"position": "left" if is_right else "right", "hash": sibling_hash})
        curr_idx //= 2
    return proof


def verify_merkle_proof(leaf_digest: str, proof: List[Dict[str, str]], expected_root: str) -> bool:
    """Verify a Merkle inclusion proof."""
    current = leaf_digest
    for step in proof:
        sibling = step["hash"]
        if step["position"] == "right":
            current = merkle_node_digest(current, sibling)
        elif step["position"] == "left":
            current = merkle_node_digest(sibling, current)
        else:
            return False
    return hmac.compare_digest(current, expected_root)


# --- Ed25519 Signing ---

def generate_ed25519_keypair() -> Tuple[ed25519.Ed25519PrivateKey, str, str]:
    """Generate Ed25519 keypair. Returns (private_key, public_key_b64, key_id)."""
    priv_key = ed25519.Ed25519PrivateKey.generate()
    pub_bytes = priv_key.public_key().public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )
    pub_b64 = base64.b64encode(pub_bytes).decode('utf-8')
    key_id = f"KEY-{hash_sha256(pub_bytes)[:12]}"
    return priv_key, pub_b64, key_id


def sign_payload_ed25519(payload: Dict[str, Any], private_key: ed25519.Ed25519PrivateKey) -> str:
    """Sign a payload dict with Ed25519."""
    canonical_str = canonical_json(payload)
    sig_bytes = private_key.sign(canonical_str.encode('utf-8'))
    return base64.b64encode(sig_bytes).decode('utf-8')


def verify_signature_ed25519(payload: Dict[str, Any], signature_b64: str, pub_key_b64: str) -> bool:
    """Verify Ed25519 signature."""
    try:
        pub_bytes = base64.b64decode(pub_key_b64.encode('utf-8'))
        pub_key = ed25519.Ed25519PublicKey.from_public_bytes(pub_bytes)
        sig_bytes = base64.b64decode(signature_b64.encode('utf-8'))
        canonical_str = canonical_json(payload)
        pub_key.verify(sig_bytes, canonical_str.encode('utf-8'))
        return True
    except Exception:
        return False


def compute_key_id(pub_key_b64: str) -> str:
    """Compute key ID from base64 public key."""
    pub_bytes = base64.b64decode(pub_key_b64.encode('utf-8'))
    return f"KEY-{hash_sha256(pub_bytes)[:12]}"
