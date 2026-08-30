import { expect, it, vi } from "vitest"; import { supplierApi } from "../../features/suppliers/api/supplierApi"; import { apiFetch } from "../../lib/api";
vi.mock("../../lib/api",()=>({apiFetch:vi.fn()}));
it("covers supplier CRUD",async()=>{const m=vi.mocked(apiFetch);m.mockResolvedValue({});await supplierApi.list(2);await supplierApi.get(4);await supplierApi.create({company_name:"ABC"});await supplierApi.update(4,{is_active:false});await supplierApi.remove(4);expect(m).toHaveBeenCalledTimes(5);});
