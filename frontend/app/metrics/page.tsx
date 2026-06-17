"use client";

import { useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import MetricCard from "../components/MetricCard";
import { Cpu, Database, Timer,Calendar,Download } from "lucide-react";
import {
  fetchAnomalies,
  fetchMetricReadings,
  MetricReading,
} from "../services/metricService";
import { Anomaly } from "../types/metric";
import AnomaliesTable from "../components/AnomaliesTable";
import api from "../lib/axios";

interface MetricData {
  readings: MetricReading[];
  anomalies: Anomaly[];
}

export default function Metrics() {
  const [cpu, setCpu] = useState<MetricData>({ readings: [], anomalies: [] });
  const [memory, setMemory] = useState<MetricData>({ readings: [], anomalies: [] });
  const [responseTime, setResponseTime] = useState<MetricData>({ readings: [], anomalies: [] });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadData() {
      try {
        const [
          cpuReadings,
          cpuAnomalies,
          memReadings,
          memAnomalies,
          respReadings,
          respAnomalies,
        ] = await Promise.all([
          fetchMetricReadings("cpu_usage"),
          fetchAnomalies("cpu_usage"),
          fetchMetricReadings("memory_usage"),
          fetchAnomalies("memory_usage"),
          fetchMetricReadings("response_time"),
          fetchAnomalies("response_time"),
        ]);
        console.log(cpuReadings)

        setCpu({ readings: cpuReadings, anomalies: cpuAnomalies.anomalies });
        setMemory({ readings: memReadings, anomalies: memAnomalies.anomalies });
        setResponseTime({ readings: respReadings, anomalies: respAnomalies.anomalies });
      } catch (err) {
        setError("Failed to load metrics. Is the backend running?");
        console.error(err);
      } finally {
        setLoading(false);
      }
    }

    loadData();
  }, []);

  const allAnomalies = [...cpu.anomalies, ...memory.anomalies, ...responseTime.anomalies];

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <Navbar />
      <div className="p-8">
        <div className="flex flex-col md:flex-row  md:items-center justify-between mb-6 gap-4">
          <div>
            <h2 className="text-2xl font-bold mb-1">System Performance Metrics</h2>
            <p className="text-slate-400 text-sm">
              Real-time analysis across primary clusters.
            </p>
          </div>

          <div className="flex gap-3">
            <button className="flex items-center gap-2 bg-slate-900 border border-slate-700 rounded-lg px-4 py-2 text-sm text-slate-300">
              <Calendar size={16} />
              Last 24 Hours
            </button>
            <button className="flex items-center gap-2 bg-indigo-500 hover:bg-indigo-600 rounded-lg px-4 py-2 text-sm font-medium">
              <Download size={16} />
              Export Report
            </button>
          </div>
        </div>

        {loading && <div className="flex flex-col gap-6">
    <div className="flex flex-col md:flex-row gap-4">
      {[...Array(3)].map((_, i) => (
        <div key={i} className="bg-slate-900 border border-slate-800 rounded-xl p-5 flex-1 h-48 animate-pulse" />
      ))}
    </div>
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 h-64 animate-pulse" />
  </div>}
        {error && <p className="text-red-400">{error}</p>}

        {!loading && !error && (
          <>
            <div className="flex flex-col md:flex-row gap-4">
              <MetricCard
                title="CPU Usage"
                icon={Cpu}
                unit="%"
                readings={cpu.readings}
                anomalies={cpu.anomalies}
                lineColor="#818cf8"
              />
              <MetricCard
                title="Memory Usage"
                icon={Database}
                unit="%"
                readings={memory.readings}
                anomalies={memory.anomalies}
                lineColor="#4ade80"
              />
              <MetricCard
                title="Response Time"
                icon={Timer}
                unit="ms"
                readings={responseTime.readings}
                anomalies={responseTime.anomalies}
                lineColor="#818cf8"
              />
            </div>

            <AnomaliesTable anomalies={allAnomalies} />
          </>
        )}
        {!loading && !error && cpu.readings.length === 0 && (
            <div className="flex flex-col items-center justify-center py-20 text-center">
              <div className="text-5xl mb-4">📊</div>
              <h3 className="text-xl font-bold mb-2">No metrics yet</h3>
              <p className="text-slate-400 text-sm mb-6">
                Generate mock metrics to see charts and anomaly detection
              </p>
              <button
                onClick={async () => {
                  await api.post("/metrics/generate");
                  window.location.reload();
                }}
                className="bg-indigo-500 hover:bg-indigo-600 rounded-lg px-6 py-2 text-sm font-medium"
              >
                Generate Mock Metrics
              </button>
            </div>
          )}
      </div>
    </div>
  );
}