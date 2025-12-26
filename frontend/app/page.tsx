import Navbar from "@/components/Navbar";
// import IntroSection from "@/components/IntroSection";
import IntroSection from "@/components/IntroSection";
import WhatSection from "@/components/WhatSection";
import { Inter } from "next/font/google";
import FeatureSection from "@/components/FeatureSection";
import AboutSection from "@/components/AboutSection";

const inter = Inter({ subsets: ["latin"] });

export default function Home() {
  return (
    <div className={`bg-white  `}>
      <Navbar />
      <IntroSection />
      <WhatSection />
      <FeatureSection/>
      <AboutSection/>
    </div>
  );
}
