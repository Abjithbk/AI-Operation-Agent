'use client'
import React, { useEffect, useRef, useState } from 'react'
import Navbar from '../components/Navbar'
import ChatSidebar from '../components/ChatSidebar'
import { Send,Bot,User,Plus } from 'lucide-react'
import { sendChatMessage } from '../services/chatService'
import { ChatMessage } from '../types/chat'
const Chat = () => {
    const [messages,setMessages] = useState<ChatMessage[]>([]);
    const [input,setInput] = useState("");
    const [loading,setLoading] = useState(false);
    const bottomRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        bottomRef.current?.scrollIntoView({behavior:"smooth"});
    },[messages]);

    const getTimestamp = () => {
        return new Date().toLocaleTimeString([],{
            hour:'2-digit',
            minute:'2-digit',
        })
    }

    const handleSend = async () => {

        if(!input.trim() || loading) return;

        const userMessage:ChatMessage = {
            role:"user",
            content:input,
            time:getTimestamp(),
        };
        setMessages((prev) => [...prev,userMessage]);
        setInput("")
        setLoading(true);

        try {
            const answer = await sendChatMessage(input);
            setMessages((prev) => [
                ...prev,
                {
                    role:"assistant",
                    content:answer,
                    time:getTimestamp()
                },
            ]);
        }
        catch(err) {
            setMessages((prev) => [
                ...prev,
                {
                    role: "assistant",
                    content: "Sorry, something went wrong. Is the backend running?",
                    time: getTimestamp(),
                },
            ]);
            console.log(err)
        }
        finally {
            setLoading(false);
        }

    }

    const handleKeyDown = (e:React.KeyboardEvent) => {
        if(e.key == "Enter" && !e.shiftKey) {
            e.preventDefault();
            handleSend()
        }

    }
  return (
    <div className="min-h-screen bg-slate-950 text-white flex flex-col">
      <Navbar />

      <div className="flex flex-1">
        <ChatSidebar />

        <div className="flex-1 flex flex-col p-8">
          {/* Messages */}
          <div className="flex-1 flex flex-col gap-6 overflow-y-auto mb-4">
            {messages.length === 0 && (
              <div className="flex flex-col items-center justify-center flex-1 text-center gap-6">
    <div className="text-5xl">💬</div>
    <div>
      <h3 className="text-xl font-bold mb-2">Ask me anything about your logs</h3>
      <p className="text-slate-400 text-sm">I can analyze patterns, explain errors, and suggest fixes</p>
    </div>
    <div className="grid grid-cols-2 gap-3 w-full max-w-lg">
      {[
        "Why did checkout fail?",
        "Which service has most errors?",
        "What database issues happened?",
        "Summarize payment errors"
      ].map((q) => (
        <button
          key={q}
          onClick={() => setInput(q)}
          className="bg-slate-900 border border-slate-700 hover:border-indigo-400 rounded-lg p-3 text-sm text-slate-300 text-left transition-colors"
        >
          {q}
        </button>
      ))}
    </div>
  </div>
            )}

            {messages.map((msg, idx) => (
              <div key={idx} className="flex flex-col gap-1">
                <div
                  className={`flex gap-3 ${
                    msg.role === "user" ? "justify-end" : "justify-start"
                  }`}
                >
                  {msg.role === "assistant" && (
                    <div className="w-9 h-9 rounded-lg bg-indigo-500/20 flex items-center justify-center flex-shrink-0">
                      <Bot size={18} className="text-indigo-400" />
                    </div>
                  )}

                  <div
                    className={`rounded-xl p-4 max-w-[75%] whitespace-pre-wrap text-sm leading-relaxed ${
                      msg.role === "user"
                        ? "bg-slate-800 text-white"
                        : "bg-slate-900 border border-slate-800 text-slate-200"
                    }`}
                  >
                    {msg.content}
                  </div>

                  {msg.role === "user" && (
                    <div className="w-9 h-9 rounded-lg bg-slate-800 flex items-center justify-center flex-shrink-0">
                      <User size={18} className="text-slate-400" />
                    </div>
                  )}
                </div>

                <span
                  className={`text-xs text-slate-500 px-1 ${
                    msg.role === "user" ? "text-right mr-12" : "ml-12"
                  }`}
                >
                  {msg.time}
                </span>
              </div>
            ))}

            {loading && (
              <div className="flex gap-3 justify-start">
                <div className="w-9 h-9 rounded-lg bg-indigo-500/20 flex items-center justify-center flex-shrink-0">
                  <Bot size={18} className="text-indigo-400" />
                </div>
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 text-sm text-slate-400">
                  Thinking...
                </div>
              </div>
            )}

            <div ref={bottomRef} />
          </div>

          {/* Input */}
          <div className="border-t border-slate-800 pt-4">
            <div className="flex gap-3 items-center bg-slate-900 border border-slate-700 rounded-xl px-4 py-2">
              <Plus size={18} className="text-slate-500" />
              <textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Ask anything about your logs..."
                rows={1}
                className="flex-1 bg-transparent text-sm text-slate-200 resize-none focus:outline-none py-2"
              />
              <button
                onClick={handleSend}
                disabled={loading}
                className="bg-indigo-500 hover:bg-indigo-600 disabled:opacity-50 rounded-lg p-2"
              >
                <Send size={18} />
              </button>
            </div>
            <p className="text-center text-xs text-slate-500 mt-2">
              AI-Ops can make mistakes. Verify critical actions before deploying.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Chat
