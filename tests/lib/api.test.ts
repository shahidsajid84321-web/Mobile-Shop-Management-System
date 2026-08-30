import { describe, expect, it, beforeEach, vi } from "vitest";
import { apiFetch, mediaUrl } from "../../lib/api";

function installStorage(token = "test-token") {
  const store = new Map([["mobile_shop_access_token", token]]);
  (globalThis as any).window = { localStorage: {
    setItem: (k: string, v: string) => store.set(k, v),
    getItem: (k: string) => store.get(k) ?? null,
    removeItem: (k: string) => store.delete(k),
  }};
}

describe("apiFetch", () => {
  beforeEach(() => { vi.restoreAllMocks(); installStorage(); });
  it("adds bearer token and JSON content type", async () => {
    const fetchMock = vi.spyOn(globalThis, "fetch").mockResolvedValue(new Response(JSON.stringify({ ok: true }), { status: 200 }));
    await apiFetch("/products", { method: "POST", body: JSON.stringify({ name: "Phone" }) }, true);
    const req = fetchMock.mock.calls[0][1] as RequestInit;
    expect((req.headers as Headers).get("Authorization")).toBe("Bearer test-token");
    expect((req.headers as Headers).get("Content-Type")).toBe("application/json");
  });
  it("throws API detail on non-2xx responses", async () => {
    vi.spyOn(globalThis, "fetch").mockResolvedValue(new Response(JSON.stringify({ detail: "Unauthorized" }), { status: 401 }));
    await expect(apiFetch("/private", {}, false)).rejects.toThrow("Unauthorized");
  });
  it("refreshes once after a 401 and retries the request", async () => {
    const fetchMock = vi.spyOn(globalThis, "fetch")
      .mockResolvedValueOnce(new Response(JSON.stringify({ detail: "expired" }), { status: 401 }))
      .mockResolvedValueOnce(new Response(JSON.stringify({ access_token: "new-token" }), { status: 200 }))
      .mockResolvedValueOnce(new Response(JSON.stringify({ data: 123 }), { status: 200 }));
    const result = await apiFetch<{data:number}>("/dashboard/", {}, true);
    expect(result.data).toBe(123);
    expect(fetchMock).toHaveBeenCalledTimes(3);
  });
});

describe("mediaUrl", () => {
  it("handles empty paths and absolute URLs", () => {
    expect(mediaUrl(null)).toBeNull();
    expect(mediaUrl("https://cdn.example.com/a.jpg")).toBe("https://cdn.example.com/a.jpg");
  });
  it("builds upload URLs for relative paths", () => {
    expect(mediaUrl("/a.jpg")).toContain("/uploads/a.jpg");
  });
});
