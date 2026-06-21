'use client'
import { useEffect, useState } from "react";
import Navbar from "./components/Navbar";
import StatCard from "./components/StatCard";
import IncidentCard from "./components/IncidentCard";
import Filters from "./components/Filters";
import { AlertTriangle, AlertCircle, Network, Heart } from "lucide-react";
import { fetchIncidents, fetchStats } from "./services/incidentService";
import { BackendIncident } from "./types/incident";
import api from "./lib/axios";
import SkeletonCard from "./components/SkeletonCard";
import { useWebSocket } from "./hooks/useWebSocket";
import toast from "react-hot-toast";

export default function Home() {
  const [incidents,setIncidents] = useState<BackendIncident[]>([]);
  const [filter,setFilter] = useState('all')
  const [stats,setStats] = useState({
    total_incidents: 0,
    critical_issues:0,
    active_services: 0,
    system_health: 100,
  })
  const [loading,setLoading] = useState(true);
  const [error,setError] = useState<string | null>(null);

  const filterIncidents = incidents.filter((incident) => {
    if(filter === 'all') return true
    return incident.ai_summary.severity.toLowerCase() === filter
  })

  const {isConnected,onMessage} = useWebSocket()

  useEffect(() => {
    const loadData = async () => {
      try {
        const data = await fetchIncidents();
        const statData = await fetchStats()
        setStats(statData)
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

  useEffect(() => {
    onMessage((message) => {
      if(message.type === 'new_incident') {
        const newIncident = message.data;

        setIncidents((prev) => [newIncident,...prev]);

        setStats((prev) => ({
          ...prev,
          total_incidents:prev.total_incidents + 1,
          critical_issues:prev.critical_issues+ (newIncident.ai_summary.severity === 'CRITICAL'? 1: 0),
        }))
        const severity = newIncident.ai_summary.severity;
      toast.success(`New ${severity} incident detected!`, {
        icon: severity === 'CRITICAL' ? '🚨' : '⚠️',
        duration: 5000,
      });
      }
    })
  },[onMessage])
  return (
   <div className="min-h-screen bg-slate-950 text-white">
    <Navbar/>
    {
      loading ? (
        <div className="flex flex-col gap-4">
          <div className="gird grid-cols-2 md:grid-cols-4 gap-4mb6
          ">
            {
              [...Array(4).map((_,i) => (
                <div key={i} className="bg-slate-900 border border-slate-800 rounded-xl p-5 h-28 animate-pulse" />
              ))]
            }

          </div>
          <div className="flex flex-col gap-4">
            <SkeletonCard />
            <SkeletonCard />
            <SkeletonCard />
          </div>

        </div>
      ) : (
        <div className="p-4 sm:p-6 lg:p-8">
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <StatCard 
        label="Total Incidents"
        value={stats.total_incidents}
        icon={AlertTriangle}
        />
        <StatCard
            label="Critical Issues"
            value={stats.critical_issues}
            icon={AlertCircle}
            iconColor="text-red-400"
            subtext="+2 since last hour"
          />
          <StatCard
            label="Active Services"
            value={stats.active_services}
            icon={Network}
            subtext="99.9% uptime"
          />
          <StatCard
            label="System Health"
            value={`${stats.system_health}%`}
            icon={Heart}
          />

      </div>
       <div className="flex flex-col md:flex-row gap-6">
        <div className="w-full md:w-64">
          <Filters selected={filter} onChange={setFilter} />

        </div>
         <div className="flex flex-1 flex-col gap-4">
          {loading && (
              <div className="flex flex-col gap-4">
                <SkeletonCard />
                <SkeletonCard />
                <SkeletonCard />
              </div>
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
      )
    }
   </div>
  );
}
