"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { useRouter } from "next/navigation";
import { getSession } from "@/lib/session";
import makeRequest, { postMqttRequest } from "@/services/request";
import { toast } from "react-toastify";
import { Spotlight } from "@/components/ui/spotlight";
import Image from "next/image";

interface Patient {
    id: number;
    full_name: string;
    phone_number: string;
    dob: string;
}

export default function DashboardPage() {
    const router = useRouter();
    const [patients, setPatients] = useState<Patient[]>([]);
    const [doctorName, setDoctorName] = useState("");
    const [doctorID, setDoctorID] = useState(0);
    const [loading, setLoading] = useState(true);
    const [selectedPatientId, setSelectedPatientId] = useState<number | null>(null);

    useEffect(() => {
        (async () => {
            const session = getSession();
            if (!session) return router.push("/login/doctor");
            setDoctorName(session.full_name);
            setDoctorID(session.user_id);
            const res = await makeRequest("GET", "patients");
            setPatients(res.patients ?? []);
            setLoading(false);
        })();
    }, [router]);

    const startStreaming = async () => {
        if (!selectedPatientId) {
            toast.warn("Please select a patient to start streaming.");
            return;
        }
        const session = getSession();
        if (!session) return router.push("/login/doctor");
        await postMqttRequest(`start/${session.user_id}/${selectedPatientId}`)
        toast.success("Started Streaming");
        console.log("Streaming started");
    };
    const stopStreaming = async () => {
        if (!selectedPatientId) {
            toast.warn("Please select a patient to start streaming.");
            return;
        }
        const session = getSession();
        if (!session) return router.push("/login/doctor");
        await postMqttRequest(`stop/${session.user_id}/${selectedPatientId}`);
        console.log("Streaming stopped");
        toast.success("Successfully finished streaming");

    };
    return (
        <div className="min-h-screen bg-black text-gray-100 relative overflow-hidden">
            {/* Skeleton Loading */}
            {loading && (
                <div className="fixed inset-0 z-50 flex flex-col items-center justify-center pointer-events-none">
                    <div className="w-12 h-12 border-4 border-blue-500/30 
                        border-t-blue-500 rounded-full animate-spin" />
                    <p className="mt-4 text-sm text-gray-400 tracking-wide">
                        Loading patients…
                    </p>
                </div>
            )}

            <div className="absolute inset-0 bg-gradient-to-br 
                    from-blue-900/45 via-blue-700/10 to-transparent" />
            {/* Image as background */}
            <Image
                src="/whale.png"
                alt="ECG background"
                fill
                priority
                className="object-contain opacity-40"
            />
            <Spotlight
                className="-top-40 left-0 md:-top-20 md:left-60"
                fill="white"
            />
            {/* Content above Image */}
            <div className="relative z-10">

                <header className="sticky top-0 z-50 border-b border-gray-800/60 bg-gray-900/80 backdrop-blur-xl">
                    <div className="max-w-6xl mx-auto px-6 py-4 flex justify-between items-center">
                        <div>
                            <h1 className="text-lg font-semibold tracking-wide">
                                ECG Monitoring Dashboard
                            </h1>
                            <p className="text-sm text-gray-400">
                                Welcome back, <span className="text-gray-200">Dr. {doctorName}</span>
                            </p>
                            <p>
                                Your ID : <span className="text-gray-400">{doctorID}</span>
                            </p>
                        </div>

                        <button className="px-4 py-2 text-sm rounded-lg border border-gray-700/60 
                       bg-gradient-to-br from-gray-800 to-gray-900
                       hover:from-gray-700 hover:to-gray-800 transition">
                            Logout
                        </button>
                    </div>
                </header>


                <main className="max-w-6xl mx-auto p-6">


                    {!loading && patients.length === 0 && (
                        <p className="text-gray-500">No patients found.</p>
                    )}

                    {/* Start and Stop Buttons */}
                    <div className="flex gap-4 mb-6">
                        {/* Start Streaming */}
                        <button
                            onClick={startStreaming}
                            disabled={!selectedPatientId}
                            className={` px-5 py-2 rounded-lg text-sm font-medium transition 
                            ${selectedPatientId ? "bg-blue-600 hover:bg-blue-500 text-white" : "bg-blue-600/40 text-blue-200 cursor-not-allowed"} `}>
                            Start Streaming
                        </button>

                        {/* Stop Streaming */}
                        <button
                            onClick={stopStreaming}
                            disabled={!selectedPatientId}
                            className={`
                                px-5 py-2 rounded-lg text-sm font-medium border transition
                                ${selectedPatientId ? "border-gray-500 text-gray-200 hover:bg-gray-800" : "border-gray-700 text-gray-500 cursor-not-allowed"} `}>
                            ■   Stop Streaming
                        </button>
                    </div>


                    {/* Table of Patients */}
                    {patients.length > 0 && (
                        <div className="overflow-hidden rounded-xl border border-gray-800/60 bg-gradient-to-br from-gray-900/70 to-gray-800/40 shadow-xl">
                            <table className="w-full text-sm">

                                <thead className="bg-gray-900/80 text-gray-400 text-xs uppercase tracking-wider">
                                    <tr>
                                        <th className="p-4 text-left"></th>
                                        <th className="p-4 text-center">ID</th>
                                        <th className="p-4 text-left">Patient</th>
                                        <th className="p-4 text-left">Phone</th>
                                        <th className="p-4 text-left">DOB</th>
                                    </tr>
                                </thead>

                                <tbody >
                                    {patients.map((p, i) => (
                                        <motion.tr
                                            key={p.id}
                                            initial={{ opacity: 0, y: 6 }}
                                            animate={{ opacity: 1, y: 0 }}
                                            transition={{ delay: i * 0.04 }}
                                            className={`
                                            border-t border-gray-800/50
                                            transition-colors
                                            hover:bg-blue-900/20 
                                            ${selectedPatientId === p.id ? "bg-blue-900/20 ring-1 ring-blue-600/30" : ""}`}
                                        >
                                            <td className="p-4">
                                                <input
                                                    type="radio"
                                                    name="selectedPatient"
                                                    checked={selectedPatientId === p.id}
                                                    onChange={() => setSelectedPatientId(p.id)}
                                                    className="w-4 h-4 accent-blue-600 cursor-pointer"
                                                />
                                            </td>
                                            <td className="p-4 text-center">#{p.id}</td>
                                            <td className="p-4 font-medium text-gray-100">{p.full_name}</td>
                                            <td className="p-4 font-mono">{p.phone_number}</td>
                                            <td className="p-4">{p.dob}</td>
                                        </motion.tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    )}
                </main>
            </div>
        </div>
    );
}
