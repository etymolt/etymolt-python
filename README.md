# etymolt — official Python SDK

> Official Python SDK for [Etymolt](https://etymolt.com) — the fact-check layer for LLM-generated names.

[![PyPI version](https://img.shields.io/pypi/v/etymolt.svg)](https://pypi.org/project/etymolt/)
[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](./LICENSE)

## Install

```bash
pip install etymolt
```

## Quick start

```python
from etymolt import Etymolt

etymolt = Etymolt()
verdict = etymolt.verify("Stratagem")

# verdict["verdict"]    → "PROCEED" | "PROCEED_STRATEGIC" | "ABANDON"
# verdict["score"]      → int | None (None when status=="partial")
# verdict["status"]     → "complete" | "partial"
# verdict["reason"]     → str (e.g. "hard_blocker", "coexistence_required", "no_workaround")
# verdict["axes"]       → { trademark, domain, cultural, sound_symbolism, pronunciation }
# verdict["disclaimer"] → Render verbatim per EVP/1 §5.

print(verdict["verdict"], verdict["score"])
print(verdict["disclaimer"])
```

The free tier requires no API key. Outputs vary by name — names mutate over time as the underlying records of record change.

## Async

```python
from etymolt import AsyncEtymolt

async with AsyncEtymolt() as etymolt:
    verdict = await etymolt.verify("Stratagem")
```

## Temporal validity

```python
from etymolt import Etymolt

if Etymolt.is_stale(verdict):
    # past valid_until — re-verify before relying on it
    verdict = etymolt.verify(verdict["name"])
```

## Develop offline

```bash
npx etymolt-mock                          # → http://localhost:4242
ETYMOLT_BASE_URL=http://localhost:4242 python my_app.py
```

The SDK honors `ETYMOLT_BASE_URL` and the constructor's `base_url` argument. See [etymolt/etymolt-mock](https://github.com/etymolt/etymolt-mock).

## Documentation

Full docs at [etymolt.com/docs](https://etymolt.com/docs). Protocol spec at [github.com/etymolt/evp-spec](https://github.com/etymolt/evp-spec).

---

*Naming, attested.*

## License

[Apache-2.0](./LICENSE)
