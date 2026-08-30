import { apiFetch } from "../../../lib/api";

export type Token = {
  access_token: string;
  token_type: string;
  expires_in: number;
};

export type Register = {
  id: number;
  full_name: string;
  email: string;
  phone: string | null;
  role_id: number;
};

export const authApi = {
  login: (email: string, password: string) =>
    apiFetch<Token>("/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    }),
  refresh: () => apiFetch<Token>("/auth/refresh", { method: "POST" }),
  logout: () => apiFetch<void>("/auth/logout", { method: "POST" }),
  register: (data: object) =>
    apiFetch<Register>("/store/register", {
      method: "POST",
      body: JSON.stringify(data),
    }),
  requestPasswordReset: (email: string) =>
    apiFetch<PasswordResetResponse>("/auth/password-reset/request", {
      method: "POST",
      body: JSON.stringify({ email }),
    }),
  verifyEmail: (token: string) =>
    apiFetch<EmailVerificationResponse>("/auth/email-verification/verify", {
      method: "POST",
      body: JSON.stringify({ token }),
    }),
  resendVerification: (email: string) =>
    apiFetch<EmailVerificationResponse>("/auth/email-verification/resend", {
      method: "POST",
      body: JSON.stringify({ email }),
    }),
  confirmPasswordReset: (token: string, new_password: string) =>
    apiFetch<PasswordResetResponse>("/auth/password-reset/confirm", {
      method: "POST",
      body: JSON.stringify({ token, new_password }),
    }),
};


export type EmailVerificationResponse = {
  message: string;
};

export type PasswordResetResponse = {
  message: string;
};
