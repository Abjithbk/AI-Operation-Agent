"use client";

import { useState } from "react";
import { AlertTriangle } from "lucide-react";
import { Anomaly } from "../types/metric";

const statusColor = {
  INVESTIGATING: "bg-orange-500/20 text-orange-400 border-orange-500/30",
  RESOLVED: "bg-green-500/20 text-green-400 border-green-500/30",
};

export default function AnomaliesTable({ anomalies }: { anomalies: Anomaly[] }) {
  const [page, setPage] = useState(1);
  const perPage = 5;
  const totalPages = Math.ceil(anomalies.length / perPage);
  const paginated = anomalies.slice((page - 1) * perPage, page * perPage);

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 mt-6">
      <div className="flex items-center gap-2 mb-4">
        <AlertTriangle className="text-orange-400" size={20} />
        <h3 className="font-bold text-lg">Anomalies Detected</h3>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left text-slate-400 uppercase text-xs border-b border-slate-800">
              <th className="py-3 pr-4">Timestamp</th>
              <th className="py-3 pr-4">Metric Name</th>
              <th className="py-3 pr-4">Value</th>
              <th className="py-3 pr-4">Service</th>
              <th className="py-3 pr-4">Status</th>
            </tr>
          </thead>
          <tbody>
            {anomalies.length === 0 && (
              <tr>
                <td colSpan={5} className="py-6 text-center text-slate-500">
                  No anomalies detected.
                </td>
              </tr>
            )}
            {paginated.map((anomaly, idx) => (
              <tr key={idx} className="border-b border-slate-800/50">
                <td className="py-3 pr-4 text-slate-300">
                  {new Date(anomaly.timestamp).toLocaleString()}
                </td>
                <td className="py-3 pr-4 text-slate-300 capitalize">
                  {anomaly.metric_name.replace("_", " ")}
                </td>
                <td className="py-3 pr-4 font-bold text-orange-400">
                  {anomaly.value}
                </td>
                <td className="py-3 pr-4 text-slate-300">{anomaly.service}</td>
                <td className="py-3 pr-4">
                  <span className={`text-xs font-bold px-2 py-1 rounded border ${statusColor.INVESTIGATING}`}>
                    {anomaly.status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="flex items-center justify-between mt-4 text-sm text-slate-400">
        <span>{anomalies.length} total anomalies</span>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setPage(p => Math.max(1, p - 1))}
            disabled={page === 1}
            className="px-3 py-1 bg-slate-800 rounded-lg disabled:opacity-50 hover:bg-slate-700"
          >
            Prev
          </button>
          <span>{page} / {totalPages}</span>
          <button
            onClick={() => setPage(p => Math.min(totalPages, p + 1))}
            disabled={page === totalPages}
            className="px-3 py-1 bg-slate-800 rounded-lg disabled:opacity-50 hover:bg-slate-700"
          >
            Next
          </button>
        </div>
      </div>
    </div>
  );
}