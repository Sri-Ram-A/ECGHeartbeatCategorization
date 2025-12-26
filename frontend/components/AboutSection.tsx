"use client";

import { motion } from "framer-motion";
import { useState } from "react";

export default function AboutSection() {
  return (
    <section className="relative w-full min-h-screen bg-black overflow-hidden flex items-center justify-center py-20">
      
      {/* Background Video */}
      <video
        autoPlay
        loop
        muted
        playsInline
        className="absolute inset-0 h-full w-full object-cover opacity-40"
      >
        <source src="/videos/baby_cosmos.mp4" type="video/mp4" />
      </video>

      {/* Gradient Overlay */}
      <div className="absolute inset-0 " />

      {/* Animated Grid Background */}
      <div className="absolute inset-0 opacity-20">
        <div className="absolute inset-0" style={{
          backgroundImage: 'linear-gradient(rgba(139, 92, 246, 0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(139, 92, 246, 0.1) 1px, transparent 1px)',
          backgroundSize: '50px 50px'
        }} />
      </div>

      {/* Content */}
      <div className="relative z-10 max-w-6xl mx-auto px-6 text-center text-white">
        
        {/* Title Section */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.6 }}
        >
          {/* Subtitle with letter animation */}
          <motion.p 
            className="text-sm tracking-[0.3em] text-violet-400 mb-2 uppercase font-light"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
          >
            This project is a
          </motion.p>

          {/* Main Title with staggered letters */}
          <div className="overflow-hidden mb-6">
            <motion.h1 
              className="text-6xl md:text-8xl font-bold tracking-tight"
              initial={{ y: 100 }}
              animate={{ y: 0 }}
              transition={{ duration: 0.8, delay: 0.3, ease: [0.6, 0.05, 0.01, 0.9] }}
            >
              {"Brainchild".split("").map((letter, index) => (
                <motion.span
                  key={index}
                  initial={{ opacity: 0, y: 50 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ 
                    duration: 0.5, 
                    delay: 0.5 + index * 0.05,
                    ease: [0.6, 0.05, 0.01, 0.9]
                  }}
                  className="inline-block bg-linear-to-r from-white via-violet-200 to-purple-300 bg-clip-text text-transparent"
                  style={{ fontFamily: 'Georgia, serif' }}
                >
                  {letter}
                </motion.span>
              ))}
            </motion.h1>
          </div>

          {/* Description with fade and slide */}
          <motion.p 
            className="mt-6 text-zinc-400 max-w-2xl mx-auto text-lg leading-relaxed"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 1 }}
          >
            Born from curiosity, built with precision, and powered by{" "}
            <span className="text-violet-400 font-medium">AI</span> &{" "}
            <span className="text-violet-400 font-medium">embedded systems</span>.
          </motion.p>
        </motion.div>

        {/* Decorative Line */}
        <motion.div 
          className="w-24 h-0.5 bg-linear-to-r from-transparent via-violet-500 to-transparent mx-auto my-4"
          initial={{ scaleX: 0, opacity: 0 }}
          animate={{ scaleX: 1, opacity: 1 }}
          transition={{ duration: 1, delay: 1.2 }}
        />

        {/* Developers Section */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.8, delay: 1.4 }}
          className="mt-2"
        >
          <motion.h2 
            className="text-2xl font-light text-zinc-300 mb-2 tracking-wide"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 1.5 }}
          >
            Meet the Team
          </motion.h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-12 max-w-3xl mx-auto">
            <DeveloperCard
              image="/images/sriram.png"
              name="Sriram"
              role="Backend Developer"
              delay={1.7}
            />

            <DeveloperCard
              image="/images/sumith.jpeg"
              name="Sumith"
              role="Frontend Developer"
              delay={1.9}
            />
          </div>
        </motion.div>

        {/* Special Thanks */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 2.1 }}
          className="mt-20"
        >
          <p className="text-sm tracking-widest text-zinc-500 uppercase mb-3">
            Special Thanks
          </p>
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.6, delay: 2.3 }}
          >
            <p className="text-2xl font-light bg-linear-to-r from-violet-400 to-purple-400 bg-clip-text text-transparent">
              Vijayalakshmi Ma'am & Vedavathi Ma'am
            </p>
          </motion.div>
        </motion.div>

        {/* Footer */}
        <motion.footer 
          className="mt-2 text-sm text-zinc-500 space-y-2"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.8, delay: 2.5 }}
        >
          <p>
            Built by{" "}
            <span className="text-white font-medium">Sriram</span> &{" "}
            <span className="text-white font-medium">Sumith</span>
          </p>
          <p className="text-xl font-semibold text-indigo-700">
            RV College of Engineering — AIML Department (5th Semester)
          </p>
        </motion.footer>
      </div>
    </section>
  );
}

/* ---------------------------------- */
/* Developer Card Component            */
/* ---------------------------------- */

function DeveloperCard({
  image,
  name,
  role,
  delay
}: {
  image: string;
  name: string;
  role: string;
  delay: number;
}) {
  const [isHovered, setIsHovered] = useState(false);

  return (
    <motion.div 
      className="flex flex-col items-center"
      initial={{ opacity: 0, y: 40 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.8, delay }}
      onHoverStart={() => setIsHovered(true)}
      onHoverEnd={() => setIsHovered(false)}
    >
      <motion.div 
        className="relative w-40 h-40 rounded-full overflow-hidden mb-2"
        whileHover={{ scale: 1.05 }}
        transition={{ duration: 0.3 }}
      >
        {/* Animated Ring */}
        <motion.div
          className="absolute inset-0 rounded-full"
          style={{
            background: 'linear-gradient(45deg, #8b5cf6, #a78bfa, #c4b5fd, #8b5cf6)',
            backgroundSize: '300% 300%',
          }}
          animate={{
            backgroundPosition: isHovered ? ['0% 0%', '100% 100%'] : '0% 0%',
            rotate: isHovered ? 360 : 0,
          }}
          transition={{
            backgroundPosition: { duration: 3, repeat: Infinity, ease: "linear" },
            rotate: { duration: 3, ease: "linear" }
          }}
        />
        
        {/* Inner container for image */}
        <div className="absolute inset-[3px] rounded-full overflow-hidden bg-black">
          <img
            src={image}
            alt={name}
            className="w-full h-full object-cover"
          />
        </div>

        {/* Hover Overlay */}
        <motion.div
          className="absolute inset-0 bg-linear-to-t from-violet-500/30 to-transparent"
          initial={{ opacity: 0 }}
          animate={{ opacity: isHovered ? 1 : 0 }}
          transition={{ duration: 0.3 }}
        />
      </motion.div>

      {/* Name Animation */}
      <motion.h3 
        className="text-2xl font-semibold mb-2"
        animate={{ 
          color: isHovered ? '#a78bfa' : '#ffffff'
        }}
        transition={{ duration: 0.3 }}
      >
        {name}
      </motion.h3>

      {/* Role with underline animation */}
      <div className="relative">
        <p className="text-zinc-400 text-sm tracking-wide">
          {role}
        </p>
        <motion.div
          className="absolute left-0 right-0 h-px bg-linear-to-r from-transparent via-violet-400 to-transparent"
          initial={{ scaleX: 0 }}
          animate={{ scaleX: isHovered ? 1 : 0 }}
          transition={{ duration: 0.3 }}
        />
      </div>
    </motion.div>
  );
}