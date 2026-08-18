"""
Release Gate Verifier — the fail-closed gate that evaluates evidence.

Simplified for teaching.
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional

from .policy import ReleasePolicyEngine
from .evidence import EvidenceBundle, create_evidence_pack


def evaluate_release_gate(
    policy_path: Path | str,
    evidence: Optional[EvidenceBundle | Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Evaluate a release gate. Returns the decision dict."""
    engine = ReleasePolicyEngine.from_yaml(policy_path)

    if evidence is None:
        evidence = create_evidence_pack(signed=True)

    passed, violations, details = engine.evaluate(evidence)

    ev_id = evidence.evidence_id if isinstance(evidence, EvidenceBundle) else evidence.get("evidence_id", "UNKNOWN")
    signed_status = evidence.signed if isinstance(evidence, EvidenceBundle) else evidence.get("signed", False)

    return {
        "status": "APPROVED" if passed else "BLOCKED",
        "passed": passed,
        "policy_name": engine.policy_name,
        "evidence_id": ev_id,
        "signed": signed_status,
        "violations": violations,
        "enforcement": "FAIL_CLOSED",
    }
