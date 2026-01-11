"use client";

import React from "react";

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
    id: string;
    label?: string;
}

export function Input({ id, label, className = "", ...props }: InputProps) {
    return (
        <div className="space-y-2">
            {label && (
                <label htmlFor={id} className="block text-sm font-medium text-white/90">
                    {label}
                </label>
            )}
            <input
                id={id}
                {...props}
                className={`w-full px-4 py-3 rounded-lg border border-white/20 bg-white/5 text-white placeholder:text-white/40 focus:outline-none focus:border-blue-500/50 focus:bg-white/10 transition-all duration-200 shadow-inner shadow-black/20 ${className}`}
            />
        </div>
    );
}

export default Input;
