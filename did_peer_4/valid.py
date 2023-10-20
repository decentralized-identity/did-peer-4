"""Validate input documents."""
from typing import Any, Mapping


def resources(document: Mapping[str, Any]):
    """Yield all resources in a document, skipping references."""
    keys = (
        "verificationMethod",
        "authentication",
        "assertionMethod",
        "keyAgreement",
        "capabilityDelegation",
        "capabilityInvocation",
        "service",
    )
    for key in keys:
        if key in document:
            if not isinstance(document[key], list):
                raise ValueError(f"{key} must be a list")

            for index, resource in enumerate(document[key]):
                if isinstance(resource, dict):
                    yield key, index, resource


def validate_input_document(document: Mapping[str, Any]) -> Mapping[str, Any]:
    """Validate did:peer:4 input document.

    This validation is deliberately superficial. It is intended to catch mistakes
    in the input document that would cause the peer DID to be invalid. It is not
    intended to validate the contents of the document, which is left to the caller
    after resolution.

    The following checks are performed:

    - The document must be a Mapping.
    - The document must not be empty.
    - The document must not contain an id.
    - If present, alsoKnownAs must be a list.
    - verificationMethod, authentication, assertionMethod, keyAgreement,
      capabilityDelegation, capabilityInvocation, and service must be lists, if
      present.
    - All resources (verification methods, embedded verification methods,
      services) must have an id.
    - All resource ids must be strings.
    - All resource ids must be relative.
    - All resources must have a type.
    """
    if not isinstance(document, Mapping):
        raise ValueError("document must be a Mapping")

    if not document:
        raise ValueError("document must not be empty")

    if "id" in document:
        raise ValueError("id must not be present in input document")

    if "alsoKnownAs" in document:
        if not isinstance(document["alsoKnownAs"], list):
            raise ValueError("alsoKnownAs must be a list")

    for key, index, resource in resources(document):
        if "id" not in resource:
            raise ValueError(f"{key}[{index}]: resource must have an id")

        ident = resource["id"]
        if not isinstance(ident, str):
            raise ValueError(f"{key}[{index}]: resource id must be a string")

        if not ident.startswith("#"):
            raise ValueError(f"{key}[{index}]: resource id must be relative")

        if "type" not in resource:
            raise ValueError(f"{key}[{index}]: resource must have a type")

    return document
