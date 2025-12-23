"use client";

import React, { createContext, useCallback, useEffect, useState } from "react";
import { Alert } from "./Alert";
import { setNotifier, clearNotifier } from "@/lib/notify";

type Notification = {
  id: string;
  type: "success" | "error" | "warn";
  message: string;
};

export const NotificationContext = createContext<{ push: (n: Omit<Notification, "id">) => void } | null>(null);

export function NotificationProvider({ children }: { children: React.ReactNode }) {
  const [items, setItems] = useState<Notification[]>([]);

  const push = useCallback((n: Omit<Notification, "id">) => {
    const id = String(Date.now()) + Math.random().toString(36).slice(2, 6);
    setItems((s) => [...s, { id, ...n }]);
  }, []);

  const remove = useCallback((id: string) => {
    setItems((s) => s.filter((i) => i.id !== id));
  }, []);

  useEffect(() => {
    setNotifier(({ type, message }) => push({ type, message }));
    return () => clearNotifier();
  }, [push]);

  return (
    <NotificationContext.Provider value={{ push }}>
      {children}
      <div className="fixed top-6 right-6 z-50 flex flex-col gap-3 w-96 max-w-full">
        {items.map((it) => (
          <Alert key={it.id} id={it.id} variant={it.type} message={it.message} onClose={remove} />
        ))}
      </div>
    </NotificationContext.Provider>
  );
}

export default NotificationProvider;
