"use client";
import { useScroll, useTransform } from "motion/react";
import React from "react";
import { GoogleGeminiEffect } from "@/components/ui/GoogleGeminiEffect";
import { Playfair_Display } from "next/font/google";

const playfair_display = Playfair_Display({ subsets: ["latin"] });

export default function Home() {
  const ref = React.useRef<HTMLDivElement>(null);

  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ["start start", "end start"],
  });

  const pathLengths = [
    useTransform(scrollYProgress, [0, 0.8], [0.2, 1.2]),
    useTransform(scrollYProgress, [0, 0.8], [0.15, 1.2]),
    useTransform(scrollYProgress, [0, 0.8], [0.1, 1.2]),
    useTransform(scrollYProgress, [0, 0.8], [0.05, 1.2]),
    useTransform(scrollYProgress, [0, 0.8], [0, 1.2]),
  ];

  return (
    <section
      ref={ref}
      className="relative h-screen overflow-hidden"
    >
      {/* 1️⃣ Background Video */}
      <video
        className="absolute inset-0 w-full h-full object-cover z-0"
        src="/videos/blue_heart.mp4"
        autoPlay
        loop
        muted
        playsInline
      />

      {/* 2️⃣ Dark Overlay */}
      <div className="absolute inset-0 bg-black/20 z-10" />

      {/* 3️⃣ Google Gemini Effect */}
      <div className="absolute inset-0 z-20 pointer-events-none">
        <GoogleGeminiEffect pathLengths={pathLengths} />
      </div>

      {/* 4️⃣ Text Content */}
      <div className="relative z-30 flex h-full items-center justify-center lg:justify-start">
        <div className=" max-w-2xl px-6 sm:px-10 lg:px-24 text-center lg:text-left "
        >
          <h1 className={`${playfair_display.className} text-9xl  bg-linear-to-r from-cyan-400/70 via-blue-500/70 to-indigo-600/70 text-white py-3 px-12 rounded-lg`}>
            MedAI
          </h1>

          <p className={`${playfair_display.className} mt-5 sm:mt-6 text-base sm:text-lg md:text-xl text-zinc-200 max-w-xl mx-auto lg:mx-0 font-semibold `}>
            AI-powered ECG analysis delivering real-time, intelligent
            cardiac insights for modern healthcare.
          </p>
        </div>
      </div>

    </section>
  );
}
