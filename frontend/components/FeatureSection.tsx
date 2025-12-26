"use client";

import { Playfair_Display } from "next/font/google";
import Image from "next/image";
import { motion } from "framer-motion";

const playfair = Playfair_Display({ subsets: ["latin"] });

const items = [
  {
    src: "/images/blue_girl.jpg",
    title: "Real-time Signal Streaming",
    desc: "Low-latency MQTT pipelines for continuous medical data ingestion.",
    height: "h-[685px]",
  },
  {
    src: "/images/green_girl.jpg",
    title: "Edge-to-Cloud Messaging",
    desc: "Secure MQTT communication from edge devices to cloud services.",
    height: "h-[300px]",
  },
  {
    src: "/images/white_boy.jpg",
    title: "Device Telemetry",
    desc: "Reliable publish–subscribe patterns for IoT healthcare devices.",
    height: "h-[360px]",
  },
  {
    src: "/images/white_man.jpg",
    title: "Scalable Architecture",
    desc: "Horizontally scalable brokers designed for hospital workloads.",
    height: "h-[685px]",
  },
  {
    src: "/images/white_heart.jpg",
    title: "Clinical-Grade Reliability",
    desc: "Designed for fault tolerance and hospital-grade uptime.",
    height: "h-[320px]",
  },
  {
    src: "/images/glass_human.png",
    title: "Scalable Architecture",
    desc: "Horizontally scalable brokers designed for hospital workloads.",
    height: "h-[340px]",
  },
];

export default function FeatureSection() {
  return (
    <section className={`${playfair.className} relative bg-white py-32 overflow-hidden`}>
      {/* Decorative blobs */}
      <motion.div
        className="absolute top-24 right-20 w-64 h-64 bg-linear-to-br from-purple-600 via-pink-500 to-orange-400 rounded-full blur-2xl opacity-20 pointer-events-none"
        animate={{
          x: [0, -30, 0],
          y: [0, 20, 0],
          scale: [1, 1.08, 1],
        }}
        transition={{
          duration: 28,
          repeat: Infinity,
          repeatType: "mirror",
          ease: "linear",
        }}
      />

      <motion.div
        className="absolute bottom-24 left-20 w-64 h-64 bg-linear-to-br from-purple-600 via-pink-500 to-orange-400 rounded-full blur-2xl opacity-20 pointer-events-none"
        animate={{
          x: [0, 25, 0],
          y: [0, -30, 0],
          scale: [1, 1.05, 1],
        }}
        transition={{
          duration: 34,
          repeat: Infinity,
          repeatType: "mirror",
          ease: "linear",
        }}
      />


      <div className="max-w-7xl mx-auto px-4 sm:px-6">
        {/* Masonry columns */}
        <div className="columns-1 sm:columns-2 lg:columns-4 gap-6">
          {items.map((item, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 40 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, ease: "easeOut", delay: i * 0.06 }}
              viewport={{ once: true }}
              className="mb-6 break-inside-avoid"
            >
              <div
                className={`relative ${item.height} overflow-hidden rounded-2xl bg-zinc-100 shadow-sm hover:shadow-lg transition-shadow`}
              >
                {/* Image */}
                <Image
                  src={item.src}
                  alt={item.title}
                  fill
                  className="object-cover"
                  sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 25vw"
                />

                {/* Overlay */}
                <div className="absolute inset-0 bg-linear-to-t from-white/95 via-white/40 to-transparent" />

                {/* Text */}
                <div className="absolute bottom-0 p-5">
                  <h3 className="text-lg font-semibold text-zinc-900">
                    {item.title}
                  </h3>
                  <p className="mt-1 text-sm text-zinc-700">
                    {item.desc}
                  </p>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
