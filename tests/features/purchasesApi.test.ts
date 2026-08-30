import { expect, it, vi } from "vitest"; import { purchaseApi } from "../../features/purchases/api/purchaseApi"; import { apiFetch } from "../../lib/api";
vi.mock("../../lib/api",()=>({apiFetch:vi.fn()}));
it("covers purchase list/get/create",async()=>{const m=vi.mocked(apiFetch);m.mockResolvedValue({});await purchaseApi.list(2);await purchaseApi.get(5);await purchaseApi.create({supplier_id:1,items:[]});expect(m).toHaveBeenCalledWith("/purchases/5",{},true);});
