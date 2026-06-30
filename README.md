# etymolt — official Python SDK

> Official Python SDK for [Etymolt](https://etymolt.com) — the fact-check layer for LLM-generated names.

[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](./LICENSE)
[![CI](https://github.com/etymolt/etymolt-python/actions/workflows/ci.yml/badge.svg)](https://github.com/etymolt/etymolt-python/actions/workflows/ci.yml)

## Install

PyPI publication is in flight (Trusted Publisher pending). Until then, install the wheel directly from the [GitHub Release](https://github.com/etymolt/etymolt-python/releases/tag/v0.2.1):

```bash
pip install https://github.com/etymolt/etymolt-python/releases/download/v0.2.1/etymolt-0.2.1-py3-none-any.whl
```

Once PyPI is live, `pip install etymolt` will be the canonical path.

## Quick start

```python
from etymolt import Etymolt

etymolt = Etymolt()
verdict = etymolt.verify("Stratagem")
print(verdict["verdict"], verdict["signature_key_id"])
# -> PROCEED_STRATEGIC etymolt-1779085662
```

`Inkstack` and `Stratagem` are deterministic example names — they return the same verdict and signature_key_id on every call, so the snippet above is reproducible.

The free tier requires no API key. Outputs vary by name; names mutate over time as the underlying records of record change.

## What you can verify

Every call returns a signed [EVP/1 envelope](https://github.com/etymolt/evp-spec). The fields the SDK surfaces:

| Field | What it is |
|---|---|
| `verdict` | One of `PROCEED`, `PROCEED_STRATEGIC`, `ABANDON` — the 3-value canonical enum. |
| `status` | `complete` or `partial` (engine-uncertain; verdict is best estimate). |
| `reason` | One of `clean`, `famous_mark`, `high_collision`, `no_distinctiveness`, `descriptive`, `insufficient_corpus`. |
| `score` | 0-100 composite. Not a substitute for the verdict. |
| `axes` | Per-axis status: `trademark`, `domain`, `cultural`, `sound_symbolism`, `pronunciation`. |
| `issued_at` / `valid_until` | RFC 3339 timestamps. Drop the result after `valid_until`. |
| `signature` / `signature_b64` | Ed25519 over the canonical payload. |
| `signature_key_id` | Look up in `https://www.etymolt.com/.well-known/verdict-keys.json` to verify. |
| `signature_payload_digest` | Hex sha256 of canonical payload — confirm before invoking Ed25519. |
| `disclaimer` | Render verbatim per [EVP/1 §5](https://github.com/etymolt/evp-spec). |

**Browser-side verification:** paste any verdict (or its `signature_b64` + canonical payload) into [`etymolt.com/verify`](https://www.etymolt.com/verify) to see the signature green-check live, no SDK required.

> Note: the `goods` block (Nice classes + intended markets) lands in EVP/1.1 (Sprint 1, §1.1 class-scoping). The SDK will accept `nice_classes=[9, 42]` in `verify()` once the server emits it — the parameter is already wired through.

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
npx etymolt-mock                          # -> http://localhost:4242
ETYMOLT_BASE_URL=http://localhost:4242 python my_app.py
```

The SDK honors `ETYMOLT_BASE_URL` and the constructor's `base_url` argument. See [etymolt/etymolt-mock](https://github.com/etymolt/etymolt-mock).

## Pricing

Free tier: anon calls rate-limited per IP. Authenticated standard: **$0.25 per verdict**. Volume tiers: $0.15 (1K-5K/mo), $0.10 (5K-20K/mo), $0.05 (20K+/mo). See [`etymolt.com/pricing`](https://www.etymolt.com/pricing).

## Documentation

Full docs at [etymolt.com/docs](https://etymolt.com/docs). Protocol spec at [github.com/etymolt/evp-spec](https://github.com/etymolt/evp-spec).

---

*Naming, attested.*

## License

[Apache-2.0](./LICENSE)
