"use client";

import React, { useEffect } from "react";

export type AlertVariant = "success" | "error" | "warn";

interface AlertProps {
  id: string;
  variant?: AlertVariant;
  message: string;
  onClose?: (id: string) => void;
  duration?: number; // ms
}

const variantClasses: Record<AlertVariant, string> = {
  success: "bg-green-600 text-white",
  error: "bg-red-600 text-white",
  warn: "bg-amber-500 text-black",
};

export function Alert({ id, variant = "success", message, onClose, duration = 3500 }: AlertProps) {
  useEffect(() => {
    if (!duration) return;
    const t = setTimeout(() => onClose?.(id), duration);
    return () => clearTimeout(t);
  }, [id, duration, onClose]);

  return (
    <div className={`rounded-md px-4 py-3 shadow-md ${variantClasses[variant]} flex items-start gap-3`} role="alert">
      <div className="flex-1 text-sm leading-snug">{message}</div>
      <button onClick={() => onClose?.(id)} className="text-sm opacity-80">✕</button>
    </div>
  );
}

export default Alert;
