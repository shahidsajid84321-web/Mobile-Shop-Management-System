import { expect, it, vi } from "vitest"; import { inventoryApi } from "../../features/inventory/api/inventoryApi"; import { apiFetch } from "../../lib/api";
vi.mock("../../lib/api",()=>({apiFetch:vi.fn()}));
it("covers inventory list/create/product history",async()=>{const m=vi.mocked(apiFetch);m.mockResolvedValue({});await inventoryApi.list(2);await inventoryApi.create({product_id:1,transaction_type:"IN",quantity:2});await inventoryApi.product(1,3);expect(m).toHaveBeenCalledWith("/inventory/product/1?page=3&page_size=10",{},true);});
