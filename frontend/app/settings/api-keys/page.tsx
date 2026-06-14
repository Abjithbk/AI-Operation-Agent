'use client';
import React, { useEffect, useState } from 'react'
import { Key, Copy, Plus, Eye, EyeOff } from "lucide-react";
import api from '@/app/lib/axios';
import Navbar from '@/app/components/Navbar';

interface ApiKey {
    id:string
    name:string
    key?:string;
    created_at:string
}
const ApiKeysPage = () => {
    const [apiKeys,setApiKeys] = useState<ApiKey[]>([]);
    const [newKeyName,setNewKeyName] = useState("")
    const [generatedKey,setGeneratedKey] = useState<string | null>(null)
    const [loading,setLoading] = useState(false)
    const [showKey,setShowKey] = useState(false)
    const [copied,setCopied] = useState(false)

    useEffect(() => {
        loadKeys();
    },[])

    const loadKeys = async () => {
        try {
            const res = await api.get('/api-keys');
            setApiKeys(res.data)
        }
        catch(err) {
            console.error(err)
        }
    }

    const handleGenerate = async() => {
        if(!newKeyName.trim()) return
        setLoading(true)

        try {
            const res = await api.post(`/api-keys?name=${newKeyName}`)
            setGeneratedKey(res.data.key)
            setNewKeyName("")
            loadKeys()
        }
        catch(err) {
            console.log(err)
        }
        finally {
            setLoading(false)
        }

    }

    const handleCopy = () => {
        if(!generatedKey) return

        navigator.clipboard.writeText(generatedKey)
        setCopied(true)
        setTimeout(() => {
            setCopied(false)
        }, 2000);
    }
  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <Navbar />
      <div className="max-w-3xl mx-auto p-8">
        <h2 className="text-2xl font-bold mb-1">API Keys</h2>
        <p className="text-slate-400 text-sm mb-8">
          Generate API keys to connect your production apps to AI Ops Agent.
        </p>

        {/* Generate New Key */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 mb-6">
          <h3 className="font-bold mb-4 flex items-center gap-2">
            <Plus size={18} className="text-indigo-400" />
            Generate New Key
          </h3>

          <div className="flex gap-3">
            <input
              type="text"
              value={newKeyName}
              onChange={(e) => setNewKeyName(e.target.value)}
              placeholder="e.g. My E-commerce App"
              className="flex-1 bg-slate-950 border border-slate-700 rounded-lg px-4 py-2 text-sm focus:outline-none focus:border-indigo-400"
            />
            <button
              onClick={handleGenerate}
              disabled={loading || !newKeyName.trim()}
              className="bg-indigo-500 hover:bg-indigo-600 disabled:opacity-50 rounded-lg px-4 py-2 text-sm font-medium"
            >
              {loading ? "Generating..." : "Generate"}
            </button>
          </div>

          {/* Show Generated Key */}
          {generatedKey && (
            <div className="mt-4 bg-slate-950 border border-green-500/30 rounded-lg p-4">
              <p className="text-xs text-green-400 font-medium mb-2">
                 Key generated! Copy it now — it won't be shown again.
              </p>
              <div className="flex items-center gap-3">
                <code className="flex-1 text-xs text-slate-300 break-all">
                  {showKey ? generatedKey : "aiops_••••••••••••••••••••••••••••••••"}
                </code>
                <button
                  onClick={() => setShowKey(!showKey)}
                  className="text-slate-400 hover:text-white"
                >
                  {showKey ? <EyeOff size={16} /> : <Eye size={16} />}
                </button>
                <button
                  onClick={handleCopy}
                  className="text-slate-400 hover:text-white"
                >
                  <Copy size={16} />
                </button>
              </div>
              {copied && (
                <p className="text-xs text-green-400 mt-2">Copied!</p>
              )}
            </div>
          )}
        </div>
        <div className='bg-slate-900 border border-slate-800 rounded-xl p-6 mb-6'>
            <h3 className='font-bold mb-4 flex items-center gap-2'>
                <Key size={18} className='text-indigo-400' />
                Your Api Keys
            </h3>
            {
                apiKeys.length === 0 && (
                    <p className='text-slate-400 text-sm'>
                        No keys yet.Generate your first key above
                    </p>
                )
            }
            {
                apiKeys.map((key) => (
                    <div key={key.id} className='flex items-center justify-between border-b border-slate-800 py-3 last:border-0'>
                        <div>
                            <p className='text-sm font-medium'>{key.name}</p>
                            <p className='text-xs text-slate-500 mt-1'>
                                aiops_•••••••••••• · Created{" "}
                  {new Date(key.created_at).toLocaleDateString()}
                            </p>

                        </div>

                    </div>
                ))
            }

        </div>

        {/* How to Use */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
          <h3 className="font-bold mb-4 flex items-center gap-2">
            <Key size={18} className="text-indigo-400" />
            How to Use Your API Key
          </h3>
          <p className="text-sm text-slate-400 mb-3">
            Add this header to every request from your production app:
          </p>
          <div className="bg-slate-950 rounded-lg p-4">
            <pre className='bg-slate-950 rounded-lg p-4 overflow-x-auto'>
                <code className="text-xs text-green-400">
              {`import requests

requests.post(
    "http://your-agent.com/api/logs",
    headers={"X-API-Key": "your_api_key_here"},
    json={
        "level": "ERROR",
        "service": "payment-service",
        "message": "Database connection failed"
    }
)`}
            </code>

            </pre>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ApiKeysPage
