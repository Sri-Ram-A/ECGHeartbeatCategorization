"use client";
import Navbar from "@/components/Navbar";

export default function Home() {
  return (
    <div className="bg-zinc-50 dark:bg-black font-sans overflow-hidden">
      <header>
        <Navbar />
      </header>

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

        <div className="absolute inset-0 flex items-center justify-center">
          <h1 className="text-white text-5xl font-bold drop-shadow-lg">
            Welcome
          </h1>
        </div>
        
      </section>

      <section className="h-screen w-full bg-yellow-400 flex items-center justify-center">
        <h2 className="text-3xl font-bold text-black">Yellow Section</h2>
      </section>
    </div>
  );
}
