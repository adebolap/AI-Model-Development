'use client'

import { ResponsiveContainer, PieChart, Pie, Cell, Tooltip, Legend } from 'recharts'

interface DataPoint {
  name: string
  value: number
  color: string
}

interface Props {
  data: DataPoint[]
}

export default function CostBreakdownChart({ data }: Props) {
  if (!data.length) {
    return <div className="h-52 flex items-center justify-center text-sm text-gray-400">No data</div>
  }

  const total = data.reduce((s, d) => s + d.value, 0)

  return (
    <div className="flex items-center gap-4">
      <ResponsiveContainer width="50%" height={190}>
        <PieChart>
          <Pie
            data={data}
            dataKey="value"
            nameKey="name"
            cx="50%"
            cy="50%"
            innerRadius={55}
            outerRadius={80}
            paddingAngle={2}
          >
            {data.map((entry, i) => (
              <Cell key={i} fill={entry.color} />
            ))}
          </Pie>
          <Tooltip
            formatter={(v: number) => [`€${v.toLocaleString('fr-BE')}`, '']}
            contentStyle={{ fontSize: 12, border: '1px solid #e5e7eb', borderRadius: 8 }}
          />
        </PieChart>
      </ResponsiveContainer>

      <div className="flex-1 space-y-2">
        {data.map((entry) => (
          <div key={entry.name} className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="w-2.5 h-2.5 rounded-full shrink-0" style={{ backgroundColor: entry.color }} />
              <span className="text-xs text-gray-600">{entry.name}</span>
            </div>
            <div className="text-right">
              <div className="text-xs font-medium text-gray-800">€{entry.value.toLocaleString('fr-BE')}</div>
              <div className="text-xs text-gray-400">{total > 0 ? Math.round((entry.value / total) * 100) : 0}%</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
