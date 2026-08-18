"""
Witness module — Witnessed Trace Completeness for detecting omission attacks.

Simplified for teaching: same mechanism as EviAssure's WTC.
"""

from __future__ import annotations

import base64
import uuid
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Set, Tuple

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from .crypto import hash_sha256, canonical_json, sign_payload_ed25519, verify_signature_ed25519, compute_key_id


# Static demo keys
def _priv(seed_hex: str) -> Ed25519PrivateKey:
    return Ed25519PrivateKey.from_private_bytes(bytes.fromhex(seed_hex))

def _pub_b64(priv: Ed25519PrivateKey) -> str:
    return base64.b64encode(priv.public_key().public_bytes_raw()).decode()

DEMO_ORCHESTRATOR_PRIV = _priv("5b7c1f6b0d3f4a2e9c8b7a6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d7e6f")
DEMO_ORCHESTRATOR_PUB_B64 = _pub_b64(DEMO_ORCHESTRATOR_PRIV)

DEMO_WITNESS_SEEDS = {
    "auth-gateway":   ("a1f0c3d2e5b4a7968877665544332211ffeeddccbbaa99887766554433221100",
                       {"verify_user_token"}),
    "policy-service": ("b2e1d4c3f6a5b8079988776655443322eeddccbbaa998877665544332211ffee",
                       {"evaluate_rbac"}),
    "db-gateway":     ("c3d2e5f4a7b6c9180099887766554433ddccbbaa99887766554433221100ffee",
                       {"execute_db_query"}),
}


@dataclass
class SessionCredential:
    """Orchestrator's statement binding a session to a release."""
    session_id: str
    release_id: str
    issued_at: str
    signature: Optional[str] = None

    def payload(self) -> Dict[str, Any]:
        return {"session_id": self.session_id, "release_id": self.release_id,
                "issued_at": self.issued_at, "type": "eviassure.session.credential/v1"}

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def issue_session_credential(release_id: str) -> SessionCredential:
    """Open one credentialed session for one release."""
    cred = SessionCredential(
        session_id=f"sess-{uuid.uuid4().hex[:12]}",
        release_id=release_id,
        issued_at=datetime.now(timezone.utc).isoformat())
    cred.signature = sign_payload_ed25519(cred.payload(), DEMO_ORCHESTRATOR_PRIV)
    return cred


def action_digest(trace: Any) -> str:
    """Action identity attested by a witness."""
    if hasattr(trace, "trace_id"):
        t = (trace.trace_id, trace.agent_id, trace.action, trace.output_hash)
    else:
        t = (trace["trace_id"], trace["agent_id"], trace["action"], trace["output_hash"])
    return hash_sha256(":".join(map(str, t)))


@dataclass
class Receipt:
    witness_id: str
    session_id: str
    seq: int
    action_digest: str
    prev: str = "genesis"
    signature: Optional[str] = None

    def payload(self) -> Dict[str, Any]:
        return {"witness_id": self.witness_id, "session_id": self.session_id,
                "seq": self.seq, "action_digest": self.action_digest, "prev": self.prev}

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Closing:
    witness_id: str
    session_id: str
    final_seq: int
    signature: Optional[str] = None

    def payload(self) -> Dict[str, Any]:
        return {"witness_id": self.witness_id, "session_id": self.session_id,
                "final_seq": self.final_seq}

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class Witness:
    """A stateful observer at an externally observable boundary."""

    def __init__(self, witness_id: str, mediates: Optional[Set[str]] = None,
                 private_key: Optional[Ed25519PrivateKey] = None):
        self.witness_id = witness_id
        self.mediates: Set[str] = set(mediates or ())
        self._priv = private_key or Ed25519PrivateKey.generate()
        self.public_key_b64 = _pub_b64(self._priv)
        self._counters: Dict[str, int] = {}
        self._last_digest: Dict[str, str] = {}
        self._closed: Set[str] = set()

    def observe(self, cred: SessionCredential, trace: Any) -> Receipt:
        """Serve one action and return its signed receipt."""
        sid = cred.session_id
        self._counters[sid] = self._counters.get(sid, 0) + 1
        r = Receipt(self.witness_id, sid, self._counters[sid],
                    action_digest(trace), prev=self._last_digest.get(sid, "genesis"))
        r.signature = sign_payload_ed25519(r.payload(), self._priv)
        self._last_digest[sid] = r.digest() if hasattr(r, 'digest') else hash_sha256(canonical_json(r.payload()))
        return r

    def close(self, cred: SessionCredential) -> Closing:
        """End-of-session closing statement."""
        sid = cred.session_id
        self._closed.add(sid)
        c = Closing(self.witness_id, sid, self._counters.get(sid, 0))
        c.signature = sign_payload_ed25519(c.payload(), self._priv)
        return c

    def registry_entry(self) -> Dict[str, Any]:
        return {"public_key": self.public_key_b64,
                "key_id": f"KEY-{hash_sha256(base64.b64decode(self.public_key_b64.encode()))[:12]}",
                "mediates": sorted(self.mediates)}


def demo_witnesses() -> Dict[str, Witness]:
    """The three demo witnesses."""
    return {wid: Witness(wid, mediates=set(acts), private_key=_priv(seed))
            for wid, (seed, acts) in DEMO_WITNESS_SEEDS.items()}


def witness_for(action: str, witnesses: Dict[str, Witness]) -> Optional[Witness]:
    for w in witnesses.values():
        if action in w.mediates:
            return w
    return None


def reconcile(traces: List[Dict[str, Any]], receipts: List[Dict[str, Any]],
              closings: List[Dict[str, Any]], witness_registry: Dict[str, str],
              session_id: str) -> Tuple[bool, List[str], Dict[str, Any]]:
    """Verify witnessed completeness of traces against attestations."""
    violations: List[str] = []

    # Authenticate and scope receipts/closings
    good_receipts = []
    for raw in receipts:
        r = Receipt(**{k: v for k, v in raw.items() if k in Receipt.__dataclass_fields__})
        pk = witness_registry.get(r.witness_id)
        if pk is None:
            violations.append(f"WITNESS: unregistered witness '{r.witness_id}'")
            continue
        if not r.signature or not verify_signature_ed25519(r.payload(), r.signature, pk):
            violations.append(f"WITNESS: invalid receipt from '{r.witness_id}' seq {r.seq}")
            continue
        if r.session_id != session_id:
            violations.append(f"WITNESS: receipt from foreign session '{r.session_id}'")
            continue
        good_receipts.append(r)

    good_closings: Dict[str, Closing] = {}
    for raw in closings:
        c = Closing(**{k: v for k, v in raw.items() if k in Closing.__dataclass_fields__})
        pk = witness_registry.get(c.witness_id)
        if pk is None:
            violations.append(f"WITNESS: closing from unregistered '{c.witness_id}'")
            continue
        if not c.signature or not verify_signature_ed25519(c.payload(), c.signature, pk):
            violations.append(f"WITNESS: invalid closing from '{c.witness_id}'")
            continue
        good_closings[c.witness_id] = c

    # Contiguous sequence check
    per_witness: Dict[str, List[Receipt]] = {}
    for r in good_receipts:
        per_witness.setdefault(r.witness_id, []).append(r)

    for wid, closing in good_closings.items():
        seqs = sorted(r.seq for r in per_witness.get(wid, []))
        expected = list(range(1, closing.final_seq + 1))
        missing = sorted(set(expected) - set(seqs))
        if missing:
            violations.append(f"WITNESS: '{wid}' seq {closing.final_seq} but {missing} missing")

    # Every registered witness must close
    for wid in witness_registry:
        if wid not in good_closings:
            violations.append(f"WITNESS: '{wid}' produced no closing (missing witness)")

    detail = {
        "witnessed": True, "session_id": session_id,
        "receipts_valid": len(good_receipts), "closings_valid": len(good_closings),
    }
    return (len(violations) == 0), violations, detail
