"use client";
import React, { useState } from "react";
import { notFound } from "next/navigation";
import { Inter } from "next/font/google";
import makeRequest from "@/services/request";

const inter = Inter({ subsets: ["latin"] });

export default function RegisterPage({ params }: { params: Promise<{ role: string }>; }) {
    const { role } = React.use(params);
    const normalizedRole = role.toLowerCase();

    // Role validation
    if (!["patient", "doctor"].includes(normalizedRole)) return notFound();
    const isDoctor = normalizedRole === "doctor";

    // Form state
    const [form, setForm] = useState({
        full_name: "",
        specialization: "",
        license_number: "",
        phone_number: "",
        password: "",
        dob: ""
    });

    const update = (field: string, value: string) =>
        setForm((f) => ({ ...f, [field]: value }));

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        const payload: any = {
            full_name: form.full_name.trim(),
            phone_number: form.phone_number.trim(),
            password: form.password.trim(), // Trailing whitespace removed
        };
        if (isDoctor) {
            payload.specialization = form.specialization.trim();
            payload.license_number = form.license_number.trim();
        }
        if (!isDoctor) {
            payload.dob = form.dob;
        }
        console.log("Role:", normalizedRole);
        const data = await makeRequest("POST", "register", normalizedRole, payload)
    };

    return (
        // Apply the imported font to the root element
        <div className={`min-h-screen bg-black flex ${inter.className}`}>

            {/* Left Section: Image and Text */}
            <section className="hidden lg:flex lg:w-1/2 relative bg-black items-end p-8">
                {/* Left Video */}
                <video muted loop autoPlay playsInline className="absolute inset-0 h-full w-full object-cover">
                    <source src="/jellyfish.mp4" type="video/mp4" />
                    Your browser does not support the video tag.
                </video>
                {/* Dark/Blue Overlay (for color/mood shift) */}
                <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/30 to-transparent"></div>
                {/* Left Content */}
                <div className="relative z-10 text-white space-y-4 pb-36">
                    <h2 className="text-4xl font-extrabold leading-tight">Healthcare Platform</h2>
                    <p className="text-white/70 text-xl font-light">Register to manage appointments, patient records, and secure your health journey.</p>
                </div>
            </section>

            {/* Right Section: Form */}
            <section className="w-full lg:w-1/2 flex items-center justify-center p-6 lg:p-12 bg-gradient-to-bl from-purple-400 via-blue-900 to-black relative rounded-l-4xl">

                {/* Form Container */}
                <div className="w-full max-w-md relative z-10 p-6 space-y-6">

                    {/* Header */}
                    <div className="space-y-2">
                        <h1 className="text-3xl font-bold text-white">Create Your Account</h1>
                        <p className="text-white/60 text-lg">
                            Register as a{" "}
                            <span className="text-white font-semibold">{isDoctor ? "Doctor" : "Patient"}</span>{" "}
                            to get started.
                        </p>
                    </div>

                    {/* Form */}
                    <form onSubmit={handleSubmit} className="space-y-3">
                        {/* Full Name */}
                        <div className="space-y-2">
                            <label htmlFor="full_name" className="block text-sm font-medium text-white/90">Full Name</label>
                            <input
                                id="full_name"
                                type="text"
                                value={form.full_name}
                                onChange={(e) => update("full_name", e.target.value)}
                                placeholder="John Doe"
                                required
                                className="w-full px-4 py-3 rounded-lg border border-white/20 bg-white/5 text-white placeholder:text-white/40 focus:outline-none focus:border-blue-500/50 focus:bg-white/10 transition-all duration-200 shadow-inner shadow-black/20"
                            />
                        </div>

                        {/* Doctor Specific Fields */}
                        {isDoctor && (
                            <>
                                {/* Specialization */}
                                <div className="space-y-2">
                                    <label htmlFor="specialization" className="block text-sm font-medium text-white/90">Specialization</label>
                                    <input
                                        id="specialization"
                                        type="text"
                                        value={form.specialization}
                                        onChange={(e) => update("specialization", e.target.value)}
                                        placeholder="Cardiology"
                                        required
                                        className="w-full px-4 py-3 rounded-lg border border-white/20 bg-white/5 text-white placeholder:text-white/40 focus:outline-none focus:border-blue-500/50 focus:bg-white/10 transition-all duration-200 shadow-inner shadow-black/20"
                                    />
                                </div>

                                {/* License Number */}
                                <div className="space-y-2">
                                    <label htmlFor="license_number" className="block text-sm font-medium text-white/90">License Number</label>
                                    <input
                                        id="license_number"
                                        type="text"
                                        value={form.license_number}
                                        onChange={(e) => update("license_number", e.target.value)}
                                        placeholder="MD123456"
                                        required
                                        className="w-full px-4 py-3 rounded-lg border border-white/20 bg-white/5 text-white placeholder:text-white/40 focus:outline-none focus:border-blue-500/50 focus:bg-white/10 transition-all duration-200 shadow-inner shadow-black/20"
                                    />
                                </div>
                            </>
                        )}

                        {/* Phone Number */}
                        <div className="space-y-2">
                            <label htmlFor="phone_number" className="block text-sm font-medium text-white/90">Phone Number</label>
                            <input
                                id="phone_number"
                                type="tel"
                                // You might want to adjust the pattern for international numbers
                                pattern="\d{10}"
                                value={form.phone_number}
                                onChange={(e) => update("phone_number", e.target.value)}
                                placeholder="1234567890"
                                required
                                className="w-full px-4 py-3 rounded-lg border border-white/20 bg-white/5 text-white placeholder:text-white/40 focus:outline-none focus:border-blue-500/50 focus:bg-white/10 transition-all duration-200 shadow-inner shadow-black/20"
                            />
                        </div>

                        {/* Password */}
                        <div className="space-y-2">
                            <label htmlFor="password" className="block text-sm font-medium text-white/90">Password</label>
                            <input
                                id="password"
                                type="password"
                                value={form.password}
                                onChange={(e) => update("password", e.target.value)}
                                placeholder="Create a secure password (min 8 characters)"
                                required
                                className="w-full px-4 py-3 rounded-lg border border-white/20 bg-white/5 text-white placeholder:text-white/40 focus:outline-none focus:border-blue-500/50 focus:bg-white/10 transition-all duration-200 shadow-inner shadow-black/20"
                            />
                        </div>

                        {/* Patient Birthdate */}
                        {!isDoctor && (
                            <div className="space-y-2">
                                <label htmlFor="dob" className="block text-sm font-medium text-white/90">
                                    Date of Birth
                                </label>
                                <input
                                    id="dob"
                                    type="date"
                                    value={form.dob}
                                    onChange={(e) => update("dob", e.target.value)}
                                    required
                                    className="w-full px-4 py-3 rounded-lg border border-white/20 bg-white/5 text-white 
                       placeholder:text-white/40 focus:outline-none focus:border-blue-500/50 
                       focus:bg-white/10 transition-all duration-200"
                                />
                            </div>
                        )}

                        {/* Submit Button */}
                        <button
                            type="submit"
                            className="w-full px-4 py-3 mt-4 rounded-lg bg-blue-600 hover:bg-blue-700 text-white font-semibold transition-all duration-200 shadow-lg shadow-blue-500/30"
                        >Create Account</button>
                    </form>

                    {/* Footer / Login Link */}
                    <div className="text-center pt-4">
                        <p className="text-sm text-white/70">
                            Already have an account?{" "}
                            <a href={`/login/${normalizedRole}`} className="text-blue-400 font-semibold hover:text-blue-300 transition-colors">
                                Login
                            </a>
                        </p>
                    </div>
                </div>
            </section>

        </div>
    );
}