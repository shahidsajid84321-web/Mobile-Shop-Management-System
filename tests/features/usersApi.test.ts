import { expect, it, vi } from "vitest"; import { userApi } from "../../features/users/api/userApi"; import { apiFetch } from "../../lib/api";
vi.mock("../../lib/api",()=>({apiFetch:vi.fn()}));
it("covers user CRUD and role lookup",async()=>{const m=vi.mocked(apiFetch);m.mockResolvedValue({});await userApi.list(2);await userApi.get(4);await userApi.create({full_name:"Admin",role_id:1});await userApi.update(4,{is_active:false});await userApi.remove(4);await userApi.roles();expect(m).toHaveBeenCalledTimes(6);});
