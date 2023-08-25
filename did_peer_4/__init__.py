import json
import re
from typing import Any, Dict
from multiformats import multibase, multicodec, multihash

from .doc_visitor import DocVisitor

BASE58_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

LONG_PATTERN = re.compile(
    r"^did:peer:4zQm[" + BASE58_ALPHABET + r"]{44}:z[" + BASE58_ALPHABET + r"]{6,}$"
)
SHORT_PATTERN = re.compile(r"^did:peer:4zQm[" + BASE58_ALPHABET + r"]{44}$")


def _encode_doc(document: Dict[str, Any]) -> str:
    """Encode the document."""
    return multibase.encode(
        multicodec.wrap("json", json.dumps(document, separators=(",", ":")).encode()),
        "base58btc",
    )


def _hash_encoded_doc(encoded_doc: str) -> str:
    """Return multihash of encoded doc."""
    return multibase.encode(
        multihash.digest(encoded_doc.encode(), "sha2-256"), "base58btc"
    )


def encode(
    document: Dict[str, Any],
) -> str:
    """Encode an input document into a did:peer:4."""
    encoded_doc = _encode_doc(document)
    hashed = _hash_encoded_doc(encoded_doc)
    return f"did:peer:4{hashed}:{encoded_doc}"


def encode_short(
    document: Dict[str, Any],
) -> str:
    """Encode an input document into a short form did:peer:4."""
    encoded_doc = _encode_doc(document)
    hashed = _hash_encoded_doc(encoded_doc)
    return f"did:peer:4{hashed}"


def decode(did: str) -> Dict[str, Any]:
    """Decode a did:peer:4 into a document."""
    if not did.startswith("did:peer:4"):
        raise ValueError(f"Invalid did:peer:4: {did}")

    if SHORT_PATTERN.match(did):
        raise ValueError("Cannot decode document from short form did:peer:4")

    if not LONG_PATTERN.match(did):
        raise ValueError(f"Invalid did:peer:4: {did}")

    hashed, encoded_doc = did[10:].split(":")
    if _hash_encoded_doc(encoded_doc) != hashed:
        raise ValueError(f"Hash is invalid for did: {did}")

    decoded_bytes = multibase.decode(encoded_doc)
    _, decoded = multicodec.unwrap(decoded_bytes)

    return json.loads(decoded)


def decoded_to_resolved(did: str, document: dict) -> dict:
    """Add DID and controller to verification methods and relationships."""

    class Visitor(DocVisitor):
        def visit_verification_method(self, value: dict):
            if "controller" not in value:
                value["controller"] = did
            return value

        def visit_verification_relationship_embedded(self, value: dict):
            if "controller" not in value:
                value["controller"] = did
            return value

        def visit_value_with_id(self, value: dict):
            if value["id"].startswith("#"):
                value["id"] = f"{did}{value['id']}"
            return value

        def visit_verification_relationship_ref(self, value: str):
            if value.startswith("#"):
                return f"{did}{value}"

    document = Visitor(document).visit()
    return document


def long_to_short(did: str) -> str:
    """Return the short form of a did:peer:4."""
    return did[: did.rfind(":")]


def resolve(did: str) -> Dict[str, Any]:
    """Resolve a did:peer:4 into a document."""

    decoded = decode(did)
    document = decoded_to_resolved(did, decoded)
    document["alsoKnownAs"] = [long_to_short(did)]
    document["id"] = did
    return document


def resolve_short(did: str):
    """Resolve the short form document variant of a did:peer:4."""
    decoded = decode(did)
    short_did = long_to_short(did)
    document = decoded_to_resolved(short_did, decoded)
    document["alsoKnownAs"] = [did]
    document["id"] = short_did
    return document


if __name__ == "__main__":
    did = encode({"hello": "world"})
    print(did)
    print(LONG_PATTERN.pattern)
    assert LONG_PATTERN.match(did)
