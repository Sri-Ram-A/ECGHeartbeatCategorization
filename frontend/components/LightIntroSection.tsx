"use client";

import GradientText from "./custom/GradientText";
import { Playfair_Display } from "next/font/google";

const playfair_display = Playfair_Display({ subsets: ["latin"] });

export default function Home() {
  return (
    <>
      {/* Hero Section with Video Background */}
      <section className="h-screen relative overflow-hidden">
        {/* Background Video */}
        <video
          className="absolute inset-0 w-full h-full object-cover"
          src="/videos/light_heart.mp4" // <-- replace with your video path
          autoPlay
          loop
          muted
          playsInline
        />

        {/* Overlay content */}
        <div className="absolute inset-0 z-10 flex items-center">
          <div className="max-w-xl px-20 text-white">
            <GradientText
              colors={[
                "#40ffaa",
                "#4079ff",
                "#40ffaa",
                "#4079ff",
                "#40ffaa",
              ]}
              animationSpeed={3}
              showBorder={false}
              className={`${playfair_display.className} text-9xl leading-none`}
            >
              MedAI
            </GradientText>

            <p
              className={`${playfair_display.className} mt-6 px-6 text-xl text-black max-w-xl font-bold`}
            >
              AI-powered ECG analysis delivering real-time, intelligent
              cardiac insights for modern healthcare.
            </p>
          </div>
        </div>
      </section>
    </>
  );
}
