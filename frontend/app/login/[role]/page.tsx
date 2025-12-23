"use client";
import React, { useState } from "react";
import { notFound } from "next/navigation";
import { Inter } from "next/font/google";
import { setSession } from '@/lib/session';
import { useRouter } from 'next/navigation';
import makeRequest from "@/services/request";
import { Input } from '@/components/ui/Input';
import { Button } from '@/components/ui/Button';

const inter = Inter({ subsets: ["latin"] });

export default function LoginPage({ params }: { params: Promise<{ role: string }> }) {
  const router = useRouter();
  const { role } = React.use(params);
  const normalizedRole = role.toLowerCase();

  // Role validation
  if (!["patient", "doctor"].includes(normalizedRole)) return notFound();
  const isDoctor = normalizedRole === "doctor";

  // Form state
  const [form, setForm] = useState({
    full_name: "",
    password: ""
  });

  const update = (field: string, value: string) =>
    setForm((f) => ({ ...f, [field]: value }));

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const payload = {
      full_name: form.full_name.trim(),
      password: form.password.trim(),
    };
    console.log("Role:", normalizedRole);
    const data = await makeRequest({
      method: "POST",
      path: `login/${normalizedRole}`,
      payload,
    });

    if (normalizedRole === 'doctor') {
      // Store session data
      setSession({
        id: data.id,
        full_name: data.full_name
      });
      // Redirect doctors to dashboard
      router.push('/dashboard');
    }
  };

  return (
    <div className={`min-h-screen flex ${inter.className}`}>
      {/* Left Section: Form */}
      <section className="w-full lg:w-1/2 flex items-center justify-center p-8 lg:p-16 bg-gradient-to-br from-blue-950 via-slate-900 to-black relative">
        {/* Form Container */}
        <div className="w-full max-w-md relative z-10 p-8 space-y-8">
          {/* Header */}
          <div className="space-y-2">
            <h1 className="text-3xl font-bold text-white">Welcome Back</h1>
            <p className="text-white/60 text-lg">
              Login as a{" "}
              <span className="text-white font-semibold">{isDoctor ? "Doctor" : "Patient"}</span>
            </p>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-5">
            <Input
              id="full_name"
              label="Username"
              type="text"
              value={form.full_name}
              onChange={(e) => update("full_name", e.target.value)}
              placeholder="Enter your full name"
              required
            />

            <Input
              id="password"
              label="Password"
              type="password"
              value={form.password}
              onChange={(e) => update("password", e.target.value)}
              placeholder="Enter your password"
              required
            />

            <Button type="submit" className="w-full bg-blue-600 hover:bg-blue-700 text-white">
              Sign In
            </Button>
          </form>

          {/* Footer / Register Link */}
          <div className="text-center pt-4">
            <p className="text-sm text-white/70">
              Don't have an account?{" "}
              <a
                href={`/register/${normalizedRole}`}
                className="text-blue-400 font-semibold hover:text-blue-300 transition-colors"
              >
                Create one
              </a>
            </p>
          </div>
        </div>
      </section>

      {/* Right Section: Video */}
      <section className="hidden lg:flex lg:w-1/2 relative bg-[#091020] items-end p-24">
        {/* Video */}
        <video muted loop autoPlay playsInline className="absolute inset-0 h-full w-full object-cover" >
          <source src="/log.mp4" type="video/mp4" />
          Your browser does not support the video tag.
        </video>

        {/* Dark Overlay */}
        <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/30 to-transparent"></div>

        {/* Content */}
        <div className="relative z-10 text-white  pb-8">
          <h2 className="text-4xl font-extrabold leading-tight">Experience Quality</h2>
          <p className="text-white/70 text-xl font-light">
            Here at sumsri, we prioritize your health with cutting-edge technology and compassionate care.
          </p>
        </div>
      </section>

    </div>
  );
}