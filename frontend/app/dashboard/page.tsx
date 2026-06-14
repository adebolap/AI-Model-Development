'use client'

import { useEffect, useState } from 'react'
import dynamic from 'next/dynamic'
import KpiCard from '@/components/KpiCard'

const MonthlyTrendChart = dynamic(() => import('@/components/charts/MonthlyTrendChart'), { ssr: false })
const CustomerMarginChart = dynamic(() => import('@/components/charts/CustomerMarginChart'), { ssr: false })
const VehicleUtilizationChart = dynamic(() => import('@/components/charts/VehicleUtilizationChart'), { ssr: false })
const CostBreakdownChart = dynamic(() => import('@/components/charts/CostBreakdownChart'), { ssr: false })

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

const fmt = (n: number) =>
  `€${Math.round(n).toLocaleString('fr-BE')}`

export default function DashboardPage() {
  const [summary, setSummary] = useState<Summary | null>(null)
  const [trend, setTrend] = useState<object[]>([])
  const [customers, setCustomers] = useState<object[]>([])
  const [vehicles, setVehicles] = useState<object[]>([])
  const [costs, setCosts] = useState<object[]>([])
  const [routes, setRoutes] = useState<object[]>([])
  const [companyId, setCompanyId] = useState<string | null>(null)
  const [seeding, setSeeding] = useState(false)

  const fetchAll = (cid: string | null) => {
    const qs = cid ? `?company_id=${cid}` : ''
    Promise.all([
      fetch(`${BACKEND}/api/profitability/summary${qs}&days=30`).then((r) => r.json()),
      fetch(`${BACKEND}/api/profitability/monthly-trend${qs}&months=6`).then((r) => r.json()),
      fetch(`${BACKEND}/api/profitability/by-customer${qs}&days=30`).then((r) => r.json()),
      fetch(`${BACKEND}/api/profitability/by-vehicle${qs}&days=30`).then((r) => r.json()),
      fetch(`${BACKEND}/api/profitability/cost-breakdown${qs}&days=30`).then((r) => r.json()),
      fetch(`${BACKEND}/api/profitability/by-route${qs}&days=30`).then((r) => r.json()),
    ])
      .then(([s, t, c, v, cb, r]) => {
        setSummary(s)
        setTrend(t)
        setCustomers(c)
        setVehicles(v)
        setCosts(cb)
        setRoutes(r.slice(0, 5))
      })
      .catch(() => {})
  }

  useEffect(() => {
    const stored = localStorage.getItem('logiflow_company_id')
    setCompanyId(stored)
    fetchAll(stored)
  }, [])

  const handleSeed = async () => {
    setSeeding(true)
    try {
      const res = await fetch(`${BACKEND}/api/seed`, { method: 'POST' })
      const data = await res.json()
      if (data.company_id) {
        localStorage.setItem('logiflow_company_id', data.company_id)
        setCompanyId(data.company_id)
        fetchAll(data.company_id)
      }
    } finally {
      setSeeding(false)
    }
  }

  const kpis = summary
    ? [
        { title: 'Revenue', value: fmt(summary.revenue_eur), delta: '+12.4%', trend: 'up' as const, subtitle: 'Last 30 days' },
        { title: 'Direct Costs', value: fmt(summary.direct_cost_eur), delta: '+8.1%', trend: 'up' as const, subtitle: 'Last 30 days' },
        { title: 'Gross Margin', value: fmt(summary.gross_margin_eur), delta: '+2.1%', trend: 'up' as const, subtitle: 'Last 30 days' },
        { title: 'Margin %', value: `${summary.margin_pct}%`, delta: '+0.8pp', trend: 'up' as const, subtitle: 'vs prior period' },
        { title: 'Trips', value: String(summary.trip_count), delta: '+6', trend: 'up' as const, subtitle: 'Last 30 days' },
        { title: 'Active Vehicles', value: String(summary.active_vehicles), delta: '—', trend: 'neutral' as const, subtitle: 'in fleet' },
      ]
    : Array(6).fill({ title: '—', value: '…', delta: '', trend: 'neutral' as const, subtitle: '' })

  return (
    <div>
      {/* Header */}
      <div className="mb-6 flex items-start justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Operations Dashboard</h1>
          <p className="text-sm text-gray-500 mt-1">
            {companyId ? 'Live data · Last 30 days' : 'Demo data · '}
            {!companyId && (
              <button
                onClick={handleSeed}
                disabled={seeding}
                className="underline text-brand-600 hover:text-brand-700 disabled:opacity-50"
              >
                {seeding ? 'Loading…' : 'Load demo data'}
              </button>
            )}
          </p>
        </div>
      </div>

      {/* KPI cards */}
      <div className="grid grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
        {kpis.map((kpi, i) => <KpiCard key={i} {...kpi} />)}
      </div>

      {/* Row 1: Monthly trend + Cost breakdown */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <div className="bg-white rounded-xl border border-gray-100 p-6 shadow-sm">
          <h2 className="text-sm font-semibold text-gray-700 mb-4">Monthly Revenue vs Costs</h2>
          <MonthlyTrendChart data={trend as Parameters<typeof MonthlyTrendChart>[0]['data']} />
        </div>

        <div className="bg-white rounded-xl border border-gray-100 p-6 shadow-sm">
          <h2 className="text-sm font-semibold text-gray-700 mb-4">Cost Breakdown</h2>
          <CostBreakdownChart data={costs as Parameters<typeof CostBreakdownChart>[0]['data']} />
        </div>
      </div>

      {/* Row 2: Customer margin + Vehicle utilization */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <div className="bg-white rounded-xl border border-gray-100 p-6 shadow-sm">
          <h2 className="text-sm font-semibold text-gray-700 mb-4">Top Customers — Margin %</h2>
          <CustomerMarginChart data={customers as Parameters<typeof CustomerMarginChart>[0]['data']} />
        </div>

        <div className="bg-white rounded-xl border border-gray-100 p-6 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-sm font-semibold text-gray-700">Vehicle Trips (30 days)</h2>
            <span className="text-xs text-gray-400">Color = margin tier</span>
          </div>
          <VehicleUtilizationChart data={vehicles as Parameters<typeof VehicleUtilizationChart>[0]['data']} />
          <div className="flex gap-4 mt-2 justify-end">
            {[['#10b981', '≥30%'], ['#3b82f6', '15–30%'], ['#ef4444', '<15%']].map(([c, l]) => (
              <div key={l} className="flex items-center gap-1">
                <div className="w-2 h-2 rounded-full" style={{ backgroundColor: c }} />
                <span className="text-xs text-gray-400">{l}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Row 3: Low-margin routes table */}
      <div className="bg-white rounded-xl border border-gray-100 p-6 shadow-sm">
        <h2 className="text-sm font-semibold text-gray-700 mb-4">
          Routes — Lowest Margin First
          <span className="ml-2 text-xs font-normal text-gray-400">Action required on red rows</span>
        </h2>
        {routes.length === 0 ? (
          <p className="text-sm text-gray-400 text-center py-6">No route data yet — upload trips CSV to populate</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-left text-xs text-gray-400 border-b border-gray-100">
                  <th className="pb-2 font-medium">Route</th>
                  <th className="pb-2 font-medium text-right">Avg Revenue</th>
                  <th className="pb-2 font-medium text-right">Avg Cost</th>
                  <th className="pb-2 font-medium text-right">Margin %</th>
                  <th className="pb-2 font-medium text-right">Trips</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-50">
                {(routes as Array<{
                  origin: string; destination: string;
                  avg_revenue_eur: number; avg_cost_eur: number;
                  avg_margin_pct: number; trip_count: number
                }>).map((r) => (
                  <tr key={`${r.origin}-${r.destination}`} className="hover:bg-gray-50">
                    <td className="py-2.5 font-medium text-gray-800">{r.origin} → {r.destination}</td>
                    <td className="py-2.5 text-right text-gray-600">{fmt(r.avg_revenue_eur)}</td>
                    <td className="py-2.5 text-right text-gray-600">{fmt(r.avg_cost_eur)}</td>
                    <td className={`py-2.5 text-right font-semibold
                      ${r.avg_margin_pct < 15 ? 'text-red-500' :
                        r.avg_margin_pct < 25 ? 'text-amber-500' : 'text-green-600'}`}>
                      {r.avg_margin_pct}%
                    </td>
                    <td className="py-2.5 text-right text-gray-400">{r.trip_count}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  )
}
