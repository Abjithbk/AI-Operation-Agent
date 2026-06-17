'use client'
import React from 'react'

const SkeletonCard = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 animate-pulse">
      <div className="flex items-center gap-3 mb-3">
        <div className="h-5 w-16 bg-slate-800 rounded" />
        <div className="h-4 w-24 bg-slate-800 rounded" />
      </div>
      <div className="h-6 w-2/3 bg-slate-800 rounded mb-3" />
      <div className="h-20 bg-slate-800 rounded mb-3" />
      <div className="h-16 bg-slate-800 rounded" />
    </div>
  )
}

export default SkeletonCard
