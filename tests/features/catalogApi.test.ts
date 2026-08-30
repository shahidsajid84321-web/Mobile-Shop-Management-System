import { describe, expect, it, vi, beforeEach } from "vitest";
import { catalogApi } from "../../features/catalog/api/catalogApi";
import { apiFetch } from "../../lib/api";
vi.mock("../../lib/api", () => ({ apiFetch: vi.fn() })); const mock=vi.mocked(apiFetch);

describe("catalogApi",()=>{beforeEach(()=>mock.mockResolvedValue({}));
it("covers category CRUD",async()=>{await catalogApi.categories(2,25);await catalogApi.category(3);await catalogApi.createCategory({name:"Phones"});await catalogApi.updateCategory(3,{name:"Mobiles"});await catalogApi.deleteCategory(3);expect(mock).toHaveBeenCalledWith("/categories/?page=2&page_size=25",{},true);expect(mock).toHaveBeenCalledWith("/categories/3",{},true);});
it("covers product CRUD",async()=>{await catalogApi.products(2,20);await catalogApi.product(4);await catalogApi.createProduct({name:"Phone"});await catalogApi.updateProduct(4,{name:"New"});await catalogApi.deleteProduct(4);expect(mock).toHaveBeenCalledWith("/products/?page=2&page_size=20",{},true);});
it("uploads product image as multipart form",async()=>{const file=new File(["x"],"phone.jpg",{type:"image/jpeg"});await catalogApi.uploadImage(file);const call=mock.mock.calls[0];expect(call[0]).toBe("/upload/product-image");expect((call[1] as any).body).toBeInstanceOf(FormData);});});
