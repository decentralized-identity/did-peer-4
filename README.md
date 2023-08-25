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

Take an Input Document like the following:

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

To construct the short form, simple omit the `:{{encoded document}}` from the end.

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
3. Add `alsoKnownAs` at the root of the document and set it to a list of length one with the short form of the DID
4. For each verification method (declared in the `verificationMethod` section or embedded in a verification relationship like `authentication`):
    - If `controller` is not set, set `controller` to the DID
5. Optionally, for other relative references in the document, make them absolute by prepending the reference with the DID.
    - This is not required because relative references are valid within DID Documents and are understood to refer to the current document

Here is an example long from DID Document (all relative references replaced with absolute references):

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
