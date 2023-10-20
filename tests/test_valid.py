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
        {"verificationMethod": "not a list"},
        {"authentication": "not a list"},
        {"assertionMethod": "not a list"},
        {"keyAgreement": "not a list"},
        {"capabilityDelegation": "not a list"},
        {"capabilityInvocation": "not a list"},
        {"service": "not a list"},
        {"verificationMethod": [{}]},
        {"authentication": [{}]},
        {"assertionMethod": [{}]},
        {"keyAgreement": [{}]},
        {"capabilityDelegation": [{}]},
        {"capabilityInvocation": [{}]},
        {"service": [{}]},
        {"verificationMethod": [{"id": "did:peer:4:123456789abcdefghi#key-1"}]},
        {"authentication": [{"id": "did:peer:4:123456789abcdefghi#key-1"}]},
        {"assertionMethod": [{"id": "did:peer:4:123456789abcdefghi#key-1"}]},
        {"keyAgreement": [{"id": "did:peer:4:123456789abcdefghi#key-1"}]},
        {"capabilityDelegation": [{"id": "did:peer:4:123456789abcdefghi#key-1"}]},
        {"capabilityInvocation": [{"id": "did:peer:4:123456789abcdefghi#key-1"}]},
        {"service": [{"id": "did:peer:4:123456789abcdefghi#key-1"}]},
        {"verificationMethod": [{"id": "#key-1"}]},
        {"authentication": [{"id": "#key-1"}]},
        {"assertionMethod": [{"id": "#key-1"}]},
        {"keyAgreement": [{"id": "#key-1"}]},
        {"capabilityDelegation": [{"id": "#key-1"}]},
        {"capabilityInvocation": [{"id": "#key-1"}]},
        {"service": [{"id": "#key-1"}]},
        {"verificationMethod": [{"id": 0}]},
        {"authentication": [{"id": 0}]},
        {"assertionMethod": [{"id": 0}]},
        {"keyAgreement": [{"id": 0}]},
        {"capabilityDelegation": [{"id": 0}]},
        {"capabilityInvocation": [{"id": 0}]},
        {"service": [{"id": 0}]},
    ],
)
def test_invalid(invalid):
    with pytest.raises(ValueError):
        validate_input_document(invalid)
