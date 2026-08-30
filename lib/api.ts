import { getToken, removeToken, saveToken } from "./auth";

export const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export function mediaUrl(path: string | null | undefined) {
  if (!path) return null;
  if (/^https?:\/\//i.test(path)) return path;
  return `${API_URL}/uploads/${path.replace(/^\//, "")}`;
}

async function refreshAccessToken(): Promise<boolean> {
  try {
    const response = await fetch(`${API_URL}/auth/refresh`, {
      method: "POST",
      credentials: "include",
      headers: { "Content-Type": "application/json" },
    });
    if (!response.ok) return false;
    const data = (await response.json()) as { access_token?: string };
    if (!data.access_token) return false;
    saveToken(data.access_token);
    return true;
  } catch {
    return false;
  }
}

export async function apiFetch<T>(
  endpoint: string,
  options: RequestInit = {},
  authenticated = false,
): Promise<T> {
  const makeRequest = async () => {
    const headers = new Headers(options.headers);
    const isFormData = typeof FormData !== "undefined" && options.body instanceof FormData;
    if (options.body && !isFormData && !headers.has("Content-Type")) {
      headers.set("Content-Type", "application/json");
    }
    if (authenticated && typeof window !== "undefined") {
      const token = getToken();
      if (token) headers.set("Authorization", `Bearer ${token}`);
    }

    return fetch(`${API_URL}${endpoint}`, {
      ...options,
      headers,
      credentials: "include",
    });
  };

  let response = await makeRequest();

  // Access tokens are intentionally short-lived. On expiry, rotate the
  // refresh token server-side and retry the original request once.
  if (authenticated && response.status === 401 && endpoint !== "/auth/refresh" && typeof window !== "undefined") {
    const refreshed = await refreshAccessToken();
    if (refreshed) {
      response = await makeRequest();
    } else {
      removeToken();
    }
  }

  const rawText = await response.text();
  let data: unknown = null;
  try {
    data = rawText ? JSON.parse(rawText) : null;
  } catch {
    data = rawText;
  }

  if (!response.ok) {
    let message = `Request failed with status ${response.status}`;
    if (typeof data === "object" && data !== null && "detail" in data) {
      const detail = (data as { detail: unknown }).detail;
      message = typeof detail === "string" ? detail : JSON.stringify(detail);
    } else if (rawText) {
      message = rawText;
    }
    throw new Error(message);
  }
  return data as T;
}
