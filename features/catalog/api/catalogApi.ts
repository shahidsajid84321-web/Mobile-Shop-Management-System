import { apiFetch } from "../../../lib/api";
import type { ApiResponse, PaginatedResponse } from "../../../shared/types/api";

export type Category = { id:number; name:string; description:string|null };
export type Product = { id:number; name:string; brand:string; model_number:string|null; sku:string; barcode:string|null; description:string|null; purchase_price:string; selling_price:string; stock_quantity:number; minimum_stock:number; image:string|null; is_active:boolean; category_id:number };
export const catalogApi = {
  categories: (page=1,pageSize=10) => apiFetch<ApiResponse<PaginatedResponse<Category>>>(`/categories/?page=${page}&page_size=${pageSize}`,{},true),
  category: (id:number) => apiFetch<ApiResponse<Category>>(`/categories/${id}`,{},true),
  createCategory: (body:object) => apiFetch<ApiResponse<Category>>("/categories/",{method:"POST",body:JSON.stringify(body)},true),
  updateCategory: (id:number,body:object) => apiFetch<ApiResponse<Category>>(`/categories/${id}`,{method:"PUT",body:JSON.stringify(body)},true),
  deleteCategory: (id:number) => apiFetch<ApiResponse<null>>(`/categories/${id}`,{method:"DELETE"},true),
  products: (page=1,pageSize=10) => apiFetch<ApiResponse<PaginatedResponse<Product>>>(`/products/?page=${page}&page_size=${pageSize}`,{},true),
  product: (id:number) => apiFetch<ApiResponse<Product>>(`/products/${id}`,{},true),
  createProduct: (body:object) => apiFetch<ApiResponse<Product>>("/products/",{method:"POST",body:JSON.stringify(body)},true),
  updateProduct: (id:number,body:object) => apiFetch<ApiResponse<Product>>(`/products/${id}`,{method:"PUT",body:JSON.stringify(body)},true),
  deleteProduct: (id:number) => apiFetch<ApiResponse<null>>(`/products/${id}`,{method:"DELETE"},true),
  uploadImage: (file:File) => { const form = new FormData(); form.append("file",file); return apiFetch<{message:string;image:string}>("/upload/product-image",{method:"POST",body:form},true); },
};
