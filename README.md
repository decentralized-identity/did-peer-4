# DID Peer Numalgo 4

[![pypi release](https://img.shields.io/pypi/v/did-peer-4)](https://pypi.org/project/did-peer-4/)

DID Peer Numalgo 4 is a statically resolvable DID Method with a short form and a long form. The short form is the hash over the long form.

## Installation

```sh
$ pip install did-peer-4
```

## Usage

```python
>>> from did_peer_4 import encode
>>> did = encode({"hello": "world"})
>>> print(did)
did:peer:4zQmb7xLdVY9TXx8oov5XgpGUmGELgqiAV2699s43i6Qdm3M:zQSJgiFTYiCHjQ9MktwNThRXM7a
>>> from did_peer_4 import decode
>>> decoded = decode(did)
>>> print(decoded)
{'hello': 'world'}
>>> from did_peer_4 import resolve
>>> document = resolve(did)
>>> print(document)
{'hello': 'world', 'alsoKnownAs': ['did:peer:4zQmb7xLdVY9TXx8oov5XgpGUmGELgqiAV2699s43i6Qdm3M'], 'id': 'did:peer:4zQmb7xLdVY9TXx8oov5XgpGUmGELgqiAV2699s43i6Qdm3M:zQSJgiFTYiCHjQ9MktwNThRXM7a'}
>>> from did_peer_4 import resolve_short
>>> short_document = resolve_short(did)
>>> print(short_document)
{'hello': 'world', 'alsoKnownAs': ['did:peer:4zQmb7xLdVY9TXx8oov5XgpGUmGELgqiAV2699s43i6Qdm3M:zQSJgiFTYiCHjQ9MktwNThRXM7a'], 'id': 'did:peer:4zQmb7xLdVY9TXx8oov5XgpGUmGELgqiAV2699s43i6Qdm3M'}
```

## Tutorial

### Creating a DID

To create a `did:peer:4` DID, you must start with a document which is very similar in structure to DID Documents. This document is referred to as the "Input Document." This document should look almost exactly like the final resolved DID Document you desire but with a few key differences:

- The document MUST NOT include an `id` at the root. For DID Documents, this is populated with the DID itself. Since we are in the process of generating a DID, we do not yet know the value of the DID. When the DID is resolved later, this value will be correctly filled in.
- All identifiers within this document MUST be relative. For example, the `id` of a `verificationMethod` might be `#key-1` instead of something like `did:example:abc123#key-1`.
- All references pointing to resources within this document MUST be relative. For example, a verification method reference in a verification relationship such as `authentication` might be `#key-1` instead of something like `did:example:abc123#key-1`.
- For verification methods, the `controller` MUST be omitted if the controller is the document owner. If it is controlled by a DID other than the owner of the document, it MUST be included.

For this tutorial, consider an Input Document like the following:

```json
{
  "@context": [
    "https://www.w3.org/ns/did/v1",
    "https://w3id.org/security/suites/x25519-2020/v1",
    "https://w3id.org/security/suites/ed25519-2020/v1"
  ],
  "verificationMethod": [
    {
      "id": "#6LSqPZfn",
      "type": "X25519KeyAgreementKey2020",
      "publicKeyMultibase": "z6LSqPZfn9krvgXma2icTMKf2uVcYhKXsudCmPoUzqGYW24U"
    },
    {
      "id": "#6MkrCD1c",
      "type": "Ed25519VerificationKey2020",
      "publicKeyMultibase": "z6MkrCD1csqtgdj8sjrsu8jxcbeyP6m7LiK87NzhfWqio5yr"
    }
  ],
  "authentication": [
    "#6MkrCD1c"
  ],
  "assertionMethod": [
    "#6MkrCD1c"
  ],
  "keyAgreement": [
    "#6LSqPZfn"
  ],
  "capabilityInvocation": [
    "#6MkrCD1c"
  ],
  "capabilityDelegation": [
    "#6MkrCD1c"
  ],
  "service": [
    {
      "id": "#didcommmessaging-0",
      "type": "DIDCommMessaging",
      "serviceEndpoint": {
        "uri": "didcomm://queue",
        "accept": ["didcomm/v2"],
        "routingKeys": [],
      }
    }
  ]
}
```

This is very similar to the "genesis document" used in numalgo 1.

To encode this value into a `did:peer:4`:

1. Encode the document:
    1. JSON stringify the object without whitespace
    2. Encode the string as utf-8 bytes
    3. Prefix the bytes with the multicodec prefix for json ([varint](https://github.com/multiformats/unsigned-varint) `0x0200`)
    4. Multibase encode the bytes as base58btc (base58 encode the value and prefix with a `z`)
    5. Consider this value the `encoded document`
2. Hash the document:
    1. Take SHA2-256 digest of the encoded document (encode the bytes as utf-8)
    2. Prefix these bytes with the [multihash](https://github.com/multiformats/multihash) prefix for SHA2-256 and the hash length (varint `0x12` for prefix, varint `0x20` for 32 bytes in length)
    3. Multibase encode the bytes as base58btc (base58 encode the value and prefix with a `z`)
    4. Consider this value the `hash`
3. Construct the did by concatenating the values as follows:

        did:peer:4{{hash}}:{{encoded document}}

Here is an example long form DID made from the input example above:

```
did:peer:4zQmd8CpeFPci817KDsbSAKWcXAE2mjvCQSasRewvbSF54Bd:z2M1k7h4psgp4CmJcnQn2Ljp7Pz7ktsd7oBhMU3dWY5s4fhFNj17qcRTQ427C7QHNT6cQ7T3XfRh35Q2GhaNFZmWHVFq4vL7F8nm36PA9Y96DvdrUiRUaiCuXnBFrn1o7mxFZAx14JL4t8vUWpuDPwQuddVo1T8myRiVH7wdxuoYbsva5x6idEpCQydJdFjiHGCpNc2UtjzPQ8awSXkctGCnBmgkhrj5gto3D4i3EREXYq4Z8r2cWGBr2UzbSmnxW2BuYddFo9Yfm6mKjtJyLpF74ytqrF5xtf84MnGFg1hMBmh1xVx1JwjZ2BeMJs7mNS8DTZhKC7KH38EgqDtUZzfjhpjmmUfkXg2KFEA3EGbbVm1DPqQXayPYKAsYPS9AyKkcQ3fzWafLPP93UfNhtUPL8JW5pMcSV3P8v6j3vPXqnnGknNyBprD6YGUVtgLiAqDBDUF3LSxFQJCVYYtghMTv8WuSw9h1a1SRFrDQLGHE4UrkgoRvwaGWr64aM87T1eVGkP5Dt4L1AbboeK2ceLArPScrdYGTpi3BpTkLwZCdjdiFSfTy9okL1YNRARqUf2wm8DvkVGUU7u5nQA3ZMaXWJAewk6k1YUxKd7LvofGUK4YEDtoxN5vb6r1Q2godrGqaPkjfL3RoYPpDYymf9XhcgG8Kx3DZaA6cyTs24t45KxYAfeCw4wqUpCH9HbpD78TbEUr9PPAsJgXBvBj2VVsxnr7FKbK4KykGcg1W8M1JPz21Z4Y72LWgGQCmixovrkHktcTX1uNHjAvKBqVD5C7XmVfHgXCHj7djCh3vzLNuVLtEED8J1hhqsB1oCBGiuh3xXr7fZ9wUjJCQ1HYHqxLJKdYKtoCiPmgKM7etVftXkmTFETZmpM19aRyih3bao76LdpQtbw636r7a3qt8v4WfxsXJetSL8c7t24SqQBcAY89FBsbEnFNrQCMK3JEseKHVaU388ctvRD45uQfe5GndFxthj4iSDomk4uRFd1uRbywoP1tRuabHTDX42UxPjz
```

To construct the short form, simply omit the `:{{encoded document}}` from the end.

Here is an example short form DID for the long form above:

```
did:peer:4zQmd8CpeFPci817KDsbSAKWcXAE2mjvCQSasRewvbSF54Bd
```

### Resolving a DID

#### Long form

Resolving a long form `did:peer:4` document is done by decoding the document from the DID and "contextualizing" the document with the DID.

To decode the document:

1. Extract the `encoded document` portion of the DID
2. Verify the hash over the `encoded document` by extracting the `hash` portion of the DID and comparing it against the result of following step 2 ("Hash the document") above to recreate the hash.
3. Perform the inverse of step 1 ("Encode the document") to get the decoded document

To "contextualize" a document:

1. Take the decoded document (which should look identical to the input example above)
2. Add `id` at the root of the document and set it to the DID
3. Add `alsoKnownAs` at the root of the document and set it to a list, if not already present, and append the short form of the DID
4. For each verification method (declared in the `verificationMethod` section or embedded in a verification relationship like `authentication`):
    - If `controller` is not set, set `controller` to the DID

> Note: Implementations may turn relative references in the document into absolute references by prepending the reference with the DID. This is not recommended due to length but this is an implementation detail that should not affect usage of the resolved document. Both relative and absolute references are valid within DID Documents.

Here is an example long form DID Document:

```json
{
  "@context": [
    "https://www.w3.org/ns/did/v1",
    "https://w3id.org/security/suites/x25519-2020/v1",
    "https://w3id.org/security/suites/ed25519-2020/v1"
  ],
  "verificationMethod": [
    {
      "id": "#6LSqPZfn",
      "type": "X25519KeyAgreementKey2020",
      "publicKeyMultibase": "z6LSqPZfn9krvgXma2icTMKf2uVcYhKXsudCmPoUzqGYW24U",
      "controller": "did:peer:4zQmd8CpeFPci817KDsbSAKWcXAE2mjvCQSasRewvbSF54Bd:z2M1k7h4psgp4CmJcnQn2Ljp7Pz7ktsd7oBhMU3dWY5s4fhFNj17qcRTQ427C7QHNT6cQ7T3XfRh35Q2GhaNFZmWHVFq4vL7F8nm36PA9Y96DvdrUiRUaiCuXnBFrn1o7mxFZAx14JL4t8vUWpuDPwQuddVo1T8myRiVH7wdxuoYbsva5x6idEpCQydJdFjiHGCpNc2UtjzPQ8awSXkctGCnBmgkhrj5gto3D4i3EREXYq4Z8r2cWGBr2UzbSmnxW2BuYddFo9Yfm6mKjtJyLpF74ytqrF5xtf84MnGFg1hMBmh1xVx1JwjZ2BeMJs7mNS8DTZhKC7KH38EgqDtUZzfjhpjmmUfkXg2KFEA3EGbbVm1DPqQXayPYKAsYPS9AyKkcQ3fzWafLPP93UfNhtUPL8JW5pMcSV3P8v6j3vPXqnnGknNyBprD6YGUVtgLiAqDBDUF3LSxFQJCVYYtghMTv8WuSw9h1a1SRFrDQLGHE4UrkgoRvwaGWr64aM87T1eVGkP5Dt4L1AbboeK2ceLArPScrdYGTpi3BpTkLwZCdjdiFSfTy9okL1YNRARqUf2wm8DvkVGUU7u5nQA3ZMaXWJAewk6k1YUxKd7LvofGUK4YEDtoxN5vb6r1Q2godrGqaPkjfL3RoYPpDYymf9XhcgG8Kx3DZaA6cyTs24t45KxYAfeCw4wqUpCH9HbpD78TbEUr9PPAsJgXBvBj2VVsxnr7FKbK4KykGcg1W8M1JPz21Z4Y72LWgGQCmixovrkHktcTX1uNHjAvKBqVD5C7XmVfHgXCHj7djCh3vzLNuVLtEED8J1hhqsB1oCBGiuh3xXr7fZ9wUjJCQ1HYHqxLJKdYKtoCiPmgKM7etVftXkmTFETZmpM19aRyih3bao76LdpQtbw636r7a3qt8v4WfxsXJetSL8c7t24SqQBcAY89FBsbEnFNrQCMK3JEseKHVaU388ctvRD45uQfe5GndFxthj4iSDomk4uRFd1uRbywoP1tRuabHTDX42UxPjz"
    },
    {
      "id": "#6MkrCD1c",
      "type": "Ed25519VerificationKey2020",
      "publicKeyMultibase": "z6MkrCD1csqtgdj8sjrsu8jxcbeyP6m7LiK87NzhfWqio5yr",
      "controller": "did:peer:4zQmd8CpeFPci817KDsbSAKWcXAE2mjvCQSasRewvbSF54Bd:z2M1k7h4psgp4CmJcnQn2Ljp7Pz7ktsd7oBhMU3dWY5s4fhFNj17qcRTQ427C7QHNT6cQ7T3XfRh35Q2GhaNFZmWHVFq4vL7F8nm36PA9Y96DvdrUiRUaiCuXnBFrn1o7mxFZAx14JL4t8vUWpuDPwQuddVo1T8myRiVH7wdxuoYbsva5x6idEpCQydJdFjiHGCpNc2UtjzPQ8awSXkctGCnBmgkhrj5gto3D4i3EREXYq4Z8r2cWGBr2UzbSmnxW2BuYddFo9Yfm6mKjtJyLpF74ytqrF5xtf84MnGFg1hMBmh1xVx1JwjZ2BeMJs7mNS8DTZhKC7KH38EgqDtUZzfjhpjmmUfkXg2KFEA3EGbbVm1DPqQXayPYKAsYPS9AyKkcQ3fzWafLPP93UfNhtUPL8JW5pMcSV3P8v6j3vPXqnnGknNyBprD6YGUVtgLiAqDBDUF3LSxFQJCVYYtghMTv8WuSw9h1a1SRFrDQLGHE4UrkgoRvwaGWr64aM87T1eVGkP5Dt4L1AbboeK2ceLArPScrdYGTpi3BpTkLwZCdjdiFSfTy9okL1YNRARqUf2wm8DvkVGUU7u5nQA3ZMaXWJAewk6k1YUxKd7LvofGUK4YEDtoxN5vb6r1Q2godrGqaPkjfL3RoYPpDYymf9XhcgG8Kx3DZaA6cyTs24t45KxYAfeCw4wqUpCH9HbpD78TbEUr9PPAsJgXBvBj2VVsxnr7FKbK4KykGcg1W8M1JPz21Z4Y72LWgGQCmixovrkHktcTX1uNHjAvKBqVD5C7XmVfHgXCHj7djCh3vzLNuVLtEED8J1hhqsB1oCBGiuh3xXr7fZ9wUjJCQ1HYHqxLJKdYKtoCiPmgKM7etVftXkmTFETZmpM19aRyih3bao76LdpQtbw636r7a3qt8v4WfxsXJetSL8c7t24SqQBcAY89FBsbEnFNrQCMK3JEseKHVaU388ctvRD45uQfe5GndFxthj4iSDomk4uRFd1uRbywoP1tRuabHTDX42UxPjz"
    }
  ],
  "service": [
    {
      "id": "#didcommmessaging-0",
      "type": "DIDCommMessaging",
      "serviceEndpoint": {
        "uri": "didcomm:transport/queue",
        "accept": [
          "didcomm/v2"
        ],
        "routingKeys": []
      }
    }
  ],
  "authentication": [
    "#6MkrCD1c"
  ],
  "keyAgreement": [
    "#6LSqPZfn"
  ],
  "assertionMethod": [
    "#6MkrCD1c"
  ],
  "capabilityDelegation": [
    "#6MkrCD1c"
  ],
  "capabilityInvocation": [
    "#6MkrCD1c"
  ],
  "alsoKnownAs": [
    "did:peer:4zQmd8CpeFPci817KDsbSAKWcXAE2mjvCQSasRewvbSF54Bd"
  ],
  "id": "did:peer:4zQmd8CpeFPci817KDsbSAKWcXAE2mjvCQSasRewvbSF54Bd:z2M1k7h4psgp4CmJcnQn2Ljp7Pz7ktsd7oBhMU3dWY5s4fhFNj17qcRTQ427C7QHNT6cQ7T3XfRh35Q2GhaNFZmWHVFq4vL7F8nm36PA9Y96DvdrUiRUaiCuXnBFrn1o7mxFZAx14JL4t8vUWpuDPwQuddVo1T8myRiVH7wdxuoYbsva5x6idEpCQydJdFjiHGCpNc2UtjzPQ8awSXkctGCnBmgkhrj5gto3D4i3EREXYq4Z8r2cWGBr2UzbSmnxW2BuYddFo9Yfm6mKjtJyLpF74ytqrF5xtf84MnGFg1hMBmh1xVx1JwjZ2BeMJs7mNS8DTZhKC7KH38EgqDtUZzfjhpjmmUfkXg2KFEA3EGbbVm1DPqQXayPYKAsYPS9AyKkcQ3fzWafLPP93UfNhtUPL8JW5pMcSV3P8v6j3vPXqnnGknNyBprD6YGUVtgLiAqDBDUF3LSxFQJCVYYtghMTv8WuSw9h1a1SRFrDQLGHE4UrkgoRvwaGWr64aM87T1eVGkP5Dt4L1AbboeK2ceLArPScrdYGTpi3BpTkLwZCdjdiFSfTy9okL1YNRARqUf2wm8DvkVGUU7u5nQA3ZMaXWJAewk6k1YUxKd7LvofGUK4YEDtoxN5vb6r1Q2godrGqaPkjfL3RoYPpDYymf9XhcgG8Kx3DZaA6cyTs24t45KxYAfeCw4wqUpCH9HbpD78TbEUr9PPAsJgXBvBj2VVsxnr7FKbK4KykGcg1W8M1JPz21Z4Y72LWgGQCmixovrkHktcTX1uNHjAvKBqVD5C7XmVfHgXCHj7djCh3vzLNuVLtEED8J1hhqsB1oCBGiuh3xXr7fZ9wUjJCQ1HYHqxLJKdYKtoCiPmgKM7etVftXkmTFETZmpM19aRyih3bao76LdpQtbw636r7a3qt8v4WfxsXJetSL8c7t24SqQBcAY89FBsbEnFNrQCMK3JEseKHVaU388ctvRD45uQfe5GndFxthj4iSDomk4uRFd1uRbywoP1tRuabHTDX42UxPjz"
}
```

#### Short form
To resolve a short form `did:peer:4` DID, you must know the corresponding long form DID. It is not possible to resolve a short form `did:peer:4` without first seeing and storing it's long form counterpart.

To resolve a short form DID, take the decoded document (which will look exactly like the input doc example above) and follow the same rules described in the [long form](#long-form) section to "contextualize" the document but using the short form DID instead of the long form DID.

Here is an example short form DID Document:

```json
{
  "@context": [
    "https://www.w3.org/ns/did/v1",
    "https://w3id.org/security/suites/x25519-2020/v1",
    "https://w3id.org/security/suites/ed25519-2020/v1"
  ],
  "verificationMethod": [
    {
      "id": "#6LSqPZfn",
      "type": "X25519KeyAgreementKey2020",
      "publicKeyMultibase": "z6LSqPZfn9krvgXma2icTMKf2uVcYhKXsudCmPoUzqGYW24U",
      "controller": "did:peer:4zQmd8CpeFPci817KDsbSAKWcXAE2mjvCQSasRewvbSF54Bd"
    },
    {
      "id": "#6MkrCD1c",
      "type": "Ed25519VerificationKey2020",
      "publicKeyMultibase": "z6MkrCD1csqtgdj8sjrsu8jxcbeyP6m7LiK87NzhfWqio5yr",
      "controller": "did:peer:4zQmd8CpeFPci817KDsbSAKWcXAE2mjvCQSasRewvbSF54Bd"
    }
  ],
  "service": [
    {
      "id": "#didcommmessaging-0",
      "type": "DIDCommMessaging",
      "serviceEndpoint": {
        "uri": "didcomm:transport/queue",
        "accept": [
          "didcomm/v2"
        ],
        "routingKeys": []
      }
    }
  ],
  "authentication": [
    "#6MkrCD1c"
  ],
  "keyAgreement": [
    "#6LSqPZfn"
  ],
  "assertionMethod": [
    "#6MkrCD1c"
  ],
  "capabilityDelegation": [
    "#6MkrCD1c"
  ],
  "capabilityInvocation": [
    "#6MkrCD1c"
  ],
  "alsoKnownAs": [
    "did:peer:4zQmd8CpeFPci817KDsbSAKWcXAE2mjvCQSasRewvbSF54Bd:z2M1k7h4psgp4CmJcnQn2Ljp7Pz7ktsd7oBhMU3dWY5s4fhFNj17qcRTQ427C7QHNT6cQ7T3XfRh35Q2GhaNFZmWHVFq4vL7F8nm36PA9Y96DvdrUiRUaiCuXnBFrn1o7mxFZAx14JL4t8vUWpuDPwQuddVo1T8myRiVH7wdxuoYbsva5x6idEpCQydJdFjiHGCpNc2UtjzPQ8awSXkctGCnBmgkhrj5gto3D4i3EREXYq4Z8r2cWGBr2UzbSmnxW2BuYddFo9Yfm6mKjtJyLpF74ytqrF5xtf84MnGFg1hMBmh1xVx1JwjZ2BeMJs7mNS8DTZhKC7KH38EgqDtUZzfjhpjmmUfkXg2KFEA3EGbbVm1DPqQXayPYKAsYPS9AyKkcQ3fzWafLPP93UfNhtUPL8JW5pMcSV3P8v6j3vPXqnnGknNyBprD6YGUVtgLiAqDBDUF3LSxFQJCVYYtghMTv8WuSw9h1a1SRFrDQLGHE4UrkgoRvwaGWr64aM87T1eVGkP5Dt4L1AbboeK2ceLArPScrdYGTpi3BpTkLwZCdjdiFSfTy9okL1YNRARqUf2wm8DvkVGUU7u5nQA3ZMaXWJAewk6k1YUxKd7LvofGUK4YEDtoxN5vb6r1Q2godrGqaPkjfL3RoYPpDYymf9XhcgG8Kx3DZaA6cyTs24t45KxYAfeCw4wqUpCH9HbpD78TbEUr9PPAsJgXBvBj2VVsxnr7FKbK4KykGcg1W8M1JPz21Z4Y72LWgGQCmixovrkHktcTX1uNHjAvKBqVD5C7XmVfHgXCHj7djCh3vzLNuVLtEED8J1hhqsB1oCBGiuh3xXr7fZ9wUjJCQ1HYHqxLJKdYKtoCiPmgKM7etVftXkmTFETZmpM19aRyih3bao76LdpQtbw636r7a3qt8v4WfxsXJetSL8c7t24SqQBcAY89FBsbEnFNrQCMK3JEseKHVaU388ctvRD45uQfe5GndFxthj4iSDomk4uRFd1uRbywoP1tRuabHTDX42UxPjz"
  ],
  "id": "did:peer:4zQmd8CpeFPci817KDsbSAKWcXAE2mjvCQSasRewvbSF54Bd"
}
```

## Size Stats

- Plain (JSON without whitespace): 732 bytes
- Long form DID: 1062 bytes
- Short form DID: 57 bytes


## FAQs

### Why Base58 encode the document?

Inconsistencies between languages for URL Safe Base64 is a nightmare. To avoid that, we chose Base58.

### The long form is really long. Why not do X to make it shorter?

For the sake of simplicity.

We think it is more valuable to have something simple and straightforward to implement than it is to have a short identifier. In practice, the long form will only need to be exchanged once and then the short form will be used thereafter.

If you'd like to see some exploration of a DID method that does try to shorten the identifier but is still statically resolvable, see my pet project: https://github.com/dbluhm/did-static

### What's wrong with `did:peer:2` + `did:peer:3`?

We believe this is a cleaner implementation. Picky parsing rules and lossy encoding in did:peer:2 limited what kind of documents could be expressed. This also made it harder to implement.

did:peer:3 was a solution to the problem of always needing to pass the full DID Doc when using did:peer:2. However, on it's own, did:peer:3 has little value. We believe it makes sense to combine the short form and long form identifiers as outlined here.

### Why use multibase/multihash/multicodec?

This keeps our options open. For instance, we could choose to messagepack the doc in the future (or something) to further shorten the identifier. This wouldn't require drastic changes to implement when we're already using multiformats.

If nothing else, having self-descriptive identifiers doesn't hurt.

## Appendix

### A. Examples

#### Example 1

Input Document:

```json
{
  "@context": "https://w3id.org/did/v1",
  "verificationMethod": [
    {
      "id": "#1",
      "type": "Ed25519VerificationKey2018",
      "publicKeyBase58": "AU2FFjtkVzjFuirgWieqGGqtNrAZWS9LDuB8TDp6EUrG"
    }
  ],
  "authentication": [
    "#1"
  ],
  "service": [
    {
      "id": "#didcomm",
      "type": "did-communication",
      "priority": 0,
      "recipientKeys": [
        "#1"
      ],
      "routingKeys": [
        "did:key:z6Mknq3MqipEt9hJegs6J9V7tiLa6T5H5rX3fFCXksJKTuv7#z6Mknq3MqipEt9hJegs6J9V7tiLa6T5H5rX3fFCXksJKTuv7"
      ],
      "serviceEndpoint": "http://bob:3000"
    }
  ]
}
```

Long Form DID:

```
did:peer:4zQmQ4dEtoGcivpiH6gtWwhWJY2ENVWuZifb62uzR76HGPPw:z7p4QX8zEXt2sMjv1Tqq8Lv8Nx8oGo2uRczBe21vyfMhQzsWDnwGmjriYfUX75WDq622czcdHjWGhh2VTbzKhLXUjY8Ma7g64dKAVcy8SaxN5QVdjwpXgD7htKCgCjah8jHEzyBZFrtdfTHiVXfSUz1BiURQf1Z3NfxW5cWYsvDJVvQzVmdHb8ekzCnvxCqL2UV1v9SBb1DsU66N3PCp9HVpSrqUJQyFU2Ddc8bb6u8SJfBU1nyCkNMgfA1zAyKnSBrzZWyyNzAm9oBV36qjC1Qjfcpq4FBnGr7foh5sLXppBwu2ES8U2nxdGrQzAbN47DKBoKJqPVxNh5tTuBdYjDGt7PcvZQjHQGNXXuhJctM5besZci2saGefCHzoZ87vSsFuKq6oXEsW512eadiNZWjHSdG9J4ToMEMK9WT66vGGLFdZszB3xhdFqEDnAMcpnoFUL5WN243aH6492jPC2Zjdi1BvHC1J8bUuvyihAKXF3WmFz7gJWmh6MrTEWNqb17K6tqbyXjFmfnS2RbAi8xBFj3sSsXkSs6TRTXAZD9DenYaQq4RMa2Kqh6VKGvkXAjVHKcPh9Ncpt6rU9ZYttNHbDJFgahwB8KisVBK8FBpG
```

Short Form DID: `did:peer:4zQmQ4dEtoGcivpiH6gtWwhWJY2ENVWuZifb62uzR76HGPPw`

Resolved Document, Long Form:

```json
{
  "@context": "https://w3id.org/did/v1",
  "verificationMethod": [
    {
      "id": "#1",
      "type": "Ed25519VerificationKey2018",
      "publicKeyBase58": "AU2FFjtkVzjFuirgWieqGGqtNrAZWS9LDuB8TDp6EUrG",
      "controller": "did:peer:4zQmQ4dEtoGcivpiH6gtWwhWJY2ENVWuZifb62uzR76HGPPw:z7p4QX8zEXt2sMjv1Tqq8Lv8Nx8oGo2uRczBe21vyfMhQzsWDnwGmjriYfUX75WDq622czcdHjWGhh2VTbzKhLXUjY8Ma7g64dKAVcy8SaxN5QVdjwpXgD7htKCgCjah8jHEzyBZFrtdfTHiVXfSUz1BiURQf1Z3NfxW5cWYsvDJVvQzVmdHb8ekzCnvxCqL2UV1v9SBb1DsU66N3PCp9HVpSrqUJQyFU2Ddc8bb6u8SJfBU1nyCkNMgfA1zAyKnSBrzZWyyNzAm9oBV36qjC1Qjfcpq4FBnGr7foh5sLXppBwu2ES8U2nxdGrQzAbN47DKBoKJqPVxNh5tTuBdYjDGt7PcvZQjHQGNXXuhJctM5besZci2saGefCHzoZ87vSsFuKq6oXEsW512eadiNZWjHSdG9J4ToMEMK9WT66vGGLFdZszB3xhdFqEDnAMcpnoFUL5WN243aH6492jPC2Zjdi1BvHC1J8bUuvyihAKXF3WmFz7gJWmh6MrTEWNqb17K6tqbyXjFmfnS2RbAi8xBFj3sSsXkSs6TRTXAZD9DenYaQq4RMa2Kqh6VKGvkXAjVHKcPh9Ncpt6rU9ZYttNHbDJFgahwB8KisVBK8FBpG"
    }
  ],
  "service": [
    {
      "id": "#didcomm",
      "type": "did-communication",
      "priority": 0,
      "recipientKeys": [
        "#1"
      ],
      "routingKeys": [
        "did:key:z6Mknq3MqipEt9hJegs6J9V7tiLa6T5H5rX3fFCXksJKTuv7#z6Mknq3MqipEt9hJegs6J9V7tiLa6T5H5rX3fFCXksJKTuv7"
      ],
      "serviceEndpoint": "http://bob:3000"
    }
  ],
  "authentication": [
    "#1"
  ],
  "alsoKnownAs": [
    "did:peer:4zQmQ4dEtoGcivpiH6gtWwhWJY2ENVWuZifb62uzR76HGPPw"
  ],
  "id": "did:peer:4zQmQ4dEtoGcivpiH6gtWwhWJY2ENVWuZifb62uzR76HGPPw:z7p4QX8zEXt2sMjv1Tqq8Lv8Nx8oGo2uRczBe21vyfMhQzsWDnwGmjriYfUX75WDq622czcdHjWGhh2VTbzKhLXUjY8Ma7g64dKAVcy8SaxN5QVdjwpXgD7htKCgCjah8jHEzyBZFrtdfTHiVXfSUz1BiURQf1Z3NfxW5cWYsvDJVvQzVmdHb8ekzCnvxCqL2UV1v9SBb1DsU66N3PCp9HVpSrqUJQyFU2Ddc8bb6u8SJfBU1nyCkNMgfA1zAyKnSBrzZWyyNzAm9oBV36qjC1Qjfcpq4FBnGr7foh5sLXppBwu2ES8U2nxdGrQzAbN47DKBoKJqPVxNh5tTuBdYjDGt7PcvZQjHQGNXXuhJctM5besZci2saGefCHzoZ87vSsFuKq6oXEsW512eadiNZWjHSdG9J4ToMEMK9WT66vGGLFdZszB3xhdFqEDnAMcpnoFUL5WN243aH6492jPC2Zjdi1BvHC1J8bUuvyihAKXF3WmFz7gJWmh6MrTEWNqb17K6tqbyXjFmfnS2RbAi8xBFj3sSsXkSs6TRTXAZD9DenYaQq4RMa2Kqh6VKGvkXAjVHKcPh9Ncpt6rU9ZYttNHbDJFgahwB8KisVBK8FBpG"
}
```

Resolved Document, Short Form:

```json
{
  "@context": "https://w3id.org/did/v1",
  "verificationMethod": [
    {
      "id": "#1",
      "type": "Ed25519VerificationKey2018",
      "publicKeyBase58": "AU2FFjtkVzjFuirgWieqGGqtNrAZWS9LDuB8TDp6EUrG",
      "controller": "did:peer:4zQmQ4dEtoGcivpiH6gtWwhWJY2ENVWuZifb62uzR76HGPPw"
    }
  ],
  "service": [
    {
      "id": "#didcomm",
      "type": "did-communication",
      "priority": 0,
      "recipientKeys": [
        "#1"
      ],
      "routingKeys": [
        "did:key:z6Mknq3MqipEt9hJegs6J9V7tiLa6T5H5rX3fFCXksJKTuv7#z6Mknq3MqipEt9hJegs6J9V7tiLa6T5H5rX3fFCXksJKTuv7"
      ],
      "serviceEndpoint": "http://bob:3000"
    }
  ],
  "authentication": [
    "#1"
  ],
  "alsoKnownAs": [
    "did:peer:4zQmQ4dEtoGcivpiH6gtWwhWJY2ENVWuZifb62uzR76HGPPw:z7p4QX8zEXt2sMjv1Tqq8Lv8Nx8oGo2uRczBe21vyfMhQzsWDnwGmjriYfUX75WDq622czcdHjWGhh2VTbzKhLXUjY8Ma7g64dKAVcy8SaxN5QVdjwpXgD7htKCgCjah8jHEzyBZFrtdfTHiVXfSUz1BiURQf1Z3NfxW5cWYsvDJVvQzVmdHb8ekzCnvxCqL2UV1v9SBb1DsU66N3PCp9HVpSrqUJQyFU2Ddc8bb6u8SJfBU1nyCkNMgfA1zAyKnSBrzZWyyNzAm9oBV36qjC1Qjfcpq4FBnGr7foh5sLXppBwu2ES8U2nxdGrQzAbN47DKBoKJqPVxNh5tTuBdYjDGt7PcvZQjHQGNXXuhJctM5besZci2saGefCHzoZ87vSsFuKq6oXEsW512eadiNZWjHSdG9J4ToMEMK9WT66vGGLFdZszB3xhdFqEDnAMcpnoFUL5WN243aH6492jPC2Zjdi1BvHC1J8bUuvyihAKXF3WmFz7gJWmh6MrTEWNqb17K6tqbyXjFmfnS2RbAi8xBFj3sSsXkSs6TRTXAZD9DenYaQq4RMa2Kqh6VKGvkXAjVHKcPh9Ncpt6rU9ZYttNHbDJFgahwB8KisVBK8FBpG"
  ],
  "id": "did:peer:4zQmQ4dEtoGcivpiH6gtWwhWJY2ENVWuZifb62uzR76HGPPw"
}
```

#### Example 2

Input Document:

```json
{
  "@context": "https://w3id.org/did/v1",
  "verificationMethod": [
    {
      "id": "#1",
      "type": "Ed25519VerificationKey2018",
      "publicKeyBase58": "3dtu2WWtd5ELwRTJEPzmEJUYEp8Qq36N2QA24g9tFXK9"
    }
  ],
  "authentication": [
    "#1"
  ],
  "service": [
    {
      "id": "#didcomm",
      "type": "did-communication",
      "recipientKeys": [
        "#1"
      ],
      "serviceEndpoint": "http://172.17.0.1:9031/a2a/5b6dyY6PndLaCnWxZbeEYW/5b6dyY6PndLaCnWxZbeEYW/2f6aae0c-6b04-40ff-a25e-faecaea39f83"
    }
  ]
}
```

Long Form DID:

```
did:peer:4zQmRMVzDUXhV64pfw3vFaDvyExjzW9oBXCF2n4zYCaHQFAT:zMx3zwMnDECV3GiFs8nmHr38TziMEEkcgFBEDH5PXQ8hxnMrwNfB9wTwskpJMjggeg8NF1jeDSK5772op2zLLdy8TGFCEiYQxpUvvku8qSCZx5Q8V9Li9mDp6WEqGabXLQ9GTinmyQHQyJ6TcfbHaTtJUFjHS962LFPdUwv3aDK673Pci2doTyHVTAsw4m5eToS2dKbtix9f7HNxwvixnbQucWNAWVAF6HTxFYRYmrRPDmeE8n7V1fXFkY7yvR6BWxKiWwHd8Vb1TbBBRStf5niRM2dUAyjJorTstPWSfG2pN5DsRF81NUd7Aif4EhNAQEJCTuAHxQ3rCnNkb9Pf7YTTxbt1t25YgDMioDi4uFhYcnTbHj7D74yNPC2Cfk6WasU69hMxj7Wxro58vtkA6hvDWGtnDyX4PzntBp3fn62R25HW2jadsZMiJpm5ufpYSktEFEHX6gGeF4KPgyU8b2hhyS3FKL4DULYLB6d6CZqUpwrJesGfDtFjfG1btbdmjd6Lm7FCbL3fU9E3AJWEmnFkg16vARiQ1CrzeS9SyNtybKCk4
```

Short Form DID: `did:peer:4zQmRMVzDUXhV64pfw3vFaDvyExjzW9oBXCF2n4zYCaHQFAT`

Resolved Document, Long Form:

```json
{
  "@context": "https://w3id.org/did/v1",
  "verificationMethod": [
    {
      "id": "#1",
      "type": "Ed25519VerificationKey2018",
      "publicKeyBase58": "3dtu2WWtd5ELwRTJEPzmEJUYEp8Qq36N2QA24g9tFXK9",
      "controller": "did:peer:4zQmRMVzDUXhV64pfw3vFaDvyExjzW9oBXCF2n4zYCaHQFAT:zMx3zwMnDECV3GiFs8nmHr38TziMEEkcgFBEDH5PXQ8hxnMrwNfB9wTwskpJMjggeg8NF1jeDSK5772op2zLLdy8TGFCEiYQxpUvvku8qSCZx5Q8V9Li9mDp6WEqGabXLQ9GTinmyQHQyJ6TcfbHaTtJUFjHS962LFPdUwv3aDK673Pci2doTyHVTAsw4m5eToS2dKbtix9f7HNxwvixnbQucWNAWVAF6HTxFYRYmrRPDmeE8n7V1fXFkY7yvR6BWxKiWwHd8Vb1TbBBRStf5niRM2dUAyjJorTstPWSfG2pN5DsRF81NUd7Aif4EhNAQEJCTuAHxQ3rCnNkb9Pf7YTTxbt1t25YgDMioDi4uFhYcnTbHj7D74yNPC2Cfk6WasU69hMxj7Wxro58vtkA6hvDWGtnDyX4PzntBp3fn62R25HW2jadsZMiJpm5ufpYSktEFEHX6gGeF4KPgyU8b2hhyS3FKL4DULYLB6d6CZqUpwrJesGfDtFjfG1btbdmjd6Lm7FCbL3fU9E3AJWEmnFkg16vARiQ1CrzeS9SyNtybKCk4"
    }
  ],
  "service": [
    {
      "id": "#didcomm",
      "type": "did-communication",
      "recipientKeys": [
        "#1"
      ],
      "serviceEndpoint": "http://172.17.0.1:9031/a2a/5b6dyY6PndLaCnWxZbeEYW/5b6dyY6PndLaCnWxZbeEYW/2f6aae0c-6b04-40ff-a25e-faecaea39f83"
    }
  ],
  "authentication": [
    "#1"
  ],
  "alsoKnownAs": [
    "did:peer:4zQmRMVzDUXhV64pfw3vFaDvyExjzW9oBXCF2n4zYCaHQFAT"
  ],
  "id": "did:peer:4zQmRMVzDUXhV64pfw3vFaDvyExjzW9oBXCF2n4zYCaHQFAT:zMx3zwMnDECV3GiFs8nmHr38TziMEEkcgFBEDH5PXQ8hxnMrwNfB9wTwskpJMjggeg8NF1jeDSK5772op2zLLdy8TGFCEiYQxpUvvku8qSCZx5Q8V9Li9mDp6WEqGabXLQ9GTinmyQHQyJ6TcfbHaTtJUFjHS962LFPdUwv3aDK673Pci2doTyHVTAsw4m5eToS2dKbtix9f7HNxwvixnbQucWNAWVAF6HTxFYRYmrRPDmeE8n7V1fXFkY7yvR6BWxKiWwHd8Vb1TbBBRStf5niRM2dUAyjJorTstPWSfG2pN5DsRF81NUd7Aif4EhNAQEJCTuAHxQ3rCnNkb9Pf7YTTxbt1t25YgDMioDi4uFhYcnTbHj7D74yNPC2Cfk6WasU69hMxj7Wxro58vtkA6hvDWGtnDyX4PzntBp3fn62R25HW2jadsZMiJpm5ufpYSktEFEHX6gGeF4KPgyU8b2hhyS3FKL4DULYLB6d6CZqUpwrJesGfDtFjfG1btbdmjd6Lm7FCbL3fU9E3AJWEmnFkg16vARiQ1CrzeS9SyNtybKCk4"
}
```

Resolved Document, Short Form:

```json
{
  "@context": "https://w3id.org/did/v1",
  "verificationMethod": [
    {
      "id": "#1",
      "type": "Ed25519VerificationKey2018",
      "publicKeyBase58": "3dtu2WWtd5ELwRTJEPzmEJUYEp8Qq36N2QA24g9tFXK9",
      "controller": "did:peer:4zQmRMVzDUXhV64pfw3vFaDvyExjzW9oBXCF2n4zYCaHQFAT"
    }
  ],
  "service": [
    {
      "id": "#didcomm",
      "type": "did-communication",
      "recipientKeys": [
        "#1"
      ],
      "serviceEndpoint": "http://172.17.0.1:9031/a2a/5b6dyY6PndLaCnWxZbeEYW/5b6dyY6PndLaCnWxZbeEYW/2f6aae0c-6b04-40ff-a25e-faecaea39f83"
    }
  ],
  "authentication": [
    "#1"
  ],
  "alsoKnownAs": [
    "did:peer:4zQmRMVzDUXhV64pfw3vFaDvyExjzW9oBXCF2n4zYCaHQFAT:zMx3zwMnDECV3GiFs8nmHr38TziMEEkcgFBEDH5PXQ8hxnMrwNfB9wTwskpJMjggeg8NF1jeDSK5772op2zLLdy8TGFCEiYQxpUvvku8qSCZx5Q8V9Li9mDp6WEqGabXLQ9GTinmyQHQyJ6TcfbHaTtJUFjHS962LFPdUwv3aDK673Pci2doTyHVTAsw4m5eToS2dKbtix9f7HNxwvixnbQucWNAWVAF6HTxFYRYmrRPDmeE8n7V1fXFkY7yvR6BWxKiWwHd8Vb1TbBBRStf5niRM2dUAyjJorTstPWSfG2pN5DsRF81NUd7Aif4EhNAQEJCTuAHxQ3rCnNkb9Pf7YTTxbt1t25YgDMioDi4uFhYcnTbHj7D74yNPC2Cfk6WasU69hMxj7Wxro58vtkA6hvDWGtnDyX4PzntBp3fn62R25HW2jadsZMiJpm5ufpYSktEFEHX6gGeF4KPgyU8b2hhyS3FKL4DULYLB6d6CZqUpwrJesGfDtFjfG1btbdmjd6Lm7FCbL3fU9E3AJWEmnFkg16vARiQ1CrzeS9SyNtybKCk4"
  ],
  "id": "did:peer:4zQmRMVzDUXhV64pfw3vFaDvyExjzW9oBXCF2n4zYCaHQFAT"
}
```

#### Example 3

Input Document:

```json
{
  "@context": [
    "https://w3.org/ns/did/v1",
    "https://w3id.org/security/suites/ed25519-2018/v1"
  ],
  "publicKey": [
    {
      "id": "#z6MkrmNwty5ajKtFqc1U48oL2MMLjWjartwc5sf2AihZwXDN",
      "type": "Ed25519VerificationKey2018",
      "publicKeyBase58": "DK7uJiq9PnPnj7AmNZqVBFoLuwTjT1hFPrk6LSjZ2JRz"
    }
  ],
  "authentication": [
    "#z6MkrmNwty5ajKtFqc1U48oL2MMLjWjartwc5sf2AihZwXDN"
  ],
  "assertionMethod": [
    "#z6MkrmNwty5ajKtFqc1U48oL2MMLjWjartwc5sf2AihZwXDN"
  ],
  "capabilityDelegation": [
    "#z6MkrmNwty5ajKtFqc1U48oL2MMLjWjartwc5sf2AihZwXDN"
  ],
  "capabilityInvocation": [
    "#z6MkrmNwty5ajKtFqc1U48oL2MMLjWjartwc5sf2AihZwXDN"
  ],
  "keyAgreement": [
    {
      "id": "#zC8GybikEfyNaausDA4mkT4egP7SNLx2T1d1kujLQbcP6h",
      "type": "X25519KeyAgreementKey2019",
      "publicKeyBase58": "CaSHXEvLKS6SfN9aBfkVGBpp15jSnaHazqHgLHp8KZ3Y"
    }
  ]
}
```

Long Form DID:

```
did:peer:4zQmTtzjstZ5p2Li62vbqPTgHBbdQM7QE5BvcKAme4t3HHPU:z2EH35ZPdC1CKXQ9hyy8oW5Jst9UVnvgwDSLyCzCK2V8zMDsKe2RD8n7GRtE25KJyYcCM4vrahEMfEVpEcAVFZrecQc8suE6SX5fAc581n8DBiifrA94GtsC1gsgLxoNMgbpNzm2Ezys92DvCgDdtT83FZj99jRQnB7fgApfd98GniT7vtyMY27QuVETYgBReAxM3KkruT4pcJXK5Co5F273u4kYzVh6kjZnjZdjJiQbzPQEBq2VwdLft1uZbEfSEbZsvpkR4nQLowGfhSvWUK8gyDHFFPtdUCqV8k2qL7VqK7KweWiEn1DZbSkVV6LV3FBi9hdKEoVu64p4JofiDWy4WgGLtPmEdVVn2C7n2n5Qpfouha4PX3BpBDWiUFXeoWeEthtpBbtdujEXpN5DnqhBNLwgQMFg3ec9cHGai2PCcFtnkLpSjEeGnTnfQAiUEowneupmC39zqRxaHgnd9gSFGPjyJ5yUwsBuWdvbYyv4xMNf5wN32pzgQuHw56hnA6xqpccqhkZxPPmjN4Kf3muRmragcTMgAGvgpUPuLpiUnoqXW6gHqohKs19thSzEAxtCYVahQ3hZPdSYBQKBo5gJVxULyL2DAaWkEzkrrbpVzA2fZ52CJm7JcWcn75Aenf49SdTgXRaYf8dKFN5t1UqsuSWhkoJmiziYMrRYQZkRFizGxs6p8HrfWmqQeq9DhC2mLd6TXQkAxYpaW28RB7xXaGwPRpFpCfeaZAFwSNfzSoT8Kee52Sow5UMANTN9FfNzPJYeQBrBq6GGN6ayLm3KJbqQeZrRcuomYy58pqJ71P1JwymdDVNMe328EMD6UczfJPnTDPH3DeenJwTSdDRuDStJDAn3BWujigjJVAHMnXeMcG63obbFMc4XTsSt9W8bKTs72CpffzB6RsZQyL5UooRBGEj1Y5xHhYjdQAtE6uix2Xg5Dp3NPwUirQ8UsU2Sw95bYr8GZFr6dAHwo8pcmF9WNWihnWMEnbzFnBZqVNAUJ6G
```

Short Form DID: `did:peer:4zQmTtzjstZ5p2Li62vbqPTgHBbdQM7QE5BvcKAme4t3HHPU`

Resolved Document, Long Form:

```json
{
  "@context": [
    "https://w3.org/ns/did/v1",
    "https://w3id.org/security/suites/ed25519-2018/v1"
  ],
  "publicKey": [
    {
      "id": "#z6MkrmNwty5ajKtFqc1U48oL2MMLjWjartwc5sf2AihZwXDN",
      "type": "Ed25519VerificationKey2018",
      "publicKeyBase58": "DK7uJiq9PnPnj7AmNZqVBFoLuwTjT1hFPrk6LSjZ2JRz"
    }
  ],
  "authentication": [
    "#z6MkrmNwty5ajKtFqc1U48oL2MMLjWjartwc5sf2AihZwXDN"
  ],
  "keyAgreement": [
    {
      "id": "#zC8GybikEfyNaausDA4mkT4egP7SNLx2T1d1kujLQbcP6h",
      "type": "X25519KeyAgreementKey2019",
      "publicKeyBase58": "CaSHXEvLKS6SfN9aBfkVGBpp15jSnaHazqHgLHp8KZ3Y",
      "controller": "did:peer:4zQmTtzjstZ5p2Li62vbqPTgHBbdQM7QE5BvcKAme4t3HHPU:z2EH35ZPdC1CKXQ9hyy8oW5Jst9UVnvgwDSLyCzCK2V8zMDsKe2RD8n7GRtE25KJyYcCM4vrahEMfEVpEcAVFZrecQc8suE6SX5fAc581n8DBiifrA94GtsC1gsgLxoNMgbpNzm2Ezys92DvCgDdtT83FZj99jRQnB7fgApfd98GniT7vtyMY27QuVETYgBReAxM3KkruT4pcJXK5Co5F273u4kYzVh6kjZnjZdjJiQbzPQEBq2VwdLft1uZbEfSEbZsvpkR4nQLowGfhSvWUK8gyDHFFPtdUCqV8k2qL7VqK7KweWiEn1DZbSkVV6LV3FBi9hdKEoVu64p4JofiDWy4WgGLtPmEdVVn2C7n2n5Qpfouha4PX3BpBDWiUFXeoWeEthtpBbtdujEXpN5DnqhBNLwgQMFg3ec9cHGai2PCcFtnkLpSjEeGnTnfQAiUEowneupmC39zqRxaHgnd9gSFGPjyJ5yUwsBuWdvbYyv4xMNf5wN32pzgQuHw56hnA6xqpccqhkZxPPmjN4Kf3muRmragcTMgAGvgpUPuLpiUnoqXW6gHqohKs19thSzEAxtCYVahQ3hZPdSYBQKBo5gJVxULyL2DAaWkEzkrrbpVzA2fZ52CJm7JcWcn75Aenf49SdTgXRaYf8dKFN5t1UqsuSWhkoJmiziYMrRYQZkRFizGxs6p8HrfWmqQeq9DhC2mLd6TXQkAxYpaW28RB7xXaGwPRpFpCfeaZAFwSNfzSoT8Kee52Sow5UMANTN9FfNzPJYeQBrBq6GGN6ayLm3KJbqQeZrRcuomYy58pqJ71P1JwymdDVNMe328EMD6UczfJPnTDPH3DeenJwTSdDRuDStJDAn3BWujigjJVAHMnXeMcG63obbFMc4XTsSt9W8bKTs72CpffzB6RsZQyL5UooRBGEj1Y5xHhYjdQAtE6uix2Xg5Dp3NPwUirQ8UsU2Sw95bYr8GZFr6dAHwo8pcmF9WNWihnWMEnbzFnBZqVNAUJ6G"
    }
  ],
  "assertionMethod": [
    "#z6MkrmNwty5ajKtFqc1U48oL2MMLjWjartwc5sf2AihZwXDN"
  ],
  "capabilityDelegation": [
    "#z6MkrmNwty5ajKtFqc1U48oL2MMLjWjartwc5sf2AihZwXDN"
  ],
  "capabilityInvocation": [
    "#z6MkrmNwty5ajKtFqc1U48oL2MMLjWjartwc5sf2AihZwXDN"
  ],
  "alsoKnownAs": [
    "did:peer:4zQmTtzjstZ5p2Li62vbqPTgHBbdQM7QE5BvcKAme4t3HHPU"
  ],
  "id": "did:peer:4zQmTtzjstZ5p2Li62vbqPTgHBbdQM7QE5BvcKAme4t3HHPU:z2EH35ZPdC1CKXQ9hyy8oW5Jst9UVnvgwDSLyCzCK2V8zMDsKe2RD8n7GRtE25KJyYcCM4vrahEMfEVpEcAVFZrecQc8suE6SX5fAc581n8DBiifrA94GtsC1gsgLxoNMgbpNzm2Ezys92DvCgDdtT83FZj99jRQnB7fgApfd98GniT7vtyMY27QuVETYgBReAxM3KkruT4pcJXK5Co5F273u4kYzVh6kjZnjZdjJiQbzPQEBq2VwdLft1uZbEfSEbZsvpkR4nQLowGfhSvWUK8gyDHFFPtdUCqV8k2qL7VqK7KweWiEn1DZbSkVV6LV3FBi9hdKEoVu64p4JofiDWy4WgGLtPmEdVVn2C7n2n5Qpfouha4PX3BpBDWiUFXeoWeEthtpBbtdujEXpN5DnqhBNLwgQMFg3ec9cHGai2PCcFtnkLpSjEeGnTnfQAiUEowneupmC39zqRxaHgnd9gSFGPjyJ5yUwsBuWdvbYyv4xMNf5wN32pzgQuHw56hnA6xqpccqhkZxPPmjN4Kf3muRmragcTMgAGvgpUPuLpiUnoqXW6gHqohKs19thSzEAxtCYVahQ3hZPdSYBQKBo5gJVxULyL2DAaWkEzkrrbpVzA2fZ52CJm7JcWcn75Aenf49SdTgXRaYf8dKFN5t1UqsuSWhkoJmiziYMrRYQZkRFizGxs6p8HrfWmqQeq9DhC2mLd6TXQkAxYpaW28RB7xXaGwPRpFpCfeaZAFwSNfzSoT8Kee52Sow5UMANTN9FfNzPJYeQBrBq6GGN6ayLm3KJbqQeZrRcuomYy58pqJ71P1JwymdDVNMe328EMD6UczfJPnTDPH3DeenJwTSdDRuDStJDAn3BWujigjJVAHMnXeMcG63obbFMc4XTsSt9W8bKTs72CpffzB6RsZQyL5UooRBGEj1Y5xHhYjdQAtE6uix2Xg5Dp3NPwUirQ8UsU2Sw95bYr8GZFr6dAHwo8pcmF9WNWihnWMEnbzFnBZqVNAUJ6G"
}
```

Resolved Document, Short Form:

```json
{
  "@context": [
    "https://w3.org/ns/did/v1",
    "https://w3id.org/security/suites/ed25519-2018/v1"
  ],
  "publicKey": [
    {
      "id": "#z6MkrmNwty5ajKtFqc1U48oL2MMLjWjartwc5sf2AihZwXDN",
      "type": "Ed25519VerificationKey2018",
      "publicKeyBase58": "DK7uJiq9PnPnj7AmNZqVBFoLuwTjT1hFPrk6LSjZ2JRz"
    }
  ],
  "authentication": [
    "#z6MkrmNwty5ajKtFqc1U48oL2MMLjWjartwc5sf2AihZwXDN"
  ],
  "keyAgreement": [
    {
      "id": "#zC8GybikEfyNaausDA4mkT4egP7SNLx2T1d1kujLQbcP6h",
      "type": "X25519KeyAgreementKey2019",
      "publicKeyBase58": "CaSHXEvLKS6SfN9aBfkVGBpp15jSnaHazqHgLHp8KZ3Y",
      "controller": "did:peer:4zQmTtzjstZ5p2Li62vbqPTgHBbdQM7QE5BvcKAme4t3HHPU"
    }
  ],
  "assertionMethod": [
    "#z6MkrmNwty5ajKtFqc1U48oL2MMLjWjartwc5sf2AihZwXDN"
  ],
  "capabilityDelegation": [
    "#z6MkrmNwty5ajKtFqc1U48oL2MMLjWjartwc5sf2AihZwXDN"
  ],
  "capabilityInvocation": [
    "#z6MkrmNwty5ajKtFqc1U48oL2MMLjWjartwc5sf2AihZwXDN"
  ],
  "alsoKnownAs": [
    "did:peer:4zQmTtzjstZ5p2Li62vbqPTgHBbdQM7QE5BvcKAme4t3HHPU:z2EH35ZPdC1CKXQ9hyy8oW5Jst9UVnvgwDSLyCzCK2V8zMDsKe2RD8n7GRtE25KJyYcCM4vrahEMfEVpEcAVFZrecQc8suE6SX5fAc581n8DBiifrA94GtsC1gsgLxoNMgbpNzm2Ezys92DvCgDdtT83FZj99jRQnB7fgApfd98GniT7vtyMY27QuVETYgBReAxM3KkruT4pcJXK5Co5F273u4kYzVh6kjZnjZdjJiQbzPQEBq2VwdLft1uZbEfSEbZsvpkR4nQLowGfhSvWUK8gyDHFFPtdUCqV8k2qL7VqK7KweWiEn1DZbSkVV6LV3FBi9hdKEoVu64p4JofiDWy4WgGLtPmEdVVn2C7n2n5Qpfouha4PX3BpBDWiUFXeoWeEthtpBbtdujEXpN5DnqhBNLwgQMFg3ec9cHGai2PCcFtnkLpSjEeGnTnfQAiUEowneupmC39zqRxaHgnd9gSFGPjyJ5yUwsBuWdvbYyv4xMNf5wN32pzgQuHw56hnA6xqpccqhkZxPPmjN4Kf3muRmragcTMgAGvgpUPuLpiUnoqXW6gHqohKs19thSzEAxtCYVahQ3hZPdSYBQKBo5gJVxULyL2DAaWkEzkrrbpVzA2fZ52CJm7JcWcn75Aenf49SdTgXRaYf8dKFN5t1UqsuSWhkoJmiziYMrRYQZkRFizGxs6p8HrfWmqQeq9DhC2mLd6TXQkAxYpaW28RB7xXaGwPRpFpCfeaZAFwSNfzSoT8Kee52Sow5UMANTN9FfNzPJYeQBrBq6GGN6ayLm3KJbqQeZrRcuomYy58pqJ71P1JwymdDVNMe328EMD6UczfJPnTDPH3DeenJwTSdDRuDStJDAn3BWujigjJVAHMnXeMcG63obbFMc4XTsSt9W8bKTs72CpffzB6RsZQyL5UooRBGEj1Y5xHhYjdQAtE6uix2Xg5Dp3NPwUirQ8UsU2Sw95bYr8GZFr6dAHwo8pcmF9WNWihnWMEnbzFnBZqVNAUJ6G"
  ],
  "id": "did:peer:4zQmTtzjstZ5p2Li62vbqPTgHBbdQM7QE5BvcKAme4t3HHPU"
}
```

#### Example 4

Input Document:

```json
{
  "@context": [
    "https://www.w3.org/ns/did/v1"
  ],
  "verificationMethod": [
    {
      "type": "Ed25519VerificationKey2018",
      "publicKeyJwk": {
        "kty": "OKP",
        "crv": "Ed25519",
        "x": "UTBElpNSZB8dS_R9rzWnWB-ozdtL7Sz96RQZhwnzur8"
      },
      "id": "#z6MkjvBkt8ETnxXGBFPSGgYKb43q7oNHLX8BiYSPcXVG6gY6"
    }
  ],
  "authentication": [
    "#z6MkjvBkt8ETnxXGBFPSGgYKb43q7oNHLX8BiYSPcXVG6gY6"
  ],
  "assertionMethod": [
    "#z6MkjvBkt8ETnxXGBFPSGgYKb43q7oNHLX8BiYSPcXVG6gY6"
  ]
}
```

Long Form DID:

```
did:peer:4zQmb5cH6UdXeQze2CkPM1FjLP3Yi6SHPHQKPq5wjeS3YiUt:z3AFKXqX5u3s7opYvAJuaLXm4vjXWp67LDGCq83dHQJ9KRRDdPYyAwMA2CXmbFT12ZFD8iAKrd9pdbERrB7KyyAvQ2fikaprHyV8ekiys1DfCd7VTWhM5zNfZY9grWGC8qvJ4qguDNaHwrvwFoWz3gEP52kt1KiY7WAgUvzkck1ikaQNDT21rSomYWLYDovJUkbvnnV13RRbbcz8GJWT5cRnacvVcXrGVTTZHiUcgw2yma2t9T1dBExetW73cobAmrAH2kU2ZsazkbMxchMen2Jf327E9AckTHt7CGcDKU2HZ442v6cRhr76LXxbmEnXqDQ92fjuZ7iPEJhVCWF6XRB2ZvMkoh6i5Gt3T9fP4cznKXLCJ8ucbE62Kp4fqMpdNs8yd6wWmr4hzxeJnN8qV1xNJ5oCF8KvV8DeRTXmcs2nfk7BTV8AijCf1CEoLvTtFWEkG7XrK3dJH1r4hJPfUAEiX17GXFyRdz4NjdKV4XHFsmYEAkwW1NJzDVoJtWdnjMRj4F2obmEkBHD6F8uPhef7RGs8HHM6Lc1XTz6g
```

Short Form DID: `did:peer:4zQmb5cH6UdXeQze2CkPM1FjLP3Yi6SHPHQKPq5wjeS3YiUt`

Resolved Document, Long Form:

```json
{
  "@context": [
    "https://www.w3.org/ns/did/v1"
  ],
  "verificationMethod": [
    {
      "type": "Ed25519VerificationKey2018",
      "publicKeyJwk": {
        "kty": "OKP",
        "crv": "Ed25519",
        "x": "UTBElpNSZB8dS_R9rzWnWB-ozdtL7Sz96RQZhwnzur8"
      },
      "id": "#z6MkjvBkt8ETnxXGBFPSGgYKb43q7oNHLX8BiYSPcXVG6gY6",
      "controller": "did:peer:4zQmb5cH6UdXeQze2CkPM1FjLP3Yi6SHPHQKPq5wjeS3YiUt:z3AFKXqX5u3s7opYvAJuaLXm4vjXWp67LDGCq83dHQJ9KRRDdPYyAwMA2CXmbFT12ZFD8iAKrd9pdbERrB7KyyAvQ2fikaprHyV8ekiys1DfCd7VTWhM5zNfZY9grWGC8qvJ4qguDNaHwrvwFoWz3gEP52kt1KiY7WAgUvzkck1ikaQNDT21rSomYWLYDovJUkbvnnV13RRbbcz8GJWT5cRnacvVcXrGVTTZHiUcgw2yma2t9T1dBExetW73cobAmrAH2kU2ZsazkbMxchMen2Jf327E9AckTHt7CGcDKU2HZ442v6cRhr76LXxbmEnXqDQ92fjuZ7iPEJhVCWF6XRB2ZvMkoh6i5Gt3T9fP4cznKXLCJ8ucbE62Kp4fqMpdNs8yd6wWmr4hzxeJnN8qV1xNJ5oCF8KvV8DeRTXmcs2nfk7BTV8AijCf1CEoLvTtFWEkG7XrK3dJH1r4hJPfUAEiX17GXFyRdz4NjdKV4XHFsmYEAkwW1NJzDVoJtWdnjMRj4F2obmEkBHD6F8uPhef7RGs8HHM6Lc1XTz6g"
    }
  ],
  "authentication": [
    "#z6MkjvBkt8ETnxXGBFPSGgYKb43q7oNHLX8BiYSPcXVG6gY6"
  ],
  "assertionMethod": [
    "#z6MkjvBkt8ETnxXGBFPSGgYKb43q7oNHLX8BiYSPcXVG6gY6"
  ],
  "alsoKnownAs": [
    "did:peer:4zQmb5cH6UdXeQze2CkPM1FjLP3Yi6SHPHQKPq5wjeS3YiUt"
  ],
  "id": "did:peer:4zQmb5cH6UdXeQze2CkPM1FjLP3Yi6SHPHQKPq5wjeS3YiUt:z3AFKXqX5u3s7opYvAJuaLXm4vjXWp67LDGCq83dHQJ9KRRDdPYyAwMA2CXmbFT12ZFD8iAKrd9pdbERrB7KyyAvQ2fikaprHyV8ekiys1DfCd7VTWhM5zNfZY9grWGC8qvJ4qguDNaHwrvwFoWz3gEP52kt1KiY7WAgUvzkck1ikaQNDT21rSomYWLYDovJUkbvnnV13RRbbcz8GJWT5cRnacvVcXrGVTTZHiUcgw2yma2t9T1dBExetW73cobAmrAH2kU2ZsazkbMxchMen2Jf327E9AckTHt7CGcDKU2HZ442v6cRhr76LXxbmEnXqDQ92fjuZ7iPEJhVCWF6XRB2ZvMkoh6i5Gt3T9fP4cznKXLCJ8ucbE62Kp4fqMpdNs8yd6wWmr4hzxeJnN8qV1xNJ5oCF8KvV8DeRTXmcs2nfk7BTV8AijCf1CEoLvTtFWEkG7XrK3dJH1r4hJPfUAEiX17GXFyRdz4NjdKV4XHFsmYEAkwW1NJzDVoJtWdnjMRj4F2obmEkBHD6F8uPhef7RGs8HHM6Lc1XTz6g"
}
```

Resolved Document, Short Form:

```json
{
  "@context": [
    "https://www.w3.org/ns/did/v1"
  ],
  "verificationMethod": [
    {
      "type": "Ed25519VerificationKey2018",
      "publicKeyJwk": {
        "kty": "OKP",
        "crv": "Ed25519",
        "x": "UTBElpNSZB8dS_R9rzWnWB-ozdtL7Sz96RQZhwnzur8"
      },
      "id": "#z6MkjvBkt8ETnxXGBFPSGgYKb43q7oNHLX8BiYSPcXVG6gY6",
      "controller": "did:peer:4zQmb5cH6UdXeQze2CkPM1FjLP3Yi6SHPHQKPq5wjeS3YiUt"
    }
  ],
  "authentication": [
    "#z6MkjvBkt8ETnxXGBFPSGgYKb43q7oNHLX8BiYSPcXVG6gY6"
  ],
  "assertionMethod": [
    "#z6MkjvBkt8ETnxXGBFPSGgYKb43q7oNHLX8BiYSPcXVG6gY6"
  ],
  "alsoKnownAs": [
    "did:peer:4zQmb5cH6UdXeQze2CkPM1FjLP3Yi6SHPHQKPq5wjeS3YiUt:z3AFKXqX5u3s7opYvAJuaLXm4vjXWp67LDGCq83dHQJ9KRRDdPYyAwMA2CXmbFT12ZFD8iAKrd9pdbERrB7KyyAvQ2fikaprHyV8ekiys1DfCd7VTWhM5zNfZY9grWGC8qvJ4qguDNaHwrvwFoWz3gEP52kt1KiY7WAgUvzkck1ikaQNDT21rSomYWLYDovJUkbvnnV13RRbbcz8GJWT5cRnacvVcXrGVTTZHiUcgw2yma2t9T1dBExetW73cobAmrAH2kU2ZsazkbMxchMen2Jf327E9AckTHt7CGcDKU2HZ442v6cRhr76LXxbmEnXqDQ92fjuZ7iPEJhVCWF6XRB2ZvMkoh6i5Gt3T9fP4cznKXLCJ8ucbE62Kp4fqMpdNs8yd6wWmr4hzxeJnN8qV1xNJ5oCF8KvV8DeRTXmcs2nfk7BTV8AijCf1CEoLvTtFWEkG7XrK3dJH1r4hJPfUAEiX17GXFyRdz4NjdKV4XHFsmYEAkwW1NJzDVoJtWdnjMRj4F2obmEkBHD6F8uPhef7RGs8HHM6Lc1XTz6g"
  ],
  "id": "did:peer:4zQmb5cH6UdXeQze2CkPM1FjLP3Yi6SHPHQKPq5wjeS3YiUt"
}
```

#### Example 5

Input Document:

```json
{
  "@context": "https://w3id.org/did/v1",
  "authentication": [
    {
      "id": "#key-1",
      "type": "Ed25519VerificationKey2020",
      "publicKeyMultibase": "z6MkqRYqQiSgvZQdnBytw86Qbs2ZWUkGv22od935YF4s8M7V"
    },
    {
      "id": "#key-2",
      "type": "Ed25519VerificationKey2020",
      "publicKeyMultibase": "z6MkgoLTnTypo3tDRwCkZXSccTPHRLhF4ZnjhueYAFpEX6vg"
    }
  ],
  "keyAgreement": [
    {
      "id": "#key-3",
      "type": "X25519KeyAgreementKey2020",
      "publicKeyMultibase": "z6LSbysY2xFMRpGMhb7tFTLMpeuPRaqaWM1yECx2AtzE3KCc"
    }
  ],
  "service": [
    {
      "id": "#didcommmessaging-0",
      "type": "DIDCommMessaging",
      "serviceEndpoint": {
        "uri": "https://example.com/endpoint",
        "routingKeys": [
          "did:example:somemediator#somekey"
        ],
        "accept": [
          "didcomm/v2",
          "didcomm/aip2;env=rfc587"
        ]
      }
    }
  ]
}
```

Long Form DID:

```
did:peer:4zQmSAu6N2xECXwbofFMA2ZgeL3EERDPNrG5XQGnaA528mzL:zAPouDipG3F4FgNtQyjLFKAaesTzXDKDm71QEEUJdxQjZ94nyzBR7SKPQ5woVNc16Yqn6yrVEaFAZTWoJKgjz6Jc9ACCvEBmCB9D1kYGCnzB4Cx65SHfsX4c65XezdJyDzBNBZhprZtmqWFFv8dX177Yzqq9pBJkjSXJvKsrpXAsMG8EKMTFFosrrFoyH9jDy9m3pUHHGgZvXD1xUejiehoR5wQsjhw3PWQSYobgGMZP7Q3YNxSwRQ4ThLQLFUVbruqK4PTRiYahi8Ym73Kyg3r7krbo8VUMfU31hsX3iTBgfGuf27Ce7ibHhdJY5d7CDBjLwrxJV5zruQR6k8bYzi5JyfR1VFYq8njUvbQkfWSjtd71fZUpmffkUr5zkAS9gw2AwYp12MsWQL2Ebw25YnyWxLs3wCyEG4MuinjA81T3V91Uv3SxHTe2Tww61nf4QSA2xh81wZaxiCrD4VuEM1DsJsu2qxatv5sfiA3CuFqtABYKx59e61G2pzCpDpcMdRaXJ1tZkZ3j7L42mEuicf7NWqg6FgyU4aT4NTzCRRGkUEcrKATT1NUAYkqpYYau8VXzdRcNWfSPY8PJLXjQQhnxAdb6oSdk2srg75ZzqYNSHU7TqhUCUTPTd8jJT9cXihqHrwTp1toeZAhf6Uyy8myALYpqrTaDQS3VULWR8QA4fuqjtRPRsjXSMaNLxYYCEksXbMVY7kNSJ4Xyr8DpDzrGZRFaCELWYuRYzjQpmGTWVrea2ZbwsirxpjKJ99t5aQ8mdSvDZZP8GskdFABXb1kJPb18JnqS4EzFPmUyLPJuzYaGMhFGbJt214iZZLUSzsp6wL1kvfg789DavkM2QiYgCYPb1kCDjtGbqGge7L4Vt2GRJGc2r39r2Trypi6VDvA8z2UcGm5d1mk4gwd15xx
```

Short Form DID: `did:peer:4zQmSAu6N2xECXwbofFMA2ZgeL3EERDPNrG5XQGnaA528mzL`

Resolved Document, Long Form:

```json
{
  "@context": "https://w3id.org/did/v1",
  "service": [
    {
      "id": "#didcommmessaging-0",
      "type": "DIDCommMessaging",
      "serviceEndpoint": {
        "uri": "https://example.com/endpoint",
        "routingKeys": [
          "did:example:somemediator#somekey"
        ],
        "accept": [
          "didcomm/v2",
          "didcomm/aip2;env=rfc587"
        ]
      }
    }
  ],
  "authentication": [
    {
      "id": "#key-1",
      "type": "Ed25519VerificationKey2020",
      "publicKeyMultibase": "z6MkqRYqQiSgvZQdnBytw86Qbs2ZWUkGv22od935YF4s8M7V",
      "controller": "did:peer:4zQmSAu6N2xECXwbofFMA2ZgeL3EERDPNrG5XQGnaA528mzL:zAPouDipG3F4FgNtQyjLFKAaesTzXDKDm71QEEUJdxQjZ94nyzBR7SKPQ5woVNc16Yqn6yrVEaFAZTWoJKgjz6Jc9ACCvEBmCB9D1kYGCnzB4Cx65SHfsX4c65XezdJyDzBNBZhprZtmqWFFv8dX177Yzqq9pBJkjSXJvKsrpXAsMG8EKMTFFosrrFoyH9jDy9m3pUHHGgZvXD1xUejiehoR5wQsjhw3PWQSYobgGMZP7Q3YNxSwRQ4ThLQLFUVbruqK4PTRiYahi8Ym73Kyg3r7krbo8VUMfU31hsX3iTBgfGuf27Ce7ibHhdJY5d7CDBjLwrxJV5zruQR6k8bYzi5JyfR1VFYq8njUvbQkfWSjtd71fZUpmffkUr5zkAS9gw2AwYp12MsWQL2Ebw25YnyWxLs3wCyEG4MuinjA81T3V91Uv3SxHTe2Tww61nf4QSA2xh81wZaxiCrD4VuEM1DsJsu2qxatv5sfiA3CuFqtABYKx59e61G2pzCpDpcMdRaXJ1tZkZ3j7L42mEuicf7NWqg6FgyU4aT4NTzCRRGkUEcrKATT1NUAYkqpYYau8VXzdRcNWfSPY8PJLXjQQhnxAdb6oSdk2srg75ZzqYNSHU7TqhUCUTPTd8jJT9cXihqHrwTp1toeZAhf6Uyy8myALYpqrTaDQS3VULWR8QA4fuqjtRPRsjXSMaNLxYYCEksXbMVY7kNSJ4Xyr8DpDzrGZRFaCELWYuRYzjQpmGTWVrea2ZbwsirxpjKJ99t5aQ8mdSvDZZP8GskdFABXb1kJPb18JnqS4EzFPmUyLPJuzYaGMhFGbJt214iZZLUSzsp6wL1kvfg789DavkM2QiYgCYPb1kCDjtGbqGge7L4Vt2GRJGc2r39r2Trypi6VDvA8z2UcGm5d1mk4gwd15xx"
    },
    {
      "id": "#key-2",
      "type": "Ed25519VerificationKey2020",
      "publicKeyMultibase": "z6MkgoLTnTypo3tDRwCkZXSccTPHRLhF4ZnjhueYAFpEX6vg",
      "controller": "did:peer:4zQmSAu6N2xECXwbofFMA2ZgeL3EERDPNrG5XQGnaA528mzL:zAPouDipG3F4FgNtQyjLFKAaesTzXDKDm71QEEUJdxQjZ94nyzBR7SKPQ5woVNc16Yqn6yrVEaFAZTWoJKgjz6Jc9ACCvEBmCB9D1kYGCnzB4Cx65SHfsX4c65XezdJyDzBNBZhprZtmqWFFv8dX177Yzqq9pBJkjSXJvKsrpXAsMG8EKMTFFosrrFoyH9jDy9m3pUHHGgZvXD1xUejiehoR5wQsjhw3PWQSYobgGMZP7Q3YNxSwRQ4ThLQLFUVbruqK4PTRiYahi8Ym73Kyg3r7krbo8VUMfU31hsX3iTBgfGuf27Ce7ibHhdJY5d7CDBjLwrxJV5zruQR6k8bYzi5JyfR1VFYq8njUvbQkfWSjtd71fZUpmffkUr5zkAS9gw2AwYp12MsWQL2Ebw25YnyWxLs3wCyEG4MuinjA81T3V91Uv3SxHTe2Tww61nf4QSA2xh81wZaxiCrD4VuEM1DsJsu2qxatv5sfiA3CuFqtABYKx59e61G2pzCpDpcMdRaXJ1tZkZ3j7L42mEuicf7NWqg6FgyU4aT4NTzCRRGkUEcrKATT1NUAYkqpYYau8VXzdRcNWfSPY8PJLXjQQhnxAdb6oSdk2srg75ZzqYNSHU7TqhUCUTPTd8jJT9cXihqHrwTp1toeZAhf6Uyy8myALYpqrTaDQS3VULWR8QA4fuqjtRPRsjXSMaNLxYYCEksXbMVY7kNSJ4Xyr8DpDzrGZRFaCELWYuRYzjQpmGTWVrea2ZbwsirxpjKJ99t5aQ8mdSvDZZP8GskdFABXb1kJPb18JnqS4EzFPmUyLPJuzYaGMhFGbJt214iZZLUSzsp6wL1kvfg789DavkM2QiYgCYPb1kCDjtGbqGge7L4Vt2GRJGc2r39r2Trypi6VDvA8z2UcGm5d1mk4gwd15xx"
    }
  ],
  "keyAgreement": [
    {
      "id": "#key-3",
      "type": "X25519KeyAgreementKey2020",
      "publicKeyMultibase": "z6LSbysY2xFMRpGMhb7tFTLMpeuPRaqaWM1yECx2AtzE3KCc",
      "controller": "did:peer:4zQmSAu6N2xECXwbofFMA2ZgeL3EERDPNrG5XQGnaA528mzL:zAPouDipG3F4FgNtQyjLFKAaesTzXDKDm71QEEUJdxQjZ94nyzBR7SKPQ5woVNc16Yqn6yrVEaFAZTWoJKgjz6Jc9ACCvEBmCB9D1kYGCnzB4Cx65SHfsX4c65XezdJyDzBNBZhprZtmqWFFv8dX177Yzqq9pBJkjSXJvKsrpXAsMG8EKMTFFosrrFoyH9jDy9m3pUHHGgZvXD1xUejiehoR5wQsjhw3PWQSYobgGMZP7Q3YNxSwRQ4ThLQLFUVbruqK4PTRiYahi8Ym73Kyg3r7krbo8VUMfU31hsX3iTBgfGuf27Ce7ibHhdJY5d7CDBjLwrxJV5zruQR6k8bYzi5JyfR1VFYq8njUvbQkfWSjtd71fZUpmffkUr5zkAS9gw2AwYp12MsWQL2Ebw25YnyWxLs3wCyEG4MuinjA81T3V91Uv3SxHTe2Tww61nf4QSA2xh81wZaxiCrD4VuEM1DsJsu2qxatv5sfiA3CuFqtABYKx59e61G2pzCpDpcMdRaXJ1tZkZ3j7L42mEuicf7NWqg6FgyU4aT4NTzCRRGkUEcrKATT1NUAYkqpYYau8VXzdRcNWfSPY8PJLXjQQhnxAdb6oSdk2srg75ZzqYNSHU7TqhUCUTPTd8jJT9cXihqHrwTp1toeZAhf6Uyy8myALYpqrTaDQS3VULWR8QA4fuqjtRPRsjXSMaNLxYYCEksXbMVY7kNSJ4Xyr8DpDzrGZRFaCELWYuRYzjQpmGTWVrea2ZbwsirxpjKJ99t5aQ8mdSvDZZP8GskdFABXb1kJPb18JnqS4EzFPmUyLPJuzYaGMhFGbJt214iZZLUSzsp6wL1kvfg789DavkM2QiYgCYPb1kCDjtGbqGge7L4Vt2GRJGc2r39r2Trypi6VDvA8z2UcGm5d1mk4gwd15xx"
    }
  ],
  "alsoKnownAs": [
    "did:peer:4zQmSAu6N2xECXwbofFMA2ZgeL3EERDPNrG5XQGnaA528mzL"
  ],
  "id": "did:peer:4zQmSAu6N2xECXwbofFMA2ZgeL3EERDPNrG5XQGnaA528mzL:zAPouDipG3F4FgNtQyjLFKAaesTzXDKDm71QEEUJdxQjZ94nyzBR7SKPQ5woVNc16Yqn6yrVEaFAZTWoJKgjz6Jc9ACCvEBmCB9D1kYGCnzB4Cx65SHfsX4c65XezdJyDzBNBZhprZtmqWFFv8dX177Yzqq9pBJkjSXJvKsrpXAsMG8EKMTFFosrrFoyH9jDy9m3pUHHGgZvXD1xUejiehoR5wQsjhw3PWQSYobgGMZP7Q3YNxSwRQ4ThLQLFUVbruqK4PTRiYahi8Ym73Kyg3r7krbo8VUMfU31hsX3iTBgfGuf27Ce7ibHhdJY5d7CDBjLwrxJV5zruQR6k8bYzi5JyfR1VFYq8njUvbQkfWSjtd71fZUpmffkUr5zkAS9gw2AwYp12MsWQL2Ebw25YnyWxLs3wCyEG4MuinjA81T3V91Uv3SxHTe2Tww61nf4QSA2xh81wZaxiCrD4VuEM1DsJsu2qxatv5sfiA3CuFqtABYKx59e61G2pzCpDpcMdRaXJ1tZkZ3j7L42mEuicf7NWqg6FgyU4aT4NTzCRRGkUEcrKATT1NUAYkqpYYau8VXzdRcNWfSPY8PJLXjQQhnxAdb6oSdk2srg75ZzqYNSHU7TqhUCUTPTd8jJT9cXihqHrwTp1toeZAhf6Uyy8myALYpqrTaDQS3VULWR8QA4fuqjtRPRsjXSMaNLxYYCEksXbMVY7kNSJ4Xyr8DpDzrGZRFaCELWYuRYzjQpmGTWVrea2ZbwsirxpjKJ99t5aQ8mdSvDZZP8GskdFABXb1kJPb18JnqS4EzFPmUyLPJuzYaGMhFGbJt214iZZLUSzsp6wL1kvfg789DavkM2QiYgCYPb1kCDjtGbqGge7L4Vt2GRJGc2r39r2Trypi6VDvA8z2UcGm5d1mk4gwd15xx"
}
```

Resolved Document, Short Form:

```json
{
  "@context": "https://w3id.org/did/v1",
  "service": [
    {
      "id": "#didcommmessaging-0",
      "type": "DIDCommMessaging",
      "serviceEndpoint": {
        "uri": "https://example.com/endpoint",
        "routingKeys": [
          "did:example:somemediator#somekey"
        ],
        "accept": [
          "didcomm/v2",
          "didcomm/aip2;env=rfc587"
        ]
      }
    }
  ],
  "authentication": [
    {
      "id": "#key-1",
      "type": "Ed25519VerificationKey2020",
      "publicKeyMultibase": "z6MkqRYqQiSgvZQdnBytw86Qbs2ZWUkGv22od935YF4s8M7V",
      "controller": "did:peer:4zQmSAu6N2xECXwbofFMA2ZgeL3EERDPNrG5XQGnaA528mzL"
    },
    {
      "id": "#key-2",
      "type": "Ed25519VerificationKey2020",
      "publicKeyMultibase": "z6MkgoLTnTypo3tDRwCkZXSccTPHRLhF4ZnjhueYAFpEX6vg",
      "controller": "did:peer:4zQmSAu6N2xECXwbofFMA2ZgeL3EERDPNrG5XQGnaA528mzL"
    }
  ],
  "keyAgreement": [
    {
      "id": "#key-3",
      "type": "X25519KeyAgreementKey2020",
      "publicKeyMultibase": "z6LSbysY2xFMRpGMhb7tFTLMpeuPRaqaWM1yECx2AtzE3KCc",
      "controller": "did:peer:4zQmSAu6N2xECXwbofFMA2ZgeL3EERDPNrG5XQGnaA528mzL"
    }
  ],
  "alsoKnownAs": [
    "did:peer:4zQmSAu6N2xECXwbofFMA2ZgeL3EERDPNrG5XQGnaA528mzL:zAPouDipG3F4FgNtQyjLFKAaesTzXDKDm71QEEUJdxQjZ94nyzBR7SKPQ5woVNc16Yqn6yrVEaFAZTWoJKgjz6Jc9ACCvEBmCB9D1kYGCnzB4Cx65SHfsX4c65XezdJyDzBNBZhprZtmqWFFv8dX177Yzqq9pBJkjSXJvKsrpXAsMG8EKMTFFosrrFoyH9jDy9m3pUHHGgZvXD1xUejiehoR5wQsjhw3PWQSYobgGMZP7Q3YNxSwRQ4ThLQLFUVbruqK4PTRiYahi8Ym73Kyg3r7krbo8VUMfU31hsX3iTBgfGuf27Ce7ibHhdJY5d7CDBjLwrxJV5zruQR6k8bYzi5JyfR1VFYq8njUvbQkfWSjtd71fZUpmffkUr5zkAS9gw2AwYp12MsWQL2Ebw25YnyWxLs3wCyEG4MuinjA81T3V91Uv3SxHTe2Tww61nf4QSA2xh81wZaxiCrD4VuEM1DsJsu2qxatv5sfiA3CuFqtABYKx59e61G2pzCpDpcMdRaXJ1tZkZ3j7L42mEuicf7NWqg6FgyU4aT4NTzCRRGkUEcrKATT1NUAYkqpYYau8VXzdRcNWfSPY8PJLXjQQhnxAdb6oSdk2srg75ZzqYNSHU7TqhUCUTPTd8jJT9cXihqHrwTp1toeZAhf6Uyy8myALYpqrTaDQS3VULWR8QA4fuqjtRPRsjXSMaNLxYYCEksXbMVY7kNSJ4Xyr8DpDzrGZRFaCELWYuRYzjQpmGTWVrea2ZbwsirxpjKJ99t5aQ8mdSvDZZP8GskdFABXb1kJPb18JnqS4EzFPmUyLPJuzYaGMhFGbJt214iZZLUSzsp6wL1kvfg789DavkM2QiYgCYPb1kCDjtGbqGge7L4Vt2GRJGc2r39r2Trypi6VDvA8z2UcGm5d1mk4gwd15xx"
  ],
  "id": "did:peer:4zQmSAu6N2xECXwbofFMA2ZgeL3EERDPNrG5XQGnaA528mzL"
}
```

#### Example 6

Input Document:

```json
{
  "@context": [
    "https://www.w3.org/ns/did/v1",
    "https://w3id.org/security/suites/jws-2020/v1"
  ],
  "authentication": [
    "#key-1"
  ],
  "service": [],
  "assertionMethod": [
    "#key-1"
  ],
  "verificationMethod": [
    {
      "id": "#key-1",
      "type": "JsonWebKey2020",
      "publicKeyJwk": {
        "kty": "EC",
        "crv": "secp256k1",
        "x": "masUHNuJ0oH0C_e5rLUu5VKwmU2l-a7rrNTqA__afN8",
        "y": "UmGGX_WgRFXbw6qTli9xcQ0owtkZVuUGVyM23e8rZe8",
        "kid": "#keys-1"
      }
    }
  ]
}
```

Long Form DID:

```
did:peer:4zQmYxyxu3ndxss6ZopgaRN7xfqrXVpUbLqJ5Qd9x8ov2HMo:z2LBoAcpyFY24cFmhR6v5E4cenhVk9os2NAz6b61FgJzvZTgjEncziY6EXJYv4hjHzke9AkCawZszR8QFYjHdf9xRk2qpqZN7tgkudQBTuZ7QNmmsfdJ9U6g2fcpoGqnqnKc3iqGqUXWWuUG4Y7wPVxFrkLAPA7jUDz6UFsLTcJ5vX5jVtdYeRBvKcMDH1pyKNSGQFzYAmXH5dnJTr6MTHf71RDicGZU2MkuLfUGzUJXHE3QEa5WJqE1WmF8mU5tUVr1ysKHxck97JdU35RBR96FG2UXqLSYcaALJZYXTRtu5q8ucwc5bb16T9sD2H4A3kZeStPs6zbHqq3uxM4En2ZwSjsRSgF8Fowkd6FpQpSRpf8MdmPchS5BZgSWTLmP2Z6T5vkgnab6KZgYsv4qvjBw9twBRBLdWRH7XeLAugb4jiEKwA3hMhmZeunGvUVbS4Q4rZ5FxW7mob2SYb7ncbDpsAMV2qFwMoua1ybbcwE1r1HYCCziLrmfe17GyNpwBdVhjdKvdwRxJFQPyHJon
```

Short Form DID: `did:peer:4zQmYxyxu3ndxss6ZopgaRN7xfqrXVpUbLqJ5Qd9x8ov2HMo`

Resolved Document, Long Form:

```json
{
  "@context": [
    "https://www.w3.org/ns/did/v1",
    "https://w3id.org/security/suites/jws-2020/v1"
  ],
  "verificationMethod": [
    {
      "id": "#key-1",
      "type": "JsonWebKey2020",
      "publicKeyJwk": {
        "kty": "EC",
        "crv": "secp256k1",
        "x": "masUHNuJ0oH0C_e5rLUu5VKwmU2l-a7rrNTqA__afN8",
        "y": "UmGGX_WgRFXbw6qTli9xcQ0owtkZVuUGVyM23e8rZe8",
        "kid": "#keys-1"
      },
      "controller": "did:peer:4zQmYxyxu3ndxss6ZopgaRN7xfqrXVpUbLqJ5Qd9x8ov2HMo:z2LBoAcpyFY24cFmhR6v5E4cenhVk9os2NAz6b61FgJzvZTgjEncziY6EXJYv4hjHzke9AkCawZszR8QFYjHdf9xRk2qpqZN7tgkudQBTuZ7QNmmsfdJ9U6g2fcpoGqnqnKc3iqGqUXWWuUG4Y7wPVxFrkLAPA7jUDz6UFsLTcJ5vX5jVtdYeRBvKcMDH1pyKNSGQFzYAmXH5dnJTr6MTHf71RDicGZU2MkuLfUGzUJXHE3QEa5WJqE1WmF8mU5tUVr1ysKHxck97JdU35RBR96FG2UXqLSYcaALJZYXTRtu5q8ucwc5bb16T9sD2H4A3kZeStPs6zbHqq3uxM4En2ZwSjsRSgF8Fowkd6FpQpSRpf8MdmPchS5BZgSWTLmP2Z6T5vkgnab6KZgYsv4qvjBw9twBRBLdWRH7XeLAugb4jiEKwA3hMhmZeunGvUVbS4Q4rZ5FxW7mob2SYb7ncbDpsAMV2qFwMoua1ybbcwE1r1HYCCziLrmfe17GyNpwBdVhjdKvdwRxJFQPyHJon"
    }
  ],
  "authentication": [
    "#key-1"
  ],
  "assertionMethod": [
    "#key-1"
  ],
  "alsoKnownAs": [
    "did:peer:4zQmYxyxu3ndxss6ZopgaRN7xfqrXVpUbLqJ5Qd9x8ov2HMo"
  ],
  "id": "did:peer:4zQmYxyxu3ndxss6ZopgaRN7xfqrXVpUbLqJ5Qd9x8ov2HMo:z2LBoAcpyFY24cFmhR6v5E4cenhVk9os2NAz6b61FgJzvZTgjEncziY6EXJYv4hjHzke9AkCawZszR8QFYjHdf9xRk2qpqZN7tgkudQBTuZ7QNmmsfdJ9U6g2fcpoGqnqnKc3iqGqUXWWuUG4Y7wPVxFrkLAPA7jUDz6UFsLTcJ5vX5jVtdYeRBvKcMDH1pyKNSGQFzYAmXH5dnJTr6MTHf71RDicGZU2MkuLfUGzUJXHE3QEa5WJqE1WmF8mU5tUVr1ysKHxck97JdU35RBR96FG2UXqLSYcaALJZYXTRtu5q8ucwc5bb16T9sD2H4A3kZeStPs6zbHqq3uxM4En2ZwSjsRSgF8Fowkd6FpQpSRpf8MdmPchS5BZgSWTLmP2Z6T5vkgnab6KZgYsv4qvjBw9twBRBLdWRH7XeLAugb4jiEKwA3hMhmZeunGvUVbS4Q4rZ5FxW7mob2SYb7ncbDpsAMV2qFwMoua1ybbcwE1r1HYCCziLrmfe17GyNpwBdVhjdKvdwRxJFQPyHJon"
}
```

Resolved Document, Short Form:

```json
{
  "@context": [
    "https://www.w3.org/ns/did/v1",
    "https://w3id.org/security/suites/jws-2020/v1"
  ],
  "verificationMethod": [
    {
      "id": "#key-1",
      "type": "JsonWebKey2020",
      "publicKeyJwk": {
        "kty": "EC",
        "crv": "secp256k1",
        "x": "masUHNuJ0oH0C_e5rLUu5VKwmU2l-a7rrNTqA__afN8",
        "y": "UmGGX_WgRFXbw6qTli9xcQ0owtkZVuUGVyM23e8rZe8",
        "kid": "#keys-1"
      },
      "controller": "did:peer:4zQmYxyxu3ndxss6ZopgaRN7xfqrXVpUbLqJ5Qd9x8ov2HMo"
    }
  ],
  "authentication": [
    "#key-1"
  ],
  "assertionMethod": [
    "#key-1"
  ],
  "alsoKnownAs": [
    "did:peer:4zQmYxyxu3ndxss6ZopgaRN7xfqrXVpUbLqJ5Qd9x8ov2HMo:z2LBoAcpyFY24cFmhR6v5E4cenhVk9os2NAz6b61FgJzvZTgjEncziY6EXJYv4hjHzke9AkCawZszR8QFYjHdf9xRk2qpqZN7tgkudQBTuZ7QNmmsfdJ9U6g2fcpoGqnqnKc3iqGqUXWWuUG4Y7wPVxFrkLAPA7jUDz6UFsLTcJ5vX5jVtdYeRBvKcMDH1pyKNSGQFzYAmXH5dnJTr6MTHf71RDicGZU2MkuLfUGzUJXHE3QEa5WJqE1WmF8mU5tUVr1ysKHxck97JdU35RBR96FG2UXqLSYcaALJZYXTRtu5q8ucwc5bb16T9sD2H4A3kZeStPs6zbHqq3uxM4En2ZwSjsRSgF8Fowkd6FpQpSRpf8MdmPchS5BZgSWTLmP2Z6T5vkgnab6KZgYsv4qvjBw9twBRBLdWRH7XeLAugb4jiEKwA3hMhmZeunGvUVbS4Q4rZ5FxW7mob2SYb7ncbDpsAMV2qFwMoua1ybbcwE1r1HYCCziLrmfe17GyNpwBdVhjdKvdwRxJFQPyHJon"
  ],
  "id": "did:peer:4zQmYxyxu3ndxss6ZopgaRN7xfqrXVpUbLqJ5Qd9x8ov2HMo"
}
```
