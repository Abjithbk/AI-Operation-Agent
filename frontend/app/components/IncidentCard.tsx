'use client'
import React, { useState } from 'react'
import { Sparkles,Wand2,Clock,Bell,BellRing } from 'lucide-react'
import { Incident } from '../types/incident';
import { resendSlackAlert } from '../services/incidentService';

const severityStyles = {
  CRITICAL: {
    badge: "bg-red-500/20 text-red-400 border-red-500/30",
    border: "border-l-red-500",
  },
  HIGH: {
    badge: "bg-orange-500/20 text-orange-400 border-orange-500/30",
    border: "border-l-orange-500",
  },
  MEDIUM: {
    badge: "bg-yellow-500/20 text-yellow-400 border-yellow-500/30",
    border: "border-l-yellow-500",
  },
  LOW: {
    badge: "bg-green-500/20 text-green-400 border-green-500/30",
    border: "border-l-green-500",
  },
};

const IncidentCard = ({incident} : {incident:Incident}) => {
    const styles = severityStyles[incident.ai_summary.severity]
    const [sending,setSending] = useState(false);
    const [sent,setSent] = useState(false)

    const handleSlackAlert = async () => {
      setSending(false)
      try {
        await resendSlackAlert(incident)
        setSent(true)
        setTimeout(() => {
          setSent(false)
        }, 3000);
      }
      catch(err) {
        console.error(err)
      }
      finally {
        setSending(false)
      }
    }
  return (
    <div
      className={`bg-slate-900 border border-slate-800 ${styles.border} border-l-4 rounded-xl p-6`}
    >
      {/* Header row */}
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-3">
          <span
            className={`text-xs font-bold px-2 py-1 rounded border ${styles.badge}`}
          >
            {incident.ai_summary.severity}
          </span>
          <span className="text-xs text-slate-500 flex items-center gap-1">
            <Clock size={12} />
            {incident.timestamp}
          </span>
        </div>
        <span className="text-xs bg-slate-800 text-slate-300 px-3 py-1 rounded-full">
          {incident.log_count} occurrences
        </span>
        <button onClick={handleSlackAlert} disabled={sending} className={`flex items-center gap-2 text-xs px-3 py-1.5 rounded-lg border transition-all ${sent? 'bg-green-500/20 border-green-500/30 text-green-400':'bg-slate-800 border-slate-700 text-slate-300 hover:border-indigo-400 hover:text-indigo-400'}`}>
        {
          sent? (
            <>
            <BellRing size={12} />
            Sent!
            </>
          ):(
            <>
             <Bell size={12} />
             {sending ?'Sending' : 'Slack Alert'}
            </>
          )
        }

        </button>
      </div>

      {/* Title */}
      <h3 className="text-xl font-bold mb-3">{incident.ai_summary.group}</h3>

      {/* AI Summary */}
      <div className="bg-slate-950 border border-slate-800 rounded-lg p-4 mb-3 flex gap-3">
        <Sparkles className="text-indigo-400 flex-shrink-0 mt-0.5" size={18} />
        <p className="text-sm text-slate-300">
          <span className="font-semibold text-white">AI Summary: </span>
          {incident.ai_summary.summary}
        </p>
      </div>

      {/* Recommended Action */}
      <div className="bg-orange-500/5 border border-orange-500/20 rounded-lg p-4 flex gap-3">
        <Wand2 className="text-orange-400 flex-shrink-0 mt-0.5" size={18} />
        <p className="text-sm text-slate-300">
          <span className="font-semibold text-orange-400">
            Recommended Action:{" "}
          </span>
          {incident.ai_summary.suggestion}
        </p>
      </div>
    </div>
  )
}

export default IncidentCard
