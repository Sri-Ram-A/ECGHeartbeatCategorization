import { BACKEND_URL } from "@/services/api";
import { toast } from "sonner";

type HttpMethod = "GET" | "POST";

interface MakeRequestOptions {
  method?: HttpMethod;
  path: string; // "register/doctor" | "mqtt/start/1/2"
  payload?: object;
  showSuccessToast?: boolean; // control UX explicitly
}

export default async function makeRequest<T = any>({
  method = "GET",
  path,
  payload,
  showSuccessToast = method !== "GET",
}: MakeRequestOptions): Promise<T> {
  // ---- Normalize URL ----
  const base = BACKEND_URL.replace(/\/+$/, "");
  const cleanPath = path.replace(/^\/+/, "");
  const url = `${base}/api/${cleanPath}/`;

  // ---- Headers ----
  const headers: HeadersInit = {
    "Content-Type": "application/json",
  };

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
  let res: Response;

  try {
    res = await fetch(url, options);
  } catch {
    toast.error("Network error. Server unreachable.");
    throw new Error("Network error");
  }

  // ---- Parse JSON ----
  let data: any;
  try {
    data = await res.json();
  } catch {
    toast.error(`Invalid JSON response (${res.status})`);
    throw new Error("Invalid JSON response");
  }

  // ---- Handle errors ----
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
  if (showSuccessToast) {
    toast.success(data?.detail || data?.message || "Operation successful");
  }

  return data as T;
}
