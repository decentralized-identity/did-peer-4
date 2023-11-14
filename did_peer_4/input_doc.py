"""Helpers for creating input documents for the DID method."""
from dataclasses import dataclass
from typing import Any, Dict, Literal, Optional, Sequence

RELATIONSHIPS = (
    "authentication",
    "assertionMethod",
    "keyAgreement",
    "capabilityDelegation",
    "capabilityInvocation",
)

Relationship = Literal[
    "authentication",
    "assertionMethod",
    "keyAgreement",
    "capabilityDelegation",
    "capabilityInvocation",
]


@dataclass
class KeySpec:
    """Key specification."""

    multikey: str
    relationships: Optional[Sequence[Relationship]] = None
    ident: Optional[str] = None
    type: Optional[str] = None


def input_doc_from_keys_and_services(
    keys: Sequence[KeySpec], services: Optional[Sequence[dict]] = None
) -> dict:
    """Create an input document for a set of keys and services."""
    input_doc: Dict[str, Any] = {
        "@context": [
            "https://www.w3.org/ns/did/v1",
            "https://w3id.org/security/multikey/v1",
        ]
    }
    for index, key in enumerate(keys):
        ident = f"#key-{index}"
        input_doc.setdefault("verificationMethod", []).append(
            {
                "id": key.ident or ident,
                "type": key.type or "Multikey",
                "publicKeyMultibase": key.multikey,
            }
        )
        for relationship in key.relationships or []:
            if relationship not in RELATIONSHIPS:
                raise ValueError(f"Invalid relationship: {relationship}")

            input_doc.setdefault(relationship, []).append(ident)

        if services:
            input_doc["service"] = services

    return input_doc
