"use client";

import React from "react";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  children: React.ReactNode;
}

export function Button({ children, className = "", ...props }: ButtonProps) {
  return (
    <button
      {...props}
      className={`px-4 py-3 rounded-lg font-semibold transition-all duration-200 ${className}`}
    >
      {children}
    </button>
  );
}

export default Button;
