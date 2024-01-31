"""Helpers for creating input documents for the DID method."""

import warnings
from dataclasses import dataclass, field
from typing import Any, Dict, Literal, Optional, Protocol, Sequence

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
    """DEPRECATED: Key specification.

    Use Multikey or JsonWebKey2020 instead.
    """

    multikey: str
    relationships: Optional[Sequence[Relationship]] = None
    ident: Optional[str] = None
    type: str = "Multikey"
    context: str = "https://w3id.org/security/multikey/v1"


@dataclass
class Multikey:
    """Multikey specification."""

    type: str = field(init=False, default="Multikey")
    context: str = field(init=False, default="https://w3id.org/security/multikey/v1")

    multikey: str
    relationships: Optional[Sequence[Relationship]] = None
    ident: Optional[str] = None


@dataclass
class JsonWebKey2020:
    """JsonWebKey2020 specification."""

    type: str = field(init=False, default="JsonWebKey2020")
    context: str = field(
        init=False, default="https://w3id.org/security/suites/jws-2020/v1"
    )

    jwk: dict
    relationships: Optional[Sequence[Relationship]] = None
    ident: Optional[str] = None


class KeyProtocol(Protocol):
    """Key protocol for keys that can be used in input documents."""

    type: str
    context: str
    relationships: Optional[Sequence[Relationship]]
    ident: Optional[str]


def input_doc_from_keys_and_services(
    keys: Sequence[KeyProtocol], services: Optional[Sequence[dict]] = None
) -> dict:
    """Create an input document for a set of keys and services."""
    input_doc: Dict[str, Any] = {
        "@context": [
            "https://www.w3.org/ns/did/v1",
        ]
    }
    for index, key in enumerate(keys):
        if isinstance(key, KeySpec):
            warnings.warn(
                "KeySpec is deprecated and will be removed in a future version; "
                "use Multikey or JsonWebKey2020 instead",
                DeprecationWarning,
            )
            prop, material = "publicKeyMultibase", key.multikey
        elif isinstance(key, Multikey):
            prop, material = "publicKeyMultibase", key.multikey
        elif isinstance(key, JsonWebKey2020):
            prop, material = "publicKeyJwk", key.jwk
        else:
            raise TypeError(f"Unknown key type: {key}")

        ident = key.ident or f"#key-{index}"
        vm: Dict[str, Any] = {
            "id": ident,
            "type": key.type,
            prop: material,
        }

        input_doc.setdefault("verificationMethod", []).append(vm)

        if key.context not in input_doc["@context"]:
            input_doc["@context"].append(key.context)

        for relationship in key.relationships or []:
            if relationship not in RELATIONSHIPS:
                raise ValueError(f"Invalid relationship: {relationship}")

            input_doc.setdefault(relationship, []).append(ident)

        if services:
            input_doc["service"] = services

    return input_doc
