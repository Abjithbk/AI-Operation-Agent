'use client'
import React from 'react'
import {Search, Bell,User} from 'lucide-react'
const Navbar = () => {
  return (
    <nav className='border-b border-slate-800 bg-slate-950 px-8 py-4 flex items-center justify-between'>
        <h1 className='text-xl font-bold text-indigo-400'>AI ops Agent</h1>
        <div className='flex gap-6 text-sm font-medium'>
            <span className='text-white border-b-2 border-indigo-400 pb-1'>
                Incidents
            </span>
            <span className='text-slate-400 hover:text-white cursor-pointer'>
                Metrics
            </span>
            <span className='text-slate-400 hover:text-white cursor-pointer'>
                Chat
            </span>
        </div>
        <div className=' flex items-center gap-4'>
            <div className='relative'>
                <Search className='absolute left-3 top-1/2 -translate-y-1/2 text-slate-500 ' size={16}/>
                <input type="text" placeholder='Search Logs..'  className='bg-slate-900 border border-slate-700 rounded-lg pl-9 py-2 pr-4 text-sm text-slate-300 w-64 focus:outline-none focus:border-indigo-400'/>

            </div>
            <Bell className='text-slate-400 hover:text-white cursor-pointer' size={20}/>
            <User className='text-slate-400 hover:text-white cursor-pointer' size={20} />

        </div>
      
    </nav>
  )
}

export default Navbar
