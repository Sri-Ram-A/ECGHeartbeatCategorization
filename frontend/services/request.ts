import { BACKEND_URL } from "@/services/api";
import { toast } from "react-toastify";

type HttpMethod = "GET" | "POST";

export default async function makeRequest<T = any>(method: HttpMethod, query: string, role?: string, payload?: object): Promise<T> {
    const url = role
        ? `${BACKEND_URL}/api/${query}/${role}`
        : `${BACKEND_URL}/api/${query}`;
    const options: RequestInit = {
        method,
        headers: { "Content-Type": "application/json", },
    };
    // Only attach body for POST
    if (method === "POST" && payload) {
        options.body = JSON.stringify(payload);
    }
    const res = await fetch(url, options);
    let data: any = null;

    try {
        data = await res.json();
    } catch {
        toast.error(`Invalid JSON response (${res.status})`);
        throw new Error("Invalid JSON response from server");
    }

    if (!res.ok) {
        const message = data?.detail || data?.message || `Request failed (${res.status})`;
        toast.error(message);
        throw new Error(message);
    } else {
        toast.success(data?.detail || data?.message || "Request successful");
    }
    return data;
}

export async function postMqttRequest<T = any>(
    query: string,
    payload?: object
): Promise<T> {
    const url = `${BACKEND_URL}/mqtt/${query}`;
    const options: RequestInit = {
        method: "POST",
        headers: {"Content-Type": "application/json",},
    };
    if (payload) {
        options.body = JSON.stringify(payload);
    }
    const res = await fetch(url, options);
    let data: any = null;
    try {
        data = await res.json();
    } catch {
        toast.error(`Invalid JSON response (${res.status})`);
        throw new Error("Invalid JSON response from MQTT server");
    }
    if (!res.ok) {
        const message =
            data?.detail ||
            data?.message ||
            `MQTT request failed (${res.status})`;
        toast.error(message);
        throw new Error(message);
    }
    return data;
}