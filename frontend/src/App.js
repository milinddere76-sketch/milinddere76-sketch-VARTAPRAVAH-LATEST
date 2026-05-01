import React from "react";
import { BrowserRouter, Routes, Route, NavLink } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import Control from "./pages/Control";
import Breaking from "./pages/Breaking";
import Ads from "./pages/Ads";
import Schedule from "./pages/Schedule";
import { LayoutDashboard, Sliders, AlertCircle, DollarSign, CalendarRange, Tv } from "lucide-react";

const NavItem = ({ to, icon: Icon, label }) => (
  <NavLink
    to={to}
    className={({ isActive }) =>
      `flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-300 group ${
        isActive 
          ? "bg-brand-accent text-white shadow-lg shadow-brand-accent/30" 
          : "text-slate-400 hover:bg-white/5 hover:text-white"
      }`
    }
  >
    <Icon className="w-5 h-5 group-hover:scale-110 transition-transform" />
    <span className="font-bold text-sm tracking-tight">{label}</span>
  </NavLink>
);

function App() {
  return (
    <BrowserRouter>
      <div className="flex min-h-screen">
        {/* Sidebar */}
        <aside className="w-64 border-r border-white/5 bg-black/20 backdrop-blur-xl flex flex-col p-6 sticky top-0 h-screen">
          <div className="flex items-center gap-3 mb-10 px-2">
            <div className="w-10 h-10 rounded-xl bg-brand-accent flex items-center justify-center shadow-lg shadow-brand-accent/40">
              <Tv className="text-white w-6 h-6" />
            </div>
            <div>
              <h1 className="font-black text-xl tracking-tighter italic">VARTA</h1>
              <p className="text-[10px] font-bold text-brand-accent tracking-widest -mt-1 uppercase">Pravah TV</p>
            </div>
          </div>

          <nav className="space-y-2 flex-1">
            <NavItem to="/" icon={LayoutDashboard} label="Dashboard" />
            <NavItem to="/control" icon={Sliders} label="Control Center" />
            <NavItem to="/breaking" icon={AlertCircle} label="Breaking News" />
            <NavItem to="/ads" icon={DollarSign} label="Ads Manager" />
            <NavItem to="/schedule" icon={CalendarRange} label="Program Schedule" />
          </nav>

          <div className="mt-auto pt-6 border-t border-white/5">
            <div className="p-4 rounded-2xl bg-white/5 text-[10px] text-slate-500 font-bold uppercase tracking-widest leading-relaxed">
              Operator: <span className="text-white">Admin-01</span><br/>
              Node: <span className="text-brand-accent">Hetzner-ARM-64</span>
            </div>
          </div>
        </aside>

        {/* Main Content */}
        <main className="flex-1 p-10 max-w-7xl mx-auto">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/control" element={<Control />} />
            <Route path="/breaking" element={<Breaking />} />
            <Route path="/ads" element={<Ads />} />
            <Route path="/schedule" element={<Schedule />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
