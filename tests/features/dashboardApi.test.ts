import { expect, it, vi } from "vitest"; import { dashboardApi } from "../../features/dashboard/api/dashboardApi"; import { apiFetch } from "../../lib/api";
vi.mock("../../lib/api",()=>({apiFetch:vi.fn()}));
it("gets dashboard summary",async()=>{const m=vi.mocked(apiFetch);m.mockResolvedValue({});await dashboardApi.get();expect(m).toHaveBeenCalledWith("/dashboard/",{},true);});
