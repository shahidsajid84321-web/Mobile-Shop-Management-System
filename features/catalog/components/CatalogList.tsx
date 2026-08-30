"use client";
import Link from "next/link";
import { useEffect,useState } from "react";
import { catalogApi, type Category, type Product } from "../api/catalogApi";
import { AdminPage,PrimaryButton,TableCard } from "../../../shared/components/AdminShell";
import { ErrorState,LoadingState,EmptyState } from "../../../shared/components/PageState";
import { Pagination } from "../../../shared/components/Pagination";

export function ProductsList(){
 const [data,setData]=useState<Product[]>([]),[page,setPage]=useState(1),[pages,setPages]=useState(0),[loading,setLoading]=useState(true),[error,setError]=useState("");
 const load=()=>{setLoading(true);catalogApi.products(page,10).then(r=>{setData(r.data.items);setPages(r.data.pages)}).catch(e=>setError(e.message)).finally(()=>setLoading(false))}; useEffect(load,[page]);
 async function remove(id:number){if(!confirm("Delete this product?"))return;try{await catalogApi.deleteProduct(id);load()}catch(e){setError(e instanceof Error?e.message:"Delete failed")}}
 return <AdminPage title="Products" description="Manage the products already exposed by the backend." action={<PrimaryButton href="/dashboard/products/new">Add Product</PrimaryButton>}>{error&&<ErrorState message={error}/>} {loading?<LoadingState/>:data.length===0?<EmptyState title="No products found"/>:<TableCard><div className="overflow-x-auto"><table className="w-full text-left text-sm"><thead className="bg-slate-50 text-slate-500"><tr>{["Product","SKU","Category","Purchase","Selling","Stock","Status","Actions"].map(h=><th key={h} className="px-4 py-3 font-medium">{h}</th>)}</tr></thead><tbody className="divide-y">{data.map(p=><tr key={p.id}><td className="px-4 py-3"><div className="font-semibold">{p.name}</div><div className="text-xs text-slate-500">{p.brand}</div></td><td className="px-4 py-3">{p.sku}</td><td className="px-4 py-3">#{p.category_id}</td><td className="px-4 py-3">Rs. {p.purchase_price}</td><td className="px-4 py-3">Rs. {p.selling_price}</td><td className="px-4 py-3">{p.stock_quantity}</td><td className="px-4 py-3">{p.is_active?"Active":"Inactive"}</td><td className="px-4 py-3"><div className="flex gap-3"><Link className="font-medium" href={`/dashboard/products/${p.id}`}>Edit</Link><button className="font-medium text-red-600" onClick={()=>remove(p.id)}>Delete</button></div></td></tr>)}</tbody></table></div><Pagination page={page} pages={pages} onPage={setPage}/></TableCard>}</AdminPage>
}

export function CategoriesList(){
 const [data,setData]=useState<Category[]>([]),[page,setPage]=useState(1),[pages,setPages]=useState(0),[loading,setLoading]=useState(true),[error,setError]=useState("");
 const load=()=>{setLoading(true);catalogApi.categories(page,10).then(r=>{setData(r.data.items);setPages(r.data.pages)}).catch(e=>setError(e.message)).finally(()=>setLoading(false))}; useEffect(load,[page]);
 async function remove(id:number){if(!confirm("Delete this category?"))return;try{await catalogApi.deleteCategory(id);load()}catch(e){setError(e instanceof Error?e.message:"Delete failed")}}
 return <AdminPage title="Categories" description="Manage product categories." action={<PrimaryButton href="/dashboard/categories/new">Add Category</PrimaryButton>}>{error&&<ErrorState message={error}/>} {loading?<LoadingState/>:data.length===0?<EmptyState title="No categories found"/>:<TableCard><div className="overflow-x-auto"><table className="w-full text-left text-sm"><thead className="bg-slate-50"><tr><th className="px-4 py-3">Name</th><th className="px-4 py-3">Description</th><th className="px-4 py-3">Actions</th></tr></thead><tbody className="divide-y">{data.map(c=><tr key={c.id}><td className="px-4 py-3 font-semibold">{c.name}</td><td className="px-4 py-3 text-slate-500">{c.description||"—"}</td><td className="px-4 py-3"><div className="flex gap-3"><Link href={`/dashboard/categories/${c.id}`}>Edit</Link><button className="text-red-600" onClick={()=>remove(c.id)}>Delete</button></div></td></tr>)}</tbody></table></div><Pagination page={page} pages={pages} onPage={setPage}/></TableCard>}</AdminPage>
}
