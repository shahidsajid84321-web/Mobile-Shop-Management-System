"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { removeToken } from "../../lib/auth";
import { authApi } from "../../features/auth/api/authApi";

const sections = [
  {
    title: "Overview",
    links: [{ name: "Dashboard", href: "/dashboard" }],
  },
  {
    title: "Catalogue",
    links: [
      { name: "Products", href: "/dashboard/products" },
      { name: "Categories", href: "/dashboard/categories" },
      { name: "Suppliers", href: "/dashboard/suppliers" },
    ],
  },
  {
    title: "Operations",
    links: [
      { name: "Customers", href: "/dashboard/customers" },
      { name: "Purchases", href: "/dashboard/purchases" },
      { name: "Sales", href: "/dashboard/sales" },
      { name: "Payments", href: "/dashboard/payments" },
      { name: "Inventory", href: "/dashboard/inventory" },
    ],
  },
  {
    title: "Online Store",
    links: [
      { name: "Orders", href: "/dashboard/orders" },
      { name: "Returns", href: "/dashboard/returns" },
    ],
  },
  {
    title: "Administration",
    links: [
      { name: "Users", href: "/dashboard/users" },
      { name: "Roles", href: "/dashboard/roles" },
      { name: "Reports", href: "/dashboard/reports" },
    ],
  },
];

export default function Sidebar() {
  const pathname = usePathname();
  const router = useRouter();

  async function logout() {
    try { await authApi.logout(); } catch {}
    removeToken();
    router.push("/login");
  }

  return (
    <aside className="flex min-h-screen w-72 shrink-0 flex-col border-r border-slate-200 bg-white sticky top-0 h-screen">
      <div className="shrink-0 border-b border-slate-200 px-6 py-5">
        <Link href="/dashboard" className="text-xl font-bold text-slate-900">
          Mobile Shop
        </Link>
        <p className="mt-1 text-xs text-slate-500">Management System</p>
      </div>

      <nav className="min-h-0 flex-1 overflow-y-auto p-4">
        {sections.map((section) => (
          <div key={section.title} className="mb-5 last:mb-0">
            <p className="px-3 pb-2 text-[11px] font-bold uppercase tracking-wider text-slate-400">
              {section.title}
            </p>

            <div className="space-y-1">
              {section.links.map((link) => {
                const active =
                  link.href === "/dashboard"
                    ? pathname === "/dashboard"
                    : pathname.startsWith(link.href);

                return (
                  <Link
                    key={link.href}
                    href={link.href}
                    className={`block rounded-lg px-3 py-2.5 text-sm font-medium transition-colors ${
                      active
                        ? "bg-slate-900 text-white"
                        : "text-slate-700 hover:bg-slate-100"
                    }`}
                  >
                    {link.name}
                  </Link>
                );
              })}
            </div>
          </div>
        ))}
      </nav>

      <div className="shrink-0 border-t border-slate-200 p-4">
        <Link
          href="/"
          className="mb-2 block rounded-lg px-3 py-2.5 text-sm font-medium text-slate-700 hover:bg-slate-100"
        >
          View Store
        </Link>
        <button
          onClick={logout}
          className="w-full rounded-lg bg-slate-900 px-3 py-2.5 text-sm font-semibold text-white hover:bg-slate-700"
        >
          Logout
        </button>
      </div>
    </aside>
  );
}
