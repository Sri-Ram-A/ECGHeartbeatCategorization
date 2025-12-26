"use client";

import { useEffect, useRef } from "react";
import gsap from "gsap";
import ScrollTrigger from "gsap/ScrollTrigger";
import { motion } from "framer-motion";
import { Merriweather } from "next/font/google";

gsap.registerPlugin(ScrollTrigger);

const merriweather = Merriweather({
    subsets: ["latin"],
    weight: ["400", "700"],
});

/* ---- Blob config (single source of truth) ---- */
const BLOBS = [
    {
        size: "w-32 h-32",
        top: "15%",
        gradient: "from-orange-400 via-rose-400 to-blue-500",
        blur: "blur-xl",
    },
    {
        size: "w-24 h-24",
        top: "30%",
        gradient: "from-amber-400 via-pink-400 to-indigo-500",
        blur: "blur-lg",
    },
    {
        size: "w-40 h-40",
        top: "50%",
        gradient: "from-purple-500 via-blue-400 to-cyan-400",
        blur: "blur-2xl",
    },
    {
        size: "w-20 h-20",
        top: "65%",
        gradient: "from-orange-500 via-fuchsia-500 to-violet-500",
        blur: "blur-md",
    },
    {
        size: "w-28 h-28",
        top: "80%",
        gradient: "from-rose-400 via-orange-400 to-yellow-400",
        blur: "blur-lg",
    },
    {
        size: "w-18 h-18",
        top: "80%",
        gradient: "from-orange-500 via-fuchsia-500 to-violet-500",
        blur: "blur-xl",
    },
    {
        size: "w-28 h-28",
        top: "80%",
        gradient: "from-amber-400 via-pink-400 to-indigo-500",
        blur: "blur-lg",
    },
];

export default function WhatSection() {
    const sectionRef = useRef<HTMLElement>(null);
    const cardRef = useRef<HTMLDivElement>(null);
    const blobsRef = useRef<HTMLDivElement[]>([]);

    useEffect(() => {
        if (!sectionRef.current || !cardRef.current) return;

        const ctx = gsap.context(() => {

            /* ---- Card entrance ---- */
            gsap.fromTo(
                cardRef.current,
                { y: "30%", scale: 0.9, opacity: 0 },
                {
                    y: "0%",
                    scale: 1,
                    opacity: 1,
                    ease: "power3.out",
                    scrollTrigger: {
                        trigger: sectionRef.current,
                        start: "top bottom",
                        end: "top top",
                        scrub: true,
                    },
                }
            );

            /* ---- Pinned blob timeline ---- */
            const tl = gsap.timeline({
                scrollTrigger: {
                    trigger: sectionRef.current,
                    start: "top -2.5%",
                    end: "+=150%",
                    scrub: 1.2,
                    pin: true,
                },
            });

            blobsRef.current.forEach((blob, i) => {
                tl.fromTo(
                    blob,
                    {
                        x: "120vw",
                        scale: 0.6,
                        opacity: 0,
                        rotate: 0,
                    },
                    {
                        x: "-100vw",
                        scale: 1.1,
                        opacity: 0.85,
                        rotate: 360,
                        ease: "none",
                    },
                    i * 0.1 // stagger inside timeline
                );
            });
        }, sectionRef);

        return () => ctx.revert();
    }, []);

    return (
        <section
            ref={sectionRef}
            className="relative bg-black min-h-screen overflow-hidden"
        >
            {/* ---- Floating blobs ---- */}
            {BLOBS.map((blob, i) => (
                <div
                    key={i}
                    ref={(el) => {
                        if (el) blobsRef.current[i] = el;
                    }}
                    className={` absolute right-0 ${blob.size} rounded-full bg-linear-to-br ${blob.gradient} ${blob.blur} opacity-0 pointer-events-none z-10`}
                    style={{ top: blob.top }}
                />
            ))}

            {/* ---- Main card ---- */}
            <div
                ref={cardRef}
                className=" relative bg-white rounded-t-3xl p-16 min-h-screen overflow-hidden "
            >
                <div className="relative max-w-7xl mx-auto">
                    {/* Heading */}
                    <motion.div
                        initial={{ opacity: 0, y: 60 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.9, ease: "easeOut" }}
                        viewport={{ once: true }}
                        className={merriweather.className}
                    >
                        <h2 className="text-7xl font-bold leading-tight">
                            Precision Healthcare
                            <br />
                            <span className="text-transparent bg-clip-text bg-linear-to-r from-orange-500 via-rose-500 to-blue-600">
                                Powered by AI
                            </span>
                        </h2>

                        <p className="m-4 text-xl text-zinc-600 max-w-2xl">
                            From ECG signal analysis to real-time decision support, our platforms
                            are designed for hospitals that value precision, safety, and
                            evidence-based care.
                        </p>
                    </motion.div>

                    {/* Videos */}
                    <motion.div
                        initial={{ opacity: 0, y: 60 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        transition={{ duration: 1, ease: "easeOut", delay: 0.2 }}
                        viewport={{ once: true }}
                        className="grid grid-cols-1 lg:grid-cols-3 gap-10"
                    >
                        <VideoCard src="/videos/jnano.mp4" />
                        <VideoCard src="/videos/white_heart.mp4" />
                        <VideoCard src="/videos/rpi.mp4" />
                    </motion.div>
                </div>
            </div>
        </section>
    );
}

/* ---- Reusable video card ---- */
function VideoCard({ src }: { src: string }) {
    return (
        <motion.div
            whileHover={{ scale: 1.05, rotate: 1 }}
            transition={{ duration: 0.3 }}
            className="aspect-square w-90 mx-auto overflow-hidden rounded-2xl shadow-lg"
        >
            <video autoPlay loop muted playsInline className="w-full h-full object-cover">
                <source src={src} type="video/mp4" />
            </video>
        </motion.div>
    );
}
