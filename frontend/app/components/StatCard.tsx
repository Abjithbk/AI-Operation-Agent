'use client'
import React from 'react'
import { LucideIcon } from "lucide-react";

interface StatCardProps {
    label:string;
    value:string|number;
    icon:LucideIcon;
    iconColor?:string;
    subtext?:string;
}
const StatCard = ({
    label,value,icon:Icon,iconColor = "text-slate-400",subtext,
} : StatCardProps) => {
  return (
    <div className='bg-slate-900 border border-slate-800 rounded-xl p-5 flex-1'>
        <div className='flex items-center justify-between mb-2'>
            <span className="text-xs font-medium text-slate-400 uppercase tracking-wide">
          {label}
        </span>
        <Icon className={iconColor} size={18} />
        </div>
        <div className="text-3xl font-bold mb-1">{value}</div>
      {subtext && <div className="text-xs text-slate-500">{subtext}</div>}
    </div>
  )
}

export default StatCard
