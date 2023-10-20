from itertools import product
import json

import pytest

from did_peer_4 import validate_input_document

from . import EXAMPLES


@pytest.mark.parametrize("example", EXAMPLES)
def test_validate_examples(example):
    with open(example) as f:
        example = json.load(f)
    validate_input_document(example)


@pytest.mark.parametrize(
    "invalid",
    [
        0,
        {},
        {"id": "did:peer:4:123456789abcdefghi"},
        {"alsoKnownAs": "not a list"},
        *[
            {k: v}
            for k, v in product(
                [
                    "verificationMethod",
                    "authentication",
                    "assertionMethod",
                    "keyAgreement",
                    "capabilityDelegation",
                    "capabilityInvocation",
                    "service",
                ],
                [
                    "not a list",
                    [{}],
                    [{"id": "did:peer:4:123456789abcdefghi#key-1"}],
                    [{"id": "#key-1"}],
                    [{"id": 0}],
                ],
            )
        ],
    ],
)
def test_invalid(invalid):
    with pytest.raises(ValueError):
        validate_input_document(invalid)
