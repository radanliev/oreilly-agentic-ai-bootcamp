#!/usr/bin/env python3
"""
Session 2: Agentic Supply-Chain & AIBOM Drift

Teaching Demo — O'Reilly Securing Agentic AI Systems Bootcamp

Learning outcome: Detect and explain dependency, deployment, AIBOM,
workflow, and permission drift; evaluate triage completeness and governance.
"""

import sys
import json
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.assurance.crypto import hash_sha256


# ── Supply-Chain Drift Scanner (simulated) ──────────────────────────────────

CLEAN_MANIFEST = {
    "dependencies": {
        "torch": "2.1.0",
        "transformers": "4.35.0",
        "cryptography": "42.0.0",
    },
    "permissions": {
        "network": "outbound-only",
        "filesystem": "read-only",
        "secrets": "none",
    },
    "aibom": {
        "model_name": "agent-v1",
        "model_hash": hash_sha256("agent-v1-weights"),
        "prompt_hash": hash_sha256("system-prompt-v1"),
        "last_evaluated": "2026-08-01T00:00:00Z",
    },
}

DRIFTED_MANIFEST = {
    "dependencies": {
        "torch": "2.1.0",
        "transformers": "4.36.2",         # DRIFT: patch bump
        "cryptography": "42.0.0",
        "requests": "2.31.0",             # DRIFT: new dependency
    },
    "permissions": {
        "network": "outbound-only",
        "filesystem": "read-write",       # DRIFT: escalated privilege
        "secrets": "read-only",           # DRIFT: new access
    },
    "aibom": {
        "model_name": "agent-v1",
        "model_hash": hash_sha256("agent-v1-weights"),
        "prompt_hash": hash_sha256("system-prompt-v2"),  # DRIFT: changed prompt
        "last_evaluated": "2026-03-15T00:00:00Z",        # DRIFT: stale evaluation
    },
}


def scan_drift(clean, drifted):
    """Compare two manifests and return atomic findings."""
    findings = []

    # Dependency drift
    for pkg, ver in drifted["dependencies"].items():
        if pkg not in clean["dependencies"]:
            findings.append({
                "id": f"DEP-{pkg}",
                "family": "dependency_drift",
                "severity": "warning",
                "detail": f"New dependency added: {pkg}=={ver}",
            })
        elif clean["dependencies"][pkg] != ver:
            findings.append({
                "id": f"DEP-{pkg}",
                "family": "dependency_drift",
                "severity": "info",
                "detail": f"Version changed: {pkg} {clean['dependencies'][pkg]} -> {ver}",
            })

    # Permission drift
    for perm, val in drifted["permissions"].items():
        if perm not in clean["permissions"]:
            findings.append({
                "id": f"PERM-{perm}",
                "family": "privileged_deployment",
                "severity": "critical",
                "detail": f"New permission granted: {perm}={val}",
            })
        elif clean["permissions"][perm] != val:
            findings.append({
                "id": f"PERM-{perm}",
                "family": "privileged_deployment",
                "severity": "critical",
                "detail": f"Permission escalated: {perm} {clean['permissions'][perm]} -> {val}",
            })

    # AIBOM drift
    for field in ["prompt_hash", "last_evaluated"]:
        if drifted["aibom"][field] != clean["aibom"][field]:
            findings.append({
                "id": f"AIBOM-{field}",
                "family": "aibom_integrity",
                "severity": "warning" if field == "last_evaluated" else "critical",
                "detail": f"AIBOM field changed: {field}",
            })

    return findings


def group_by_family(findings):
    """Map atomic findings to ground-truth families."""
    families = {}
    for f in findings:
        fam = f["family"]
        families.setdefault(fam, []).append(f)
    return families


# ── Exception Governance ─────────────────────────────────────────────────────

def create_exception(finding_id, approver, ttl_hours=24):
    """Create a signed, time-limited exception."""
    now = datetime.now(timezone.utc)
    expires = now.timestamp() + (ttl_hours * 3600)
    exception = {
        "finding_id": finding_id,
        "approver": approver,
        "issued_at": now.isoformat(),
        "expires_at": datetime.fromtimestamp(expires, tz=timezone.utc).isoformat(),
        "reason": "Reviewed and accepted for this release cycle",
        "signature": hash_sha256(f"{finding_id}:{approver}:{expires}"),
    }
    return exception


def validate_exception(exception):
    """Validate an exception record."""
    from datetime import datetime as dt
    now = datetime.now(timezone.utc)
    expires = dt.fromisoformat(exception["expires_at"])
    if expires.tzinfo is None:
        expires = expires.replace(tzinfo=timezone.utc)

    if now > expires:
        return False, "EXCEPTION_EXPIRED"
    if not exception.get("approver"):
        return False, "NO_APPROVER"
    return True, "VALID"


# ── Main Demo ────────────────────────────────────────────────────────────────

def main():
    print("=" * 70)
    print("SESSION 2: AGENTIC SUPPLY-CHAIN & AIBOM DRIFT")
    print("=" * 70)
    print()

    # Step 1: Clean baseline
    print("─── STEP 1: CLEAN BASELINE ───")
    clean_findings = scan_drift(CLEAN_MANIFEST, CLEAN_MANIFEST)
    print(f"  Clean manifest scan: {len(clean_findings)} findings (expected: 0)")
    print(f"  Status: {'PASS' if len(clean_findings) == 0 else 'FAIL'}")
    print()

    # Step 2: Detect drift
    print("─── STEP 2: DRIFT DETECTION ───")
    drifted_findings = scan_drift(CLEAN_MANIFEST, DRIFTED_MANIFEST)
    print(f"  Drifted manifest scan: {len(drifted_findings)} atomic findings")
    for f in drifted_findings:
        print(f"    [{f['severity'].upper():8s}] {f['id']}: {f['detail']}")
    print()

    # Step 3: Reconcile into families
    print("─── STEP 3: RECONCILIATION ───")
    families = group_by_family(drifted_findings)
    for fam, items in families.items():
        print(f"  {fam}: {len(items)} finding(s)")
        for item in items:
            print(f"    - {item['detail']}")
    print(f"  Families found: {len(families)} (expected: 3)")
    print()

    # Step 4: Exception governance
    print("─── STEP 4: EXCEPTION GOVERNANCE ───")
    valid_exc = create_exception("DEP-transformers", "security-lead", ttl_hours=24)
    expired_exc = create_exception("PERM-filesystem", "security-lead", ttl_hours=-1)

    v1, r1 = validate_exception(valid_exc)
    v2, r2 = validate_exception(expired_exc)
    print(f"  Valid exception:    {r1} (should be VALID)")
    print(f"  Expired exception:  {r2} (should be EXCEPTION_EXPIRED)")

    # Tampered exception
    tampered_exc = dict(valid_exc)
    tampered_exc["approver"] = ""
    v3, r3 = validate_exception(tampered_exc)
    print(f"  Tampered exception: {r3} (should be NO_APPROVER)")
    print()

    # Checkpoint
    print("=" * 70)
    print("SESSION 2 CHECKPOINT")
    print("=" * 70)
    print()
    checkpoint = {
        "session": 2,
        "atomic_findings": len(drifted_findings),
        "families": list(families.keys()),
        "family_count": len(families),
        "exception_valid": v1,
        "exception_expired": not v2,
    }
    print(json.dumps(checkpoint, indent=2))
    print()
    print("  DEBRIEF QUESTIONS:")
    print("  1. Why must two assessors work independently?")
    print("  2. What happens if you drop the AIBOM check entirely?")
    print("  3. Can an expired exception be re-used?")


if __name__ == "__main__":
    main()
