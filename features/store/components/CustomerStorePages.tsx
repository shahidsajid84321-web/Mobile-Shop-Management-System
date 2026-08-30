"use client";
import {FormEvent,useEffect,useState} from "react"; import Link from "next/link"; import {useParams,useRouter} from "next/navigation"; import {apiFetch} from "../../../lib/api"; import {getToken} from "../../../lib/auth";
type CartItem={product_id:number;name:string;sku:string;quantity:number;unit_price:string;subtotal:string}; type Cart={items:CartItem[];subtotal:string;total_items?:number}; type OrderItem={product_id:number;product_name:string;sku:string;quantity:number;unit_price:string;subtotal:string}; type History={status:string;note:string|null;created_at:string}; type ReturnRequest={id:number;order_id:number;customer_id:number;status:string;reason:string;refund_amount:string;notes:string|null;created_at:string;resolved_at:string|null}; type Order={id:number;order_number:string;status:string;payment_status:string;payment_method:string;subtotal:string;discount:string;shipping_fee:string;total_amount:string;delivery_name:string;delivery_phone:string;delivery_address:string;delivery_city:string;tracking_number:string|null;notes:string|null;placed_at:string;items:OrderItem[];status_history:History[]}; type Api<T>={success:boolean;message:string;data:T};
const input="w-full rounded-lg border px-4 py-3";
export function CartPage(){const [cart,setCart]=useState<Cart|null>(null),[error,setError]=useState(""),[loading,setLoading]=useState(true);const load=()=>{if(!getToken()){setError("Please login to view your cart.");setLoading(false);return}apiFetch<Api<Cart>>("/store/cart",{},true).then(r=>setCart(r.data)).catch(e=>setError(e.message)).finally(()=>setLoading(false))};useEffect(load,[]);async function update(id:number,q:number){if(q<1)return;try{await apiFetch(`/store/cart/items/${id}`,{method:"PATCH",body:JSON.stringify({product_id:id,quantity:q})},true);load()}catch(e){setError(e instanceof Error?e.message:"Unable to update cart")}}async function remove(id:number){try{await apiFetch(`/store/cart/items/${id}`,{method:"DELETE"},true);load()}catch(e){setError(e instanceof Error?e.message:"Unable to remove item")}}if(loading)return <main className="mx-auto max-w-6xl p-8">Loading cart...</main>;if(error)return <main className="mx-auto max-w-6xl p-8"><div className="rounded-xl border bg-white p-8"><p className="text-red-600">{error}</p><Link href="/login" className="mt-5 inline-block rounded-lg bg-slate-900 px-5 py-3 text-white">Login</Link></div></main>;if(!cart||!cart.items.length)return <main className="mx-auto max-w-6xl p-8"><h1 className="text-3xl font-bold">Shopping Cart</h1><div className="mt-8 rounded-xl border bg-white p-10 text-center"><h2 className="text-xl font-semibold">Your cart is empty</h2><Link href="/products" className="mt-6 inline-block rounded-lg bg-slate-900 px-6 py-3 font-semibold text-white">Browse Products</Link></div></main>;return <main className="mx-auto max-w-6xl p-8"><div className="flex justify-between"><h1 className="text-3xl font-bold">Shopping Cart</h1><span className="text-slate-500">{cart.total_items??cart.items.reduce((n,i)=>n+i.quantity,0)} item(s)</span></div><div className="mt-8 grid gap-8 lg:grid-cols-3"><div className="space-y-4 lg:col-span-2">{cart.items.map(i=><div key={i.product_id} className="rounded-xl border bg-white p-5"><div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between"><div><h2 className="font-semibold">{i.name}</h2><p className="text-sm text-slate-500">SKU: {i.sku}</p><p className="mt-2">Rs. {i.unit_price}</p></div><div className="flex items-center gap-3"><button disabled={i.quantity<=1} onClick={()=>update(i.product_id,i.quantity-1)} className="h-9 w-9 rounded-lg border disabled:opacity-40">-</button><span>{i.quantity}</span><button onClick={()=>update(i.product_id,i.quantity+1)} className="h-9 w-9 rounded-lg border">+</button><button onClick={()=>remove(i.product_id)} className="ml-2 text-sm text-red-600">Remove</button></div></div><div className="mt-4 border-t pt-4 text-right font-bold">Rs. {i.subtotal}</div></div>)}</div><aside className="h-fit rounded-xl border bg-white p-6"><h2 className="text-xl font-semibold">Order Summary</h2><div className="mt-5 flex justify-between"><span>Subtotal</span><strong>Rs. {cart.subtotal}</strong></div><Link href="/checkout" className="mt-6 block rounded-lg bg-slate-900 px-5 py-3 text-center font-semibold text-white">Proceed to Checkout</Link></aside></div></main>}
export function CheckoutPage(){const router=useRouter();const [cart,setCart]=useState<Cart|null>(null),[error,setError]=useState(""),[saving,setSaving]=useState(false);const [form,setForm]=useState({delivery_name:"",delivery_phone:"",delivery_address:"",delivery_city:"",payment_method:"Cash on Delivery",shipping_fee:"250",notes:""});useEffect(()=>{if(!getToken()){router.push("/login");return}apiFetch<Api<Cart>>("/store/cart",{},true).then(r=>setCart(r.data)).catch(e=>setError(e.message))},[router]);const set=(k:string,v:string)=>setForm(x=>({...x,[k]:v}));async function submit(e:FormEvent){e.preventDefault();if(!cart?.items.length){setError("Your cart is empty.");return}try{setSaving(true);const fee=Number(form.shipping_fee);if(!Number.isFinite(fee)||fee<0)throw new Error("Shipping fee must be zero or greater.");const r=await apiFetch<Api<Order>>("/store/checkout",{method:"POST",body:JSON.stringify({...form,shipping_fee:fee})},true);router.push(`/orders/${r.data.id}`)}catch(e){setError(e instanceof Error?e.message:"Unable to place order")}finally{setSaving(false)}}if(!cart)return <main className="mx-auto max-w-6xl p-8">{error?<p className="text-red-600">{error}</p>:"Loading checkout..."}</main>;const total=Number(cart.subtotal)+(Number(form.shipping_fee)||0);return <main className="mx-auto max-w-6xl p-8"><h1 className="text-3xl font-bold">Checkout</h1><div className="mt-8 grid gap-8 lg:grid-cols-3"><form onSubmit={submit} className="space-y-5 lg:col-span-2"><section className="rounded-xl border bg-white p-6"><h2 className="text-xl font-semibold">Delivery Information</h2><div className="mt-5 grid gap-4 md:grid-cols-2"><input className={input} placeholder="Full name" value={form.delivery_name} onChange={e=>set("delivery_name",e.target.value)} required/><input className={input} placeholder="Phone" value={form.delivery_phone} onChange={e=>set("delivery_phone",e.target.value)} required/><input className={input} placeholder="City" value={form.delivery_city} onChange={e=>set("delivery_city",e.target.value)} required/><input className={input} type="number" min="0" step="0.01" placeholder="Shipping fee" value={form.shipping_fee} onChange={e=>set("shipping_fee",e.target.value)}/><textarea className={`${input} md:col-span-2`} rows={4} placeholder="Delivery address" value={form.delivery_address} onChange={e=>set("delivery_address",e.target.value)} required/><textarea className={`${input} md:col-span-2`} rows={3} placeholder="Order notes" value={form.notes} onChange={e=>set("notes",e.target.value)}/></div></section><section className="rounded-xl border bg-white p-6"><h2 className="text-xl font-semibold">Payment Method</h2><select className={`${input} mt-4`} value={form.payment_method} onChange={e=>set("payment_method",e.target.value)}><option>Cash on Delivery</option><option>Bank Transfer</option></select></section>{error&&<p className="rounded-lg bg-red-50 p-4 text-red-700">{error}</p>}<button disabled={saving} className="w-full rounded-lg bg-slate-900 px-6 py-4 font-semibold text-white disabled:opacity-50">{saving?"Placing Order...":`Place Order — Rs. ${total.toLocaleString()}`}</button></form><aside className="h-fit rounded-xl border bg-white p-6"><h2 className="text-xl font-semibold">Order Summary</h2><div className="mt-5 space-y-4">{cart.items.map(i=><div key={i.product_id} className="flex justify-between gap-4 text-sm"><span>{i.name} × {i.quantity}</span><strong>Rs. {i.subtotal}</strong></div>)}</div><div className="mt-5 space-y-2 border-t pt-4"><div className="flex justify-between"><span>Subtotal</span><span>Rs. {Number(cart.subtotal).toLocaleString()}</span></div><div className="flex justify-between"><span>Shipping</span><span>Rs. {(Number(form.shipping_fee)||0).toLocaleString()}</span></div><div className="flex justify-between border-t pt-3 text-lg font-bold"><span>Total</span><span>Rs. {total.toLocaleString()}</span></div></div></aside></div></main>}
export function OrdersPage(){const [orders,setOrders]=useState<Order[]>([]),[error,setError]=useState(""),[loading,setLoading]=useState(true);useEffect(()=>{if(!getToken()){setError("Please login to view your orders.");setLoading(false);return}apiFetch<Api<Order[]>>("/store/orders",{},true).then(r=>setOrders(r.data)).catch(e=>setError(e.message)).finally(()=>setLoading(false))},[]);if(loading)return <main className="mx-auto max-w-6xl p-8">Loading orders...</main>;if(error)return <main className="mx-auto max-w-6xl p-8"><p className="text-red-600">{error}</p><Link href="/login" className="mt-5 inline-block rounded-lg bg-slate-900 px-5 py-3 text-white">Login</Link></main>;return <main className="mx-auto max-w-6xl p-8"><div className="flex justify-between"><h1 className="text-3xl font-bold">My Orders</h1><Link href="/products" className="rounded-lg border px-4 py-2">Continue Shopping</Link></div>{orders.length===0?<div className="mt-8 rounded-xl border bg-white p-10 text-center"><h2 className="text-xl font-semibold">You have no orders yet.</h2><Link href="/products" className="mt-6 inline-block rounded-lg bg-slate-900 px-6 py-3 text-white">Browse Products</Link></div>:<div className="mt-8 space-y-4">{orders.map(o=><div key={o.id} className="rounded-xl border bg-white p-6"><div className="flex flex-col justify-between gap-3 sm:flex-row"><div><p className="text-sm text-slate-500">Order</p><h2 className="text-xl font-bold">{o.order_number}</h2><p className="text-xs text-slate-500">{new Date(o.placed_at).toLocaleString()}</p></div><div className="flex gap-2"><span className="rounded-full bg-slate-100 px-3 py-1 text-sm">{o.status}</span><span className="rounded-full bg-slate-100 px-3 py-1 text-sm">{o.payment_status}</span></div></div><div className="mt-5 grid gap-4 border-t pt-5 sm:grid-cols-3"><div><p className="text-xs text-slate-500">Payment</p><p>{o.payment_method}</p></div><div><p className="text-xs text-slate-500">Subtotal</p><p>Rs. {Number(o.subtotal).toLocaleString()}</p></div><div><p className="text-xs text-slate-500">Total</p><p className="font-bold">Rs. {Number(o.total_amount).toLocaleString()}</p></div></div><Link href={`/orders/${o.id}`} className="mt-5 inline-block rounded-lg bg-slate-900 px-5 py-3 text-white">View Order</Link></div>)}</div>}</main>}
export function OrderDetailPage(){const {id}=useParams<{id:string}>();const [o,setO]=useState<Order|null>(null),[error,setError]=useState("");useEffect(()=>{if(!id)return;if(!getToken()){setError("Please login to view this order.");return}apiFetch<Api<Order>>(`/store/orders/${id}`,{},true).then(r=>setO(r.data)).catch(e=>setError(e.message))},[id]);if(!o)return <main className="mx-auto max-w-5xl p-8">{error?<p className="text-red-600">{error}</p>:"Loading order..."}</main>;return <main className="mx-auto max-w-5xl p-8"><div className="flex flex-col justify-between gap-3 sm:flex-row"><div><p className="text-sm text-slate-500">{new Date(o.placed_at).toLocaleString()}</p><h1 className="text-3xl font-bold">Order {o.order_number}</h1></div><div className="flex gap-2"><span className="rounded-full bg-slate-100 px-3 py-1 text-sm">{o.status}</span><span className="rounded-full bg-slate-100 px-3 py-1 text-sm">{o.payment_status}</span></div></div><div className="mt-8 grid gap-8 lg:grid-cols-3"><section className="space-y-6 lg:col-span-2"><div className="rounded-xl border bg-white p-6"><h2 className="text-xl font-semibold">Order Items</h2><div className="mt-5 space-y-4">{o.items.map(i=><div key={i.product_id} className="flex justify-between border-b pb-4 last:border-0"><div><p className="font-semibold">{i.product_name}</p><p className="text-sm text-slate-500">{i.quantity} × Rs. {Number(i.unit_price).toLocaleString()}</p></div><strong>Rs. {Number(i.subtotal).toLocaleString()}</strong></div>)}</div></div><div className="rounded-xl border bg-white p-6"><h2 className="text-xl font-semibold">Order Status</h2><div className="mt-5 space-y-4">{o.status_history.map((h,i)=><div key={`${h.created_at}-${i}`} className="border-l-2 pl-4"><p className="font-semibold">{h.status}</p>{h.note&&<p className="text-sm text-slate-600">{h.note}</p>}<p className="text-xs text-slate-400">{new Date(h.created_at).toLocaleString()}</p></div>)}</div></div></section><aside className="space-y-6"><div className="rounded-xl border bg-white p-6"><h2 className="text-xl font-semibold">Delivery</h2><div className="mt-4 space-y-2 text-sm"><p>{o.delivery_name}</p><p>{o.delivery_phone}</p><p>{o.delivery_address}</p><p>{o.delivery_city}</p>{o.tracking_number&&<p>Tracking: {o.tracking_number}</p>}</div></div><div className="rounded-xl border bg-white p-6"><h2 className="text-xl font-semibold">Summary</h2><div className="mt-4 space-y-2"><div className="flex justify-between"><span>Subtotal</span><span>Rs. {Number(o.subtotal).toLocaleString()}</span></div><div className="flex justify-between"><span>Discount</span><span>Rs. {Number(o.discount).toLocaleString()}</span></div><div className="flex justify-between"><span>Shipping</span><span>Rs. {Number(o.shipping_fee).toLocaleString()}</span></div><div className="flex justify-between border-t pt-3 font-bold"><span>Total</span><span>Rs. {Number(o.total_amount).toLocaleString()}</span></div></div></div></aside></div><div className="mt-8 flex gap-3"><Link href="/orders" className="rounded-lg border px-5 py-3">My Orders</Link><Link href="/products" className="rounded-lg bg-slate-900 px-5 py-3 text-white">Continue Shopping</Link></div></main>}


export function ReturnsPage() {
  const router = useRouter();
  const [returns, setReturns] = useState<ReturnRequest[]>([]);
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");
  const [form, setForm] = useState({ order_id: "", reason: "", notes: "" });

  useEffect(() => {
    if (!getToken()) {
      router.push("/login");
      return;
    }

    Promise.all([
      apiFetch<Api<ReturnRequest[]>>("/store/returns", {}, true),
      apiFetch<Api<Order[]>>("/store/orders", {}, true),
    ])
      .then(([returnsResponse, ordersResponse]) => {
        setReturns(returnsResponse.data);
        setOrders(ordersResponse.data);
      })
      .catch((err) =>
        setError(err instanceof Error ? err.message : "Unable to load returns."),
      )
      .finally(() => setLoading(false));
  }, [router]);

  async function submit(event: FormEvent) {
    event.preventDefault();
    setError("");
    setMessage("");

    if (!form.order_id) {
      setError("Please select an order.");
      return;
    }

    try {
      setSubmitting(true);
      const response = await apiFetch<Api<ReturnRequest>>("/store/returns", {
        method: "POST",
        body: JSON.stringify({
          order_id: Number(form.order_id),
          reason: form.reason,
          notes: form.notes || null,
        }),
      }, true);

      setReturns((current) => [response.data, ...current]);
      setForm({ order_id: "", reason: "", notes: "" });
      setMessage("Return request submitted successfully.");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to submit return request.");
    } finally {
      setSubmitting(false);
    }
  }

  if (loading) {
    return <main className="mx-auto max-w-6xl p-8">Loading returns...</main>;
  }

  return (
    <main className="mx-auto max-w-6xl p-8">
      <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-center">
        <div>
          <h1 className="text-3xl font-bold">Returns</h1>
          <p className="mt-2 text-slate-500">
            Request and track returns for your delivered online orders.
          </p>
        </div>
        <Link href="/orders" className="rounded-lg border px-5 py-3 text-center">
          My Orders
        </Link>
      </div>

      {error && <p className="mt-6 rounded-lg bg-red-50 p-4 text-red-700">{error}</p>}
      {message && <p className="mt-6 rounded-lg bg-green-50 p-4 text-green-700">{message}</p>}

      <div className="mt-8 grid gap-8 lg:grid-cols-3">
        <section className="rounded-xl border bg-white p-6 lg:col-span-1">
          <h2 className="text-xl font-semibold">Request a Return</h2>
          <form onSubmit={submit} className="mt-5 space-y-4">
            <select
              className={input}
              value={form.order_id}
              onChange={(event) =>
                setForm((current) => ({ ...current, order_id: event.target.value }))
              }
              required
            >
              <option value="">Select delivered order</option>
              {orders
                .filter((order) => order.status === "Delivered")
                .map((order) => (
                  <option key={order.id} value={order.id}>
                    {order.order_number} — Rs. {Number(order.total_amount).toLocaleString()}
                  </option>
                ))}
            </select>

            <textarea
              className={input}
              rows={5}
              minLength={5}
              maxLength={500}
              placeholder="Reason for return"
              value={form.reason}
              onChange={(event) =>
                setForm((current) => ({ ...current, reason: event.target.value }))
              }
              required
            />

            <textarea
              className={input}
              rows={3}
              maxLength={500}
              placeholder="Additional notes (optional)"
              value={form.notes}
              onChange={(event) =>
                setForm((current) => ({ ...current, notes: event.target.value }))
              }
            />

            <button
              type="submit"
              disabled={submitting}
              className="w-full rounded-lg bg-slate-900 px-5 py-3 font-semibold text-white disabled:opacity-50"
            >
              {submitting ? "Submitting..." : "Submit Return Request"}
            </button>
          </form>
        </section>

        <section className="lg:col-span-2">
          <h2 className="text-xl font-semibold">My Return Requests</h2>
          {returns.length === 0 ? (
            <div className="mt-4 rounded-xl border bg-white p-8 text-center text-slate-500">
              You have no return requests yet.
            </div>
          ) : (
            <div className="mt-4 space-y-4">
              {returns.map((item) => (
                <article key={item.id} className="rounded-xl border bg-white p-6">
                  <div className="flex flex-col justify-between gap-3 sm:flex-row">
                    <div>
                      <p className="text-sm text-slate-500">Return Request #{item.id}</p>
                      <h3 className="text-lg font-bold">Order #{item.order_id}</h3>
                    </div>
                    <span className="h-fit rounded-full bg-slate-100 px-3 py-1 text-sm font-medium">
                      {item.status}
                    </span>
                  </div>

                  <div className="mt-5 grid gap-4 border-t pt-5 sm:grid-cols-2">
                    <div>
                      <p className="text-xs text-slate-500">Reason</p>
                      <p className="mt-1">{item.reason}</p>
                    </div>
                    <div>
                      <p className="text-xs text-slate-500">Refund Amount</p>
                      <p className="mt-1 font-semibold">
                        Rs. {Number(item.refund_amount).toLocaleString()}
                      </p>
                    </div>
                    <div>
                      <p className="text-xs text-slate-500">Requested</p>
                      <p className="mt-1 text-sm">{new Date(item.created_at).toLocaleString()}</p>
                    </div>
                    {item.resolved_at && (
                      <div>
                        <p className="text-xs text-slate-500">Resolved</p>
                        <p className="mt-1 text-sm">{new Date(item.resolved_at).toLocaleString()}</p>
                      </div>
                    )}
                  </div>

                  {item.notes && (
                    <div className="mt-4 rounded-lg bg-slate-50 p-4 text-sm text-slate-700">
                      {item.notes}
                    </div>
                  )}
                </article>
              ))}
            </div>
          )}
        </section>
      </div>
    </main>
  );
}
