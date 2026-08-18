"""
Evidence Bundle: the signed, Merkle-backed attestation of an agentic execution.

Simplified for teaching — same schema and signing as EviAssure.
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
import uuid
from typing import List, Dict, Any, Optional

from .crypto import (
    hash_sha256, canonical_json, merkle_leaf_digest,
    build_merkle_tree, sign_payload_ed25519, verify_signature_ed25519
)

# Static demo key (DEMO/TEST ONLY — never use in production)
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
DEMO_PRIV_SEED = bytes.fromhex(
    "d842fd18d672140d2cb1f725f5b72e79574461dbae1c80f16a986264fea4407e")
DEMO_PRIV_KEY = Ed25519PrivateKey.from_private_bytes(DEMO_PRIV_SEED)
DEMO_PUB_KEY = DEMO_PRIV_KEY.public_key()
import base64
DEMO_PUB_KEY_B64 = base64.b64encode(DEMO_PUB_KEY.public_bytes_raw()).decode("utf-8")


@dataclass
class ExecutionTraceRecord:
    """A single agent execution trace record."""
    trace_id: str
    agent_id: str
    action: str
    status: str
    duration_ms: float
    output_hash: str

    def to_hash(self) -> str:
        return merkle_leaf_digest(
            f"{self.trace_id}:{self.agent_id}:{self.action}:{self.status}:{self.duration_ms}:{self.output_hash}")


@dataclass
class EvidenceBundle:
    """A signed evidence bundle containing Merkle-rooted execution traces."""
    evidence_id: str
    timestamp: str
    nonce: str
    agent_system_version: str
    test_pass_pct: float
    unresolved_drift: int
    execution_traces_count: int
    merkle_root: str
    traces: List[Dict[str, Any]] = field(default_factory=list)
    artifact_digests: Dict[str, str] = field(default_factory=dict)
    sig_alg: str = "ed25519"
    key_id: Optional[str] = None
    public_key: Optional[str] = None
    session_id: Optional[str] = None
    witness_receipts: List[Dict[str, Any]] = field(default_factory=list)
    witness_closings: List[Dict[str, Any]] = field(default_factory=list)
    signed: bool = False
    signature: Optional[str] = None

    def payload_for_signing(self) -> Dict[str, Any]:
        """Canonical payload that the signature covers."""
        return {
            "evidence_id": self.evidence_id,
            "timestamp": self.timestamp,
            "nonce": self.nonce,
            "agent_system_version": self.agent_system_version,
            "test_pass_pct": self.test_pass_pct,
            "unresolved_drift": self.unresolved_drift,
            "execution_traces_count": self.execution_traces_count,
            "merkle_root": self.merkle_root,
            "artifact_digests": self.artifact_digests,
            "session_id": self.session_id,
            "witness_digest": self.witness_digest(),
        }

    def witness_digest(self) -> str:
        """Commitment to the witness attestation set (order-independent)."""
        items = sorted(canonical_json(r) for r in (self.witness_receipts or []))
        items += sorted(canonical_json(c) for c in (self.witness_closings or []))
        return hash_sha256("|".join(items)) if items else hash_sha256("NO_WITNESS")

    def sign(self, private_key=None, pub_key_b64=None):
        """Sign the bundle with Ed25519."""
        pk = private_key or DEMO_PRIV_KEY
        pub = pub_key_b64 or DEMO_PUB_KEY_B64
        self.sig_alg = "ed25519"
        self.public_key = pub
        self.key_id = f"KEY-{hash_sha256(base64.b64decode(pub.encode('utf-8')))[:12]}"
        payload = self.payload_for_signing()
        self.signature = sign_payload_ed25519(payload, pk)
        self.signed = True

    def verify(self) -> bool:
        """Verify the bundle's signature."""
        if not self.signed or not self.signature or not self.public_key:
            return False
        return verify_signature_ed25519(
            self.payload_for_signing(), self.signature, self.public_key)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def create_evidence_pack(
    traces: Optional[List[ExecutionTraceRecord]] = None,
    test_pass_pct: float = 100.0,
    unresolved_drift: int = 0,
    agent_version: str = "v1.0.0",
    signed: bool = True,
) -> EvidenceBundle:
    """Create a fully signed EvidenceBundle with default demo traces."""
    if traces is None:
        traces = [
            ExecutionTraceRecord(
                trace_id="TR-001", agent_id="agent-auth-guard",
                action="verify_user_token", status="SUCCESS",
                duration_ms=4.2, output_hash=hash_sha256("TOKEN_VALIDATED")),
            ExecutionTraceRecord(
                trace_id="TR-002", agent_id="agent-policy-gate",
                action="evaluate_rbac", status="SUCCESS",
                duration_ms=8.7, output_hash=hash_sha256("RBAC_APPROVED")),
            ExecutionTraceRecord(
                trace_id="TR-003", agent_id="agent-tool-executor",
                action="execute_db_query", status="SUCCESS",
                duration_ms=12.1, output_hash=hash_sha256("QUERY_EXECUTED_READONLY")),
        ]

    trace_dicts = [asdict(t) for t in traces]
    leaf_hashes = [t.to_hash() for t in traces]
    merkle_root, _ = build_merkle_tree(leaf_hashes)

    timestamp = datetime.now(timezone.utc).isoformat()
    nonce = str(uuid.uuid4())
    evidence_id = f"EVD-{hash_sha256(f'{timestamp}:{nonce}')[:8]}"

    artifact_digests = {
        "model_weights": hash_sha256("MODEL_WEIGHTS_V1.0"),
        "agent_prompt_spec": hash_sha256("SYSTEM_PROMPT"),
        "policy_definition": hash_sha256("FAIL_CLOSED_POLICY"),
    }

    bundle = EvidenceBundle(
        evidence_id=evidence_id,
        timestamp=timestamp,
        nonce=nonce,
        agent_system_version=agent_version,
        test_pass_pct=test_pass_pct,
        unresolved_drift=unresolved_drift,
        execution_traces_count=len(traces),
        merkle_root=merkle_root,
        traces=trace_dicts,
        artifact_digests=artifact_digests,
        signed=False,
    )

    if signed:
        bundle.sign()

    return bundle
