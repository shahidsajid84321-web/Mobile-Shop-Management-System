"use client";

import { FormEvent, useEffect, useState } from "react";
import Link from "next/link";
import { authApi } from "../../features/auth/api/authApi";

const input = "w-full rounded-lg border px-4 py-3";

export default function VerifyEmailPage() {
  const [token, setToken] = useState("");
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(true);
  const [resending, setResending] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    const value = new URLSearchParams(window.location.search).get("token") || "";
    setToken(value);
    if (!value) {
      setLoading(false);
      return;
    }
    authApi.verifyEmail(value)
      .then((response) => setMessage(response.message))
      .catch((err) => setError(err instanceof Error ? err.message : "Unable to verify email."))
      .finally(() => setLoading(false));
  }, []);

  async function resend(e: FormEvent) {
    e.preventDefault();
    try {
      setResending(true);
      setError("");
      setMessage("");
      const response = await authApi.resendVerification(email);
      setMessage(response.message);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unable to resend verification email.");
    } finally {
      setResending(false);
    }
  }

  return (
    <main className="flex min-h-[calc(100vh-73px)] items-center justify-center p-6">
      <div className="w-full max-w-md rounded-2xl border bg-white p-8 shadow-sm">
        <h1 className="text-3xl font-bold">Verify Email</h1>
        {loading ? (
          <p className="mt-4 text-sm text-slate-500">Verifying your email address...</p>
        ) : message ? (
          <>
            <p className="mt-4 rounded-lg bg-green-50 p-3 text-sm text-green-700">{message}</p>
            <Link href="/login" className="mt-6 block w-full rounded-lg bg-slate-900 px-4 py-3 text-center font-semibold text-white">Go to Login</Link>
          </>
        ) : (
          <>
            <p className="mt-2 text-sm text-slate-500">
              {token ? "This verification link is invalid or expired. Enter your email to receive a new link." : "Enter your account email to receive a verification link."}
            </p>
            <form onSubmit={resend} className="mt-6 space-y-4">
              <input className={input} type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} required />
              {error && <p className="rounded-lg bg-red-50 p-3 text-sm text-red-700">{error}</p>}
              <button disabled={resending} className="w-full rounded-lg bg-slate-900 px-4 py-3 font-semibold text-white disabled:opacity-50">
                {resending ? "Sending..." : "Send Verification Link"}
              </button>
            </form>
            <p className="mt-6 text-center text-sm text-slate-500"><Link href="/login" className="font-semibold text-slate-900">Back to login</Link></p>
          </>
        )}
      </div>
    </main>
  );
}
