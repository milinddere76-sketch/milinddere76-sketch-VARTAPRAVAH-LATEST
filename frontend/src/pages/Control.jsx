import React from "react";
import api from "../api";
import { Power, Play, Square, RefreshCcw } from "lucide-react";

export default function Control() {
  const start = () => {
    alert("Starting Broadcast...");
    api.post("/control/start");
  };
  
  const stop = () => {
    if(window.confirm("Are you sure you want to STOP the broadcast?")) {
      api.post("/control/stop");
    }
  };

  const restart = () => {
    api.post("/control/restart");
  };

  return (
    <div className="space-y-8 max-w-2xl mx-auto">
      <div className="text-center">
        <h2 className="text-3xl font-bold">Broadcast Control</h2>
        <p className="text-slate-400 mt-2">Manage the 24/7 news cycle and relay servers</p>
      </div>

      <div className="glass-card flex flex-col items-center gap-8 py-12">
        <div className="grid grid-cols-2 gap-6 w-full max-w-md">
          <button 
            onClick={start}
            className="flex flex-col items-center gap-4 p-8 rounded-3xl bg-emerald-500/10 border border-emerald-500/20 hover:bg-emerald-500/20 hover:border-emerald-500/40 transition-all group"
          >
            <div className="w-16 h-16 rounded-full bg-emerald-500 flex items-center justify-center shadow-[0_0_30px_rgba(16,185,129,0.4)] group-hover:scale-110 transition-transform">
              <Play className="text-white w-8 h-8 fill-white" />
            </div>
            <span className="font-bold text-emerald-400 tracking-wide">START STREAM</span>
          </button>

          <button 
            onClick={stop}
            className="flex flex-col items-center gap-4 p-8 rounded-3xl bg-rose-500/10 border border-rose-500/20 hover:bg-rose-500/20 hover:border-rose-500/40 transition-all group"
          >
            <div className="w-16 h-16 rounded-full bg-rose-500 flex items-center justify-center shadow-[0_0_30px_rgba(244,63,94,0.4)] group-hover:scale-110 transition-transform">
              <Square className="text-white w-8 h-8 fill-white" />
            </div>
            <span className="font-bold text-rose-400 tracking-wide">STOP STREAM</span>
          </button>
        </div>

        <button 
          onClick={restart}
          className="flex items-center gap-2 px-6 py-3 rounded-full bg-white/5 border border-white/10 hover:bg-white/10 transition-all text-slate-300 font-medium"
        >
          <RefreshCcw className="w-4 h-4" />
          Soft Restart Pipeline
        </button>
      </div>

      <div className="p-4 rounded-xl bg-amber-500/10 border border-amber-500/20 text-amber-500 text-sm flex gap-3">
        <Power className="w-5 h-5 flex-shrink-0" />
        <div>
          <p className="font-bold">Caution</p>
          <p className="opacity-80">Stopping the stream will cause an immediate disconnect on YouTube Live. Use only for emergency maintenance.</p>
        </div>
      </div>
    </div>
  );
}
