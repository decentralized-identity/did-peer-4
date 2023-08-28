import json
import pytest
from pathlib import Path

from did_peer_4 import encode, long_to_short, resolve, resolve_short


def examples():
    """Load json from examples directory and return generator over examples."""
    examples_dir = Path(__file__).parent / "examples"
    yield from examples_dir.glob("*.json")


EXAMPLES = list(examples())


@pytest.mark.parametrize("example", EXAMPLES)
def test_examples(example):
    with open(example) as f:
        example = json.load(f)
    encoded = encode(example)
    resolved = resolve(encoded)
    resolved_short = resolve_short(encoded)
    print("Input Document:", json.dumps(example, indent=2, sort_keys=True), sep="\n")
    print("Long Form DID:", encoded)
    print("Short Form DID:", long_to_short(encoded))
    print(
        "Resolved Document, Long Form:",
        json.dumps(resolved, indent=2, sort_keys=True),
        sep="\n",
    )
    print(
        "Resolved Document, Short Form:",
        json.dumps(resolved_short, indent=2, sort_keys=True),
        sep="\n",
    )
