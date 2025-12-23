"use client"

import React, { useRef, useEffect, useState } from "react"
import { motion } from "framer-motion"

interface ScrollableChartProps {
  children: React.ReactNode
  className?: string
}

export function ScrollableChart({ children, className = "" }: ScrollableChartProps) {
  const containerRef = useRef<HTMLDivElement>(null)
  const [scrollLeft, setScrollLeft] = useState(0)
  const [maxScroll, setMaxScroll] = useState(0)

  useEffect(() => {
    if (containerRef.current) {
      const { scrollWidth, clientWidth } = containerRef.current
      setMaxScroll(scrollWidth - clientWidth)
    }
  }, [children])

  const scroll = (direction: "left" | "right") => {
    if (!containerRef.current) return
    
    const scrollAmount = 200
    const newScrollLeft = direction === "left" 
      ? Math.max(0, scrollLeft - scrollAmount)
      : Math.min(maxScroll, scrollLeft + scrollAmount)
    
    containerRef.current.scrollLeft = newScrollLeft
    setScrollLeft(newScrollLeft)
  }

  return (
    <div className={`relative ${className}`}>
      {/* Scroll buttons */}
      {scrollLeft > 0 && (
        <button
          onClick={() => scroll("left")}
          className="absolute left-2 top-1/2 -translate-y-1/2 z-10 w-8 h-8 bg-gray-900/80 backdrop-blur-sm rounded-full flex items-center justify-center text-gray-400 hover:text-white hover:bg-gray-800 border border-gray-700 transition-all"
        >
          ←
        </button>
      )}
      
      {scrollLeft < maxScroll && maxScroll > 0 && (
        <button
          onClick={() => scroll("right")}
          className="absolute right-2 top-1/2 -translate-y-1/2 z-10 w-8 h-8 bg-gray-900/80 backdrop-blur-sm rounded-full flex items-center justify-center text-gray-400 hover:text-white hover:bg-gray-800 border border-gray-700 transition-all"
        >
          →
        </button>
      )}

      {/* Chart container with scroll */}
      <div
        ref={containerRef}
        className="overflow-x-auto scrollbar-thin scrollbar-thumb-gray-700 scrollbar-track-transparent"
        style={{ scrollBehavior: 'smooth' }}
      >
        <div className="min-w-[800px]">
          {children}
        </div>
      </div>

      {/* Scroll indicator */}
      {maxScroll > 0 && (
        <div className="flex items-center justify-center mt-3 space-x-1">
          <div className="text-xs text-gray-500">
            Scroll horizontally to explore ECG data →
          </div>
        </div>
      )}
    </div>
  )
}