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

print(verdict["verdict"])     # "ITERATE"
print(verdict["score"])       # 60
print(verdict["disclaimer"])  # Render verbatim per EVP/1 §5.
```

The free tier requires no API key.

## Async

```python
from etymolt import AsyncEtymolt

async with AsyncEtymolt() as etymolt:
    verdict = await etymolt.verify("Stratagem")
```

## Documentation

Full docs at [etymolt.com/docs](https://etymolt.com/docs). Protocol spec at [github.com/etymolt/evp-spec](https://github.com/etymolt/evp-spec).

## License

[Apache-2.0](./LICENSE)
