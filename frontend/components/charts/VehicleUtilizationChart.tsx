'use client'

import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Cell,
} from 'recharts'

interface DataPoint {
  plate: string
  trips: number
  revenue_eur: number
  margin_pct: number
}

interface Props {
  data: DataPoint[]
}

const MARGIN_COLOR = (m: number) =>
  m >= 30 ? '#10b981' : m >= 15 ? '#3b82f6' : '#ef4444'

export default function VehicleUtilizationChart({ data }: Props) {
  if (!data.length) {
    return <div className="h-52 flex items-center justify-center text-sm text-gray-400">No data</div>
  }

  return (
    <ResponsiveContainer width="100%" height={210}>
      <BarChart data={data} margin={{ top: 4, right: 8, left: 0, bottom: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#f3f4f6" />
        <XAxis
          dataKey="plate"
          tick={{ fontSize: 10, fill: '#6b7280', fontFamily: 'monospace' }}
          axisLine={false}
          tickLine={false}
        />
        <YAxis
          tick={{ fontSize: 11, fill: '#9ca3af' }}
          axisLine={false}
          tickLine={false}
          label={{ value: 'Trips', angle: -90, position: 'insideLeft', fontSize: 10, fill: '#9ca3af', dx: -4 }}
        />
        <Tooltip
          formatter={(v: number, name: string) => [
            name === 'trips' ? v : `${v}%`,
            name === 'trips' ? 'Trips' : 'Margin %',
          ]}
          contentStyle={{ fontSize: 12, border: '1px solid #e5e7eb', borderRadius: 8 }}
        />
        <Bar dataKey="trips" radius={[4, 4, 0, 0]}>
          {data.map((entry, i) => (
            <Cell key={i} fill={MARGIN_COLOR(entry.margin_pct)} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  )
}
