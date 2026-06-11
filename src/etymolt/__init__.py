"""
etymolt — official Python SDK for Etymolt.

The fact-check layer for LLM-generated names. Issues signed EVP/1
verdicts across five canonical axes (trademark, domain, cultural,
sound, pronunciation).

Quick start:

    from etymolt import Etymolt

    etymolt = Etymolt()
    verdict = etymolt.verify("Stratagem")

    print(verdict["verdict"])  # "PROCEED_STRATEGIC"
    print(verdict["score"])    # 60

See https://github.com/etymolt/evp-spec for the protocol.
"""

from .client import Etymolt, EtymoltError, AsyncEtymolt
from .types import Verdict, VerdictAxes, AxisStatus

__version__ = "0.2.0"

__all__ = [
    "Etymolt",
    "AsyncEtymolt",
    "EtymoltError",
    "Verdict",
    "VerdictAxes",
    "AxisStatus",
    "__version__",
]
