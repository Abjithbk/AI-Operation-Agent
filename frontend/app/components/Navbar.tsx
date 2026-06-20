'use client'
import React, { useEffect, useRef, useState } from 'react'
import {Search, Bell,User, LogOut, Key, ChevronDown, Hash} from 'lucide-react'
import Link from 'next/link'
import { usePathname,useRouter } from 'next/navigation'
import { supabase } from '../lib/supabase'
const Navbar = () => {


    const pathname = usePathname();
    const router = useRouter()
    const [email,setEmail] = useState<string | null>(null)
    const [showDropdown,setShowDropdown] = useState(false)
    const tabs = [
    { name: "Incidents", href: "/" },
    { name: "Metrics", href: "/metrics" },
    { name: "Chat", href: "/chat" },
  ];
  const dropdownref = useRef<HTMLDivElement>(null)

  useEffect(() => {
    supabase.auth.getSession().then(({data :{session}}) => {
        setEmail(session?.user?.email?? null);
    })
  },[]);

  useEffect(() => {
    const handleClickOutside = (e:MouseEvent) => {
        if(dropdownref.current && !dropdownref.current.contains(e.target as Node)) {
            setShowDropdown(false);
        }
    }
    document.addEventListener("mousedown",handleClickOutside);
    return () => document.removeEventListener("mousedown",handleClickOutside)
  },[])

  const handleLogout = async () => {
    await supabase.auth.signOut()
    router.push('/login')
  }
  return (
    <nav className="border-b border-slate-800 bg-slate-950 px-4 md:px-8 py-3 flex items-center justify-between gap-4">
      <h1 className="text-lg md:text-xl font-bold text-indigo-400 whitespace-nowrap">AI Ops Agent</h1>

      <div className="flex gap-3 md:gap-6 text-sm font-medium ">
        {tabs.map((tab) => (
          <Link
            key={tab.href}
            href={tab.href}
            className={
              pathname === tab.href
                ? "text-white border-b-2 border-indigo-400 pb-1 transition-all whitespace-nowrap"
                : "text-slate-400 hover:text-white transition-colors whitespace-nowrap"
            }
          >
            {tab.name}
          </Link>
        ))}
      </div>

      <div className="flex items-center gap-2 md:gap-4">
        <div className="hidden md:flex relative">
          <Search
            className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500"
            size={16}
          />
          <input
            type="text"
            placeholder="Search logs..."
            className="bg-slate-900 border border-slate-700 rounded-lg pl-9 pr-4 py-2 text-sm text-slate-300 w-64 focus:outline-none focus:border-indigo-400 "
          />
        </div>

        <Bell
          className="hidden md:block text-slate-400 hover:text-white cursor-pointer"
          size={20}
        />

        {/* Profile Dropdown */}
        <div className="relative" ref={dropdownref}>
          <button
            onClick={() => setShowDropdown(!showDropdown)}
            className="flex items-center gap-1 md:gap-2 bg-slate-900 border border-slate-700 hover:border-indigo-400 rounded-lg px-2 md:px-3 py-2 transition-all duration-200"
          >
            <div className="w-6 h-6 rounded-full bg-indigo-500 flex items-center justify-center">
              <User size={14} className="text-white" />
            </div>
            <span className="hidden md:block text-sm text-slate-300 max-w-[120px] truncate">
              {email?.split("@")[0] ?? "Account"}
            </span>
            <ChevronDown
              size={14}
              className={`text-slate-400 transition-transform duration-200 ${
                showDropdown ? "rotate-180" : ""
              }`}
            />
          </button>

          {/* Dropdown Menu */}
          <div
            className={`absolute right-0 top-12 w-56 bg-slate-900 border border-slate-700 rounded-xl shadow-xl z-50 overflow-hidden transition-all duration-200 ${
              showDropdown
                ? "opacity-100 translate-y-0 pointer-events-auto"
                : "opacity-0 -translate-y-2 pointer-events-none"
            }`}
          >
            {/* User Info */}
            <div className="px-4 py-3 border-b border-slate-800">
              <p className="text-xs text-slate-500">Signed in as</p>
              <p className="text-sm font-medium text-white truncate mt-0.5">
                {email}
              </p>
            </div>

            {/* Menu Items */}
            <div className="p-2">
              <Link
                href="/settings/api-keys"
                onClick={() => setShowDropdown(false)}
                className="flex items-center gap-3 px-3 py-2 rounded-lg text-sm text-slate-300 hover:bg-slate-800 hover:text-white transition-colors"
              >
                <Key size={16} className="text-indigo-400" />
                API Keys
              </Link>
              <Link
              href='/settings/slack_integration'
              onClick={() =>setShowDropdown(false)}
              className="flex items-center gap-3 px-3 py-2 rounded-lg text-sm text-slate-300 hover:bg-slate-800 hover:text-white transition-colors"
              >
              <Hash size={16} className='text-indigo-400'/>
              Slack Integration
              </Link>

              <button
                onClick={handleLogout}
                className="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm text-red-400 hover:bg-red-500/10 hover:text-red-300 transition-colors mt-1"
              >
                <LogOut size={16} />
                Logout
              </button>
            </div>
          </div>
        </div>
      </div>
    </nav>
  )
}

export default Navbar
