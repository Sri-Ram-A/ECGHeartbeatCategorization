"use client";

import { motion } from "framer-motion";
import { Playfair_Display } from "next/font/google";

const playfair = Playfair_Display({ subsets: ["latin"] });

export default function WhatSection() {
    return (
        <section className="relative w-full bg-background overflow-hidden">
            {/* Background gradient */}
            <div className="absolute inset-0 bg-gradient-to-br from-background via-background to-secondary/10 pointer-events-none" />

            {/* Main content */}
            <div className={`${playfair.className} relative z-10`}>
                    <div className="max-w-7xl mx-auto py-20">
                    {/* Header */}
                    <motion.div
                        initial={{ opacity: 0, y: 30 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.8 }}
                        viewport={{ once: true }}
                        className="text-center mb-16"
                    >
                        <p className="text-primary font-semibold text-sm tracking-widest uppercase mb-4">
                            Our Solutions
                        </p>
                        <h2 className="text-5xl md:text-6xl font-bold text-foreground mb-6 leading-tight">
                            Precision Healthcare
                            <br />
                            <span className="text-primary">Powered by AI</span>
                        </h2>
                        <p className="text-xl text-muted-foreground max-w-3xl mx-auto leading-relaxed">
                            From ECG signal analysis to real-time decision support, our platforms are designed for hospitals that value precision, safety, and evidence-based care.
                        </p>
                    </motion.div>

                    {/* Divider */}
                    <motion.div 
                        className="w-16 h-1 bg-primary mx-auto mb-16 rounded-full"
                        initial={{ scaleX: 0 }}
                        animate={{ scaleX: 1 }}
                        transition={{ duration: 0.8, delay: 0.2 }}
                    />

                    {/* Image Grid */}
                    <motion.div
                        initial={{ opacity: 0 }}
                        whileInView={{ opacity: 1 }}
                        transition={{ duration: 0.8, delay: 0.3 }}
                        viewport={{ once: true }}
                        className="grid grid-cols-1 md:grid-cols-3 gap-6"
                    >
                        <ImageCard
                            title="Jetson Nano Integration"
                            image="/images/jetson_nano_ai.jpg"
                            delay={0.4}
                        />
                        <ImageCard
                            title="Heart Monitoring"
                            image="/images/techstack_dbms.png"
                            delay={0.5}
                        />
                        <ImageCard
                            title="Raspberry Pi Deployment"
                            image="/images/rpi_ai.jpeg"
                            delay={0.6}
                        />
                    </motion.div>
                </div>
            </div>
        </section>
    );
}

/* ---- Image card component ---- */
function ImageCard({
    title,
    image,
    delay,
}: {
    title: string;
    image: string;
    delay: number;
}) {
    return (
        <motion.div
            initial={{ opacity: 0, y: 40 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay }}
            viewport={{ once: true }}
            whileHover={{ y: -12 }}
            className="group rounded"
        >
                <img
                    src={image || "/placeholder.svg"}
                    alt={title}
                    className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500 rounded-xl"
                />
            <h3 className="text-lg font-semibold text-foreground mt-4 flex justify-center">{title}</h3>
        </motion.div>
    );
}
