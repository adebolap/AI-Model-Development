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
  customer: string
  margin_pct: number
  revenue_eur: number
}

interface Props {
  data: DataPoint[]
}

const BAR_COLOR = (margin: number) =>
  margin >= 35 ? '#10b981' : margin >= 20 ? '#3b82f6' : '#f59e0b'

export default function CustomerMarginChart({ data }: Props) {
  if (!data.length) {
    return <div className="h-52 flex items-center justify-center text-sm text-gray-400">No data</div>
  }

  const display = [...data].sort((a, b) => b.margin_pct - a.margin_pct).slice(0, 5)

  return (
    <ResponsiveContainer width="100%" height={210}>
      <BarChart data={display} layout="vertical" margin={{ top: 4, right: 24, left: 0, bottom: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#f3f4f6" horizontal={false} />
        <XAxis
          type="number"
          domain={[0, 100]}
          tick={{ fontSize: 11, fill: '#9ca3af' }}
          axisLine={false}
          tickLine={false}
          tickFormatter={(v) => `${v}%`}
        />
        <YAxis
          type="category"
          dataKey="customer"
          tick={{ fontSize: 11, fill: '#374151' }}
          axisLine={false}
          tickLine={false}
          width={110}
        />
        <Tooltip
          formatter={(v: number) => [`${v}%`, 'Margin']}
          contentStyle={{ fontSize: 12, border: '1px solid #e5e7eb', borderRadius: 8 }}
        />
        <Bar dataKey="margin_pct" radius={[0, 4, 4, 0]}>
          {display.map((entry, i) => (
            <Cell key={i} fill={BAR_COLOR(entry.margin_pct)} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  )
}
