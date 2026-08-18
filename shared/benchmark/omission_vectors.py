"""
Omission vectors for testing Witnessed Trace Completeness.

Each function removes traces from a bundle while leaving other fields intact.
"""

from typing import Dict, Any


def omit_single_trace(bundle: Dict[str, Any]) -> Dict[str, Any]:
    """Remove the last trace (single omission)."""
    b = dict(bundle)
    b["traces"] = list(b.get("traces", []))[:-1]
    return b


def omit_suffix_traces(bundle: Dict[str, Any]) -> Dict[str, Any]:
    """Remove the last half of traces (suffix truncation)."""
    b = dict(bundle)
    traces = b.get("traces", [])
    b["traces"] = traces[:len(traces) // 2]
    return b


def omit_witness_closings(bundle: Dict[str, Any]) -> Dict[str, Any]:
    """Strip all witness closings (unattested count)."""
    b = dict(bundle)
    b["witness_closings"] = []
    return b


OMISSION_VECTORS = {
    "single_omit": omit_single_trace,
    "suffix_truncate": omit_suffix_traces,
    "strip_closings": omit_witness_closings,
}
