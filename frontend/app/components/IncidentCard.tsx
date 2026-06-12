'use client'
import React from 'react'
import { Sparkles,Wand2,Clock } from 'lucide-react'
import { Incident } from '../types/incident';

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
