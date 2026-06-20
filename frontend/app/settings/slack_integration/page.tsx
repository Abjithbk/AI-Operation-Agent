'use client'
import Navbar from '@/app/components/Navbar'
import api from '@/app/lib/axios'
import { MessageSquare, Save } from 'lucide-react'
import React, { useEffect, useState } from 'react'

const SlackSettings = () => {
    const [slackUrl,setSlackUrl] = useState("")
    const [loading,setLoading] = useState(false)
    const [message,setMessage] = useState({text:'',type:''});

    useEffect(() => {
        const fetchSlackUrl = async () => {
            try {
                const res = await api.get('/slack')
                const url = res.data?.slack_webhook_url
                setSlackUrl(url === null || url === undefined ? '': url);
            }
            catch(err) {
                console.error(err)
            }
        }
        fetchSlackUrl()
    },[])

    const handleSaveSlackUrl = async () => {
        setLoading(true)
        setMessage({text:'',type:''})
        try {
            const res = await api.post('/slack',{
            slack_webhook_url:slackUrl
        });

        setMessage({text:res.data.message , type:'success'})
        }
        catch(err) {
            setMessage({text:'Failed to save.Please check the url',type:'error'})
        }
        finally{
            setLoading(false)
        }
    }
  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <Navbar /> 
      <div className="max-w-3xl mx-auto p-8">
        <h2 className="text-2xl font-bold mb-1">Settings</h2>
        <p className="text-slate-400 text-sm mb-8">
          Manage your integrations and alert preferences.
        </p>

        {/* Slack Integration */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 mb-6">
          <h3 className="font-bold mb-4 flex items-center gap-2">
            <MessageSquare size={18} className="text-indigo-400" />
            Slack Integration
          </h3>

          <label className="block text-sm font-medium text-slate-300 mb-2">
            Incoming Webhook URL
          </label>
          <input
            type="text"
            value={slackUrl || ''}
            onChange={(e) => setSlackUrl(e.target.value)}
            placeholder="https://hooks.slack.com/services/T00.../B00.../xxx"
            className="w-full bg-slate-950 border border-slate-700 rounded-lg px-4 py-2 text-sm focus:outline-none focus:border-indigo-400 mb-2"
          />
          <p className="text-xs text-slate-500 mb-4">
            Paste your Slack Incoming Webhook URL here. Critical incidents will be automatically sent to this channel.
          </p>

          <button
            onClick={handleSaveSlackUrl}
            disabled={loading}
            className="bg-indigo-500 hover:bg-indigo-600 disabled:opacity-50 rounded-lg px-4 py-2 text-sm font-medium flex items-center gap-2"
          >
            <Save size={16} />
            {loading ? 'Saving...' : 'Save Settings'}
          </button>

          {message.text && (
            <p className={`text-sm mt-4 ${message.type === 'success' ? 'text-green-400' : 'text-red-400'}`}>
              {message.text}
            </p>
          )}
        </div>

        {/* How to Get Your Slack Webhook URL */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
          <h3 className="font-bold mb-4 flex items-center gap-2">
            <MessageSquare size={18} className="text-indigo-400" />
            How to Get Your Slack Webhook URL
          </h3>
          <ol className="text-sm text-slate-400 space-y-2 list-decimal list-inside">
            <li>Go to your Slack workspace</li>
            <li>Click <span className="text-slate-300 font-medium">Settings & administration</span> → <span className="text-slate-300 font-medium">Manage apps</span></li>
            <li>Search for <span className="text-slate-300 font-medium">Incoming Webhooks</span> and add it to a channel</li>
            <li>Copy the <span className="text-slate-300 font-medium">Webhook URL</span> and paste it above</li>
          </ol>
        </div>
      </div>
    </div>
  )
}

export default SlackSettings
