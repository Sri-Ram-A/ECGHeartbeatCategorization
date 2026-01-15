"use client"

import { useState, useMemo, useEffect } from "react"
import { WifiOff, LogOut, PlayCircle, StopCircle, AlertCircle, TrendingUp, Search, Eye, HeartPulse, ClipboardList, } from "lucide-react"
import { motion, AnimatePresence } from "framer-motion"
import { toast } from "sonner"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Dialog, DialogContent, DialogTitle } from "@/components/ui/dialog"
import { Input } from "@/components/custom/Input"
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts"

// Hooks & Services
import { useWebSocket } from "@/hooks/useWebSocket"
import { getSession } from "@/lib/session"
import makeRequest from "@/services/request"
import { BACKEND_WS_URL } from "@/services/api"

/* ===================== TYPES ===================== */
interface Patient {
  id: number
  full_name: string
  phone_number: string
  dob: string
  last_visit?: string
}

/* ===================== LOGIC HOOKS ===================== */

/**
 * Handles the logic for streaming ECG data and managing WebSocket state
 */
const useEcgSession = (doctorId: number | null, patientId: number | null) => {
  const [ecgData, setEcgData] = useState<{ time: number; ecg: number }[]>([])
  const [isStreaming, setIsStreaming] = useState(false)
  const [prediction, setPrediction] = useState<{ label: string; conf: number } | null>(null)
  const [sampleIndex, setSampleIndex] = useState(0)

  const wsUrl = useMemo(
    () => (doctorId && patientId ? `${BACKEND_WS_URL}/ws/ecg/${doctorId}/${patientId}/` : ""),
    [doctorId, patientId],
  )

  const { connect, disconnect, isConnected } = useWebSocket({
    url: wsUrl,
    autoConnect: false,
    onOpen: () => {
      toast.success("Live Connection Established")
      setIsStreaming(true)
    },
    onClose: () => setIsStreaming(false),
    onMessage: (payload) => {
      if (payload?.values) {
        setEcgData((prev) => {
          const next = payload.values.map((v: number, i: number) => ({
            time: sampleIndex + i,
            ecg: v,
          }))
          return [...prev, ...next].slice(-300)
        })
        setSampleIndex((i) => i + payload.values.length)
      }
      if (payload?.prediction) {
        setPrediction({ label: payload.prediction, conf: payload.confidence })
      }
    },
  })

  const startSession = async () => {
    try {
      await makeRequest({ method: "POST", path: `mqtt/start/${doctorId}/${patientId}` })
      connect()
    } catch (err) {
      toast.error("Failed to start MQTT stream")
    }
  }

  const stopSession = async () => {
    await makeRequest({ method: "POST", path: `mqtt/stop/${doctorId}/${patientId}` })
    disconnect()
    setEcgData([])
    setPrediction(null)
    setSampleIndex(0)
  }

  return { ecgData, isStreaming, isConnected, prediction, startSession, stopSession }
}

/* ===================== COMPONENTS ===================== */

export default function PremiumECGDashboard() {
  const [doctor, setDoctor] = useState<{ id: number; name: string } | null>(null)
  const [patients, setPatients] = useState<Patient[]>([])
  const [searchQuery, setSearchQuery] = useState("")
  const [selectedPatient, setSelectedPatient] = useState<Patient | null>(null)
  const [isModalOpen, setIsModalOpen] = useState(false)

  const { ecgData, isStreaming, isConnected, prediction, startSession, stopSession } = useEcgSession(
    doctor?.id || null,
    selectedPatient?.id || null,
  )

  // Auth & Data Fetching
  useEffect(() => {
    const session = getSession()
    if (session) setDoctor({ id: session.id, name: session.full_name })

    makeRequest({ method: "GET", path: "patients" }).then((res) => setPatients(res.patients || []))
  }, [])

  const filteredPatients = patients.filter((p) => p.full_name.toLowerCase().includes(searchQuery.toLowerCase()))

  const handleOpenMonitor = (patient: Patient) => {
    setSelectedPatient(patient)
    setIsModalOpen(true)
  }

  const handleCloseMonitor = () => {
    if (isStreaming) stopSession()
    setIsModalOpen(false)
  }

  return (
    <div className="min-h-screen bg-linear-to-br from-slate-900 via-slate-950 to-slate-900 text-slate-50 font-sans">
      {/* Background linear Accents */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden">
        <div className="absolute top-20 right-0 w-[600px] h-[600px] bg-indigo-600/5 rounded-full blur-3xl" />
        <div className="absolute bottom-40 left-0 w-[500px] h-[500px] bg-cyan-600/5 rounded-full blur-3xl" />
      </div>

      {/* 1. TOP NAVIGATION */}
      <header className="sticky top-0 z-50 w-full border-b border-slate-800/50 backdrop-blur-md bg-slate-950/80">
        <div className="max-w-[1400px] mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-linear-to-br from-indigo-500 to-cyan-500 flex items-center justify-center shadow-lg">
              <HeartPulse className="text-white w-5 h-5" />
            </div>
            <div>
              <h1 className="text-lg font-bold tracking-tight text-white">Med AI</h1>
              <p className="text-[10px] text-slate-400 uppercase font-semibold">Clinical Monitoring</p>
            </div>
          </div>

          <div className="flex items-center gap-4">
            <div className="hidden md:flex flex-col items-end">
              <span className="text-sm font-medium text-slate-200">{doctor?.name}</span>
              <span className="text-xs text-slate-500">Cardiologist ID: {doctor?.id}</span>
            </div>
            <Button variant="ghost" size="icon" className="rounded-full hover:bg-slate-800">
              <LogOut className="w-5 h-5 text-slate-400" />
            </Button>
          </div>
        </div>
      </header>

      <main className="max-w-[1400px] mx-auto p-6 space-y-6 relative z-10">
        {/* 2. PATIENT TABLE CARD */}
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}>
          <Card className="border-slate-800/60 bg-slate-900/40 backdrop-blur-xl shadow-2xl overflow-hidden">
            <CardHeader className="flex md:flex-row flex-col md:items-center justify-between gap-4 border-b border-slate-800/40 pb-6">
              <div>
                <CardTitle className="text-xl text-white flex items-center gap-2">
                  <ClipboardList className="w-5 h-5 text-indigo-400" />
                  Patient Directory
                </CardTitle>
                <CardDescription className="text-slate-400 mt-1">Select a patient to begin monitoring</CardDescription>
              </div>
              <div className="relative w-full md:w-80">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
                <Input
                  id="input-search"
                  placeholder="Search by name..."
                  className="pl-9 bg-slate-800/50 border-slate-700/50 text-slate-100 placeholder:text-slate-500 focus:border-indigo-500/50 focus:ring-indigo-500/20"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                />
              </div>
            </CardHeader>
            <CardContent className="p-0">
              <Table>
                <TableHeader className="bg-slate-800/30 border-b border-slate-800/40">
                  <TableRow className="hover:bg-transparent">
                    <TableHead className="text-slate-400 font-semibold w-20">ID</TableHead>
                    <TableHead className="text-slate-400 font-semibold">Patient Name</TableHead>
                    <TableHead className="text-slate-400 font-semibold">DOB</TableHead>
                    <TableHead className="text-slate-400 font-semibold">Contact</TableHead>
                    <TableHead className="text-right text-slate-400 font-semibold">Action</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredPatients.map((p) => (
                    <motion.tr
                      key={p.id}
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      className="border-b border-slate-800/30 hover:bg-slate-800/20 transition-colors"
                    >
                      <TableCell className="py-4 px-6">
                        <Badge variant="secondary" className="bg-slate-700/50 text-slate-300 font-mono text-xs">
                          #{p.id}
                        </Badge>
                      </TableCell>
                      <TableCell className="py-4 px-6">
                        <div className="flex items-center gap-3">
                          <img
                            src={`https://api.dicebear.com/7.x/avataaars/svg?seed=${p.full_name}`}
                            alt={p.full_name}
                            className="w-9 h-9 rounded-full ring-2 ring-indigo-500/30"
                          />
                          <span className="font-medium text-slate-100">{p.full_name}</span>
                        </div>
                      </TableCell>
                      <TableCell className="py-4 px-6 text-slate-400 text-sm">{p.dob}</TableCell>
                      <TableCell className="py-4 px-6 text-slate-400 text-sm">{p.phone_number}</TableCell>
                      <TableCell className="py-4 px-6 text-right">
                        <Button
                          size="sm"
                          className="gap-2 bg-indigo-600 hover:bg-indigo-700 text-white shadow-lg hover:shadow-indigo-600/20"
                          onClick={() => handleOpenMonitor(p)}
                        >
                          <Eye className="w-4 h-4" /> Monitor
                        </Button>
                      </TableCell>
                    </motion.tr>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </motion.div>
      </main>

      {/* 3. PREMIUM ECG MONITOR MODAL */}
      <Dialog open={isModalOpen} onOpenChange={handleCloseMonitor}>
        <DialogContent className="max-w-8xl h-[90vh] flex flex-col p-0 overflow-hidden bg-slate-950 border-slate-800/60 shadow-2xl">
          <div className="p-6 bg-linear-to-r from-slate-900 to-slate-950 border-b border-slate-800/50 flex flex-row items-center justify-between">
            <div className="flex items-center gap-4">
              <motion.div
                animate={{ scale: isConnected ? [1, 1.1, 1] : 1 }}
                transition={{ duration: 2, repeat: Number.POSITIVE_INFINITY }}
                className="w-12 h-12 rounded-full bg-indigo-500/20 flex items-center justify-center border border-indigo-500/40 shadow-lg shadow-indigo-500/10"
              >
                <HeartPulse className="text-indigo-400 w-6 h-6" />
              </motion.div>
              <div>
                <DialogTitle className="text-white text-xl font-bold">{selectedPatient?.full_name}</DialogTitle>
                <div className="flex gap-2 mt-2">
                  <Badge variant="outline" className="text-slate-400 border-slate-700 bg-slate-800/50">
                    ID: {selectedPatient?.id}
                  </Badge>
                  <Badge
                    className={`font-semibold ${isConnected ? "bg-emerald-500/20 text-emerald-400 border-emerald-500/30 border" : "bg-red-500/20 text-red-400 border-red-500/30 border"}`}
                  >
                    {isConnected ? "● CONNECTED" : "● DISCONNECTED"}
                  </Badge>
                </div>
              </div>
            </div>

            <div className="flex gap-3">
              {!isStreaming ? (
                <Button
                  onClick={startSession}
                  className="bg-linear-to-r from-indigo-600 to-indigo-700 hover:from-indigo-700 hover:to-indigo-800 gap-2 shadow-lg hover:shadow-indigo-600/30"
                >
                  <PlayCircle className="w-4 h-4" /> Start
                </Button>
              ) : (
                <Button
                  onClick={stopSession}
                  variant="destructive"
                  className="gap-2 bg-red-600/80 hover:bg-red-700 shadow-lg hover:shadow-red-600/20"
                >
                  <StopCircle className="w-4 h-4" /> Stop
                </Button>
              )}
            </div>
          </div>

          <div className="flex-1 p-6 flex flex-col gap-6 overflow-y-auto">
            <div className="bg-slate-900/50 border border-slate-800/60 rounded-2xl p-4 flex-1 min-h-[400px] shadow-xl">
              <div className="flex items-center justify-between mb-4">
                <span className="text-xs font-bold text-indigo-300 flex items-center gap-2 uppercase tracking-wider">
                  <motion.div
                    animate={{ scale: [1, 1.2, 1] }}
                    transition={{ duration: 1, repeat: Number.POSITIVE_INFINITY }}
                    className="w-2 h-2 rounded-full bg-indigo-500"
                  />
                  Live ECG Feed (II)
                </span>
                <span className="text-[10px] text-slate-500 font-mono">25mm/sec • 10mm/mV</span>
              </div>

              <div className="h-full w-full">
                {ecgData.length > 0 ? (
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={ecgData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                      <CartesianGrid stroke="rgba(71, 85, 105, 0.2)" strokeDasharray="4 4" vertical={false} />
                      <XAxis hide dataKey="time" />
                      <YAxis domain={[-2, 2]} stroke="rgba(71, 85, 105, 0.4)" fontSize={10} width={30} />
                      <Tooltip
                        contentStyle={{
                          backgroundColor: "rgba(15, 23, 42, 0.95)",
                          border: "1px solid rgba(71, 85, 105, 0.3)",
                          borderRadius: "8px",
                        }}
                        labelStyle={{ color: "#cbd5e1" }}
                      />
                      <Line
                        type="monotone"
                        dataKey="ecg"
                        stroke="rgb(99, 102, 241)"
                        strokeWidth={2.5}
                        dot={false}
                        isAnimationActive={false}
                        fill="url(#ecgFill)"
                      />
                    </LineChart>
                  </ResponsiveContainer>
                ) : (
                  <div className="h-full flex flex-col items-center justify-center text-slate-500 space-y-4">
                    <motion.div
                      animate={{ scale: [1, 1.1, 1] }}
                      transition={{ duration: 2, repeat: Number.POSITIVE_INFINITY }}
                      className="w-20 h-20 rounded-full border-2 border-dashed border-slate-700/40 flex items-center justify-center"
                    >
                      <WifiOff className="w-8 h-8 opacity-30" />
                    </motion.div>
                    <p className="text-sm">Press "Start" to receive signal</p>
                  </div>
                )}
              </div>
            </div>

            <AnimatePresence>
              {prediction && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: 20 }}
                  className="bg-indigo-500/10 border border-indigo-500/30 rounded-xl p-5 backdrop-blur-sm shadow-lg"
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <motion.div
                        animate={{ rotate: 360 }}
                        transition={{ duration: 2, repeat: Number.POSITIVE_INFINITY }}
                      >
                        <AlertCircle className="text-indigo-400 w-6 h-6" />
                      </motion.div>
                      <div>
                        <p className="text-xs text-indigo-300/80 uppercase tracking-wider font-semibold">
                          Analysis Result
                        </p>
                        <p className="text-xl font-bold text-white mt-1">{prediction.label}</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="text-xs text-indigo-300/80 uppercase tracking-wider font-semibold mb-2">
                        Confidence
                      </p>
                      <div className="flex items-center gap-2 text-white font-mono font-bold text-lg">
                        <TrendingUp className="w-5 h-5 text-emerald-400" />
                        {(prediction.conf * 100).toFixed(1)}%
                      </div>
                    </div>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  )
}
