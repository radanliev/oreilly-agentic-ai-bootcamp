# Shared assurance library — extracted from EviAssure for teaching
from .crypto import hash_sha256, canonical_json, build_merkle_tree, merkle_leaf_digest, sign_payload_ed25519, verify_signature_ed25519, generate_ed25519_keypair
from .evidence import EvidenceBundle, ExecutionTraceRecord, create_evidence_pack
from .policy import ReleasePolicyEngine
from .witness import Witness, issue_session_credential, reconcile
from .verifier import evaluate_release_gate
