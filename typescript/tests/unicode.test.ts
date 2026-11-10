import { describe, expect, it } from "vitest";
import { decode, encode } from "../src/index.js";

/**
 * The embedded document is encoded as UTF-8 (matching the Python reference and
 * this library's own decoder). Non-ASCII content must survive a round-trip;
 * encoding it as latin1 silently corrupts multi-byte characters.
 */
describe("non-ASCII document round-trip", () => {
  const documents = [
    { service: "café" },
    { name: "你好" },
    { label: "🚀" },
    { alsoKnownAs: ["did:example:Ωmega"] },
  ];

  for (const document of documents) {
    it(`preserves ${JSON.stringify(document)} through encode/decode`, () => {
      expect(decode(encode(document))).toEqual(document);
    });
  }
});
