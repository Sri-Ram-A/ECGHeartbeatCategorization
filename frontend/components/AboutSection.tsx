"use client";

import { motion } from "framer-motion";
import { Playfair_Display } from "next/font/google";

const playfair = Playfair_Display({ subsets: ["latin"] });

export default function AboutSection() {
  return (
    <section className={ `${playfair.className} relative w-full bg-background overflow-hidden`}>
      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-6 py-20 border-t border-border">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center mb-24"
        >
          <h2 className="text-primary font-semibold text-sm tracking-widest uppercase mb-4">
            Our Journey
          </h2>
          <h1 className="text-6xl md:text-7xl font-bold text-foreground mb-2 leading-tight">
            Meet the Team
          </h1>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto leading-relaxed">
            Born from curiosity and built with precision, powered by <span className="text-primary font-semibold">AI</span> and <span className="text-primary font-semibold">embedded systems</span>.
          </p>
        </motion.div>

        {/* Team Grid - Side by Side */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-12 mb-32 px-6">
          <DeveloperCard
            name="Sriram"
            role="Backend Developer"
            image="/images/sriram.png"
            description="Passionate about building robust backend systems and solving complex problems with elegant code. Sriram brings curioisty in learning embedded systems and AI integration, architecting the foundation that powers our platform."
            delay={0.4}
          />

          <DeveloperCard
            name="Sumith"
            role="Frontend Developer and Model Training"
            image="/images/sumith.jpeg"
            description="A creative developer who transforms designs into seamless, interactive experiences. Sumith specializes in crafting pixel-perfect interfaces that not only look stunning but deliver exceptional user experiences across all devices."
            delay={0.5}
          />
        </div>

        {/* Special Thanks Section */}
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          viewport={{ once: true }}
          className=" text-center py-16 border-t border-border"
        >
          <p className="text-primary font-semibold text-xs tracking-widest uppercase mb-4">
            Special Recognition
          </p>
          <h3 className="text-4xl font-bold text-foreground mb-4">
            Our Mentors & Guides
          </h3>
          <p className="text-2xl text-primary font-semibold">
            Vijayalakshmi Mam & Vedavathi Mam
          </p>
          <p className="text-muted-foreground mt-4 max-w-xl mx-auto">
            For their invaluable guidance, support, and mentorship throughout this journey
          </p>
        </motion.div>

        {/* Footer */}
        <motion.div 
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          transition={{ duration: 0.8 }}
          viewport={{ once: true }}
          className="pt-12 border-t border-border text-center"
        >
          <p className="text-muted-foreground mb-2">
            Built with passion by <span className="text-foreground font-semibold">Sriram</span> & <span className="text-foreground font-semibold">Sumith</span>
          </p>
          <p className="text-primary font-medium">
            RV College of Engineering — AIML Department (5th Semester)
          </p>
        </motion.div>
      </div>
    </section>
  );
}

function DeveloperCard({
  name,
  role,
  image,
  description,
  delay
}: {
  name: string;
  role: string;
  image: string;
  description: string;
  delay: number;
}) {
  const getRoleTag = (role: string) => {
    if (role.includes("Backend")) return "Backend";
    if (role.includes("Frontend")) return "UI/Frontend";
    return "Developer";
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 40 }}
      whileInView={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, delay }}
      viewport={{ once: true }}
      className="flex flex-col"
    >
      {/* Image with Badge */}
      <motion.div
        className="relative rounded-2xl overflow-hidden mb-6 shadow-lg"
        whileHover={{ y: -8 }}
        transition={{ duration: 0.3 }}
      >
        <div className="aspect-[3/4] overflow-hidden rounded-2xl">
          <img
            src={image || "/placeholder.svg"}
            alt={name}
            className="w-full h-full object-cover"
          />
        </div>
        
        {/* Gradient overlay for depth */}
        <div className="absolute inset-0 bg-gradient-to-t from-foreground/20 to-transparent rounded-2xl" />

        {/* Role Badge - Bottom Left */}
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: delay + 0.2 }}
          viewport={{ once: true }}
          className="absolute bottom-4 left-4"
        >
          <span className="inline-block px-3 py-1 bg-primary text-white text-xs font-semibold rounded-full">
            {getRoleTag(role)}
          </span>
        </motion.div>
      </motion.div>

      {/* Content Below Image */}
      <div className="flex flex-col">
        <h3 className="text-3xl font-bold text-foreground mb-1">{name}</h3>
        <p className="text-sm font-semibold mb-4">{role}</p>
        <p className="text-base text-muted-foreground leading-relaxed">
          {description}
        </p>
      </div>
    </motion.div>
  );
}
