import assert from "node:assert/strict";
import { test } from "node:test";
import {
  assertApiDeploymentConfig,
  browserWorkerUrl,
  type Config,
  shadowedEnvKeys,
} from "../apps/server/src/config.ts";

const sampleConfig: Config = {
  mode: "sample",
  port: 8787,
  host: "127.0.0.1",
  publicUrl: "http://localhost:8787",
  dataDir: ".openmuse",
  agentBackend: "sample",
  googleRedirectUri: "http://localhost:8787/api/google/callback",
  allowedOrigins: ["http://localhost:8081"],
};

function liveConfig(intelligenceApiKey?: string): Config {
  return {
    ...sampleConfig,
    mode: "live",
    agentBackend: "model",
    intelligenceApiKey,
  };
}

// NEREUS persists threads in its own store (PostgreSQL / PGlite) through the
// SSE-mode runner, so the closed CopilotKit Intelligence key is OPTIONAL. The
// deployment guard now only checks the public URL.
test("deployment config no longer requires the closed Intelligence key", () => {
  for (const mode of [sampleConfig, liveConfig()]) {
    for (const key of [undefined, "", " \t\n", "cpk-test-key"]) {
      assert.doesNotThrow(() => assertApiDeploymentConfig({ ...mode, intelligenceApiKey: key }));
    }
  }
});

test("deployment config still rejects a missing public URL", () => {
  assert.throws(() => assertApiDeploymentConfig({ ...sampleConfig, publicUrl: "" }), {
    name: "Error",
    message: "PUBLIC_API_URL must be set",
  });
});

test("Jev mode is off by default and validates explicit modes", async () => {
  const { readConfig } = await import("../apps/server/src/config.ts");
  const old = {
    JEV_MODE: process.env.JEV_MODE,
    TYPESAFE_API_KEY: process.env.TYPESAFE_API_KEY,
    CPK_INTELLIGENCE_API_KEY: process.env.CPK_INTELLIGENCE_API_KEY,
  };
  try {
    delete process.env.CPK_INTELLIGENCE_API_KEY;
    delete process.env.JEV_MODE;
    assert.equal(readConfig().jevMode, "off");
    process.env.JEV_MODE = "sample";
    assert.equal(readConfig().jevMode, "sample");
    process.env.JEV_MODE = "live";
    delete process.env.TYPESAFE_API_KEY;
    assert.throws(() => readConfig(), /TYPESAFE_API_KEY/);
    process.env.TYPESAFE_API_KEY = "fixture-key";
    assert.equal(readConfig().typesafeApiKey, "fixture-key");
    process.env.JEV_MODE = "invalid";
    assert.throws(() => readConfig(), /JEV_MODE/);
  } finally {
    for (const [key, value] of Object.entries(old)) {
      if (value === undefined) delete process.env[key];
      else process.env[key] = value;
    }
  }
});

test("browser worker URL keeps an existing scheme and adds http to host:port", () => {
  assert.equal(browserWorkerUrl(undefined), undefined);
  assert.equal(browserWorkerUrl("  "), undefined);
  assert.equal(browserWorkerUrl("http://127.0.0.1:8790"), "http://127.0.0.1:8790");
  assert.equal(browserWorkerUrl("https://browser.internal:8790"), "https://browser.internal:8790");
  assert.equal(browserWorkerUrl("openmuse-browser-h4fx:8790"), "http://openmuse-browser-h4fx:8790");
});

test("environment variables that override a different .env value are reported by name", () => {
  const file = { OPENAI_API_KEY: "sk-or-file", MODEL: "openai/gpt-5", PORT: "8787", EMPTY: "" };
  const env = { OPENAI_API_KEY: "sk-or-env", MODEL: "openai/gpt-5", EMPTY: "set" };
  assert.deepEqual(shadowedEnvKeys(file, env), ["OPENAI_API_KEY", "EMPTY"]);
  assert.deepEqual(shadowedEnvKeys(file, {}), []);
});
