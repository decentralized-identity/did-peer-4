# Tests

| File | Covers |
|------|--------|
| `vectors.test.ts` | Shared JSON vectors (`fixtures/vectors/`) — hello-world + DIF `test_did_peer_4.py` DOC |
| `examples.test.ts` | All `tests/examples/*.json` (DIF repo) or vendored `fixtures/examples/` |

**Fixture resolution:** `fixturesPath.ts`

- In **DIF repo:** `../../tests/examples` (shared with Python)
- In **pico-engine contrib:** `fixtures/examples/` (vendored copy; see README there)
- Override: `DID_PEER_4_EXAMPLES_DIR`

**Not ported (Python-only helpers):** `test_input_doc.py`, `validate_input_document` in `test_valid.py`.

Run from `contrib/did-peer-4-typescript/`:

```bash
npm test
```
