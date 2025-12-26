"use client";

import Link from "next/link";
import { useState } from "react";
import { Merriweather } from "next/font/google";
import { Menu, X } from "lucide-react";

const merriweather = Merriweather();

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <nav className={`fixed top-0 left-0 w-full z-50 backdrop-blur ${merriweather.className}`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 py-4 flex items-center justify-between">
        {/* Logo */}
        <Link href="/" className="text-xl font-extrabold text-indigo-600">
          ECG-AI
        </Link>

        {/* Desktop Navigation Links */}
        <div className="hidden md:flex items-center gap-6 text-sm font-extrabold">
          <Link href="/register/patient" className="text-indigo-600 hover:text-blue-400 transition-colors">
            Patient Register
          </Link>
          <Link href="/login/doctor" className="text-indigo-600 hover:text-blue-400 transition-colors">
            Doctor Login
          </Link>
          <Link href="/register/doctor" className="text-indigo-600 hover:text-blue-400 transition-colors">
            Doctor Register
          </Link>
        </div>

        {/* Mobile Menu Button */}
        <button
          className="md:hidden text-indigo-600 hover:text-blue-400 transition-colors"
          onClick={() => setIsOpen(!isOpen)}
          aria-label="Toggle menu"
        >
          {isOpen ? <X size={28} /> : <Menu size={28} />}
        </button>
      </div>

      {/* Mobile Menu */}
      {isOpen && (
        <div className="md:hidden bg-white/90 dark:bg-gray-900/90 backdrop-blur-lg shadow-lg">
          <div className="px-4 py-6 space-y-4">
            <Link
              href="/register/patient"
              className="block text-lg font-extrabold text-indigo-600 hover:text-blue-400 transition-colors py-2"
              onClick={() => setIsOpen(false)}
            >
              Patient Register
            </Link>
            <Link
              href="/login/doctor"
              className="block text-lg font-extrabold text-indigo-600 hover:text-blue-400 transition-colors py-2"
              onClick={() => setIsOpen(false)}
            >
              Doctor Login
            </Link>
            <Link
              href="/register/doctor"
              className="block text-lg font-extrabold text-indigo-600 hover:text-blue-400 transition-colors py-2"
              onClick={() => setIsOpen(false)}
            >
              Doctor Register
            </Link>
          </div>
        </div>
      )}
    </nav>
  );
}