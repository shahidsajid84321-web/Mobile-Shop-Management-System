"use client";

import { useEffect, useState } from "react";
import { storeApi, type Order, type Return } from "../api/storeApi";
import { AdminPage } from "../../../shared/components/AdminShell";
import {
  EmptyState,
  ErrorState,
  LoadingState,
} from "../../../shared/components/PageState";

const ORDER_STATUSES = [
  "Pending",
  "Confirmed",
  "Processing",
  "Packed",
  "Shipped",
  "Delivered",
  "Cancelled",
] as const;

const RETURN_STATUSES = ["Requested", "Approved", "Rejected", "Refunded"] as const;

export function OrdersManagement() {
  const [orders, setOrders] = useState<Order[]>([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [updatingId, setUpdatingId] = useState<number | null>(null);

  const load = () => {
    setLoading(true);
    setError("");

    storeApi
      .managementOrders()
      .then((response) => setOrders(response.data))
      .catch((err) =>
        setError(err instanceof Error ? err.message : "Unable to load orders."),
      )
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    load();
  }, []);

  async function update(id: number, status: string) {
    setUpdatingId(id);
    setError("");

    try {
      await storeApi.updateOrder(id, { status });
      await load();
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Unable to update order status.",
      );
    } finally {
      setUpdatingId(null);
    }
  }

  return (
    <AdminPage
      title="Online Orders"
      description="Manage online orders using the existing store endpoints."
    >
      {error && <ErrorState message={error} />}

      {loading ? (
        <LoadingState />
      ) : orders.length === 0 ? (
        <EmptyState title="No online orders found" />
      ) : (
        <div className="overflow-x-auto rounded-xl border bg-white">
          <table className="w-full text-left text-sm">
            <thead className="bg-slate-50">
              <tr>
                <th className="p-3">Order</th>
                <th className="p-3">Customer</th>
                <th className="p-3">Total</th>
                <th className="p-3">Payment</th>
                <th className="p-3">Status</th>
                <th className="p-3">Update</th>
              </tr>
            </thead>
            <tbody className="divide-y">
              {orders.map((order) => {
                const canChange =
                  order.status !== "Delivered" &&
                  order.status !== "Cancelled" &&
                  order.status !== "Returned";

                return (
                  <tr key={order.id}>
                    <td className="p-3 font-semibold">{order.order_number}</td>
                    <td className="p-3">
                      {order.delivery_name}
                      <div className="text-xs text-slate-500">
                        {order.delivery_phone}
                      </div>
                    </td>
                    <td className="p-3">
                      Rs. {Number(order.total_amount).toLocaleString()}
                    </td>
                    <td className="p-3">{order.payment_status}</td>
                    <td className="p-3">{order.status}</td>
                    <td className="p-3">
                      {canChange ? (
                        <select
                          className="rounded border px-2 py-1"
                          value={order.status}
                          disabled={updatingId === order.id}
                          onChange={(event) =>
                            update(order.id, event.target.value)
                          }
                        >
                          {!ORDER_STATUSES.includes(
                            order.status as (typeof ORDER_STATUSES)[number],
                          ) && (
                            <option value={order.status}>{order.status}</option>
                          )}
                          {ORDER_STATUSES.map((status) => (
                            <option key={status} value={status}>
                              {status}
                            </option>
                          ))}
                        </select>
                      ) : (
                        <span className="text-sm text-slate-500">Finalized</span>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </AdminPage>
  );
}

export function ReturnsManagement() {
  const [returns, setReturns] = useState<Return[]>([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [updatingId, setUpdatingId] = useState<number | null>(null);

  const load = () => {
    setLoading(true);
    setError("");

    storeApi
      .managementReturns()
      .then((response) => setReturns(response.data))
      .catch((err) =>
        setError(err instanceof Error ? err.message : "Unable to load returns."),
      )
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    load();
  }, []);

  async function update(id: number, status: string) {
    setUpdatingId(id);
    setError("");

    try {
      await storeApi.updateReturn(id, { status });
      await load();
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Unable to update return status.",
      );
    } finally {
      setUpdatingId(null);
    }
  }

  return (
    <AdminPage
      title="Returns"
      description="Review return requests and update their status."
    >
      {error && <ErrorState message={error} />}

      {loading ? (
        <LoadingState />
      ) : returns.length === 0 ? (
        <EmptyState title="No returns found" />
      ) : (
        <div className="overflow-x-auto rounded-xl border bg-white">
          <table className="w-full text-left text-sm">
            <thead className="bg-slate-50">
              <tr>
                <th className="p-3">Order</th>
                <th className="p-3">Reason</th>
                <th className="p-3">Refund</th>
                <th className="p-3">Status</th>
                <th className="p-3">Update</th>
              </tr>
            </thead>
            <tbody className="divide-y">
              {returns.map((item) => {
                const finalized =
                  item.status === "Rejected" || item.status === "Refunded";

                return (
                  <tr key={item.id}>
                    <td className="p-3 font-semibold">#{item.order_id}</td>
                    <td className="max-w-md p-3">{item.reason}</td>
                    <td className="p-3">
                      Rs. {Number(item.refund_amount).toLocaleString()}
                    </td>
                    <td className="p-3">{item.status}</td>
                    <td className="p-3">
                      {finalized ? (
                        <span className="text-sm text-slate-500">Finalized</span>
                      ) : (
                        <select
                          className="rounded border px-2 py-1"
                          value={item.status}
                          disabled={updatingId === item.id}
                          onChange={(event) =>
                            update(item.id, event.target.value)
                          }
                        >
                          {!RETURN_STATUSES.includes(
                            item.status as (typeof RETURN_STATUSES)[number],
                          ) && (
                            <option value={item.status}>{item.status}</option>
                          )}
                          {RETURN_STATUSES.map((status) => (
                            <option key={status} value={status}>
                              {status}
                            </option>
                          ))}
                        </select>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </AdminPage>
  );
}
