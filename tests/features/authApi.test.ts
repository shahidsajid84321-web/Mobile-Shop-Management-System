import { describe, expect, it, vi, beforeEach } from "vitest";
import { authApi } from "../../features/auth/api/authApi";
import { apiFetch } from "../../lib/api";
vi.mock("../../lib/api", () => ({ apiFetch: vi.fn() }));
const mock = vi.mocked(apiFetch);

describe("authApi", () => {
  beforeEach(() => mock.mockResolvedValue({ message: "ok" }));
  it("covers registration, login, refresh and logout", async () => {
    await authApi.register({ full_name: "Ali Khan", email: "ali@example.com", password: "StrongPass123" });
    expect(mock).toHaveBeenCalledWith("/store/register", expect.objectContaining({method:"POST"}));
    await authApi.login("a@example.com", "Password123");
    expect(mock).toHaveBeenCalledWith("/auth/login", expect.objectContaining({method:"POST", body: JSON.stringify({email:"a@example.com",password:"Password123"})}));
    await authApi.refresh(); expect(mock).toHaveBeenCalledWith("/auth/refresh", {method:"POST"});
    await authApi.logout(); expect(mock).toHaveBeenCalledWith("/auth/logout", {method:"POST"});
  });
  it("covers verification and password reset flows", async () => {
    await authApi.verifyEmail("x".repeat(20));
    await authApi.resendVerification("a@example.com");
    await authApi.requestPasswordReset("a@example.com");
    await authApi.confirmPasswordReset("x".repeat(20), "NewPassword123");
    expect(mock).toHaveBeenCalledTimes(4);
  });
});
