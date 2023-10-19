import json
import re
from typing import Any, Dict, Optional
from base58 import b58decode, b58encode
from hashlib import sha256

from .doc_visitor import DocVisitor

# Regex patterns
BASE58_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
LONG_PATTERN = re.compile(
    r"^did:peer:4zQm[" + BASE58_ALPHABET + r"]{44}:z[" + BASE58_ALPHABET + r"]{6,}$"
)
SHORT_PATTERN = re.compile(r"^did:peer:4zQm[" + BASE58_ALPHABET + r"]{44}$")

# Multiformats constants
MULTICODEC_JSON = b"\x80\x04"
MULTICODEC_SHA2_256 = b"\x12\x20"
MULTIBASE_BASE58_BTC = "z"


def _encode_doc(document: Dict[str, Any]) -> str:
    """Encode the document."""
    return (
        MULTIBASE_BASE58_BTC
        + b58encode(
            MULTICODEC_JSON + json.dumps(document, separators=(",", ":")).encode()
        ).decode()
    )


def _decode_doc(encoded_doc: str) -> Dict[str, Any]:
    """Decode the document."""
    encoding = encoded_doc[0]
    encoded = encoded_doc[1:]
    if encoding != MULTIBASE_BASE58_BTC:
        raise ValueError(f"Unsupported encoding: {encoding}")

    decoded_bytes = b58decode(encoded)
    if not decoded_bytes.startswith(MULTICODEC_JSON):
        raise ValueError(f"Unsupported multicodec: {decoded_bytes[:2]}...")

    value = decoded_bytes[2:]
    return json.loads(value)


def _hash_encoded_doc(encoded_doc: str) -> str:
    """Return multihash of encoded doc."""
    return (
        MULTIBASE_BASE58_BTC
        + b58encode(
            MULTICODEC_SHA2_256 + sha256(encoded_doc.encode()).digest()
        ).decode()
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

    return _decode_doc(encoded_doc)


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

    document = Visitor(document).visit()
    return document


def long_to_short(did: str) -> str:
    """Return the short form of a did:peer:4."""
    if not LONG_PATTERN.match(did):
        raise ValueError(f"DID is not a long form did:peer:4: {did}")

    return did[: did.rfind(":")]


def resolve(did: str) -> Dict[str, Any]:
    """Resolve a did:peer:4 into a document.

    did is expected to be long form.
    """

    decoded = decode(did)
    document = decoded_to_resolved(did, decoded)
    document.setdefault("alsoKnownAs", []).append(long_to_short(did))
    document["id"] = did
    return document


def resolve_short(did: str):
    """Resolve the short form document variant of a did:peer:4.

    did is expected to be long form.
    """
    decoded = decode(did)
    short_did = long_to_short(did)
    document = decoded_to_resolved(short_did, decoded)
    document.setdefault("alsoKnownAs", []).append(did)
    document["id"] = short_did
    return document


def resolve_short_from_doc(
    document: Dict[str, Any], did: Optional[str] = None
) -> Dict[str, Any]:
    """Resolve the short form document variant from the decoded document.

    did is expected to be short form.
    If the did is provided, it will be checked against the document.
    """
    long = encode(document)
    if did is not None:
        if did != long_to_short(long):
            raise ValueError("Document does not match DID")

    return resolve_short(long)
