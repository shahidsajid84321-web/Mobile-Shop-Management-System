import {apiFetch} from "../../../lib/api"; import type {ApiResponse,PaginatedResponse} from "../../../shared/types/api";
export type Payment={id:number;sale_id:number;amount:string;payment_method:string;payment_date:string;reference_number:string|null;remarks:string|null};
export const paymentApi={list:(p=1)=>apiFetch<ApiResponse<PaginatedResponse<Payment>>>(`/payments/?page=${p}&page_size=10`,{},true),get:(id:number)=>apiFetch<ApiResponse<Payment>>(`/payments/${id}`,{},true),create:(b:object)=>apiFetch<ApiResponse<Payment>>("/payments/",{method:"POST",body:JSON.stringify(b)},true)};
