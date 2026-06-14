'use client'

import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from 'recharts'

interface DataPoint {
  month: string
  revenue_eur: number
  cost_eur: number
  trips: number
}

interface Props {
  data: DataPoint[]
}

const fmt = (v: number) =>
  `€${(v / 1000).toFixed(0)}k`

export default function MonthlyTrendChart({ data }: Props) {
  if (!data.length) {
    return <div className="h-52 flex items-center justify-center text-sm text-gray-400">No data</div>
  }
  return (
    <ResponsiveContainer width="100%" height={210}>
      <LineChart data={data} margin={{ top: 4, right: 8, left: 0, bottom: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#f3f4f6" />
        <XAxis dataKey="month" tick={{ fontSize: 11, fill: '#9ca3af' }} axisLine={false} tickLine={false} />
        <YAxis tickFormatter={fmt} tick={{ fontSize: 11, fill: '#9ca3af' }} axisLine={false} tickLine={false} width={44} />
        <Tooltip
          formatter={(v: number, name: string) => [
            `€${v.toLocaleString('fr-BE')}`,
            name === 'revenue_eur' ? 'Revenue' : 'Costs',
          ]}
          contentStyle={{ fontSize: 12, border: '1px solid #e5e7eb', borderRadius: 8 }}
        />
        <Legend
          formatter={(v) => (v === 'revenue_eur' ? 'Revenue' : 'Costs')}
          iconType="circle"
          iconSize={8}
          wrapperStyle={{ fontSize: 11, paddingTop: 8 }}
        />
        <Line
          type="monotone"
          dataKey="revenue_eur"
          stroke="#3b82f6"
          strokeWidth={2.5}
          dot={{ r: 3, fill: '#3b82f6' }}
          activeDot={{ r: 5 }}
        />
        <Line
          type="monotone"
          dataKey="cost_eur"
          stroke="#f59e0b"
          strokeWidth={2}
          strokeDasharray="4 3"
          dot={{ r: 3, fill: '#f59e0b' }}
          activeDot={{ r: 5 }}
        />
      </LineChart>
    </ResponsiveContainer>
  )
}
