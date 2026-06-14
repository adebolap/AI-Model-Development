'use client'

import { useEffect, useState } from 'react'
import KpiCard from '@/components/KpiCard'

const BACKEND = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000'

interface Summary {
  revenue_eur: number
  direct_cost_eur: number
  gross_margin_eur: number
  margin_pct: number
  trip_count: number
  active_vehicles: number
  top_customer: string | null
}

interface RouteRow {
  origin: string
  destination: string
  avg_revenue_eur: number
  avg_cost_eur: number
  avg_margin_pct: number
  trip_count: number
}

interface CustomerRow {
  customer: string
  revenue_eur: number
  margin_pct: number
}

const MONTHLY_TREND = [32, 38, 41, 36, 44, 48]
const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']

export default function DashboardPage() {
  const [summary, setSummary] = useState<Summary | null>(null)
  const [routes, setRoutes] = useState<RouteRow[]>([])
  const [customers, setCustomers] = useState<CustomerRow[]>([])
  const [companyId, setCompanyId] = useState<string | null>(null)

  useEffect(() => {
    const stored = localStorage.getItem('logiflow_company_id')
    setCompanyId(stored)
    const qs = stored ? `?company_id=${stored}&days=30` : ''
    Promise.all([
      fetch(`${BACKEND}/api/profitability/summary${qs}`).then((r) => r.json()),
      fetch(`${BACKEND}/api/profitability/by-route${qs}`).then((r) => r.json()),
      fetch(`${BACKEND}/api/profitability/by-customer${qs}`).then((r) => r.json()),
    ])
      .then(([s, r, c]) => {
        setSummary(s)
        setRoutes(r.slice(0, 4))
        setCustomers(c.slice(0, 4))
      })
      .catch(() => {})
  }, [])

  const fmt = (n: number) => `€${n.toLocaleString('fr-BE', { minimumFractionDigits: 0 })}`

  const kpis = summary
    ? [
        { title: 'Revenue', value: fmt(summary.revenue_eur), delta: '+12.4%', trend: 'up' as const, subtitle: 'This month' },
        { title: 'Direct Costs', value: fmt(summary.direct_cost_eur), delta: '+8.1%', trend: 'up' as const, subtitle: 'This month' },
        { title: 'Gross Margin', value: fmt(summary.gross_margin_eur), delta: '+2.1%', trend: 'up' as const, subtitle: 'This month' },
        { title: 'Margin %', value: `${summary.margin_pct}%`, delta: '+0.8pp', trend: 'up' as const, subtitle: 'vs last month' },
        { title: 'Trips', value: String(summary.trip_count), delta: '+6', trend: 'up' as const, subtitle: 'This month' },
        { title: 'Active Vehicles', value: String(summary.active_vehicles), delta: '0', trend: 'neutral' as const, subtitle: 'of fleet' },
      ]
    : Array(6).fill({ title: '—', value: '…', delta: '', trend: 'neutral' as const, subtitle: '' })

  return (
    <div>
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Operations Dashboard</h1>
          <p className="text-sm text-gray-500 mt-1">
            Last 30 days — {companyId ? 'Live data' : 'Demo data — '}
            {!companyId && (
              <button
                onClick={async () => {
                  const res = await fetch(`${BACKEND}/api/seed`, { method: 'POST' })
                  const data = await res.json()
                  if (data.company_id) {
                    localStorage.setItem('logiflow_company_id', data.company_id)
                    window.location.reload()
                  }
                }}
                className="underline text-brand-600 hover:text-brand-700 ml-1"
              >
                Load demo data
              </button>
            )}
          </p>
        </div>
      </div>

      <div className="grid grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
        {kpis.map((kpi, i) => (
          <KpiCard key={i} {...kpi} />
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <div className="bg-white rounded-xl border border-gray-100 p-6 shadow-sm">
          <h2 className="text-sm font-semibold text-gray-700 mb-4">Monthly Revenue Trend</h2>
          <div className="h-40 flex items-end gap-2">
            {MONTHLY_TREND.map((v, i) => (
              <div key={i} className="flex-1 flex flex-col items-center gap-1">
                <div
                  className="w-full bg-brand-500 rounded-t-sm opacity-80 hover:opacity-100 transition-opacity"
                  style={{ height: `${(v / 48) * 100}%` }}
                  title={`€${v}k`}
                />
                <span className="text-xs text-gray-400">{MONTHS[i]}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-xl border border-gray-100 p-6 shadow-sm">
          <h2 className="text-sm font-semibold text-gray-700 mb-4">Top Customers by Margin</h2>
          <div className="space-y-3">
            {customers.map((c) => (
              <div key={c.customer} className="flex items-center gap-3">
                <div className="w-32 text-xs text-gray-600 font-medium truncate">{c.customer}</div>
                <div className="flex-1 bg-gray-100 rounded-full h-2">
                  <div className="h-2 rounded-full bg-brand-500" style={{ width: `${Math.min(c.margin_pct, 100)}%` }} />
                </div>
                <div className="w-12 text-xs text-gray-500 text-right">{c.margin_pct}%</div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="bg-white rounded-xl border border-gray-100 p-6 shadow-sm">
        <h2 className="text-sm font-semibold text-gray-700 mb-4">Routes — Sorted by Margin (lowest first)</h2>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left text-xs text-gray-400 border-b border-gray-100">
                <th className="pb-2 font-medium">Route</th>
                <th className="pb-2 font-medium text-right">Avg Revenue</th>
                <th className="pb-2 font-medium text-right">Avg Cost</th>
                <th className="pb-2 font-medium text-right">Margin</th>
                <th className="pb-2 font-medium text-right">Trips</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-50">
              {routes.map((r) => (
                <tr key={`${r.origin}-${r.destination}`} className="hover:bg-gray-50">
                  <td className="py-2 font-medium text-gray-800">{r.origin} → {r.destination}</td>
                  <td className="py-2 text-right text-gray-600">{fmt(r.avg_revenue_eur)}</td>
                  <td className="py-2 text-right text-gray-600">{fmt(r.avg_cost_eur)}</td>
                  <td className={`py-2 text-right font-semibold ${r.avg_margin_pct < 15 ? 'text-red-500' : r.avg_margin_pct < 25 ? 'text-amber-500' : 'text-green-600'}`}>
                    {r.avg_margin_pct}%
                  </td>
                  <td className="py-2 text-right text-gray-400">{r.trip_count}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
