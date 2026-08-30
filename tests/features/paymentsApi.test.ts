import { expect, it, vi } from "vitest"; import { paymentApi } from "../../features/payments/api/paymentApi"; import { apiFetch } from "../../lib/api";
vi.mock("../../lib/api",()=>({apiFetch:vi.fn()}));
it("covers payment list/get/create",async()=>{const m=vi.mocked(apiFetch);m.mockResolvedValue({});await paymentApi.list(2);await paymentApi.get(5);await paymentApi.create({sale_id:1,amount:"10"});expect(m).toHaveBeenCalledWith("/payments/5",{},true);});
