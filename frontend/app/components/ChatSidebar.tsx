"use client"
import React, { useState } from 'react'

import {
  MessageSquare,
  History,
  BarChart3,
  Gauge,
  AlertCircle,
} from "lucide-react";

const chats = [
  { icon: MessageSquare, label: "Current Alert" },
  { icon: History, label: "System Check" },
  { icon: BarChart3, label: "Model Drift" },
  { icon: Gauge, label: "Latency spike" },
  { icon: AlertCircle, label: "API Error" },
];


const ChatSidebar = () => {
    const [active,setActive] = useState("Current Alert");
  return (
    <div className="w-64 border-r border-slate-800 p-5 flex flex-col">
      <h3 className="font-bold mb-1">Recent Chats</h3>
      <p className="text-xs text-slate-500 mb-4">AI Assistant History</p>

      <div className="flex flex-col gap-1">
        {chats.map((chat) => {
          const Icon = chat.icon;
          const isActive = active === chat.label;
          return (
            <button
              key={chat.label}
              onClick={() => setActive(chat.label)}
              className={`flex items-center gap-3 px-3 py-2 rounded-lg text-sm text-left ${
                isActive
                  ? "bg-slate-800 text-white"
                  : "text-slate-400 hover:text-white hover:bg-slate-900"
              }`}
            >
              <Icon size={16} />
              {chat.label}
            </button>
          );
        })}
      </div>
    </div>
  )
}

export default ChatSidebar
