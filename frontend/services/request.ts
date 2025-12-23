import { BACKEND_URL } from "@/services/api";
import { toast } from "react-toastify";

type HttpMethod = "GET" | "POST";

interface MakeRequestOptions {
  method?: HttpMethod;
  path: string;          // e.g. "register/doctor" OR "mqtt/start/1/2"
  payload?: object;
}

export default async function makeRequest<T = any>({
  method = "GET",
  path,
  payload,
}: MakeRequestOptions): Promise<T> {

  // ---- Normalize URL (no double slashes) ----
  const base = BACKEND_URL.replace(/\/+$/, "");
  const cleanPath = path.replace(/^\/+/, "");
  const url = `${base}/api/${cleanPath}/`;
  // ---- Headers ----
  const headers: HeadersInit = {
    "Content-Type": "application/json",
  };
  // Add ngrok header ONLY when needed
  if (base.includes("ngrok")) {
    headers["ngrok-skip-browser-warning"] = "69420";
  }
  const options: RequestInit = {
    method,
    headers,
  };
  if (method === "POST" && payload) {
    options.body = JSON.stringify(payload);
  }
  // ---- Fetch ----
  const res = await fetch(url, options);
  let data: any = null;
  try {
    data = await res.json();
  } catch {
    toast.error(`Invalid JSON response (${res.status})`);
    throw new Error("Invalid JSON response from server");
  }
  // ---- Error handling ----
  if (!res.ok) {
    const message =
      data?.detail ||
      data?.error ||
      data?.message ||
      `Request failed (${res.status})`;

    toast.error(message);
    throw new Error(message);
  }
  // ---- Success ----
  toast.success(data?.detail || data?.message || "Request successful");
  return data as T;
}
