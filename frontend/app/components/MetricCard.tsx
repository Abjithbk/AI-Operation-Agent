'use client';
import React from 'react'

import { LineChart, Line, ResponsiveContainer, YAxis } from "recharts";
import { LucideIcon } from "lucide-react";
import { MetricReading } from "../services/metricService";
import { Anomaly } from "../types/metric";

interface MetricCardProps {
    title:string;
    icon:LucideIcon;
    unit:string;
    readings:MetricReading[];
    anomalies:Anomaly[];
    lineColor:string;
}


const MetricCard = ({
  title,
  icon: Icon,
  unit,
  readings,
  anomalies,
  lineColor,
}:MetricCardProps) => {
    const latestValue = readings.length > 0 ? readings[readings.length - 1].value : 0;
  const chartData = readings.map((r) => ({ value: r.value }));
  const hasAnomaly = anomalies.length > 0;
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 flex-1">
      <div className="flex items-center justify-between mb-2">
        <span className="text-sm font-medium text-slate-300">{title}</span>
        <Icon className="text-slate-400" size={18} />
      </div>

      <div className="text-3xl font-bold mb-3">
        {latestValue.toFixed(1)}{unit}
      </div>

      <div className="relative h-32">
        {hasAnomaly && (
          <span className="absolute top-0 right-0 bg-red-500 text-white text-xs font-bold px-2 py-1 rounded">
            ANOMALY
          </span>
        )}
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={chartData}>
            <YAxis hide domain={["dataMin - 5", "dataMax + 5"]} />
            <Line
              type="monotone"
              dataKey="value"
              stroke={lineColor}
              strokeWidth={2}
              dot={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}

export default MetricCard
