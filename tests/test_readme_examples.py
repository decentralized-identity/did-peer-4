import json
import pytest

from did_peer_4 import encode, long_to_short, resolve, resolve_short

from . import EXAMPLES


def print_example(
    index: int, input_doc: dict, encoded: str, resolved: dict, resolved_short: dict
):
    example = f"""
#### Example {index}

Input Document:

```json
{json.dumps(input_doc, indent=2)}
```

Long Form DID:

```
{encoded}
```

Short Form DID: `{long_to_short(encoded)}`

Resolved Document, Long Form:

```json
{json.dumps(resolved, indent=2)}
```

Resolved Document, Short Form:

```json
{json.dumps(resolved_short, indent=2)}
```

    """
    print(example)


@pytest.mark.parametrize(("index", "example"), enumerate(EXAMPLES, start=1))
def test_examples(index: int, example):
    with open(example) as f:
        example = json.load(f)
    encoded = encode(example)
    resolved = resolve(encoded)
    resolved_short = resolve_short(encoded)
    print_example(index, example, encoded, resolved, resolved_short)
