# DID Peer Numalgo 4

DID Peer Numalgo 4 is a statically resolvable DID Method with a short form and a long form. The short form is the hash over the long form.

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
      "serviceEndpoint": "didcomm://queue",
      "accept": [
        "didcomm/v2"
      ],
      "routingKeys": []
    }
  ]
}
```

This is very similar to the "genesis document" used in numalgo 1.

To encode this value into a `did:peer:4`:

1. Encode the document:
    1. JSON stringify the object without whitespace. Leaving the whitespace in won't break anything but it cuts out unnecessary characters.
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
did:peer:4zQmNsz8npvrAyj983LTownQhp3PmGVGzMYrhBRGfig6rZ6P:z3U8mHxj7WY8i5EQD5rmkfPaDTws9dw5NRERbsFhsDFh5kvAEAY1afMFTWWbZT2d7TjCYtGBt47e1WpYoXYKSoEjxQX9qhNSw2ujMPiHn5rVyVCwQH1kBLzs95n37MoD6ikVDd29fkJoZaBrGhNaxcFiW9b1N85NWGQ9vs1LEMxsqt5ZHiFXGp1tMU85Da4VETb7veFZjvxRsadgbgeK1tFG83c6SSyDjoVzQbagXJ44kZXaMMmbs4Kk6VJszrCM1CUHPk7kFgHmojWU8kFAmPE88oesxBW5Wdc5cCNB6cB4QzRGuYrkK15hMdoFWq4kVHJn1xbruCzJ7Mb9f2rKUF6KTiUbTYpHuo4Kbnu26tJKQ9D7xHkAM2N3ZPN3eRkXBefKme5mLhGjRgXm6fAZiCHuK4dMyg4Bd9HDXiy8vSdY8cyZnyuJdPsjq5FRvRD92cFNtJZBJJwRQu6WiwKhTL9jELwwGfU2jukeESmARHjpQRTkXhtyG5NHDwj3Yx9CsbyBR5xdGsB3raA8JiMP4nAsbZhfXiBErBUx4MwYRnBDZERZztPjJWJniyKVG6hfoBokzEtkZt6gYMh1tpjsBAcSVw4C9H7o7QrY3mW6DjSufDdHSdWPVJjfHgRzxUM218CSiEwqEctqxJP9fc2FVSDxai7JUnroVzgYzhb62S4ueLGKM83abkd3Fm5NeSuewPRbgwETTLvknz1Wq1G4qygq75Fp3Kr21qknM2tsgrkwyprYR9ZTK5YzY5sHCwNP14VXZeX24QdSfevspNdvFtFtiDq6dUufmy5bKeLdHxx7Mpb7vFToU8bk9zZNUkcgXvX12U6iT1zLEyszTS6B3csHRr1HmvLUgEQKfd2aWjV2ScktEBsjZRHWdWuxQRcs85sF92kW2fVX7k1EGAwYGsnr6Wf9Q7jkM7SgJM5WJ1rHHsxKXwj8j11QmwXRcgREVEJphWdj87tpsC36A4rfEYhyJDw13UB68JgoK544NbsA
```

To construct the short form, simply omit the `:{{encoded document}}` from the end.

Here is an example short form DID for the long form above:

```
did:peer:4zQmNsz8npvrAyj983LTownQhp3PmGVGzMYrhBRGfig6rZ6P
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
5. Optionally, for any relative references in the document, make them absolute by prepending the reference with the DID
    - This is not required because relative references are valid within DID Documents and are understood to refer to the current document

Here is an example long form DID Document (all relative references have been replaced with absolute references; however, this is optional):

```json
{
  "@context": [
    "https://www.w3.org/ns/did/v1",
    "https://w3id.org/security/suites/x25519-2020/v1",
    "https://w3id.org/security/suites/ed25519-2020/v1"
  ],
  "verificationMethod": [
    {
      "id": "did:peer:4zQmNsz8npvrAyj983LTownQhp3PmGVGzMYrhBRGfig6rZ6P:z3U8mHxj7WY8i5EQD5rmkfPaDTws9dw5NRERbsFhsDFh5kvAEAY1afMFTWWbZT2d7TjCYtGBt47e1WpYoXYKSoEjxQX9qhNSw2ujMPiHn5rVyVCwQH1kBLzs95n37MoD6ikVDd29fkJoZaBrGhNaxcFiW9b1N85NWGQ9vs1LEMxsqt5ZHiFXGp1tMU85Da4VETb7veFZjvxRsadgbgeK1tFG83c6SSyDjoVzQbagXJ44kZXaMMmbs4Kk6VJszrCM1CUHPk7kFgHmojWU8kFAmPE88oesxBW5Wdc5cCNB6cB4QzRGuYrkK15hMdoFWq4kVHJn1xbruCzJ7Mb9f2rKUF6KTiUbTYpHuo4Kbnu26tJKQ9D7xHkAM2N3ZPN3eRkXBefKme5mLhGjRgXm6fAZiCHuK4dMyg4Bd9HDXiy8vSdY8cyZnyuJdPsjq5FRvRD92cFNtJZBJJwRQu6WiwKhTL9jELwwGfU2jukeESmARHjpQRTkXhtyG5NHDwj3Yx9CsbyBR5xdGsB3raA8JiMP4nAsbZhfXiBErBUx4MwYRnBDZERZztPjJWJniyKVG6hfoBokzEtkZt6gYMh1tpjsBAcSVw4C9H7o7QrY3mW6DjSufDdHSdWPVJjfHgRzxUM218CSiEwqEctqxJP9fc2FVSDxai7JUnroVzgYzhb62S4ueLGKM83abkd3Fm5NeSuewPRbgwETTLvknz1Wq1G4qygq75Fp3Kr21qknM2tsgrkwyprYR9ZTK5YzY5sHCwNP14VXZeX24QdSfevspNdvFtFtiDq6dUufmy5bKeLdHxx7Mpb7vFToU8bk9zZNUkcgXvX12U6iT1zLEyszTS6B3csHRr1HmvLUgEQKfd2aWjV2ScktEBsjZRHWdWuxQRcs85sF92kW2fVX7k1EGAwYGsnr6Wf9Q7jkM7SgJM5WJ1rHHsxKXwj8j11QmwXRcgREVEJphWdj87tpsC36A4rfEYhyJDw13UB68JgoK544NbsA#6LSqPZfn",
      "type": "X25519KeyAgreementKey2020",
      "publicKeyMultibase": "z6LSqPZfn9krvgXma2icTMKf2uVcYhKXsudCmPoUzqGYW24U",
      "controller": "did:peer:4zQmNsz8npvrAyj983LTownQhp3PmGVGzMYrhBRGfig6rZ6P:z3U8mHxj7WY8i5EQD5rmkfPaDTws9dw5NRERbsFhsDFh5kvAEAY1afMFTWWbZT2d7TjCYtGBt47e1WpYoXYKSoEjxQX9qhNSw2ujMPiHn5rVyVCwQH1kBLzs95n37MoD6ikVDd29fkJoZaBrGhNaxcFiW9b1N85NWGQ9vs1LEMxsqt5ZHiFXGp1tMU85Da4VETb7veFZjvxRsadgbgeK1tFG83c6SSyDjoVzQbagXJ44kZXaMMmbs4Kk6VJszrCM1CUHPk7kFgHmojWU8kFAmPE88oesxBW5Wdc5cCNB6cB4QzRGuYrkK15hMdoFWq4kVHJn1xbruCzJ7Mb9f2rKUF6KTiUbTYpHuo4Kbnu26tJKQ9D7xHkAM2N3ZPN3eRkXBefKme5mLhGjRgXm6fAZiCHuK4dMyg4Bd9HDXiy8vSdY8cyZnyuJdPsjq5FRvRD92cFNtJZBJJwRQu6WiwKhTL9jELwwGfU2jukeESmARHjpQRTkXhtyG5NHDwj3Yx9CsbyBR5xdGsB3raA8JiMP4nAsbZhfXiBErBUx4MwYRnBDZERZztPjJWJniyKVG6hfoBokzEtkZt6gYMh1tpjsBAcSVw4C9H7o7QrY3mW6DjSufDdHSdWPVJjfHgRzxUM218CSiEwqEctqxJP9fc2FVSDxai7JUnroVzgYzhb62S4ueLGKM83abkd3Fm5NeSuewPRbgwETTLvknz1Wq1G4qygq75Fp3Kr21qknM2tsgrkwyprYR9ZTK5YzY5sHCwNP14VXZeX24QdSfevspNdvFtFtiDq6dUufmy5bKeLdHxx7Mpb7vFToU8bk9zZNUkcgXvX12U6iT1zLEyszTS6B3csHRr1HmvLUgEQKfd2aWjV2ScktEBsjZRHWdWuxQRcs85sF92kW2fVX7k1EGAwYGsnr6Wf9Q7jkM7SgJM5WJ1rHHsxKXwj8j11QmwXRcgREVEJphWdj87tpsC36A4rfEYhyJDw13UB68JgoK544NbsA"
    },
    {
      "id": "did:peer:4zQmNsz8npvrAyj983LTownQhp3PmGVGzMYrhBRGfig6rZ6P:z3U8mHxj7WY8i5EQD5rmkfPaDTws9dw5NRERbsFhsDFh5kvAEAY1afMFTWWbZT2d7TjCYtGBt47e1WpYoXYKSoEjxQX9qhNSw2ujMPiHn5rVyVCwQH1kBLzs95n37MoD6ikVDd29fkJoZaBrGhNaxcFiW9b1N85NWGQ9vs1LEMxsqt5ZHiFXGp1tMU85Da4VETb7veFZjvxRsadgbgeK1tFG83c6SSyDjoVzQbagXJ44kZXaMMmbs4Kk6VJszrCM1CUHPk7kFgHmojWU8kFAmPE88oesxBW5Wdc5cCNB6cB4QzRGuYrkK15hMdoFWq4kVHJn1xbruCzJ7Mb9f2rKUF6KTiUbTYpHuo4Kbnu26tJKQ9D7xHkAM2N3ZPN3eRkXBefKme5mLhGjRgXm6fAZiCHuK4dMyg4Bd9HDXiy8vSdY8cyZnyuJdPsjq5FRvRD92cFNtJZBJJwRQu6WiwKhTL9jELwwGfU2jukeESmARHjpQRTkXhtyG5NHDwj3Yx9CsbyBR5xdGsB3raA8JiMP4nAsbZhfXiBErBUx4MwYRnBDZERZztPjJWJniyKVG6hfoBokzEtkZt6gYMh1tpjsBAcSVw4C9H7o7QrY3mW6DjSufDdHSdWPVJjfHgRzxUM218CSiEwqEctqxJP9fc2FVSDxai7JUnroVzgYzhb62S4ueLGKM83abkd3Fm5NeSuewPRbgwETTLvknz1Wq1G4qygq75Fp3Kr21qknM2tsgrkwyprYR9ZTK5YzY5sHCwNP14VXZeX24QdSfevspNdvFtFtiDq6dUufmy5bKeLdHxx7Mpb7vFToU8bk9zZNUkcgXvX12U6iT1zLEyszTS6B3csHRr1HmvLUgEQKfd2aWjV2ScktEBsjZRHWdWuxQRcs85sF92kW2fVX7k1EGAwYGsnr6Wf9Q7jkM7SgJM5WJ1rHHsxKXwj8j11QmwXRcgREVEJphWdj87tpsC36A4rfEYhyJDw13UB68JgoK544NbsA#6MkrCD1c",
      "type": "Ed25519VerificationKey2020",
      "publicKeyMultibase": "z6MkrCD1csqtgdj8sjrsu8jxcbeyP6m7LiK87NzhfWqio5yr",
      "controller": "did:peer:4zQmNsz8npvrAyj983LTownQhp3PmGVGzMYrhBRGfig6rZ6P:z3U8mHxj7WY8i5EQD5rmkfPaDTws9dw5NRERbsFhsDFh5kvAEAY1afMFTWWbZT2d7TjCYtGBt47e1WpYoXYKSoEjxQX9qhNSw2ujMPiHn5rVyVCwQH1kBLzs95n37MoD6ikVDd29fkJoZaBrGhNaxcFiW9b1N85NWGQ9vs1LEMxsqt5ZHiFXGp1tMU85Da4VETb7veFZjvxRsadgbgeK1tFG83c6SSyDjoVzQbagXJ44kZXaMMmbs4Kk6VJszrCM1CUHPk7kFgHmojWU8kFAmPE88oesxBW5Wdc5cCNB6cB4QzRGuYrkK15hMdoFWq4kVHJn1xbruCzJ7Mb9f2rKUF6KTiUbTYpHuo4Kbnu26tJKQ9D7xHkAM2N3ZPN3eRkXBefKme5mLhGjRgXm6fAZiCHuK4dMyg4Bd9HDXiy8vSdY8cyZnyuJdPsjq5FRvRD92cFNtJZBJJwRQu6WiwKhTL9jELwwGfU2jukeESmARHjpQRTkXhtyG5NHDwj3Yx9CsbyBR5xdGsB3raA8JiMP4nAsbZhfXiBErBUx4MwYRnBDZERZztPjJWJniyKVG6hfoBokzEtkZt6gYMh1tpjsBAcSVw4C9H7o7QrY3mW6DjSufDdHSdWPVJjfHgRzxUM218CSiEwqEctqxJP9fc2FVSDxai7JUnroVzgYzhb62S4ueLGKM83abkd3Fm5NeSuewPRbgwETTLvknz1Wq1G4qygq75Fp3Kr21qknM2tsgrkwyprYR9ZTK5YzY5sHCwNP14VXZeX24QdSfevspNdvFtFtiDq6dUufmy5bKeLdHxx7Mpb7vFToU8bk9zZNUkcgXvX12U6iT1zLEyszTS6B3csHRr1HmvLUgEQKfd2aWjV2ScktEBsjZRHWdWuxQRcs85sF92kW2fVX7k1EGAwYGsnr6Wf9Q7jkM7SgJM5WJ1rHHsxKXwj8j11QmwXRcgREVEJphWdj87tpsC36A4rfEYhyJDw13UB68JgoK544NbsA"
    }
  ],
  "authentication": [
    "did:peer:4zQmNsz8npvrAyj983LTownQhp3PmGVGzMYrhBRGfig6rZ6P:z3U8mHxj7WY8i5EQD5rmkfPaDTws9dw5NRERbsFhsDFh5kvAEAY1afMFTWWbZT2d7TjCYtGBt47e1WpYoXYKSoEjxQX9qhNSw2ujMPiHn5rVyVCwQH1kBLzs95n37MoD6ikVDd29fkJoZaBrGhNaxcFiW9b1N85NWGQ9vs1LEMxsqt5ZHiFXGp1tMU85Da4VETb7veFZjvxRsadgbgeK1tFG83c6SSyDjoVzQbagXJ44kZXaMMmbs4Kk6VJszrCM1CUHPk7kFgHmojWU8kFAmPE88oesxBW5Wdc5cCNB6cB4QzRGuYrkK15hMdoFWq4kVHJn1xbruCzJ7Mb9f2rKUF6KTiUbTYpHuo4Kbnu26tJKQ9D7xHkAM2N3ZPN3eRkXBefKme5mLhGjRgXm6fAZiCHuK4dMyg4Bd9HDXiy8vSdY8cyZnyuJdPsjq5FRvRD92cFNtJZBJJwRQu6WiwKhTL9jELwwGfU2jukeESmARHjpQRTkXhtyG5NHDwj3Yx9CsbyBR5xdGsB3raA8JiMP4nAsbZhfXiBErBUx4MwYRnBDZERZztPjJWJniyKVG6hfoBokzEtkZt6gYMh1tpjsBAcSVw4C9H7o7QrY3mW6DjSufDdHSdWPVJjfHgRzxUM218CSiEwqEctqxJP9fc2FVSDxai7JUnroVzgYzhb62S4ueLGKM83abkd3Fm5NeSuewPRbgwETTLvknz1Wq1G4qygq75Fp3Kr21qknM2tsgrkwyprYR9ZTK5YzY5sHCwNP14VXZeX24QdSfevspNdvFtFtiDq6dUufmy5bKeLdHxx7Mpb7vFToU8bk9zZNUkcgXvX12U6iT1zLEyszTS6B3csHRr1HmvLUgEQKfd2aWjV2ScktEBsjZRHWdWuxQRcs85sF92kW2fVX7k1EGAwYGsnr6Wf9Q7jkM7SgJM5WJ1rHHsxKXwj8j11QmwXRcgREVEJphWdj87tpsC36A4rfEYhyJDw13UB68JgoK544NbsA#6MkrCD1c"
  ],
  "assertionMethod": [
    "did:peer:4zQmNsz8npvrAyj983LTownQhp3PmGVGzMYrhBRGfig6rZ6P:z3U8mHxj7WY8i5EQD5rmkfPaDTws9dw5NRERbsFhsDFh5kvAEAY1afMFTWWbZT2d7TjCYtGBt47e1WpYoXYKSoEjxQX9qhNSw2ujMPiHn5rVyVCwQH1kBLzs95n37MoD6ikVDd29fkJoZaBrGhNaxcFiW9b1N85NWGQ9vs1LEMxsqt5ZHiFXGp1tMU85Da4VETb7veFZjvxRsadgbgeK1tFG83c6SSyDjoVzQbagXJ44kZXaMMmbs4Kk6VJszrCM1CUHPk7kFgHmojWU8kFAmPE88oesxBW5Wdc5cCNB6cB4QzRGuYrkK15hMdoFWq4kVHJn1xbruCzJ7Mb9f2rKUF6KTiUbTYpHuo4Kbnu26tJKQ9D7xHkAM2N3ZPN3eRkXBefKme5mLhGjRgXm6fAZiCHuK4dMyg4Bd9HDXiy8vSdY8cyZnyuJdPsjq5FRvRD92cFNtJZBJJwRQu6WiwKhTL9jELwwGfU2jukeESmARHjpQRTkXhtyG5NHDwj3Yx9CsbyBR5xdGsB3raA8JiMP4nAsbZhfXiBErBUx4MwYRnBDZERZztPjJWJniyKVG6hfoBokzEtkZt6gYMh1tpjsBAcSVw4C9H7o7QrY3mW6DjSufDdHSdWPVJjfHgRzxUM218CSiEwqEctqxJP9fc2FVSDxai7JUnroVzgYzhb62S4ueLGKM83abkd3Fm5NeSuewPRbgwETTLvknz1Wq1G4qygq75Fp3Kr21qknM2tsgrkwyprYR9ZTK5YzY5sHCwNP14VXZeX24QdSfevspNdvFtFtiDq6dUufmy5bKeLdHxx7Mpb7vFToU8bk9zZNUkcgXvX12U6iT1zLEyszTS6B3csHRr1HmvLUgEQKfd2aWjV2ScktEBsjZRHWdWuxQRcs85sF92kW2fVX7k1EGAwYGsnr6Wf9Q7jkM7SgJM5WJ1rHHsxKXwj8j11QmwXRcgREVEJphWdj87tpsC36A4rfEYhyJDw13UB68JgoK544NbsA#6MkrCD1c"
  ],
  "keyAgreement": [
    "did:peer:4zQmNsz8npvrAyj983LTownQhp3PmGVGzMYrhBRGfig6rZ6P:z3U8mHxj7WY8i5EQD5rmkfPaDTws9dw5NRERbsFhsDFh5kvAEAY1afMFTWWbZT2d7TjCYtGBt47e1WpYoXYKSoEjxQX9qhNSw2ujMPiHn5rVyVCwQH1kBLzs95n37MoD6ikVDd29fkJoZaBrGhNaxcFiW9b1N85NWGQ9vs1LEMxsqt5ZHiFXGp1tMU85Da4VETb7veFZjvxRsadgbgeK1tFG83c6SSyDjoVzQbagXJ44kZXaMMmbs4Kk6VJszrCM1CUHPk7kFgHmojWU8kFAmPE88oesxBW5Wdc5cCNB6cB4QzRGuYrkK15hMdoFWq4kVHJn1xbruCzJ7Mb9f2rKUF6KTiUbTYpHuo4Kbnu26tJKQ9D7xHkAM2N3ZPN3eRkXBefKme5mLhGjRgXm6fAZiCHuK4dMyg4Bd9HDXiy8vSdY8cyZnyuJdPsjq5FRvRD92cFNtJZBJJwRQu6WiwKhTL9jELwwGfU2jukeESmARHjpQRTkXhtyG5NHDwj3Yx9CsbyBR5xdGsB3raA8JiMP4nAsbZhfXiBErBUx4MwYRnBDZERZztPjJWJniyKVG6hfoBokzEtkZt6gYMh1tpjsBAcSVw4C9H7o7QrY3mW6DjSufDdHSdWPVJjfHgRzxUM218CSiEwqEctqxJP9fc2FVSDxai7JUnroVzgYzhb62S4ueLGKM83abkd3Fm5NeSuewPRbgwETTLvknz1Wq1G4qygq75Fp3Kr21qknM2tsgrkwyprYR9ZTK5YzY5sHCwNP14VXZeX24QdSfevspNdvFtFtiDq6dUufmy5bKeLdHxx7Mpb7vFToU8bk9zZNUkcgXvX12U6iT1zLEyszTS6B3csHRr1HmvLUgEQKfd2aWjV2ScktEBsjZRHWdWuxQRcs85sF92kW2fVX7k1EGAwYGsnr6Wf9Q7jkM7SgJM5WJ1rHHsxKXwj8j11QmwXRcgREVEJphWdj87tpsC36A4rfEYhyJDw13UB68JgoK544NbsA#6LSqPZfn"
  ],
  "capabilityInvocation": [
    "did:peer:4zQmNsz8npvrAyj983LTownQhp3PmGVGzMYrhBRGfig6rZ6P:z3U8mHxj7WY8i5EQD5rmkfPaDTws9dw5NRERbsFhsDFh5kvAEAY1afMFTWWbZT2d7TjCYtGBt47e1WpYoXYKSoEjxQX9qhNSw2ujMPiHn5rVyVCwQH1kBLzs95n37MoD6ikVDd29fkJoZaBrGhNaxcFiW9b1N85NWGQ9vs1LEMxsqt5ZHiFXGp1tMU85Da4VETb7veFZjvxRsadgbgeK1tFG83c6SSyDjoVzQbagXJ44kZXaMMmbs4Kk6VJszrCM1CUHPk7kFgHmojWU8kFAmPE88oesxBW5Wdc5cCNB6cB4QzRGuYrkK15hMdoFWq4kVHJn1xbruCzJ7Mb9f2rKUF6KTiUbTYpHuo4Kbnu26tJKQ9D7xHkAM2N3ZPN3eRkXBefKme5mLhGjRgXm6fAZiCHuK4dMyg4Bd9HDXiy8vSdY8cyZnyuJdPsjq5FRvRD92cFNtJZBJJwRQu6WiwKhTL9jELwwGfU2jukeESmARHjpQRTkXhtyG5NHDwj3Yx9CsbyBR5xdGsB3raA8JiMP4nAsbZhfXiBErBUx4MwYRnBDZERZztPjJWJniyKVG6hfoBokzEtkZt6gYMh1tpjsBAcSVw4C9H7o7QrY3mW6DjSufDdHSdWPVJjfHgRzxUM218CSiEwqEctqxJP9fc2FVSDxai7JUnroVzgYzhb62S4ueLGKM83abkd3Fm5NeSuewPRbgwETTLvknz1Wq1G4qygq75Fp3Kr21qknM2tsgrkwyprYR9ZTK5YzY5sHCwNP14VXZeX24QdSfevspNdvFtFtiDq6dUufmy5bKeLdHxx7Mpb7vFToU8bk9zZNUkcgXvX12U6iT1zLEyszTS6B3csHRr1HmvLUgEQKfd2aWjV2ScktEBsjZRHWdWuxQRcs85sF92kW2fVX7k1EGAwYGsnr6Wf9Q7jkM7SgJM5WJ1rHHsxKXwj8j11QmwXRcgREVEJphWdj87tpsC36A4rfEYhyJDw13UB68JgoK544NbsA#6MkrCD1c"
  ],
  "capabilityDelegation": [
    "did:peer:4zQmNsz8npvrAyj983LTownQhp3PmGVGzMYrhBRGfig6rZ6P:z3U8mHxj7WY8i5EQD5rmkfPaDTws9dw5NRERbsFhsDFh5kvAEAY1afMFTWWbZT2d7TjCYtGBt47e1WpYoXYKSoEjxQX9qhNSw2ujMPiHn5rVyVCwQH1kBLzs95n37MoD6ikVDd29fkJoZaBrGhNaxcFiW9b1N85NWGQ9vs1LEMxsqt5ZHiFXGp1tMU85Da4VETb7veFZjvxRsadgbgeK1tFG83c6SSyDjoVzQbagXJ44kZXaMMmbs4Kk6VJszrCM1CUHPk7kFgHmojWU8kFAmPE88oesxBW5Wdc5cCNB6cB4QzRGuYrkK15hMdoFWq4kVHJn1xbruCzJ7Mb9f2rKUF6KTiUbTYpHuo4Kbnu26tJKQ9D7xHkAM2N3ZPN3eRkXBefKme5mLhGjRgXm6fAZiCHuK4dMyg4Bd9HDXiy8vSdY8cyZnyuJdPsjq5FRvRD92cFNtJZBJJwRQu6WiwKhTL9jELwwGfU2jukeESmARHjpQRTkXhtyG5NHDwj3Yx9CsbyBR5xdGsB3raA8JiMP4nAsbZhfXiBErBUx4MwYRnBDZERZztPjJWJniyKVG6hfoBokzEtkZt6gYMh1tpjsBAcSVw4C9H7o7QrY3mW6DjSufDdHSdWPVJjfHgRzxUM218CSiEwqEctqxJP9fc2FVSDxai7JUnroVzgYzhb62S4ueLGKM83abkd3Fm5NeSuewPRbgwETTLvknz1Wq1G4qygq75Fp3Kr21qknM2tsgrkwyprYR9ZTK5YzY5sHCwNP14VXZeX24QdSfevspNdvFtFtiDq6dUufmy5bKeLdHxx7Mpb7vFToU8bk9zZNUkcgXvX12U6iT1zLEyszTS6B3csHRr1HmvLUgEQKfd2aWjV2ScktEBsjZRHWdWuxQRcs85sF92kW2fVX7k1EGAwYGsnr6Wf9Q7jkM7SgJM5WJ1rHHsxKXwj8j11QmwXRcgREVEJphWdj87tpsC36A4rfEYhyJDw13UB68JgoK544NbsA#6MkrCD1c"
  ],
  "service": [
    {
      "id": "did:peer:4zQmNsz8npvrAyj983LTownQhp3PmGVGzMYrhBRGfig6rZ6P:z3U8mHxj7WY8i5EQD5rmkfPaDTws9dw5NRERbsFhsDFh5kvAEAY1afMFTWWbZT2d7TjCYtGBt47e1WpYoXYKSoEjxQX9qhNSw2ujMPiHn5rVyVCwQH1kBLzs95n37MoD6ikVDd29fkJoZaBrGhNaxcFiW9b1N85NWGQ9vs1LEMxsqt5ZHiFXGp1tMU85Da4VETb7veFZjvxRsadgbgeK1tFG83c6SSyDjoVzQbagXJ44kZXaMMmbs4Kk6VJszrCM1CUHPk7kFgHmojWU8kFAmPE88oesxBW5Wdc5cCNB6cB4QzRGuYrkK15hMdoFWq4kVHJn1xbruCzJ7Mb9f2rKUF6KTiUbTYpHuo4Kbnu26tJKQ9D7xHkAM2N3ZPN3eRkXBefKme5mLhGjRgXm6fAZiCHuK4dMyg4Bd9HDXiy8vSdY8cyZnyuJdPsjq5FRvRD92cFNtJZBJJwRQu6WiwKhTL9jELwwGfU2jukeESmARHjpQRTkXhtyG5NHDwj3Yx9CsbyBR5xdGsB3raA8JiMP4nAsbZhfXiBErBUx4MwYRnBDZERZztPjJWJniyKVG6hfoBokzEtkZt6gYMh1tpjsBAcSVw4C9H7o7QrY3mW6DjSufDdHSdWPVJjfHgRzxUM218CSiEwqEctqxJP9fc2FVSDxai7JUnroVzgYzhb62S4ueLGKM83abkd3Fm5NeSuewPRbgwETTLvknz1Wq1G4qygq75Fp3Kr21qknM2tsgrkwyprYR9ZTK5YzY5sHCwNP14VXZeX24QdSfevspNdvFtFtiDq6dUufmy5bKeLdHxx7Mpb7vFToU8bk9zZNUkcgXvX12U6iT1zLEyszTS6B3csHRr1HmvLUgEQKfd2aWjV2ScktEBsjZRHWdWuxQRcs85sF92kW2fVX7k1EGAwYGsnr6Wf9Q7jkM7SgJM5WJ1rHHsxKXwj8j11QmwXRcgREVEJphWdj87tpsC36A4rfEYhyJDw13UB68JgoK544NbsA#didcommmessaging-0",
      "type": "DIDCommMessaging",
      "serviceEndpoint": "didcomm://queue",
      "accept": [
        "didcomm/v2"
      ],
      "routingKeys": []
    }
  ],
  "alsoKnownAs": [
    "did:peer:4zQmNsz8npvrAyj983LTownQhp3PmGVGzMYrhBRGfig6rZ6P"
  ],
  "id": "did:peer:4zQmNsz8npvrAyj983LTownQhp3PmGVGzMYrhBRGfig6rZ6P:z3U8mHxj7WY8i5EQD5rmkfPaDTws9dw5NRERbsFhsDFh5kvAEAY1afMFTWWbZT2d7TjCYtGBt47e1WpYoXYKSoEjxQX9qhNSw2ujMPiHn5rVyVCwQH1kBLzs95n37MoD6ikVDd29fkJoZaBrGhNaxcFiW9b1N85NWGQ9vs1LEMxsqt5ZHiFXGp1tMU85Da4VETb7veFZjvxRsadgbgeK1tFG83c6SSyDjoVzQbagXJ44kZXaMMmbs4Kk6VJszrCM1CUHPk7kFgHmojWU8kFAmPE88oesxBW5Wdc5cCNB6cB4QzRGuYrkK15hMdoFWq4kVHJn1xbruCzJ7Mb9f2rKUF6KTiUbTYpHuo4Kbnu26tJKQ9D7xHkAM2N3ZPN3eRkXBefKme5mLhGjRgXm6fAZiCHuK4dMyg4Bd9HDXiy8vSdY8cyZnyuJdPsjq5FRvRD92cFNtJZBJJwRQu6WiwKhTL9jELwwGfU2jukeESmARHjpQRTkXhtyG5NHDwj3Yx9CsbyBR5xdGsB3raA8JiMP4nAsbZhfXiBErBUx4MwYRnBDZERZztPjJWJniyKVG6hfoBokzEtkZt6gYMh1tpjsBAcSVw4C9H7o7QrY3mW6DjSufDdHSdWPVJjfHgRzxUM218CSiEwqEctqxJP9fc2FVSDxai7JUnroVzgYzhb62S4ueLGKM83abkd3Fm5NeSuewPRbgwETTLvknz1Wq1G4qygq75Fp3Kr21qknM2tsgrkwyprYR9ZTK5YzY5sHCwNP14VXZeX24QdSfevspNdvFtFtiDq6dUufmy5bKeLdHxx7Mpb7vFToU8bk9zZNUkcgXvX12U6iT1zLEyszTS6B3csHRr1HmvLUgEQKfd2aWjV2ScktEBsjZRHWdWuxQRcs85sF92kW2fVX7k1EGAwYGsnr6Wf9Q7jkM7SgJM5WJ1rHHsxKXwj8j11QmwXRcgREVEJphWdj87tpsC36A4rfEYhyJDw13UB68JgoK544NbsA"
}
```

#### Short form
To resolve a short form `did:peer:4` DID, you must know the corresponding long form DID. It is not possible to resolve a short form `did:peer:4` without first seeing and storing it's long form counterpart.

To resolve a short form DID, take the decoded document (which will look exactly like the input doc example above) and follow the same rules described in the [long form](#long-form) section to "contextualize" the document but using the short form DID instead of the long form DID.

Here is an example short form DID Document (all relative references replaced with absolute references):

```json
{
  "@context": [
    "https://www.w3.org/ns/did/v1",
    "https://w3id.org/security/suites/x25519-2020/v1",
    "https://w3id.org/security/suites/ed25519-2020/v1"
  ],
  "verificationMethod": [
    {
      "id": "did:peer:4zQmNsz8npvrAyj983LTownQhp3PmGVGzMYrhBRGfig6rZ6P#6LSqPZfn",
      "type": "X25519KeyAgreementKey2020",
      "publicKeyMultibase": "z6LSqPZfn9krvgXma2icTMKf2uVcYhKXsudCmPoUzqGYW24U",
      "controller": "did:peer:4zQmNsz8npvrAyj983LTownQhp3PmGVGzMYrhBRGfig6rZ6P"
    },
    {
      "id": "did:peer:4zQmNsz8npvrAyj983LTownQhp3PmGVGzMYrhBRGfig6rZ6P#6MkrCD1c",
      "type": "Ed25519VerificationKey2020",
      "publicKeyMultibase": "z6MkrCD1csqtgdj8sjrsu8jxcbeyP6m7LiK87NzhfWqio5yr",
      "controller": "did:peer:4zQmNsz8npvrAyj983LTownQhp3PmGVGzMYrhBRGfig6rZ6P"
    }
  ],
  "authentication": [
    "did:peer:4zQmNsz8npvrAyj983LTownQhp3PmGVGzMYrhBRGfig6rZ6P#6MkrCD1c"
  ],
  "assertionMethod": [
    "did:peer:4zQmNsz8npvrAyj983LTownQhp3PmGVGzMYrhBRGfig6rZ6P#6MkrCD1c"
  ],
  "keyAgreement": [
    "did:peer:4zQmNsz8npvrAyj983LTownQhp3PmGVGzMYrhBRGfig6rZ6P#6LSqPZfn"
  ],
  "capabilityInvocation": [
    "did:peer:4zQmNsz8npvrAyj983LTownQhp3PmGVGzMYrhBRGfig6rZ6P#6MkrCD1c"
  ],
  "capabilityDelegation": [
    "did:peer:4zQmNsz8npvrAyj983LTownQhp3PmGVGzMYrhBRGfig6rZ6P#6MkrCD1c"
  ],
  "service": [
    {
      "id": "did:peer:4zQmNsz8npvrAyj983LTownQhp3PmGVGzMYrhBRGfig6rZ6P#didcommmessaging-0",
      "type": "DIDCommMessaging",
      "serviceEndpoint": "didcomm://queue",
      "accept": [
        "didcomm/v2"
      ],
      "routingKeys": []
    }
  ],
  "alsoKnownAs": [
    "did:peer:4zQmNsz8npvrAyj983LTownQhp3PmGVGzMYrhBRGfig6rZ6P:z3U8mHxj7WY8i5EQD5rmkfPaDTws9dw5NRERbsFhsDFh5kvAEAY1afMFTWWbZT2d7TjCYtGBt47e1WpYoXYKSoEjxQX9qhNSw2ujMPiHn5rVyVCwQH1kBLzs95n37MoD6ikVDd29fkJoZaBrGhNaxcFiW9b1N85NWGQ9vs1LEMxsqt5ZHiFXGp1tMU85Da4VETb7veFZjvxRsadgbgeK1tFG83c6SSyDjoVzQbagXJ44kZXaMMmbs4Kk6VJszrCM1CUHPk7kFgHmojWU8kFAmPE88oesxBW5Wdc5cCNB6cB4QzRGuYrkK15hMdoFWq4kVHJn1xbruCzJ7Mb9f2rKUF6KTiUbTYpHuo4Kbnu26tJKQ9D7xHkAM2N3ZPN3eRkXBefKme5mLhGjRgXm6fAZiCHuK4dMyg4Bd9HDXiy8vSdY8cyZnyuJdPsjq5FRvRD92cFNtJZBJJwRQu6WiwKhTL9jELwwGfU2jukeESmARHjpQRTkXhtyG5NHDwj3Yx9CsbyBR5xdGsB3raA8JiMP4nAsbZhfXiBErBUx4MwYRnBDZERZztPjJWJniyKVG6hfoBokzEtkZt6gYMh1tpjsBAcSVw4C9H7o7QrY3mW6DjSufDdHSdWPVJjfHgRzxUM218CSiEwqEctqxJP9fc2FVSDxai7JUnroVzgYzhb62S4ueLGKM83abkd3Fm5NeSuewPRbgwETTLvknz1Wq1G4qygq75Fp3Kr21qknM2tsgrkwyprYR9ZTK5YzY5sHCwNP14VXZeX24QdSfevspNdvFtFtiDq6dUufmy5bKeLdHxx7Mpb7vFToU8bk9zZNUkcgXvX12U6iT1zLEyszTS6B3csHRr1HmvLUgEQKfd2aWjV2ScktEBsjZRHWdWuxQRcs85sF92kW2fVX7k1EGAwYGsnr6Wf9Q7jkM7SgJM5WJ1rHHsxKXwj8j11QmwXRcgREVEJphWdj87tpsC36A4rfEYhyJDw13UB68JgoK544NbsA"
  ],
  "id": "did:peer:4zQmNsz8npvrAyj983LTownQhp3PmGVGzMYrhBRGfig6rZ6P"
}
```

## Stats

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
```
{
  "@context": "https://w3id.org/did/v1",
  "authentication": [
    "#1"
  ],
  "service": [
    {
      "id": "#didcomm",
      "priority": 0,
      "recipientKeys": [
        "#1"
      ],
      "routingKeys": [
        "did:key:z6Mknq3MqipEt9hJegs6J9V7tiLa6T5H5rX3fFCXksJKTuv7#z6Mknq3MqipEt9hJegs6J9V7tiLa6T5H5rX3fFCXksJKTuv7"
      ],
      "serviceEndpoint": "http://bob:3000",
      "type": "did-communication"
    }
  ],
  "verificationMethod": [
    {
      "id": "#1",
      "publicKeyBase58": "AU2FFjtkVzjFuirgWieqGGqtNrAZWS9LDuB8TDp6EUrG",
      "type": "Ed25519VerificationKey2018"
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
```
{
  "@context": "https://w3id.org/did/v1",
  "alsoKnownAs": [
    "did:peer:4zQmQ4dEtoGcivpiH6gtWwhWJY2ENVWuZifb62uzR76HGPPw"
  ],
  "authentication": [
    "#1"
  ],
  "id": "did:peer:4zQmQ4dEtoGcivpiH6gtWwhWJY2ENVWuZifb62uzR76HGPPw:z7p4QX8zEXt2sMjv1Tqq8Lv8Nx8oGo2uRczBe21vyfMhQzsWDnwGmjriYfUX75WDq622czcdHjWGhh2VTbzKhLXUjY8Ma7g64dKAVcy8SaxN5QVdjwpXgD7htKCgCjah8jHEzyBZFrtdfTHiVXfSUz1BiURQf1Z3NfxW5cWYsvDJVvQzVmdHb8ekzCnvxCqL2UV1v9SBb1DsU66N3PCp9HVpSrqUJQyFU2Ddc8bb6u8SJfBU1nyCkNMgfA1zAyKnSBrzZWyyNzAm9oBV36qjC1Qjfcpq4FBnGr7foh5sLXppBwu2ES8U2nxdGrQzAbN47DKBoKJqPVxNh5tTuBdYjDGt7PcvZQjHQGNXXuhJctM5besZci2saGefCHzoZ87vSsFuKq6oXEsW512eadiNZWjHSdG9J4ToMEMK9WT66vGGLFdZszB3xhdFqEDnAMcpnoFUL5WN243aH6492jPC2Zjdi1BvHC1J8bUuvyihAKXF3WmFz7gJWmh6MrTEWNqb17K6tqbyXjFmfnS2RbAi8xBFj3sSsXkSs6TRTXAZD9DenYaQq4RMa2Kqh6VKGvkXAjVHKcPh9Ncpt6rU9ZYttNHbDJFgahwB8KisVBK8FBpG",
  "service": [
    {
      "id": "#didcomm",
      "priority": 0,
      "recipientKeys": [
        "#1"
      ],
      "routingKeys": [
        "did:key:z6Mknq3MqipEt9hJegs6J9V7tiLa6T5H5rX3fFCXksJKTuv7#z6Mknq3MqipEt9hJegs6J9V7tiLa6T5H5rX3fFCXksJKTuv7"
      ],
      "serviceEndpoint": "http://bob:3000",
      "type": "did-communication"
    }
  ],
  "verificationMethod": [
    {
      "controller": "did:peer:4zQmQ4dEtoGcivpiH6gtWwhWJY2ENVWuZifb62uzR76HGPPw:z7p4QX8zEXt2sMjv1Tqq8Lv8Nx8oGo2uRczBe21vyfMhQzsWDnwGmjriYfUX75WDq622czcdHjWGhh2VTbzKhLXUjY8Ma7g64dKAVcy8SaxN5QVdjwpXgD7htKCgCjah8jHEzyBZFrtdfTHiVXfSUz1BiURQf1Z3NfxW5cWYsvDJVvQzVmdHb8ekzCnvxCqL2UV1v9SBb1DsU66N3PCp9HVpSrqUJQyFU2Ddc8bb6u8SJfBU1nyCkNMgfA1zAyKnSBrzZWyyNzAm9oBV36qjC1Qjfcpq4FBnGr7foh5sLXppBwu2ES8U2nxdGrQzAbN47DKBoKJqPVxNh5tTuBdYjDGt7PcvZQjHQGNXXuhJctM5besZci2saGefCHzoZ87vSsFuKq6oXEsW512eadiNZWjHSdG9J4ToMEMK9WT66vGGLFdZszB3xhdFqEDnAMcpnoFUL5WN243aH6492jPC2Zjdi1BvHC1J8bUuvyihAKXF3WmFz7gJWmh6MrTEWNqb17K6tqbyXjFmfnS2RbAi8xBFj3sSsXkSs6TRTXAZD9DenYaQq4RMa2Kqh6VKGvkXAjVHKcPh9Ncpt6rU9ZYttNHbDJFgahwB8KisVBK8FBpG",
      "id": "#1",
      "publicKeyBase58": "AU2FFjtkVzjFuirgWieqGGqtNrAZWS9LDuB8TDp6EUrG",
      "type": "Ed25519VerificationKey2018"
    }
  ]
}
```

Resolved Document, Short Form:
```
{
  "@context": "https://w3id.org/did/v1",
  "alsoKnownAs": [
    "did:peer:4zQmQ4dEtoGcivpiH6gtWwhWJY2ENVWuZifb62uzR76HGPPw:z7p4QX8zEXt2sMjv1Tqq8Lv8Nx8oGo2uRczBe21vyfMhQzsWDnwGmjriYfUX75WDq622czcdHjWGhh2VTbzKhLXUjY8Ma7g64dKAVcy8SaxN5QVdjwpXgD7htKCgCjah8jHEzyBZFrtdfTHiVXfSUz1BiURQf1Z3NfxW5cWYsvDJVvQzVmdHb8ekzCnvxCqL2UV1v9SBb1DsU66N3PCp9HVpSrqUJQyFU2Ddc8bb6u8SJfBU1nyCkNMgfA1zAyKnSBrzZWyyNzAm9oBV36qjC1Qjfcpq4FBnGr7foh5sLXppBwu2ES8U2nxdGrQzAbN47DKBoKJqPVxNh5tTuBdYjDGt7PcvZQjHQGNXXuhJctM5besZci2saGefCHzoZ87vSsFuKq6oXEsW512eadiNZWjHSdG9J4ToMEMK9WT66vGGLFdZszB3xhdFqEDnAMcpnoFUL5WN243aH6492jPC2Zjdi1BvHC1J8bUuvyihAKXF3WmFz7gJWmh6MrTEWNqb17K6tqbyXjFmfnS2RbAi8xBFj3sSsXkSs6TRTXAZD9DenYaQq4RMa2Kqh6VKGvkXAjVHKcPh9Ncpt6rU9ZYttNHbDJFgahwB8KisVBK8FBpG"
  ],
  "authentication": [
    "#1"
  ],
  "id": "did:peer:4zQmQ4dEtoGcivpiH6gtWwhWJY2ENVWuZifb62uzR76HGPPw",
  "service": [
    {
      "id": "#didcomm",
      "priority": 0,
      "recipientKeys": [
        "#1"
      ],
      "routingKeys": [
        "did:key:z6Mknq3MqipEt9hJegs6J9V7tiLa6T5H5rX3fFCXksJKTuv7#z6Mknq3MqipEt9hJegs6J9V7tiLa6T5H5rX3fFCXksJKTuv7"
      ],
      "serviceEndpoint": "http://bob:3000",
      "type": "did-communication"
    }
  ],
  "verificationMethod": [
    {
      "controller": "did:peer:4zQmQ4dEtoGcivpiH6gtWwhWJY2ENVWuZifb62uzR76HGPPw",
      "id": "#1",
      "publicKeyBase58": "AU2FFjtkVzjFuirgWieqGGqtNrAZWS9LDuB8TDp6EUrG",
      "type": "Ed25519VerificationKey2018"
    }
  ]
}
```

#### Example 2

Input Document:
```
{
  "@context": "https://w3id.org/did/v1",
  "authentication": [
    "#1"
  ],
  "service": [
    {
      "id": "#didcomm",
      "recipientKeys": [
        "#1"
      ],
      "serviceEndpoint": "http://172.17.0.1:9031/a2a/5b6dyY6PndLaCnWxZbeEYW/5b6dyY6PndLaCnWxZbeEYW/2f6aae0c-6b04-40ff-a25e-faecaea39f83",
      "type": "did-communication"
    }
  ],
  "verificationMethod": [
    {
      "id": "#1",
      "publicKeyBase58": "3dtu2WWtd5ELwRTJEPzmEJUYEp8Qq36N2QA24g9tFXK9",
      "type": "Ed25519VerificationKey2018"
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
```
{
  "@context": "https://w3id.org/did/v1",
  "alsoKnownAs": [
    "did:peer:4zQmRMVzDUXhV64pfw3vFaDvyExjzW9oBXCF2n4zYCaHQFAT"
  ],
  "authentication": [
    "#1"
  ],
  "id": "did:peer:4zQmRMVzDUXhV64pfw3vFaDvyExjzW9oBXCF2n4zYCaHQFAT:zMx3zwMnDECV3GiFs8nmHr38TziMEEkcgFBEDH5PXQ8hxnMrwNfB9wTwskpJMjggeg8NF1jeDSK5772op2zLLdy8TGFCEiYQxpUvvku8qSCZx5Q8V9Li9mDp6WEqGabXLQ9GTinmyQHQyJ6TcfbHaTtJUFjHS962LFPdUwv3aDK673Pci2doTyHVTAsw4m5eToS2dKbtix9f7HNxwvixnbQucWNAWVAF6HTxFYRYmrRPDmeE8n7V1fXFkY7yvR6BWxKiWwHd8Vb1TbBBRStf5niRM2dUAyjJorTstPWSfG2pN5DsRF81NUd7Aif4EhNAQEJCTuAHxQ3rCnNkb9Pf7YTTxbt1t25YgDMioDi4uFhYcnTbHj7D74yNPC2Cfk6WasU69hMxj7Wxro58vtkA6hvDWGtnDyX4PzntBp3fn62R25HW2jadsZMiJpm5ufpYSktEFEHX6gGeF4KPgyU8b2hhyS3FKL4DULYLB6d6CZqUpwrJesGfDtFjfG1btbdmjd6Lm7FCbL3fU9E3AJWEmnFkg16vARiQ1CrzeS9SyNtybKCk4",
  "service": [
    {
      "id": "#didcomm",
      "recipientKeys": [
        "#1"
      ],
      "serviceEndpoint": "http://172.17.0.1:9031/a2a/5b6dyY6PndLaCnWxZbeEYW/5b6dyY6PndLaCnWxZbeEYW/2f6aae0c-6b04-40ff-a25e-faecaea39f83",
      "type": "did-communication"
    }
  ],
  "verificationMethod": [
    {
      "controller": "did:peer:4zQmRMVzDUXhV64pfw3vFaDvyExjzW9oBXCF2n4zYCaHQFAT:zMx3zwMnDECV3GiFs8nmHr38TziMEEkcgFBEDH5PXQ8hxnMrwNfB9wTwskpJMjggeg8NF1jeDSK5772op2zLLdy8TGFCEiYQxpUvvku8qSCZx5Q8V9Li9mDp6WEqGabXLQ9GTinmyQHQyJ6TcfbHaTtJUFjHS962LFPdUwv3aDK673Pci2doTyHVTAsw4m5eToS2dKbtix9f7HNxwvixnbQucWNAWVAF6HTxFYRYmrRPDmeE8n7V1fXFkY7yvR6BWxKiWwHd8Vb1TbBBRStf5niRM2dUAyjJorTstPWSfG2pN5DsRF81NUd7Aif4EhNAQEJCTuAHxQ3rCnNkb9Pf7YTTxbt1t25YgDMioDi4uFhYcnTbHj7D74yNPC2Cfk6WasU69hMxj7Wxro58vtkA6hvDWGtnDyX4PzntBp3fn62R25HW2jadsZMiJpm5ufpYSktEFEHX6gGeF4KPgyU8b2hhyS3FKL4DULYLB6d6CZqUpwrJesGfDtFjfG1btbdmjd6Lm7FCbL3fU9E3AJWEmnFkg16vARiQ1CrzeS9SyNtybKCk4",
      "id": "#1",
      "publicKeyBase58": "3dtu2WWtd5ELwRTJEPzmEJUYEp8Qq36N2QA24g9tFXK9",
      "type": "Ed25519VerificationKey2018"
    }
  ]
}
```

Resolved Document, Short Form:
```
{
  "@context": "https://w3id.org/did/v1",
  "alsoKnownAs": [
    "did:peer:4zQmRMVzDUXhV64pfw3vFaDvyExjzW9oBXCF2n4zYCaHQFAT:zMx3zwMnDECV3GiFs8nmHr38TziMEEkcgFBEDH5PXQ8hxnMrwNfB9wTwskpJMjggeg8NF1jeDSK5772op2zLLdy8TGFCEiYQxpUvvku8qSCZx5Q8V9Li9mDp6WEqGabXLQ9GTinmyQHQyJ6TcfbHaTtJUFjHS962LFPdUwv3aDK673Pci2doTyHVTAsw4m5eToS2dKbtix9f7HNxwvixnbQucWNAWVAF6HTxFYRYmrRPDmeE8n7V1fXFkY7yvR6BWxKiWwHd8Vb1TbBBRStf5niRM2dUAyjJorTstPWSfG2pN5DsRF81NUd7Aif4EhNAQEJCTuAHxQ3rCnNkb9Pf7YTTxbt1t25YgDMioDi4uFhYcnTbHj7D74yNPC2Cfk6WasU69hMxj7Wxro58vtkA6hvDWGtnDyX4PzntBp3fn62R25HW2jadsZMiJpm5ufpYSktEFEHX6gGeF4KPgyU8b2hhyS3FKL4DULYLB6d6CZqUpwrJesGfDtFjfG1btbdmjd6Lm7FCbL3fU9E3AJWEmnFkg16vARiQ1CrzeS9SyNtybKCk4"
  ],
  "authentication": [
    "#1"
  ],
  "id": "did:peer:4zQmRMVzDUXhV64pfw3vFaDvyExjzW9oBXCF2n4zYCaHQFAT",
  "service": [
    {
      "id": "#didcomm",
      "recipientKeys": [
        "#1"
      ],
      "serviceEndpoint": "http://172.17.0.1:9031/a2a/5b6dyY6PndLaCnWxZbeEYW/5b6dyY6PndLaCnWxZbeEYW/2f6aae0c-6b04-40ff-a25e-faecaea39f83",
      "type": "did-communication"
    }
  ],
  "verificationMethod": [
    {
      "controller": "did:peer:4zQmRMVzDUXhV64pfw3vFaDvyExjzW9oBXCF2n4zYCaHQFAT",
      "id": "#1",
      "publicKeyBase58": "3dtu2WWtd5ELwRTJEPzmEJUYEp8Qq36N2QA24g9tFXK9",
      "type": "Ed25519VerificationKey2018"
    }
  ]
}
```

#### Example 3

Input Document:
```
{
  "@context": "https://w3id.org/did/v1",
  "authentication": [
    {
      "id": "#key-1",
      "publicKeyMultibase": "z6MkqRYqQiSgvZQdnBytw86Qbs2ZWUkGv22od935YF4s8M7V",
      "type": "Ed25519VerificationKey2020"
    },
    {
      "id": "#key-2",
      "publicKeyMultibase": "z6MkgoLTnTypo3tDRwCkZXSccTPHRLhF4ZnjhueYAFpEX6vg",
      "type": "Ed25519VerificationKey2020"
    }
  ],
  "keyAgreement": [
    {
      "id": "#key-3",
      "publicKeyMultibase": "z6LSbysY2xFMRpGMhb7tFTLMpeuPRaqaWM1yECx2AtzE3KCc",
      "type": "X25519KeyAgreementKey2020"
    }
  ],
  "service": [
    {
      "accept": [
        "didcomm/v2",
        "didcomm/aip2;env=rfc587"
      ],
      "id": "#didcommmessaging-0",
      "routingKeys": [
        "did:example:somemediator#somekey"
      ],
      "serviceEndpoint": "https://example.com/endpoint",
      "type": "DIDCommMessaging"
    }
  ]
}
```

Long Form DID:
```
did:peer:4zQmVHkQgf9eJFjYCr2RPsraFeXpp3rAUnf2CKbAZn4GUqfk:zDixcnMB2dFazLTgmYwi6fRLSDSRJETgb755Zd65vq7tvYiaXbSW2GXhkyuapJ2SHQ2LgGjZcMaVunPoW4JrDvRHb2YJqvMtGQZX1mVWPjXMUVjKS9qXyQpcy58d1BhavareJAEBk4uCemXymN4xz26usDiH14FGsVjZMsmzTnbVhDFwxTxSoJskoVtEDSUEbayUBo1EFU6bvdR8r8nSXfuXXjtHNMQGQyF4ooWrxfAHmcFNFpb7c8d3J7gvMNnWSNE7LZkjUr5byEmUTqsnhY1U4xuuQ1pd428xjN6a8ZMjmz9eC8jpxwvZdB4Gf6TZGDmVDBzGHLSoVN7mg5aWwybBJHAU9HL36DUgGjTD64Z192qJpdEaK6iArFDDF5HVWpwa2nL4xZtAAMSEWorBqGpVKATmpVCK6h1GwJSMiSnZpU5xBurAuJq4174KCZUgMnZyrkrjcpAZLgtvw2yWKXAaHJXazVR3AW1zgjTyPnFdP67LRJtKUZTm4z9rRchjb9Y6No5ArcJ5SHH6P4pR2snmTG7aPpPtyp4WguxGnRuEdRyVd3iHijRK3LCx69bnPgVGapZjdnXNT7no5X386c1H132BNZwTAAabFRwBVyHKL8bHqz87iu6h4unwwXeLmC2quMnqUXnEaaWqYPQsNZzSZyASGnzARHHJPn69Uv86whwD2i1vBtGmSATXpmJ6kSyx8WJUWEcsr4AcLHqsgdsrWD5pZk14FmDL8jfxyYK3cV4oSi2NhHrjgnH8DDBzkicrDTG1cWDjs67E4z5hxf4eHJLpS9C834KXHE4LiG79eDYXSgXfKAwkJjdoggDb4WPrqrnZ3pCShvMJxvvU8zDa3jFhZ25KKzgbrdriwW8P15tfebgvEyAo33Rv1Z187Xa3PsBNmoK2
```

Short Form DID: `did:peer:4zQmVHkQgf9eJFjYCr2RPsraFeXpp3rAUnf2CKbAZn4GUqfk`

Resolved Document, Long Form:
```
{
  "@context": "https://w3id.org/did/v1",
  "alsoKnownAs": [
    "did:peer:4zQmVHkQgf9eJFjYCr2RPsraFeXpp3rAUnf2CKbAZn4GUqfk"
  ],
  "authentication": [
    {
      "controller": "did:peer:4zQmVHkQgf9eJFjYCr2RPsraFeXpp3rAUnf2CKbAZn4GUqfk:zDixcnMB2dFazLTgmYwi6fRLSDSRJETgb755Zd65vq7tvYiaXbSW2GXhkyuapJ2SHQ2LgGjZcMaVunPoW4JrDvRHb2YJqvMtGQZX1mVWPjXMUVjKS9qXyQpcy58d1BhavareJAEBk4uCemXymN4xz26usDiH14FGsVjZMsmzTnbVhDFwxTxSoJskoVtEDSUEbayUBo1EFU6bvdR8r8nSXfuXXjtHNMQGQyF4ooWrxfAHmcFNFpb7c8d3J7gvMNnWSNE7LZkjUr5byEmUTqsnhY1U4xuuQ1pd428xjN6a8ZMjmz9eC8jpxwvZdB4Gf6TZGDmVDBzGHLSoVN7mg5aWwybBJHAU9HL36DUgGjTD64Z192qJpdEaK6iArFDDF5HVWpwa2nL4xZtAAMSEWorBqGpVKATmpVCK6h1GwJSMiSnZpU5xBurAuJq4174KCZUgMnZyrkrjcpAZLgtvw2yWKXAaHJXazVR3AW1zgjTyPnFdP67LRJtKUZTm4z9rRchjb9Y6No5ArcJ5SHH6P4pR2snmTG7aPpPtyp4WguxGnRuEdRyVd3iHijRK3LCx69bnPgVGapZjdnXNT7no5X386c1H132BNZwTAAabFRwBVyHKL8bHqz87iu6h4unwwXeLmC2quMnqUXnEaaWqYPQsNZzSZyASGnzARHHJPn69Uv86whwD2i1vBtGmSATXpmJ6kSyx8WJUWEcsr4AcLHqsgdsrWD5pZk14FmDL8jfxyYK3cV4oSi2NhHrjgnH8DDBzkicrDTG1cWDjs67E4z5hxf4eHJLpS9C834KXHE4LiG79eDYXSgXfKAwkJjdoggDb4WPrqrnZ3pCShvMJxvvU8zDa3jFhZ25KKzgbrdriwW8P15tfebgvEyAo33Rv1Z187Xa3PsBNmoK2",
      "id": "#key-1",
      "publicKeyMultibase": "z6MkqRYqQiSgvZQdnBytw86Qbs2ZWUkGv22od935YF4s8M7V",
      "type": "Ed25519VerificationKey2020"
    },
    {
      "controller": "did:peer:4zQmVHkQgf9eJFjYCr2RPsraFeXpp3rAUnf2CKbAZn4GUqfk:zDixcnMB2dFazLTgmYwi6fRLSDSRJETgb755Zd65vq7tvYiaXbSW2GXhkyuapJ2SHQ2LgGjZcMaVunPoW4JrDvRHb2YJqvMtGQZX1mVWPjXMUVjKS9qXyQpcy58d1BhavareJAEBk4uCemXymN4xz26usDiH14FGsVjZMsmzTnbVhDFwxTxSoJskoVtEDSUEbayUBo1EFU6bvdR8r8nSXfuXXjtHNMQGQyF4ooWrxfAHmcFNFpb7c8d3J7gvMNnWSNE7LZkjUr5byEmUTqsnhY1U4xuuQ1pd428xjN6a8ZMjmz9eC8jpxwvZdB4Gf6TZGDmVDBzGHLSoVN7mg5aWwybBJHAU9HL36DUgGjTD64Z192qJpdEaK6iArFDDF5HVWpwa2nL4xZtAAMSEWorBqGpVKATmpVCK6h1GwJSMiSnZpU5xBurAuJq4174KCZUgMnZyrkrjcpAZLgtvw2yWKXAaHJXazVR3AW1zgjTyPnFdP67LRJtKUZTm4z9rRchjb9Y6No5ArcJ5SHH6P4pR2snmTG7aPpPtyp4WguxGnRuEdRyVd3iHijRK3LCx69bnPgVGapZjdnXNT7no5X386c1H132BNZwTAAabFRwBVyHKL8bHqz87iu6h4unwwXeLmC2quMnqUXnEaaWqYPQsNZzSZyASGnzARHHJPn69Uv86whwD2i1vBtGmSATXpmJ6kSyx8WJUWEcsr4AcLHqsgdsrWD5pZk14FmDL8jfxyYK3cV4oSi2NhHrjgnH8DDBzkicrDTG1cWDjs67E4z5hxf4eHJLpS9C834KXHE4LiG79eDYXSgXfKAwkJjdoggDb4WPrqrnZ3pCShvMJxvvU8zDa3jFhZ25KKzgbrdriwW8P15tfebgvEyAo33Rv1Z187Xa3PsBNmoK2",
      "id": "#key-2",
      "publicKeyMultibase": "z6MkgoLTnTypo3tDRwCkZXSccTPHRLhF4ZnjhueYAFpEX6vg",
      "type": "Ed25519VerificationKey2020"
    }
  ],
  "id": "did:peer:4zQmVHkQgf9eJFjYCr2RPsraFeXpp3rAUnf2CKbAZn4GUqfk:zDixcnMB2dFazLTgmYwi6fRLSDSRJETgb755Zd65vq7tvYiaXbSW2GXhkyuapJ2SHQ2LgGjZcMaVunPoW4JrDvRHb2YJqvMtGQZX1mVWPjXMUVjKS9qXyQpcy58d1BhavareJAEBk4uCemXymN4xz26usDiH14FGsVjZMsmzTnbVhDFwxTxSoJskoVtEDSUEbayUBo1EFU6bvdR8r8nSXfuXXjtHNMQGQyF4ooWrxfAHmcFNFpb7c8d3J7gvMNnWSNE7LZkjUr5byEmUTqsnhY1U4xuuQ1pd428xjN6a8ZMjmz9eC8jpxwvZdB4Gf6TZGDmVDBzGHLSoVN7mg5aWwybBJHAU9HL36DUgGjTD64Z192qJpdEaK6iArFDDF5HVWpwa2nL4xZtAAMSEWorBqGpVKATmpVCK6h1GwJSMiSnZpU5xBurAuJq4174KCZUgMnZyrkrjcpAZLgtvw2yWKXAaHJXazVR3AW1zgjTyPnFdP67LRJtKUZTm4z9rRchjb9Y6No5ArcJ5SHH6P4pR2snmTG7aPpPtyp4WguxGnRuEdRyVd3iHijRK3LCx69bnPgVGapZjdnXNT7no5X386c1H132BNZwTAAabFRwBVyHKL8bHqz87iu6h4unwwXeLmC2quMnqUXnEaaWqYPQsNZzSZyASGnzARHHJPn69Uv86whwD2i1vBtGmSATXpmJ6kSyx8WJUWEcsr4AcLHqsgdsrWD5pZk14FmDL8jfxyYK3cV4oSi2NhHrjgnH8DDBzkicrDTG1cWDjs67E4z5hxf4eHJLpS9C834KXHE4LiG79eDYXSgXfKAwkJjdoggDb4WPrqrnZ3pCShvMJxvvU8zDa3jFhZ25KKzgbrdriwW8P15tfebgvEyAo33Rv1Z187Xa3PsBNmoK2",
  "keyAgreement": [
    {
      "controller": "did:peer:4zQmVHkQgf9eJFjYCr2RPsraFeXpp3rAUnf2CKbAZn4GUqfk:zDixcnMB2dFazLTgmYwi6fRLSDSRJETgb755Zd65vq7tvYiaXbSW2GXhkyuapJ2SHQ2LgGjZcMaVunPoW4JrDvRHb2YJqvMtGQZX1mVWPjXMUVjKS9qXyQpcy58d1BhavareJAEBk4uCemXymN4xz26usDiH14FGsVjZMsmzTnbVhDFwxTxSoJskoVtEDSUEbayUBo1EFU6bvdR8r8nSXfuXXjtHNMQGQyF4ooWrxfAHmcFNFpb7c8d3J7gvMNnWSNE7LZkjUr5byEmUTqsnhY1U4xuuQ1pd428xjN6a8ZMjmz9eC8jpxwvZdB4Gf6TZGDmVDBzGHLSoVN7mg5aWwybBJHAU9HL36DUgGjTD64Z192qJpdEaK6iArFDDF5HVWpwa2nL4xZtAAMSEWorBqGpVKATmpVCK6h1GwJSMiSnZpU5xBurAuJq4174KCZUgMnZyrkrjcpAZLgtvw2yWKXAaHJXazVR3AW1zgjTyPnFdP67LRJtKUZTm4z9rRchjb9Y6No5ArcJ5SHH6P4pR2snmTG7aPpPtyp4WguxGnRuEdRyVd3iHijRK3LCx69bnPgVGapZjdnXNT7no5X386c1H132BNZwTAAabFRwBVyHKL8bHqz87iu6h4unwwXeLmC2quMnqUXnEaaWqYPQsNZzSZyASGnzARHHJPn69Uv86whwD2i1vBtGmSATXpmJ6kSyx8WJUWEcsr4AcLHqsgdsrWD5pZk14FmDL8jfxyYK3cV4oSi2NhHrjgnH8DDBzkicrDTG1cWDjs67E4z5hxf4eHJLpS9C834KXHE4LiG79eDYXSgXfKAwkJjdoggDb4WPrqrnZ3pCShvMJxvvU8zDa3jFhZ25KKzgbrdriwW8P15tfebgvEyAo33Rv1Z187Xa3PsBNmoK2",
      "id": "#key-3",
      "publicKeyMultibase": "z6LSbysY2xFMRpGMhb7tFTLMpeuPRaqaWM1yECx2AtzE3KCc",
      "type": "X25519KeyAgreementKey2020"
    }
  ],
  "service": [
    {
      "accept": [
        "didcomm/v2",
        "didcomm/aip2;env=rfc587"
      ],
      "id": "#didcommmessaging-0",
      "routingKeys": [
        "did:example:somemediator#somekey"
      ],
      "serviceEndpoint": "https://example.com/endpoint",
      "type": "DIDCommMessaging"
    }
  ]
}
```

Resolved Document, Short Form:
```
{
  "@context": "https://w3id.org/did/v1",
  "alsoKnownAs": [
    "did:peer:4zQmVHkQgf9eJFjYCr2RPsraFeXpp3rAUnf2CKbAZn4GUqfk:zDixcnMB2dFazLTgmYwi6fRLSDSRJETgb755Zd65vq7tvYiaXbSW2GXhkyuapJ2SHQ2LgGjZcMaVunPoW4JrDvRHb2YJqvMtGQZX1mVWPjXMUVjKS9qXyQpcy58d1BhavareJAEBk4uCemXymN4xz26usDiH14FGsVjZMsmzTnbVhDFwxTxSoJskoVtEDSUEbayUBo1EFU6bvdR8r8nSXfuXXjtHNMQGQyF4ooWrxfAHmcFNFpb7c8d3J7gvMNnWSNE7LZkjUr5byEmUTqsnhY1U4xuuQ1pd428xjN6a8ZMjmz9eC8jpxwvZdB4Gf6TZGDmVDBzGHLSoVN7mg5aWwybBJHAU9HL36DUgGjTD64Z192qJpdEaK6iArFDDF5HVWpwa2nL4xZtAAMSEWorBqGpVKATmpVCK6h1GwJSMiSnZpU5xBurAuJq4174KCZUgMnZyrkrjcpAZLgtvw2yWKXAaHJXazVR3AW1zgjTyPnFdP67LRJtKUZTm4z9rRchjb9Y6No5ArcJ5SHH6P4pR2snmTG7aPpPtyp4WguxGnRuEdRyVd3iHijRK3LCx69bnPgVGapZjdnXNT7no5X386c1H132BNZwTAAabFRwBVyHKL8bHqz87iu6h4unwwXeLmC2quMnqUXnEaaWqYPQsNZzSZyASGnzARHHJPn69Uv86whwD2i1vBtGmSATXpmJ6kSyx8WJUWEcsr4AcLHqsgdsrWD5pZk14FmDL8jfxyYK3cV4oSi2NhHrjgnH8DDBzkicrDTG1cWDjs67E4z5hxf4eHJLpS9C834KXHE4LiG79eDYXSgXfKAwkJjdoggDb4WPrqrnZ3pCShvMJxvvU8zDa3jFhZ25KKzgbrdriwW8P15tfebgvEyAo33Rv1Z187Xa3PsBNmoK2"
  ],
  "authentication": [
    {
      "controller": "did:peer:4zQmVHkQgf9eJFjYCr2RPsraFeXpp3rAUnf2CKbAZn4GUqfk",
      "id": "#key-1",
      "publicKeyMultibase": "z6MkqRYqQiSgvZQdnBytw86Qbs2ZWUkGv22od935YF4s8M7V",
      "type": "Ed25519VerificationKey2020"
    },
    {
      "controller": "did:peer:4zQmVHkQgf9eJFjYCr2RPsraFeXpp3rAUnf2CKbAZn4GUqfk",
      "id": "#key-2",
      "publicKeyMultibase": "z6MkgoLTnTypo3tDRwCkZXSccTPHRLhF4ZnjhueYAFpEX6vg",
      "type": "Ed25519VerificationKey2020"
    }
  ],
  "id": "did:peer:4zQmVHkQgf9eJFjYCr2RPsraFeXpp3rAUnf2CKbAZn4GUqfk",
  "keyAgreement": [
    {
      "controller": "did:peer:4zQmVHkQgf9eJFjYCr2RPsraFeXpp3rAUnf2CKbAZn4GUqfk",
      "id": "#key-3",
      "publicKeyMultibase": "z6LSbysY2xFMRpGMhb7tFTLMpeuPRaqaWM1yECx2AtzE3KCc",
      "type": "X25519KeyAgreementKey2020"
    }
  ],
  "service": [
    {
      "accept": [
        "didcomm/v2",
        "didcomm/aip2;env=rfc587"
      ],
      "id": "#didcommmessaging-0",
      "routingKeys": [
        "did:example:somemediator#somekey"
      ],
      "serviceEndpoint": "https://example.com/endpoint",
      "type": "DIDCommMessaging"
    }
  ]
}
```

#### Example 4
Input Document:

```
{
  "@context": [
    "https://w3.org/ns/did/v1",
    "https://w3id.org/security/suites/ed25519-2018/v1"
  ],
  "assertionMethod": [
    "#z6MkrmNwty5ajKtFqc1U48oL2MMLjWjartwc5sf2AihZwXDN"
  ],
  "authentication": [
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
      "publicKeyBase58": "CaSHXEvLKS6SfN9aBfkVGBpp15jSnaHazqHgLHp8KZ3Y",
      "type": "X25519KeyAgreementKey2019"
    }
  ],
  "publicKey": [
    {
      "id": "#z6MkrmNwty5ajKtFqc1U48oL2MMLjWjartwc5sf2AihZwXDN",
      "publicKeyBase58": "DK7uJiq9PnPnj7AmNZqVBFoLuwTjT1hFPrk6LSjZ2JRz",
      "type": "Ed25519VerificationKey2018"
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
```
{
  "@context": [
    "https://w3.org/ns/did/v1",
    "https://w3id.org/security/suites/ed25519-2018/v1"
  ],
  "alsoKnownAs": [
    "did:peer:4zQmTtzjstZ5p2Li62vbqPTgHBbdQM7QE5BvcKAme4t3HHPU"
  ],
  "assertionMethod": [
    "#z6MkrmNwty5ajKtFqc1U48oL2MMLjWjartwc5sf2AihZwXDN"
  ],
  "authentication": [
    "#z6MkrmNwty5ajKtFqc1U48oL2MMLjWjartwc5sf2AihZwXDN"
  ],
  "capabilityDelegation": [
    "#z6MkrmNwty5ajKtFqc1U48oL2MMLjWjartwc5sf2AihZwXDN"
  ],
  "capabilityInvocation": [
    "#z6MkrmNwty5ajKtFqc1U48oL2MMLjWjartwc5sf2AihZwXDN"
  ],
  "id": "did:peer:4zQmTtzjstZ5p2Li62vbqPTgHBbdQM7QE5BvcKAme4t3HHPU:z2EH35ZPdC1CKXQ9hyy8oW5Jst9UVnvgwDSLyCzCK2V8zMDsKe2RD8n7GRtE25KJyYcCM4vrahEMfEVpEcAVFZrecQc8suE6SX5fAc581n8DBiifrA94GtsC1gsgLxoNMgbpNzm2Ezys92DvCgDdtT83FZj99jRQnB7fgApfd98GniT7vtyMY27QuVETYgBReAxM3KkruT4pcJXK5Co5F273u4kYzVh6kjZnjZdjJiQbzPQEBq2VwdLft1uZbEfSEbZsvpkR4nQLowGfhSvWUK8gyDHFFPtdUCqV8k2qL7VqK7KweWiEn1DZbSkVV6LV3FBi9hdKEoVu64p4JofiDWy4WgGLtPmEdVVn2C7n2n5Qpfouha4PX3BpBDWiUFXeoWeEthtpBbtdujEXpN5DnqhBNLwgQMFg3ec9cHGai2PCcFtnkLpSjEeGnTnfQAiUEowneupmC39zqRxaHgnd9gSFGPjyJ5yUwsBuWdvbYyv4xMNf5wN32pzgQuHw56hnA6xqpccqhkZxPPmjN4Kf3muRmragcTMgAGvgpUPuLpiUnoqXW6gHqohKs19thSzEAxtCYVahQ3hZPdSYBQKBo5gJVxULyL2DAaWkEzkrrbpVzA2fZ52CJm7JcWcn75Aenf49SdTgXRaYf8dKFN5t1UqsuSWhkoJmiziYMrRYQZkRFizGxs6p8HrfWmqQeq9DhC2mLd6TXQkAxYpaW28RB7xXaGwPRpFpCfeaZAFwSNfzSoT8Kee52Sow5UMANTN9FfNzPJYeQBrBq6GGN6ayLm3KJbqQeZrRcuomYy58pqJ71P1JwymdDVNMe328EMD6UczfJPnTDPH3DeenJwTSdDRuDStJDAn3BWujigjJVAHMnXeMcG63obbFMc4XTsSt9W8bKTs72CpffzB6RsZQyL5UooRBGEj1Y5xHhYjdQAtE6uix2Xg5Dp3NPwUirQ8UsU2Sw95bYr8GZFr6dAHwo8pcmF9WNWihnWMEnbzFnBZqVNAUJ6G",
  "keyAgreement": [
    {
      "controller": "did:peer:4zQmTtzjstZ5p2Li62vbqPTgHBbdQM7QE5BvcKAme4t3HHPU:z2EH35ZPdC1CKXQ9hyy8oW5Jst9UVnvgwDSLyCzCK2V8zMDsKe2RD8n7GRtE25KJyYcCM4vrahEMfEVpEcAVFZrecQc8suE6SX5fAc581n8DBiifrA94GtsC1gsgLxoNMgbpNzm2Ezys92DvCgDdtT83FZj99jRQnB7fgApfd98GniT7vtyMY27QuVETYgBReAxM3KkruT4pcJXK5Co5F273u4kYzVh6kjZnjZdjJiQbzPQEBq2VwdLft1uZbEfSEbZsvpkR4nQLowGfhSvWUK8gyDHFFPtdUCqV8k2qL7VqK7KweWiEn1DZbSkVV6LV3FBi9hdKEoVu64p4JofiDWy4WgGLtPmEdVVn2C7n2n5Qpfouha4PX3BpBDWiUFXeoWeEthtpBbtdujEXpN5DnqhBNLwgQMFg3ec9cHGai2PCcFtnkLpSjEeGnTnfQAiUEowneupmC39zqRxaHgnd9gSFGPjyJ5yUwsBuWdvbYyv4xMNf5wN32pzgQuHw56hnA6xqpccqhkZxPPmjN4Kf3muRmragcTMgAGvgpUPuLpiUnoqXW6gHqohKs19thSzEAxtCYVahQ3hZPdSYBQKBo5gJVxULyL2DAaWkEzkrrbpVzA2fZ52CJm7JcWcn75Aenf49SdTgXRaYf8dKFN5t1UqsuSWhkoJmiziYMrRYQZkRFizGxs6p8HrfWmqQeq9DhC2mLd6TXQkAxYpaW28RB7xXaGwPRpFpCfeaZAFwSNfzSoT8Kee52Sow5UMANTN9FfNzPJYeQBrBq6GGN6ayLm3KJbqQeZrRcuomYy58pqJ71P1JwymdDVNMe328EMD6UczfJPnTDPH3DeenJwTSdDRuDStJDAn3BWujigjJVAHMnXeMcG63obbFMc4XTsSt9W8bKTs72CpffzB6RsZQyL5UooRBGEj1Y5xHhYjdQAtE6uix2Xg5Dp3NPwUirQ8UsU2Sw95bYr8GZFr6dAHwo8pcmF9WNWihnWMEnbzFnBZqVNAUJ6G",
      "id": "#zC8GybikEfyNaausDA4mkT4egP7SNLx2T1d1kujLQbcP6h",
      "publicKeyBase58": "CaSHXEvLKS6SfN9aBfkVGBpp15jSnaHazqHgLHp8KZ3Y",
      "type": "X25519KeyAgreementKey2019"
    }
  ],
  "publicKey": [
    {
      "id": "#z6MkrmNwty5ajKtFqc1U48oL2MMLjWjartwc5sf2AihZwXDN",
      "publicKeyBase58": "DK7uJiq9PnPnj7AmNZqVBFoLuwTjT1hFPrk6LSjZ2JRz",
      "type": "Ed25519VerificationKey2018"
    }
  ]
}
```

Resolved Document, Short Form:
```
{
  "@context": [
    "https://w3.org/ns/did/v1",
    "https://w3id.org/security/suites/ed25519-2018/v1"
  ],
  "alsoKnownAs": [
    "did:peer:4zQmTtzjstZ5p2Li62vbqPTgHBbdQM7QE5BvcKAme4t3HHPU:z2EH35ZPdC1CKXQ9hyy8oW5Jst9UVnvgwDSLyCzCK2V8zMDsKe2RD8n7GRtE25KJyYcCM4vrahEMfEVpEcAVFZrecQc8suE6SX5fAc581n8DBiifrA94GtsC1gsgLxoNMgbpNzm2Ezys92DvCgDdtT83FZj99jRQnB7fgApfd98GniT7vtyMY27QuVETYgBReAxM3KkruT4pcJXK5Co5F273u4kYzVh6kjZnjZdjJiQbzPQEBq2VwdLft1uZbEfSEbZsvpkR4nQLowGfhSvWUK8gyDHFFPtdUCqV8k2qL7VqK7KweWiEn1DZbSkVV6LV3FBi9hdKEoVu64p4JofiDWy4WgGLtPmEdVVn2C7n2n5Qpfouha4PX3BpBDWiUFXeoWeEthtpBbtdujEXpN5DnqhBNLwgQMFg3ec9cHGai2PCcFtnkLpSjEeGnTnfQAiUEowneupmC39zqRxaHgnd9gSFGPjyJ5yUwsBuWdvbYyv4xMNf5wN32pzgQuHw56hnA6xqpccqhkZxPPmjN4Kf3muRmragcTMgAGvgpUPuLpiUnoqXW6gHqohKs19thSzEAxtCYVahQ3hZPdSYBQKBo5gJVxULyL2DAaWkEzkrrbpVzA2fZ52CJm7JcWcn75Aenf49SdTgXRaYf8dKFN5t1UqsuSWhkoJmiziYMrRYQZkRFizGxs6p8HrfWmqQeq9DhC2mLd6TXQkAxYpaW28RB7xXaGwPRpFpCfeaZAFwSNfzSoT8Kee52Sow5UMANTN9FfNzPJYeQBrBq6GGN6ayLm3KJbqQeZrRcuomYy58pqJ71P1JwymdDVNMe328EMD6UczfJPnTDPH3DeenJwTSdDRuDStJDAn3BWujigjJVAHMnXeMcG63obbFMc4XTsSt9W8bKTs72CpffzB6RsZQyL5UooRBGEj1Y5xHhYjdQAtE6uix2Xg5Dp3NPwUirQ8UsU2Sw95bYr8GZFr6dAHwo8pcmF9WNWihnWMEnbzFnBZqVNAUJ6G"
  ],
  "assertionMethod": [
    "#z6MkrmNwty5ajKtFqc1U48oL2MMLjWjartwc5sf2AihZwXDN"
  ],
  "authentication": [
    "#z6MkrmNwty5ajKtFqc1U48oL2MMLjWjartwc5sf2AihZwXDN"
  ],
  "capabilityDelegation": [
    "#z6MkrmNwty5ajKtFqc1U48oL2MMLjWjartwc5sf2AihZwXDN"
  ],
  "capabilityInvocation": [
    "#z6MkrmNwty5ajKtFqc1U48oL2MMLjWjartwc5sf2AihZwXDN"
  ],
  "id": "did:peer:4zQmTtzjstZ5p2Li62vbqPTgHBbdQM7QE5BvcKAme4t3HHPU",
  "keyAgreement": [
    {
      "controller": "did:peer:4zQmTtzjstZ5p2Li62vbqPTgHBbdQM7QE5BvcKAme4t3HHPU",
      "id": "#zC8GybikEfyNaausDA4mkT4egP7SNLx2T1d1kujLQbcP6h",
      "publicKeyBase58": "CaSHXEvLKS6SfN9aBfkVGBpp15jSnaHazqHgLHp8KZ3Y",
      "type": "X25519KeyAgreementKey2019"
    }
  ],
  "publicKey": [
    {
      "id": "#z6MkrmNwty5ajKtFqc1U48oL2MMLjWjartwc5sf2AihZwXDN",
      "publicKeyBase58": "DK7uJiq9PnPnj7AmNZqVBFoLuwTjT1hFPrk6LSjZ2JRz",
      "type": "Ed25519VerificationKey2018"
    }
  ]
}
```

#### Example 5

Input Document:
```
{
  "@context": [
    "https://www.w3.org/ns/did/v1"
  ],
  "assertionMethod": [
    "#z6MkjvBkt8ETnxXGBFPSGgYKb43q7oNHLX8BiYSPcXVG6gY6"
  ],
  "authentication": [
    "#z6MkjvBkt8ETnxXGBFPSGgYKb43q7oNHLX8BiYSPcXVG6gY6"
  ],
  "verificationMethod": [
    {
      "id": "#z6MkjvBkt8ETnxXGBFPSGgYKb43q7oNHLX8BiYSPcXVG6gY6",
      "publicKeyJwk": {
        "crv": "Ed25519",
        "kty": "OKP",
        "x": "UTBElpNSZB8dS_R9rzWnWB-ozdtL7Sz96RQZhwnzur8"
      },
      "type": "Ed25519VerificationKey2018"
    }
  ]
}
```

Long Form DID:
```
did:peer:4zQmb5cH6UdXeQze2CkPM1FjLP3Yi6SHPHQKPq5wjeS3YiUt:z3AFKXqX5u3s7opYvAJuaLXm4vjXWp67LDGCq83dHQJ9KRRDdPYyAwMA2CXmbFT12ZFD8iAKrd9pdbERrB7KyyAvQ2fikaprHyV8ekiys1DfCd7VTWhM5zNfZY9grWGC8qvJ4qguDNaHwrvwFoWz3gEP52kt1KiY7WAgUvzkck1ikaQNDT21rSomYWLYDovJUkbvnnV13RRbbcz8GJWT5cRnacvVcXrGVTTZHiUcgw2yma2t9T1dBExetW73cobAmrAH2kU2ZsazkbMxchMen2Jf327E9AckTHt7CGcDKU2HZ442v6cRhr76LXxbmEnXqDQ92fjuZ7iPEJhVCWF6XRB2ZvMkoh6i5Gt3T9fP4cznKXLCJ8ucbE62Kp4fqMpdNs8yd6wWmr4hzxeJnN8qV1xNJ5oCF8KvV8DeRTXmcs2nfk7BTV8AijCf1CEoLvTtFWEkG7XrK3dJH1r4hJPfUAEiX17GXFyRdz4NjdKV4XHFsmYEAkwW1NJzDVoJtWdnjMRj4F2obmEkBHD6F8uPhef7RGs8HHM6Lc1XTz6g
```

Short Form DID: `did:peer:4zQmb5cH6UdXeQze2CkPM1FjLP3Yi6SHPHQKPq5wjeS3YiUt`

Resolved Document, Long Form:
```
{
  "@context": [
    "https://www.w3.org/ns/did/v1"
  ],
  "alsoKnownAs": [
    "did:peer:4zQmb5cH6UdXeQze2CkPM1FjLP3Yi6SHPHQKPq5wjeS3YiUt"
  ],
  "assertionMethod": [
    "#z6MkjvBkt8ETnxXGBFPSGgYKb43q7oNHLX8BiYSPcXVG6gY6"
  ],
  "authentication": [
    "#z6MkjvBkt8ETnxXGBFPSGgYKb43q7oNHLX8BiYSPcXVG6gY6"
  ],
  "id": "did:peer:4zQmb5cH6UdXeQze2CkPM1FjLP3Yi6SHPHQKPq5wjeS3YiUt:z3AFKXqX5u3s7opYvAJuaLXm4vjXWp67LDGCq83dHQJ9KRRDdPYyAwMA2CXmbFT12ZFD8iAKrd9pdbERrB7KyyAvQ2fikaprHyV8ekiys1DfCd7VTWhM5zNfZY9grWGC8qvJ4qguDNaHwrvwFoWz3gEP52kt1KiY7WAgUvzkck1ikaQNDT21rSomYWLYDovJUkbvnnV13RRbbcz8GJWT5cRnacvVcXrGVTTZHiUcgw2yma2t9T1dBExetW73cobAmrAH2kU2ZsazkbMxchMen2Jf327E9AckTHt7CGcDKU2HZ442v6cRhr76LXxbmEnXqDQ92fjuZ7iPEJhVCWF6XRB2ZvMkoh6i5Gt3T9fP4cznKXLCJ8ucbE62Kp4fqMpdNs8yd6wWmr4hzxeJnN8qV1xNJ5oCF8KvV8DeRTXmcs2nfk7BTV8AijCf1CEoLvTtFWEkG7XrK3dJH1r4hJPfUAEiX17GXFyRdz4NjdKV4XHFsmYEAkwW1NJzDVoJtWdnjMRj4F2obmEkBHD6F8uPhef7RGs8HHM6Lc1XTz6g",
  "verificationMethod": [
    {
      "controller": "did:peer:4zQmb5cH6UdXeQze2CkPM1FjLP3Yi6SHPHQKPq5wjeS3YiUt:z3AFKXqX5u3s7opYvAJuaLXm4vjXWp67LDGCq83dHQJ9KRRDdPYyAwMA2CXmbFT12ZFD8iAKrd9pdbERrB7KyyAvQ2fikaprHyV8ekiys1DfCd7VTWhM5zNfZY9grWGC8qvJ4qguDNaHwrvwFoWz3gEP52kt1KiY7WAgUvzkck1ikaQNDT21rSomYWLYDovJUkbvnnV13RRbbcz8GJWT5cRnacvVcXrGVTTZHiUcgw2yma2t9T1dBExetW73cobAmrAH2kU2ZsazkbMxchMen2Jf327E9AckTHt7CGcDKU2HZ442v6cRhr76LXxbmEnXqDQ92fjuZ7iPEJhVCWF6XRB2ZvMkoh6i5Gt3T9fP4cznKXLCJ8ucbE62Kp4fqMpdNs8yd6wWmr4hzxeJnN8qV1xNJ5oCF8KvV8DeRTXmcs2nfk7BTV8AijCf1CEoLvTtFWEkG7XrK3dJH1r4hJPfUAEiX17GXFyRdz4NjdKV4XHFsmYEAkwW1NJzDVoJtWdnjMRj4F2obmEkBHD6F8uPhef7RGs8HHM6Lc1XTz6g",
      "id": "#z6MkjvBkt8ETnxXGBFPSGgYKb43q7oNHLX8BiYSPcXVG6gY6",
      "publicKeyJwk": {
        "crv": "Ed25519",
        "kty": "OKP",
        "x": "UTBElpNSZB8dS_R9rzWnWB-ozdtL7Sz96RQZhwnzur8"
      },
      "type": "Ed25519VerificationKey2018"
    }
  ]
}
```

Resolved Document, Short Form:
```
{
  "@context": [
    "https://www.w3.org/ns/did/v1"
  ],
  "alsoKnownAs": [
    "did:peer:4zQmb5cH6UdXeQze2CkPM1FjLP3Yi6SHPHQKPq5wjeS3YiUt:z3AFKXqX5u3s7opYvAJuaLXm4vjXWp67LDGCq83dHQJ9KRRDdPYyAwMA2CXmbFT12ZFD8iAKrd9pdbERrB7KyyAvQ2fikaprHyV8ekiys1DfCd7VTWhM5zNfZY9grWGC8qvJ4qguDNaHwrvwFoWz3gEP52kt1KiY7WAgUvzkck1ikaQNDT21rSomYWLYDovJUkbvnnV13RRbbcz8GJWT5cRnacvVcXrGVTTZHiUcgw2yma2t9T1dBExetW73cobAmrAH2kU2ZsazkbMxchMen2Jf327E9AckTHt7CGcDKU2HZ442v6cRhr76LXxbmEnXqDQ92fjuZ7iPEJhVCWF6XRB2ZvMkoh6i5Gt3T9fP4cznKXLCJ8ucbE62Kp4fqMpdNs8yd6wWmr4hzxeJnN8qV1xNJ5oCF8KvV8DeRTXmcs2nfk7BTV8AijCf1CEoLvTtFWEkG7XrK3dJH1r4hJPfUAEiX17GXFyRdz4NjdKV4XHFsmYEAkwW1NJzDVoJtWdnjMRj4F2obmEkBHD6F8uPhef7RGs8HHM6Lc1XTz6g"
  ],
  "assertionMethod": [
    "#z6MkjvBkt8ETnxXGBFPSGgYKb43q7oNHLX8BiYSPcXVG6gY6"
  ],
  "authentication": [
    "#z6MkjvBkt8ETnxXGBFPSGgYKb43q7oNHLX8BiYSPcXVG6gY6"
  ],
  "id": "did:peer:4zQmb5cH6UdXeQze2CkPM1FjLP3Yi6SHPHQKPq5wjeS3YiUt",
  "verificationMethod": [
    {
      "controller": "did:peer:4zQmb5cH6UdXeQze2CkPM1FjLP3Yi6SHPHQKPq5wjeS3YiUt",
      "id": "#z6MkjvBkt8ETnxXGBFPSGgYKb43q7oNHLX8BiYSPcXVG6gY6",
      "publicKeyJwk": {
        "crv": "Ed25519",
        "kty": "OKP",
        "x": "UTBElpNSZB8dS_R9rzWnWB-ozdtL7Sz96RQZhwnzur8"
      },
      "type": "Ed25519VerificationKey2018"
    }
  ]
}
```

#### Example 6

Input Document:
```
{
  "@context": [
    "https://www.w3.org/ns/did/v1",
    "https://w3id.org/security/suites/jws-2020/v1"
  ],
  "assertionMethod": [
    "#key-1"
  ],
  "authentication": [
    "#key-1"
  ],
  "service": [],
  "verificationMethod": [
    {
      "id": "#key-1",
      "publicKeyJwk": {
        "crv": "secp256k1",
        "kid": "#keys-1",
        "kty": "EC",
        "x": "masUHNuJ0oH0C_e5rLUu5VKwmU2l-a7rrNTqA__afN8",
        "y": "UmGGX_WgRFXbw6qTli9xcQ0owtkZVuUGVyM23e8rZe8"
      },
      "type": "JsonWebKey2020"
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
```
{
  "@context": [
    "https://www.w3.org/ns/did/v1",
    "https://w3id.org/security/suites/jws-2020/v1"
  ],
  "alsoKnownAs": [
    "did:peer:4zQmYxyxu3ndxss6ZopgaRN7xfqrXVpUbLqJ5Qd9x8ov2HMo"
  ],
  "assertionMethod": [
    "#key-1"
  ],
  "authentication": [
    "#key-1"
  ],
  "id": "did:peer:4zQmYxyxu3ndxss6ZopgaRN7xfqrXVpUbLqJ5Qd9x8ov2HMo:z2LBoAcpyFY24cFmhR6v5E4cenhVk9os2NAz6b61FgJzvZTgjEncziY6EXJYv4hjHzke9AkCawZszR8QFYjHdf9xRk2qpqZN7tgkudQBTuZ7QNmmsfdJ9U6g2fcpoGqnqnKc3iqGqUXWWuUG4Y7wPVxFrkLAPA7jUDz6UFsLTcJ5vX5jVtdYeRBvKcMDH1pyKNSGQFzYAmXH5dnJTr6MTHf71RDicGZU2MkuLfUGzUJXHE3QEa5WJqE1WmF8mU5tUVr1ysKHxck97JdU35RBR96FG2UXqLSYcaALJZYXTRtu5q8ucwc5bb16T9sD2H4A3kZeStPs6zbHqq3uxM4En2ZwSjsRSgF8Fowkd6FpQpSRpf8MdmPchS5BZgSWTLmP2Z6T5vkgnab6KZgYsv4qvjBw9twBRBLdWRH7XeLAugb4jiEKwA3hMhmZeunGvUVbS4Q4rZ5FxW7mob2SYb7ncbDpsAMV2qFwMoua1ybbcwE1r1HYCCziLrmfe17GyNpwBdVhjdKvdwRxJFQPyHJon",
  "verificationMethod": [
    {
      "controller": "did:peer:4zQmYxyxu3ndxss6ZopgaRN7xfqrXVpUbLqJ5Qd9x8ov2HMo:z2LBoAcpyFY24cFmhR6v5E4cenhVk9os2NAz6b61FgJzvZTgjEncziY6EXJYv4hjHzke9AkCawZszR8QFYjHdf9xRk2qpqZN7tgkudQBTuZ7QNmmsfdJ9U6g2fcpoGqnqnKc3iqGqUXWWuUG4Y7wPVxFrkLAPA7jUDz6UFsLTcJ5vX5jVtdYeRBvKcMDH1pyKNSGQFzYAmXH5dnJTr6MTHf71RDicGZU2MkuLfUGzUJXHE3QEa5WJqE1WmF8mU5tUVr1ysKHxck97JdU35RBR96FG2UXqLSYcaALJZYXTRtu5q8ucwc5bb16T9sD2H4A3kZeStPs6zbHqq3uxM4En2ZwSjsRSgF8Fowkd6FpQpSRpf8MdmPchS5BZgSWTLmP2Z6T5vkgnab6KZgYsv4qvjBw9twBRBLdWRH7XeLAugb4jiEKwA3hMhmZeunGvUVbS4Q4rZ5FxW7mob2SYb7ncbDpsAMV2qFwMoua1ybbcwE1r1HYCCziLrmfe17GyNpwBdVhjdKvdwRxJFQPyHJon",
      "id": "#key-1",
      "publicKeyJwk": {
        "crv": "secp256k1",
        "kid": "#keys-1",
        "kty": "EC",
        "x": "masUHNuJ0oH0C_e5rLUu5VKwmU2l-a7rrNTqA__afN8",
        "y": "UmGGX_WgRFXbw6qTli9xcQ0owtkZVuUGVyM23e8rZe8"
      },
      "type": "JsonWebKey2020"
    }
  ]
}
```

Resolved Document, Short Form:
```
{
  "@context": [
    "https://www.w3.org/ns/did/v1",
    "https://w3id.org/security/suites/jws-2020/v1"
  ],
  "alsoKnownAs": [
    "did:peer:4zQmYxyxu3ndxss6ZopgaRN7xfqrXVpUbLqJ5Qd9x8ov2HMo:z2LBoAcpyFY24cFmhR6v5E4cenhVk9os2NAz6b61FgJzvZTgjEncziY6EXJYv4hjHzke9AkCawZszR8QFYjHdf9xRk2qpqZN7tgkudQBTuZ7QNmmsfdJ9U6g2fcpoGqnqnKc3iqGqUXWWuUG4Y7wPVxFrkLAPA7jUDz6UFsLTcJ5vX5jVtdYeRBvKcMDH1pyKNSGQFzYAmXH5dnJTr6MTHf71RDicGZU2MkuLfUGzUJXHE3QEa5WJqE1WmF8mU5tUVr1ysKHxck97JdU35RBR96FG2UXqLSYcaALJZYXTRtu5q8ucwc5bb16T9sD2H4A3kZeStPs6zbHqq3uxM4En2ZwSjsRSgF8Fowkd6FpQpSRpf8MdmPchS5BZgSWTLmP2Z6T5vkgnab6KZgYsv4qvjBw9twBRBLdWRH7XeLAugb4jiEKwA3hMhmZeunGvUVbS4Q4rZ5FxW7mob2SYb7ncbDpsAMV2qFwMoua1ybbcwE1r1HYCCziLrmfe17GyNpwBdVhjdKvdwRxJFQPyHJon"
  ],
  "assertionMethod": [
    "#key-1"
  ],
  "authentication": [
    "#key-1"
  ],
  "id": "did:peer:4zQmYxyxu3ndxss6ZopgaRN7xfqrXVpUbLqJ5Qd9x8ov2HMo",
  "verificationMethod": [
    {
      "controller": "did:peer:4zQmYxyxu3ndxss6ZopgaRN7xfqrXVpUbLqJ5Qd9x8ov2HMo",
      "id": "#key-1",
      "publicKeyJwk": {
        "crv": "secp256k1",
        "kid": "#keys-1",
        "kty": "EC",
        "x": "masUHNuJ0oH0C_e5rLUu5VKwmU2l-a7rrNTqA__afN8",
        "y": "UmGGX_WgRFXbw6qTli9xcQ0owtkZVuUGVyM23e8rZe8"
      },
      "type": "JsonWebKey2020"
    }
  ]
}
```
