import { useEffect, useState } from 'react'

type ModeStatus = {
  mode: string
  simulation_mode: boolean
  live_available: boolean
  message: string
}

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export function TradingModeControl() {
  const [status, setStatus] = useState<ModeStatus | null>(null)

  useEffect(() => {
    let active = true
    const load = async () => {
      try {
        const response = await fetch(`${API_BASE}/api/trading-mode`)
        if (!response.ok) throw new Error('Mode status unavailable')
        const value = (await response.json()) as ModeStatus
        if (active) setStatus(value)
      } catch {
        if (active) setStatus(null)
      }
    }
    void load()
    const interval = window.setInterval(() => void load(), 15000)
    return () => {
      active = false
      window.clearInterval(interval)
    }
  }, [])

  const paper = status?.simulation_mode === true
  const label = status === null ? 'MODE UNKNOWN' : paper ? 'PAPER ACTIVE' : 'LIVE BLOCKED'

  return (
    <div className="flex items-center gap-1.5 shrink-0" title={status?.message || 'Unable to verify trading mode'}>
      <span className="px-1.5 py-0.5 text-[9px] font-bold uppercase border border-amber-500/30 bg-amber-500/10 text-amber-300">
        {label}
      </span>
      <button
        type="button"
        disabled
        aria-disabled="true"
        title="Live trading is locked until a verified order executor and fill reconciliation are implemented and tested."
        className="px-2 py-1 text-[9px] uppercase tracking-wider border border-neutral-800 text-neutral-600 bg-neutral-950 cursor-not-allowed opacity-70"
      >
        Live locked
      </button>
    </div>
  )
}
