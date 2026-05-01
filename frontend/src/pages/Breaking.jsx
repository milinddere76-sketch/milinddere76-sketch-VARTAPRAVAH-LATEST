import React, { useState } from "react";
import api from "../api";
import { AlertCircle, Send, UploadCloud, RefreshCcw } from "lucide-react";

export default function Breaking() {
  const [file, setFile] = useState("");
  const [status, setStatus] = useState("");

  const sendBreaking = async () => {
    if(!file) return alert("Please enter a video path");
    setStatus("injecting...");
    try {
      await api.post("/breaking", { file });
      setStatus("success");
      setTimeout(() => setStatus(""), 3000);
    } catch (err) {
      setStatus("failed");
    }
  };

  return (
    <div className="max-w-2xl mx-auto space-y-8">
      <div className="flex items-center gap-4">
        <div className="w-12 h-12 rounded-2xl bg-amber-500 flex items-center justify-center animate-pulse">
          <AlertCircle className="text-black w-6 h-6" />
        </div>
        <div>
          <h2 className="text-3xl font-black">Breaking News Injection</h2>
          <p className="text-slate-400">High-priority bulletins skip the queue</p>
        </div>
      </div>

      <div className="glass-card space-y-6">
        <div>
          <label className="block text-sm font-medium text-slate-400 mb-2">Remote Video Path (Oracle)</label>
          <div className="relative">
            <input
              type="text"
              placeholder="/home/ubuntu/videos/urgent_news.mp4"
              onChange={(e) => setFile(e.target.value)}
              className="w-full bg-black/30 border border-white/10 rounded-xl px-4 py-4 text-brand-accent placeholder:text-slate-600 focus:outline-none focus:border-brand-accent transition-all"
            />
            <UploadCloud className="absolute right-4 top-4 text-slate-600 w-6 h-6" />
          </div>
        </div>

        <button 
          onClick={sendBreaking}
          disabled={status === "injecting..."}
          className="w-full py-4 rounded-xl bg-amber-500 hover:bg-amber-600 text-black font-black flex items-center justify-center gap-2 transition-all shadow-[0_0_20px_rgba(245,158,11,0.3)] disabled:opacity-50"
        >
          {status === "injecting..." ? <RefreshCcw className="animate-spin" /> : <Send className="w-5 h-5" />}
          {status === "success" ? "INJECTED SUCCESSFULLY" : "INJECT BREAKING BULLETIN"}
        </button>

        <div className="p-4 rounded-xl bg-white/5 border border-white/5 text-xs text-slate-500 italic">
          Tip: Breaking news is automatically placed at the top of the /breaking/ directory on the Oracle server.
        </div>
      </div>
    </div>
  );
}
