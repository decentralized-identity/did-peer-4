import { readFileSync } from "node:fs";
import path from "node:path";
import { describe, expect, it } from "vitest";
import {
  decode,
  encode,
  encodeShort,
  longToShort,
  matches,
  resolve,
  resolveShort,
} from "../src/index.js";
import { vectorsDir } from "./fixturesPath.js";

interface VectorFile {
  description?: string;
  inputDocument: Record<string, unknown>;
  longForm?: string;
  shortForm?: string;
}

function loadVector(name: string): VectorFile {
  const raw = readFileSync(path.join(vectorsDir(), name), "utf8");
  return JSON.parse(raw) as VectorFile;
}

describe("hello-world vector (shared JSON)", () => {
  const v = loadVector("hello-world.json");

  it("encode matches known long form", () => {
    expect(encode(v.inputDocument)).toBe(v.longForm);
  });

  it("decode roundtrips", () => {
    expect(decode(v.longForm!)).toEqual(v.inputDocument);
  });

  it("short form matches encodeShort and longToShort", () => {
    const long = encode(v.inputDocument);
    expect(encodeShort(v.inputDocument)).toBe(v.shortForm);
    expect(longToShort(long)).toBe(v.shortForm);
  });

  it("resolve contextualizes id and alsoKnownAs", () => {
    const doc = resolve(v.longForm!);
    expect(doc.id).toBe(v.longForm);
    expect(doc.alsoKnownAs).toContain(v.shortForm);
  });

  it("resolveShort from long form", () => {
    const doc = resolveShort(v.longForm!);
    expect(doc.id).toBe(v.shortForm);
    expect(doc.alsoKnownAs).toContain(v.longForm);
  });

  it("matches short and long forms", () => {
    expect(matches(v.longForm!, v.shortForm!)).toBe(true);
    expect(matches(v.shortForm!, v.longForm!)).toBe(true);
  });
});

describe("DIF didcomm-keys doc vector", () => {
  const v = loadVector("didcomm-keys-doc.json");

  it("encode/decode roundtrip", () => {
    const long = encode(v.inputDocument);
    expect(decode(long)).toEqual(v.inputDocument);
    expect(encodeShort(v.inputDocument)).toBe(longToShort(long));
  });

  it("resolve sets controller on verification methods", () => {
    const long = encode(v.inputDocument);
    const doc = resolve(long);
    expect(doc.id).toBe(long);
    const vms = doc.verificationMethod as Array<{ controller?: string }>;
    expect(vms.every((vm) => vm.controller === long)).toBe(true);
  });
});
