import clsx from 'clsx'

interface KpiCardProps {
  title: string
  value: string
  delta: string
  trend: 'up' | 'down' | 'neutral'
  subtitle: string
}

export default function KpiCard({ title, value, delta, trend, subtitle }: KpiCardProps) {
  return (
    <div className="bg-white rounded-xl border border-gray-100 p-5 shadow-sm hover:shadow-md transition-shadow">
      <div className="text-xs font-medium text-gray-400 uppercase tracking-wide mb-2">{title}</div>
      <div className="text-2xl font-bold text-gray-900 mb-1">{value}</div>
      <div className="flex items-center gap-1.5">
        <span className={clsx(
          'text-xs font-semibold',
          trend === 'up' && 'text-green-500',
          trend === 'down' && 'text-red-500',
          trend === 'neutral' && 'text-gray-400',
        )}>
          {trend === 'up' ? '↑' : trend === 'down' ? '↓' : '→'} {delta}
        </span>
        <span className="text-xs text-gray-400">{subtitle}</span>
      </div>
    </div>
  )
}
