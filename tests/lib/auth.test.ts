import { describe, expect, it, beforeEach } from "vitest";
import { getToken, isLoggedIn, removeToken, saveToken } from "../../lib/auth";

function installStorage() {
  const store = new Map<string, string>();
  (globalThis as any).window = { localStorage: {
    setItem: (k: string, v: string) => store.set(k, v),
    getItem: (k: string) => store.get(k) ?? null,
    removeItem: (k: string) => store.delete(k),
  }};
}

describe("auth token storage", () => {
  beforeEach(installStorage);
  it("saves and reads the access token", () => {
    saveToken("abc");
    expect(getToken()).toBe("abc");
    expect(isLoggedIn()).toBe(true);
  });
  it("removes the access token", () => {
    saveToken("abc"); removeToken();
    expect(getToken()).toBeNull();
    expect(isLoggedIn()).toBe(false);
  });
});
