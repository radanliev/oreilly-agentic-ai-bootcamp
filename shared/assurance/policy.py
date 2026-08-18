"""
Release Policy Engine — fail-closed gate that evaluates evidence bundles.

Simplified for teaching: same logic as EviAssure but with fewer policy conditions.
"""

from datetime import datetime, timezone
from typing import Dict, Any, List, Tuple, Optional
import yaml
from pathlib import Path

from .evidence import EvidenceBundle
from .crypto import build_merkle_tree, merkle_leaf_digest, hash_sha256, canonical_json, verify_signature_ed25519


def execution_trace_leaf_string(trace: Dict[str, Any]) -> str:
    """Canonical leaf string for a trace record."""
    return f"{trace['trace_id']}:{trace['agent_id']}:{trace['action']}:{trace['status']}:{trace['duration_ms']}:{trace['output_hash']}"


class ReleasePolicyEngine:
    """Fail-closed policy engine that evaluates evidence bundles."""

    def __init__(self, policy_data: Dict[str, Any], trusted_keys: Optional[Dict[str, str]] = None):
        self.policy_name = policy_data.get("policy_name", "Release Gate Policy")
        self.release_conditions = policy_data.get("release_conditions", {})
        self.trusted_keys = trusted_keys or {}

    @classmethod
    def from_yaml(cls, yaml_path: Path | str) -> "ReleasePolicyEngine":
        """Load policy + trusted keys from YAML files."""
        yaml_path = Path(yaml_path)
        with open(yaml_path, 'r') as f:
            data = yaml.safe_load(f)
        trusted = {}
        keys_path = yaml_path.parent / "trusted_keys.yaml"
        if keys_path.exists():
            with open(keys_path, 'r') as f:
                raw = (yaml.safe_load(f) or {}).get("trusted_keys", {})
            # Flatten: YAML has {key_id: {public_key: "xxx", ...}}
            # but we need {key_id: "xxx"}
            for kid, info in raw.items():
                if isinstance(info, dict) and info.get("public_key"):
                    trusted[kid] = info["public_key"]
                elif isinstance(info, str):
                    trusted[kid] = info
        return cls(data, trusted_keys=trusted)

    def evaluate(self, evidence: EvidenceBundle | Dict[str, Any]) -> Tuple[bool, List[str], Dict[str, Any]]:
        """Evaluate evidence against policy. Returns (passed, violations, details)."""
        try:
            return self._evaluate(evidence)
        except Exception as exc:
            return False, [f"FAIL_CLOSED: Malformed evidence: {type(exc).__name__}"], {
                "passed": False, "violations_count": 1, "fail_closed_enforced": True,
            }

    def _evaluate(self, evidence: EvidenceBundle | Dict[str, Any]) -> Tuple[bool, List[str], Dict[str, Any]]:
        violations: List[str] = []
        details: Dict[str, Any] = {}
        rc = self.release_conditions

        if isinstance(evidence, dict):
            bundle = evidence
            is_signed = bundle.get("signed", False)
            sig = bundle.get("signature")
            pub_key = bundle.get("public_key")
            key_id = bundle.get("key_id")
            test_pass_pct = bundle.get("test_pass_pct", 0.0)
            unresolved_drift = bundle.get("unresolved_drift", 999)
            timestamp_str = bundle.get("timestamp", "")
            nonce = bundle.get("nonce", "")
            merkle_root = bundle.get("merkle_root", "")
            traces = bundle.get("traces", [])
            evidence_id = bundle.get("evidence_id", "UNKNOWN")
        else:
            is_signed = evidence.signed
            sig = evidence.signature
            pub_key = evidence.public_key
            key_id = evidence.key_id
            test_pass_pct = evidence.test_pass_pct
            unresolved_drift = evidence.unresolved_drift
            timestamp_str = evidence.timestamp
            nonce = evidence.nonce
            merkle_root = evidence.merkle_root
            traces = evidence.traces
            evidence_id = evidence.evidence_id
            bundle = evidence.to_dict()

        # 1. Signature check
        if rc.get("require_signed_evidence", True):
            if not is_signed or not sig:
                violations.append("POLICY_VIOLATION: Unsigned evidence bundle rejected.")
            elif self.trusted_keys:
                if key_id not in self.trusted_keys:
                    violations.append(f"POLICY_VIOLATION: Key '{key_id}' not in trusted registry.")
                else:
                    pinned = self.trusted_keys[key_id]
                    # Build the exact payload the evidence module signed:
                    # only the fields listed in payload_for_signing(), plus
                    # the recomputed witness_digest.
                    items = sorted(canonical_json(r) for r in (bundle.get("witness_receipts") or []))
                    items += sorted(canonical_json(c) for c in (bundle.get("witness_closings") or []))
                    witness_digest = hash_sha256("|".join(items)) if items else hash_sha256("NO_WITNESS")
                    payload = {
                        "evidence_id": bundle.get("evidence_id", ""),
                        "timestamp": bundle.get("timestamp", ""),
                        "nonce": bundle.get("nonce", ""),
                        "agent_system_version": bundle.get("agent_system_version", ""),
                        "test_pass_pct": bundle.get("test_pass_pct", 0.0),
                        "unresolved_drift": bundle.get("unresolved_drift", 0),
                        "execution_traces_count": bundle.get("execution_traces_count", 0),
                        "merkle_root": bundle.get("merkle_root", ""),
                        "artifact_digests": bundle.get("artifact_digests", {}),
                        "session_id": bundle.get("session_id"),
                        "witness_digest": witness_digest,
                    }
                    if not verify_signature_ed25519(payload, sig, pinned):
                        violations.append("POLICY_VIOLATION: Invalid Ed25519 signature.")

        # 2. Merkle root integrity
        if rc.get("verify_merkle_root", True) and traces:
            leaf_hashes = [merkle_leaf_digest(execution_trace_leaf_string(t)) for t in traces]
            recalculated, _ = build_merkle_tree(leaf_hashes)
            if recalculated != merkle_root:
                violations.append("POLICY_VIOLATION: Merkle root mismatch — traces may have been tampered.")

        # 3. Test pass percentage
        min_pass = rc.get("min_passing_tests_pct", 100.0)
        if test_pass_pct < min_pass:
            violations.append(f"POLICY_VIOLATION: Test pass rate {test_pass_pct}% < {min_pass}%.")

        # 4. Drift findings
        allowed_drift = rc.get("allowed_drift_findings", 0)
        if unresolved_drift > allowed_drift:
            violations.append(f"POLICY_VIOLATION: {unresolved_drift} unresolved drift > {allowed_drift} allowed.")

        # 5. Timestamp freshness
        max_age = rc.get("max_evidence_age_seconds", 3600)
        if timestamp_str:
            try:
                ev_dt = datetime.fromisoformat(timestamp_str)
                if ev_dt.tzinfo is None:
                    ev_dt = ev_dt.replace(tzinfo=timezone.utc)
                age = (datetime.now(timezone.utc) - ev_dt).total_seconds()
                if age > max_age:
                    violations.append(f"POLICY_VIOLATION: Evidence expired ({int(age)}s > {max_age}s).")
            except Exception:
                violations.append("POLICY_VIOLATION: Invalid timestamp format.")

        # 6. Replay nonce
        if not nonce:
            violations.append("POLICY_VIOLATION: No replay nonce present.")

        passed = len(violations) == 0
        details.update({
            "evidence_id": evidence_id,
            "policy_name": self.policy_name,
            "passed": passed,
            "violations_count": len(violations),
            "violations": violations,
            "fail_closed_enforced": True,
        })
        return passed, violations, details
