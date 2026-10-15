# did-peer-4 TypeScript — upstream PR scaffold

Working copy for a contribution to [`decentralized-identity/did-peer-4`](https://github.com/decentralized-identity/did-peer-4).

**Not built or published from pico-engine.** Source of truth for production today:
`packages/pico-engine/src/identity/peerDid4.ts`.

## Prepare PR

Maintainer approved layout in [did-peer-4#11](https://github.com/decentralized-identity/did-peer-4/issues/11).

1. Follow [`PR-SUBMIT.md`](./PR-SUBMIT.md) (fork, rsync → `typescript/`, DCO commit, `gh pr create`)
2. Sync `src/peerDid4.ts` from `packages/pico-engine/src/identity/peerDid4.ts` if drifted before copy
3. `npm test` — vectors + all DIF `tests/examples/*.json` encode/decode roundtrips

Full checklist: [`docs/contributing/did-peer-4-upstream.md`](../../docs/contributing/did-peer-4-upstream.md)

## Local dev (scaffold)

```bash
cd contrib/did-peer-4-typescript
npm install
npm test
npm run build
```
