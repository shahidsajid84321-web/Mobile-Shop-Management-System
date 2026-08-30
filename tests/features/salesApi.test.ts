import { expect, it, vi } from "vitest"; import { saleApi } from "../../features/sales/api/saleApi"; import { apiFetch } from "../../lib/api";
vi.mock("../../lib/api",()=>({apiFetch:vi.fn()}));
it("covers sale list/get/create",async()=>{const m=vi.mocked(apiFetch);m.mockResolvedValue({});await saleApi.list(2);await saleApi.get(5);await saleApi.create({customer_id:1,items:[]});expect(m).toHaveBeenCalledWith("/sales/5",{},true);});
