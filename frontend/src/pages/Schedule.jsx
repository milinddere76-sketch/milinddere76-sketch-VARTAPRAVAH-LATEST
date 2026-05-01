import React from "react";
import { Calendar, MapPin, Clock3 } from "lucide-react";

export default function Schedule() {
  const slots = [
    { time: "05:00", name: "Sakal Prabhat", type: "Morning", color: "bg-orange-500" },
    { time: "12:00", name: "Madhyanha Batmya", type: "Afternoon", color: "bg-blue-500" },
    { time: "17:00", name: "Sandhyakal Specials", type: "Evening", color: "bg-indigo-500" },
    { time: "20:00", name: "Varta Pravah Prime", type: "Prime Time", color: "bg-rose-500" },
    { time: "23:00", name: "Ratra Majha", type: "Night", color: "bg-slate-700" },
  ];

  return (
    <div className="max-w-4xl mx-auto space-y-10">
      <div className="flex items-end justify-between border-b border-white/10 pb-6">
        <div>
          <h2 className="text-4xl font-black italic tracking-tighter">BULLETIN SCHEDULE</h2>
          <p className="text-slate-400 mt-2">24-Hour Autonomous Programming Grid</p>
        </div>
        <div className="text-right">
          <p className="text-brand-accent font-mono font-bold text-2xl uppercase tracking-widest">PRO MODE</p>
          <p className="text-[10px] text-slate-500 font-bold uppercase tracking-widest">Automatic Generation Active</p>
        </div>
      </div>

      <div className="space-y-4">
        {slots.map((slot, idx) => (
          <div 
            key={idx}
            className="glass-card flex items-center group hover:translate-x-2 transition-all cursor-default"
          >
            <div className={`w-2 h-16 rounded-full ${slot.color} mr-8 group-hover:scale-y-110 transition-transform`} />
            <div className="w-32">
              <span className="text-2xl font-black font-mono tracking-tighter">{slot.time}</span>
            </div>
            <div className="flex-1">
              <h3 className="text-xl font-bold tracking-tight">{slot.name}</h3>
              <p className="text-sm text-slate-500 uppercase font-black tracking-widest mt-1">{slot.type}</p>
            </div>
            <div className="flex items-center gap-6 text-slate-500">
              <div className="flex flex-col items-end">
                <span className="text-[10px] font-bold uppercase tracking-widest">Priority</span>
                <span className="text-white font-bold">{idx < 3 ? "Standard" : "High"}</span>
              </div>
              <div className="flex flex-col items-end border-l border-white/10 pl-6">
                <span className="text-[10px] font-bold uppercase tracking-widest">Anchor</span>
                <span className="text-white font-bold">{idx % 2 === 0 ? "Female" : "Male"}</span>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="p-6 rounded-2xl bg-brand-accent/5 border border-brand-accent/20 flex gap-6 items-center">
        <div className="w-16 h-16 rounded-full bg-brand-accent/20 flex items-center justify-center flex-shrink-0">
          <Clock3 className="text-brand-accent w-8 h-8" />
        </div>
        <div>
          <p className="font-bold text-lg">Next Refresh</p>
          <p className="text-slate-400 text-sm">The AI Factory checks for new global and regional headlines every 15 minutes to rebuild the upcoming slot's script.</p>
        </div>
      </div>
    </div>
  );
}
