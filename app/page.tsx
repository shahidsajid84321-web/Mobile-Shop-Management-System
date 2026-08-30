import Link from "next/link";

export default function HomePage() {
  return (
    <main>
      <section className="bg-black px-6 py-24 text-white">
        <div className="mx-auto max-w-7xl">
          <p className="mb-4 text-sm uppercase tracking-widest text-gray-400">
            Mobile Shop
          </p>

          <h1 className="max-w-3xl text-5xl font-bold md:text-6xl">
            Find your next smartphone and accessories.
          </h1>

          <p className="mt-6 max-w-2xl text-lg text-gray-300">
            Shop smartphones, chargers and accessories with
            fast online ordering.
          </p>

          <div className="mt-8 flex gap-4">
            <Link
              href="/products"
              className="rounded-lg bg-white px-6 py-3 font-semibold text-black"
            >
              Shop Products
            </Link>

            <Link
              href="/register"
              className="rounded-lg border border-white px-6 py-3 font-semibold"
            >
              Create Account
            </Link>
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-7xl px-6 py-16">
        <h2 className="text-3xl font-bold">
          Why shop with us?
        </h2>

        <div className="mt-8 grid gap-6 md:grid-cols-3">
          <div className="rounded-xl border bg-white p-6">
            <h3 className="text-xl font-semibold">
              Genuine Products
            </h3>
            <p className="mt-2 text-gray-600">
              Browse verified smartphones and accessories.
            </p>
          </div>

          <div className="rounded-xl border bg-white p-6">
            <h3 className="text-xl font-semibold">
              Easy Ordering
            </h3>
            <p className="mt-2 text-gray-600">
              Add products to your cart and place orders
              online.
            </p>
          </div>

          <div className="rounded-xl border bg-white p-6">
            <h3 className="text-xl font-semibold">
              Order Tracking
            </h3>
            <p className="mt-2 text-gray-600">
              Track your order status from confirmation to
              delivery.
            </p>
          </div>
        </div>
      </section>
    </main>
  );
}