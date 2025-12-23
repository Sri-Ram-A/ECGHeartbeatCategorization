"use client"

import {
  Area,
  AreaChart,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer
} from "recharts"
import { ScrollableChart } from "./ScrollableChart"

interface EcgPoint {
  index: number
  value: number
}

interface Props {
  data: EcgPoint[]
  title?: string
}

export function EcgAreaChart({ data, title = "Live ECG Signal" }: Props) {
  const chartColor = "#00d4aa" // Modern teal color

  return (
    <div className="bg-gray-900/50 backdrop-blur-xl rounded-2xl border border-gray-800/50 p-6 shadow-2xl">
      {/* Header */}
      <div className="mb-6">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-semibold text-white">{title}</h3>
            <div className="flex items-center gap-4 mt-2">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 rounded-full" style={{ backgroundColor: chartColor }} />
                <span className="text-xs text-gray-400">ECG Signal</span>
              </div>
              <div className="text-xs text-gray-500">
                {data.length} samples • {data.length > 0 ? `Range: ${Math.min(...data.map(d => d.value)).toFixed(1)} - ${Math.max(...data.map(d => d.value)).toFixed(1)}` : 'No data'}
              </div>
            </div>
          </div>
          
          <div className="flex items-center gap-2 px-3 py-1.5 bg-gray-800/50 rounded-lg">
            <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
            <span className="text-xs text-gray-300">Live</span>
          </div>
        </div>
      </div>

      {/* Chart with horizontal scroll */}
      <ScrollableChart>
        <div className="bg-gray-900/30 rounded-xl p-4 border border-gray-800/30">
          <ResponsiveContainer width="100%" height={320}>
            <AreaChart 
              data={data}
              margin={{ top: 10, right: 30, left: 0, bottom: 20 }}
            >
              <defs>
                <linearGradient id="ecgGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor={chartColor} stopOpacity={0.8}/>
                  <stop offset="100%" stopColor={chartColor} stopOpacity={0.1}/>
                </linearGradient>
                <linearGradient id="gridGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#374151" stopOpacity={0.3}/>
                  <stop offset="100%" stopColor="#374151" stopOpacity={0.1}/>
                </linearGradient>
              </defs>
              
              <CartesianGrid 
                strokeDasharray="3 4" 
                stroke="url(#gridGradient)"
                strokeWidth={0.5}
              />
              
              <XAxis 
                dataKey="index" 
                stroke="#6b7280"
                strokeWidth={0.5}
                tick={{ fill: '#9ca3af', fontSize: 11 }}
                tickLine={false}
                axisLine={{ stroke: '#4b5563', strokeWidth: 0.5 }}
              />
              
              <YAxis
                domain={["auto", "auto"]}
                stroke="#6b7280"
                strokeWidth={0.5}
                tick={{ fill: '#9ca3af', fontSize: 11 }}
                tickLine={false}
                axisLine={{ stroke: '#4b5563', strokeWidth: 0.5 }}
                tickFormatter={(value) => value.toFixed(1)}
              />

              <Tooltip
                content={({ active, payload }) => {
                  if (active && payload && payload.length) {
                    return (
                      <div className="bg-gray-900/90 backdrop-blur-sm border border-gray-700 rounded-lg p-3 shadow-2xl">
                        <div className="text-xs text-gray-400">Sample #{payload[0].payload.index}</div>
                        <div className="text-sm font-medium text-white mt-1">
                          {payload[0].value?.toFixed(2) || '0.00'} mV
                        </div>
                      </div>
                    )
                  }
                  return null
                }}
                cursor={{
                  stroke: chartColor,
                  strokeWidth: 1,
                  strokeDasharray: "5 5",
                  strokeOpacity: 0.5
                }}
              />

              <Area
                type="monotone"
                dataKey="value"
                stroke={chartColor}
                strokeWidth={2}
                fill="url(#ecgGradient)"
                isAnimationActive={true}
                animationDuration={300}
                dot={false}
                activeDot={{
                  r: 4,
                  fill: chartColor,
                  stroke: "#ffffff",
                  strokeWidth: 2
                }}
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </ScrollableChart>
    </div>
  )
}