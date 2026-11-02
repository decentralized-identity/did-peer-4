import { existsSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));

function firstExistingDir(candidates: string[]): string {
  for (const dir of candidates) {
    if (existsSync(dir)) {
      return dir;
    }
  }
  throw new Error(
    `No did:peer:4 example fixtures found. Tried:\n${candidates
      .map((d) => `  - ${d}`)
      .join(
        "\n"
      )}\nSet DID_PEER_4_EXAMPLES_DIR to tests/examples (DIF clone) or use the layout in contrib/README.`
  );
}

/**
 * Shared JSON examples for cross-language tests.
 *
 * | Layout | Examples path |
 * |--------|----------------|
 * | DIF repo (`typescript/tests/`) | `../../tests/examples` |
 * | pico-engine nested (`contrib/.../typescript/tests/`) | `../../tests/fixtures/examples` (parent `tests/`) |
 * | pico-engine flat (`contrib/.../tests/`) | `./fixtures/examples` |
 */
export function examplesDir(): string {
  if (process.env.DID_PEER_4_EXAMPLES_DIR) {
    return process.env.DID_PEER_4_EXAMPLES_DIR;
  }
  return firstExistingDir([
    path.resolve(here, "../../tests/examples"),
    path.resolve(here, "../../tests/fixtures/examples"),
    path.join(here, "fixtures/examples"),
  ]);
}

export function vectorsDir(): string {
  return path.join(here, "fixtures/vectors");
}
