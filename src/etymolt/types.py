"""Type definitions for EVP/1 verdicts. See spec at github.com/etymolt/evp-spec."""

from typing import TypedDict, Literal, Optional


class AxisStatus(TypedDict):
    status: Literal["CLEAR", "CAUTION", "BLOCKED", "INSUFFICIENT_SIGNAL", "UNKNOWN"]
    score: Optional[float]
    confidence: Optional[float]


class VerdictAxes(TypedDict):
    trademark: AxisStatus
    domain: AxisStatus
    cultural: AxisStatus
    sound_symbolism: AxisStatus
    pronunciation: AxisStatus


class Verdict(TypedDict, total=False):
    evp_version: str
    name: str
    verdict: Literal["PROCEED", "PROCEED_STRATEGIC", "ABANDON"]
    status: Literal["complete", "partial"]
    reason: Optional[str]
    score: Optional[int]
    axes: VerdictAxes
    verdict_id: str
    issued_at: str
    valid_until: Optional[str]
    axis_freshness: Optional[dict]
    disclaimer: str
    signature: str
    signature_key_id: str
    signature_payload_digest: str
    permalink: Optional[str]
