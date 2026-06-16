'use client'
import { useEffect, useState } from "react";
import Navbar from "./components/Navbar";
import StatCard from "./components/StatCard";
import IncidentCard from "./components/IncidentCard";
import Filters from "./components/Filters";
import { AlertTriangle, AlertCircle, Network, Heart } from "lucide-react";
import { dummyStats,dummyIncidents } from "./data/dummyData";
import { fetchIncidents } from "./services/incidentService";
import { BackendIncident } from "./types/incident";
import api from "./lib/axios";

export default function Home() {
  const [incidents,setIncidents] = useState<BackendIncident[]>([]);
  const [filter,setFilter] = useState('all')
  const [loading,setLoading] = useState(true);
  const [error,setError] = useState<string | null>(null);

  const filterIncidents = incidents.filter((incident) => {
    if(filter === 'all') return true
    return incident.ai_summary.severity.toLowerCase() === filter
  })

  useEffect(() => {
    const loadData = async () => {

      try {
        const data = await fetchIncidents();
        console.log("Incidents Data:",data)
        console.log("Incidents length:",data.length)
        setIncidents(data);
      }
      catch(err) {
        setError("Failed to load Incidents"+err);
      }
      finally {
        setLoading(false)
      }

    }

    loadData()

  },[])
  return (
   <div className="min-h-screen bg-slate-950 text-white">
    <Navbar/>
    <div className="p-8">
      <div className="flex gap-4 mb-6">
        <StatCard 
        label="Total Incidents"
        value={dummyStats.totalIncidents}
        icon={AlertTriangle}
        />
        <StatCard
            label="Critical Issues"
            value={dummyStats.criticalIssues}
            icon={AlertCircle}
            iconColor="text-red-400"
            subtext="+2 since last hour"
          />
          <StatCard
            label="Active Services"
            value={dummyStats.activeServices}
            icon={Network}
            subtext="99.9% uptime"
          />
          <StatCard
            label="System Health"
            value={`${dummyStats.systemHealth}%`}
            icon={Heart}
          />

      </div>
       <div className="flex gap-6">
        <div className="w-64">
          <Filters selected={filter} onChange={setFilter} />

        </div>
         <div className="flex flex-1 flex-col gap-4">
          {loading && (
              <p className="text-slate-400">Loading incidents...</p>
            )}

            {error && <p className="text-red-400">{error}</p>}

            {!loading && !error && incidents.length === 0 && (
              <div className="flex flex-col items-center justify-center py-20 text-center">
                <h3 className="text-xl font-bold mb-2">No incidents yet</h3>
                <p className="text-slate-400 text-sm mb-6">
                  Generate some mock logs to see AI analysis in action
                </p>
                <button 
                onClick={async () => {
                  await api.post('/logs/generate');
                  await api.post('/logs/analyse/async')
                  window.location.reload();

                }}
                className="bg-indigo-500 hover:bg-indigo-600 rounded-lg px-6 py-2 text-sm font-medium">
                  Generate Mock Logs
                </button>

              </div>
            )}
          {Array.isArray(incidents) && filterIncidents.map((incident) => (
            <IncidentCard key={incident.cluster_id} incident={{...incident,timestamp:"Just Now"}} />
          ))}
        </div>

       </div>
    </div>
   </div>
  );
}
