import json
from did_peer_4 import decode, encode, resolve, resolve_short


DOC = {
    "@context": [
        "https://www.w3.org/ns/did/v1",
        "https://w3id.org/security/suites/x25519-2020/v1",
        "https://w3id.org/security/suites/ed25519-2020/v1",
    ],
    "verificationMethod": [
        {
            "id": "#6LSqPZfn",
            "type": "X25519KeyAgreementKey2020",
            "publicKeyMultibase": "z6LSqPZfn9krvgXma2icTMKf2uVcYhKXsudCmPoUzqGYW24U",
        },
        {
            "id": "#6MkrCD1c",
            "type": "Ed25519VerificationKey2020",
            "publicKeyMultibase": "z6MkrCD1csqtgdj8sjrsu8jxcbeyP6m7LiK87NzhfWqio5yr",
        },
    ],
    "authentication": ["#6MkrCD1c"],
    "assertionMethod": ["#6MkrCD1c"],
    "keyAgreement": ["#6LSqPZfn"],
    "capabilityInvocation": ["#6MkrCD1c"],
    "capabilityDelegation": ["#6MkrCD1c"],
    "service": [
        {
            "id": "#didcommmessaging-0",
            "type": "DIDCommMessaging",
            "serviceEndpoint": "didcomm://queue",
            "accept": ["didcomm/v2"],
            "routingKeys": [],
        }
    ],
}

def test_encode_decode():
    encoded = encode(DOC)
    decoded = decode(encoded)
    assert decoded == DOC


def test_resolve():
    encoded = encode(DOC)
    print(json.dumps(resolve(encoded), indent=2))


def test_resolve_short():
    encoded = encode(DOC)
    print(json.dumps(resolve_short(encoded), indent=2))
