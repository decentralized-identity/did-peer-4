from did_peer_4 import encode
from did_peer_4.input_doc import input_doc_from_keys_and_services, KeySpec
from did_peer_4.valid import validate_input_document

ED25519_MULTIKEY = "z6MkrCD1csqtgdj8sjrsu8jxcbeyP6m7LiK87NzhfWqio5yr"
X25519_MULTIKEY = "z6LSqPZfn9krvgXma2icTMKf2uVcYhKXsudCmPoUzqGYW24U"


def test_input_doc_generation():
    input_doc = input_doc_from_keys_and_services(
        [
            KeySpec(
                multikey=ED25519_MULTIKEY,
                relationships=["authentication"],
            ),
            KeySpec(
                multikey=X25519_MULTIKEY,
                relationships=["keyAgreement"],
            ),
        ],
        [
            {
                "id": "#didcommmessaging-0",
                "type": "DIDCommMessaging",
                "serviceEndpoint": {
                    "uri": "didcomm:transport/queue",
                    "accept": ["didcomm/v2"],
                },
            }
        ],
    )

    assert input_doc == {
        "@context": [
            "https://www.w3.org/ns/did/v1",
            "https://w3id.org/security/multikey/v1",
        ],
        "verificationMethod": [
            {
                "id": "#key-0",
                "type": "Multikey",
                "publicKeyMultibase": ED25519_MULTIKEY,
            },
            {
                "id": "#key-1",
                "type": "Multikey",
                "publicKeyMultibase": X25519_MULTIKEY,
            },
        ],
        "authentication": ["#key-0"],
        "keyAgreement": ["#key-1"],
        "service": [
            {
                "id": "#didcommmessaging-0",
                "type": "DIDCommMessaging",
                "serviceEndpoint": {
                    "uri": "didcomm:transport/queue",
                    "accept": ["didcomm/v2"],
                },
            }
        ],
    }
    assert validate_input_document(input_doc)
    assert encode(input_doc)
