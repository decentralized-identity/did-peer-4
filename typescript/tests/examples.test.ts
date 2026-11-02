import { readdirSync, readFileSync } from "node:fs";
import path from "node:path";
import { describe, expect, it } from "vitest";
import { decode, encode, encodeShort, longToShort } from "../src/index.js";
import { examplesDir } from "./fixturesPath.js";

/** Parity with Python `tests/test_valid.py` encode path (validate_input_document not ported to TS). */
describe("DIF tests/examples/*.json", () => {
  const dir = examplesDir();
  const files = readdirSync(dir)
    .filter((f) => f.endsWith(".json"))
    .sort();

  it("loads example fixtures", () => {
    expect(files.length).toBeGreaterThan(0);
  });

  for (const file of files) {
    it(`${file} encodes and decodes`, () => {
      const doc = JSON.parse(
        readFileSync(path.join(dir, file), "utf8")
      ) as Record<string, unknown>;
      const long = encode(doc);
      expect(decode(long)).toEqual(doc);
      expect(encodeShort(doc)).toBe(longToShort(long));
    });
  }
});
