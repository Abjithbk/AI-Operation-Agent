"use client";

import { useState } from "react";

export default function Filters() {
  const [filter, setFilter] = useState("all");

  const options = [
    { id: "all", label: "All Incidents" },
    { id: "critical", label: "Critical Only" },
    { id: "resolved", label: "Resolved" },
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 h-fit">
      <h3 className="font-bold mb-4">Filters</h3>
      <div className="flex flex-col gap-3">
        {options.map((option) => (
          <label
            key={option.id}
            className="flex items-center gap-3 cursor-pointer text-sm text-slate-300"
          >
            <input
              type="radio"
              name="filter"
              checked={filter === option.id}
              onChange={() => setFilter(option.id)}
              className="w-4 h-4 accent-indigo-500"
            />
            {option.label}
          </label>
        ))}
      </div>
    </div>
  );
}