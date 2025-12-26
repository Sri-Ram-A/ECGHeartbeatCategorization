"use client"

import { useEffect, useMemo, useState } from "react"
import { useRouter } from "next/navigation"
import { motion } from "framer-motion"

import { getSession } from "@/lib/session"
import makeRequest from "@/services/request"
import { notifySuccess, notifyWarn } from "@/lib/notify"
import { useWebSocket } from "@/lib/useWebSocket"

import { Button } from "@/components/ui/Button"
import { Table, Column } from "@/components/ui/Table"
import { Spotlight } from "@/components/ui/spotlight"
import { EcgAreaChart } from "@/components/ui/EcgAreaChart"
import {BACKEND_WS_URL}  from "@/services/api"
interface Patient {
    id: number
    full_name: string
    phone_number: string
    dob: string
}

interface EcgPoint {
    index: number
    value: number
}

interface Doctor {
    id: number
    name: string
}

/* ---------------- AUTH ---------------- */
const useAuth = () => {
    const router = useRouter()
    const [doctor, setDoctor] = useState<Doctor | null>(null)

    useEffect(() => {
        const session = getSession()
        if (!session) {
            router.push("/login/doctor")
            return
        }
        setDoctor({ id: session.id, name: session.full_name })
    }, [router])

    return doctor
}

/* ---------------- DATA ---------------- */
const usePatients = () => {
    const [patients, setPatients] = useState<Patient[]>([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        ; (async () => {
            try {
                const res = await makeRequest({ method: "GET", path: "patients" })
                setPatients(res.patients ?? [])
            } finally {
                setLoading(false)
            }
        })()
    }, [])

    return { patients, loading }
}

export default function DashboardPage() {
    const router = useRouter()
    const doctor = useAuth()
    const { patients, loading } = usePatients()

    /* ---------------- ECG STATE ---------------- */
    const [selectedPatientId, setSelectedPatientId] = useState<number | null>(null)
    const [ecgData, setEcgData] = useState<EcgPoint[]>([])
    const [sampleIndex, setSampleIndex] = useState(0)
    const [isStreaming, setIsStreaming] = useState(false)

    const selectedPatient = patients.find(p => p.id === selectedPatientId)

    /* ---------------- WS URL ---------------- */
    const wsUrl = useMemo(() => {
        if (!doctor || !selectedPatientId) return ""
        return `${BACKEND_WS_URL}/ws/ecg/${doctor.id}/${selectedPatientId}/`
    }, [doctor, selectedPatientId])

    /* ---------------- WEBSOCKET ---------------- */
    const { connect, disconnect, isConnected } = useWebSocket({
        url: wsUrl,
        autoConnect: false,

        onOpen: () => {
            notifySuccess("Live ECG connected")
            setIsStreaming(true)
        },

        onClose: () => {
            notifyWarn("Live ECG disconnected")
            setIsStreaming(false)
        },

        onMessage: (payload) => {
            if (!payload?.values?.length) return

            setEcgData(prev => {
                const next = payload.values.map((v: number, i: number) => ({
                    index: sampleIndex + i,
                    value: v,
                }))
                return [...prev, ...next].slice(-2000)
            })

            setSampleIndex(i => i + payload.values.length)
        },
    })

    /* ---------------- MQTT ---------------- */
    const startStreaming = async () => {
        if (!doctor || !selectedPatientId) {
            notifyWarn("Select a patient first")
            return
        }

        await makeRequest({
            method: "POST",
            path: `mqtt/start/${doctor.id}/${selectedPatientId}`,
        })

        notifySuccess("Streaming started")
    }

    const stopStreaming = async () => {
        if (!doctor || !selectedPatientId) return

        await makeRequest({
            method: "POST",
            path: `mqtt/stop/${doctor.id}/${selectedPatientId}`,
        })

        disconnect()
        setEcgData([])
        setSampleIndex(0)
        setIsStreaming(false)
        notifySuccess("Streaming stopped")
    }

    /* ---------------- LOADING ---------------- */
    if (loading || !doctor) {
        return (
            <div className="min-h-screen flex items-center justify-center bg-black">
                <div className="w-12 h-12 border-4 border-cyan-500/30 border-t-cyan-500 rounded-full animate-spin" />
            </div>
        )
    }

    return (
        <div className="min-h-screen bg-black text-gray-100 relative overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-br from-cyan-900/20 via-transparent to-black" />
            <div className="absolute inset-0 bg-[linear-gradient(to_right,#1f2937_1px,transparent_1px),linear-gradient(to_bottom,#1f2937_1px,transparent_1px)] bg-[size:4rem_4rem] opacity-20" />
            <Spotlight className="-top-40 left-20" fill="white" />

            {/* HEADER */}
            <header className="sticky top-0 z-40 backdrop-blur bg-gray-900/50 border-b border-gray-800">
                <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between">
                    <div>
                        <h1 className="text-lg font-semibold">ECG Monitoring</h1>
                        <p className="text-sm text-gray-400">
                            Dr. {doctor.name} · ID {doctor.id}
                        </p>
                    </div>

                    <div className="flex items-center gap-4">
                        <span className="text-xs flex items-center gap-2">
                            <span className={`w-2 h-2 rounded-full ${isStreaming ? "bg-green-500 animate-pulse" : "bg-gray-500"}`} />
                            {isStreaming ? "Live" : "Idle"}
                        </span>

                        <Button onClick={() => router.push("/login/doctor")}>
                            Logout
                        </Button>
                    </div>
                </div>
            </header>

            {/* MAIN */}
            <main className="max-w-7xl mx-auto px-6 py-8 space-y-8 relative z-10">

                {/* CONTROLS */}
                <div className="flex flex-wrap gap-4 items-center">
                    <Button
                        onClick={startStreaming}
                        disabled={!selectedPatientId || isStreaming}
                        className="bg-green-600 hover:bg-green-500"
                    >
                        Start Streaming
                    </Button>

                    <Button
                        onClick={stopStreaming}
                        disabled={!isStreaming}
                        className="bg-red-700 hover:bg-red-500"
                    >
                        Stop Streaming
                    </Button>

                    <Button
                        onClick={connect}
                        disabled={!selectedPatientId || isConnected}
                        className="bg-blue-600 hover:bg-blue-500"
                    >
                        {isConnected ? "Live View Active" : "View Live ECG"}
                    </Button>

                    {selectedPatient && (
                        <span className="text-sm text-gray-400">
                            Patient: <span className="text-white">{selectedPatient.full_name}</span>
                        </span>
                    )}
                </div>

                {/* PATIENT TABLE */}
                <Table
                    data={patients}
                    rowKey={(r) => r.id}
                    columns={[
                        {
                            key: "select",
                            label: "",
                            render: (r) => (
                                <input
                                    type="radio"
                                    checked={selectedPatientId === r.id}
                                    onChange={() => setSelectedPatientId(r.id)}
                                    className="accent-cyan-500"
                                />
                            ),
                        },
                        { key: "id", label: "ID", render: r => `#${r.id}` },
                        { key: "full_name", label: "Name" },
                        { key: "phone_number", label: "Phone" },
                        { key: "dob", label: "DOB" },
                    ] as Column<Patient>[]}
                />

                {/* ECG */}
                {isConnected && (
                    <motion.div
                        initial={{ opacity: 0, y: 16 }}
                        animate={{ opacity: 1, y: 0 }}
                    >
                        <EcgAreaChart data={ecgData} />
                    </motion.div>
                )}
            </main>
        </div>
    )
}
