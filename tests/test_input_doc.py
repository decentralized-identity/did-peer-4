from did_peer_4 import encode
from did_peer_4.input_doc import input_doc_from_keys_and_services, KeySpec
from did_peer_4.valid import validate_input_document

ED25519_MULTIKEY = "z6MkrCD1csqtgdj8sjrsu8jxcbeyP6m7LiK87NzhfWqio5yr"
X25519_MULTIKEY = "z6LSqPZfn9krvgXma2icTMKf2uVcYhKXsudCmPoUzqGYW24U"
ANOTHER_ED25519_MULTIKEY = "z6Mkq4o8kZj1nK5z5Y8K8gY7aV9j8jg6YJzqZ6Dj9j7eY4d2"


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


def test_input_doc_generation_extra_params():
    input_doc = input_doc_from_keys_and_services(
        [
            KeySpec(
                ident="#auth-0",
                multikey=ED25519_MULTIKEY,
                relationships=["authentication"],
            ),
            KeySpec(
                ident="#agree-0",
                multikey=X25519_MULTIKEY,
                relationships=["keyAgreement"],
            ),
            KeySpec(
                multikey=ANOTHER_ED25519_MULTIKEY,
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
                "id": "#auth-0",
                "type": "Multikey",
                "publicKeyMultibase": ED25519_MULTIKEY,
            },
            {
                "id": "#agree-0",
                "type": "Multikey",
                "publicKeyMultibase": X25519_MULTIKEY,
            },
            {
                "id": "#key-2",
                "type": "Multikey",
                "publicKeyMultibase": ANOTHER_ED25519_MULTIKEY,
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
