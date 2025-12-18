"use client";

import Link from "next/link";

export default function Home() {
  return (
    <div className="bg-zinc-50 dark:bg-black font-sans overflow-hidden">

      {/* Navbar */}
      <nav className="fixed top-0 left-0 w-full z-50 backdrop-blur-md bg-white/70 dark:bg-black/60 border-b border-zinc-200 dark:border-zinc-800">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">

          {/* Nav Links */}
          <div className="flex items-center gap-6 text-sm font-medium">

            <Link
              href="/register/patient"
              className="text-zinc-700 dark:text-zinc-300 hover:text-black dark:hover:text-white transition"
            >
              Patient Register
            </Link>

            <div className="h-5 w-px bg-zinc-300 dark:bg-zinc-700" />

            <Link
              href="/login/doctor"
              className="text-zinc-700 dark:text-zinc-300 hover:text-black dark:hover:text-white transition"
            >
              Doctor Login
            </Link>

            <Link
              href="/register/doctor"
              className="px-4 py-2 rounded-full bg-black text-white dark:bg-white dark:text-black hover:opacity-90 transition"
            >
              Doctor Register
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="h-screen w-full overflow-hidden relative">
        <video
          muted
          loop
          autoPlay
          playsInline
          className="h-full w-full object-cover"
        >
          <source src="dna.mp4" type="video/mp4" />
        </video>

        {/* Overlay */}
        <div className="absolute inset-0 bg-black/40" />

        <div className="absolute inset-0 flex items-center justify-center">
          <h1 className="text-white text-5xl font-bold drop-shadow-lg">
            Welcome
          </h1>
        </div>
      </section>

      {/* Second Section */}
      <section className="h-screen w-full bg-yellow-400 flex items-center justify-center">
        <h2 className="text-3xl font-bold text-black">
          Yellow Section
        </h2>
      </section>

    </div>
  );
}
