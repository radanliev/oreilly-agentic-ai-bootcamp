"""
Tamper vectors for testing release gate resilience.

Each function mutates an evidence bundle in a specific way.
"""

from typing import Dict, Any


def tamper_merkle_root(bundle: Dict[str, Any]) -> Dict[str, Any]:
    """Replace the Merkle root with a forged value."""
    b = dict(bundle)
    b["merkle_root"] = "a" * 64
    return b


def tamper_signature(bundle: Dict[str, Any]) -> Dict[str, Any]:
    """Corrupt the signature."""
    b = dict(bundle)
    b["signature"] = "TAMPERED_" + (b.get("signature") or "")[9:]
    return b


def tamper_trace_count(bundle: Dict[str, Any]) -> Dict[str, Any]:
    """Lie about the trace count."""
    b = dict(bundle)
    b["execution_traces_count"] = b.get("execution_traces_count", 0) + 1
    return b


def tamper_test_pass_pct(bundle: Dict[str, Any]) -> Dict[str, Any]:
    """Lie about test pass percentage (set below threshold)."""
    b = dict(bundle)
    b["test_pass_pct"] = 99.0
    return b


def tamper_drift(bundle: Dict[str, Any]) -> Dict[str, Any]:
    """Introduce drift findings that should be detected."""
    b = dict(bundle)
    b["unresolved_drift"] = 5
    return b


def tamper_nonce_replay(bundle: Dict[str, Any]) -> Dict[str, Any]:
    """Reuse a nonce (replay attack)."""
    b = dict(bundle)
    b["nonce"] = "replayed-nonce-0000"
    return b


def tamper_timestamp(bundle: Dict[str, Any]) -> Dict[str, Any]:
    """Use a stale timestamp."""
    b = dict(bundle)
    b["timestamp"] = "2020-01-01T00:00:00+00:00"
    return b


def strip_signature(bundle: Dict[str, Any]) -> Dict[str, Any]:
    """Remove the signature entirely."""
    b = dict(bundle)
    b["signed"] = False
    b["signature"] = None
    return b


TAMPER_VECTORS = {
    "merkle_root_forge": tamper_merkle_root,
    "signature_corrupt": tamper_signature,
    "trace_count_lie": tamper_trace_count,
    "test_pass_inflate": tamper_test_pass_pct,
    "drift_hide": tamper_drift,
    "nonce_replay": tamper_nonce_replay,
    "timestamp_stale": tamper_timestamp,
    "strip_signature": strip_signature,
}
