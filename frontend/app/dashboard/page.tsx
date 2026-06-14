import KpiCard from '@/components/KpiCard'

const KPI_DATA = [
  { title: 'Revenue', value: '€48,200', delta: '+12.4%', trend: 'up', subtitle: 'This month' },
  { title: 'Direct Costs', value: '€31,800', delta: '+8.1%', trend: 'up', subtitle: 'This month' },
  { title: 'Gross Margin', value: '€16,400', delta: '+2.1%', trend: 'up', subtitle: 'This month' },
  { title: 'Margin %', value: '34.0%', delta: '+0.8pp', trend: 'up', subtitle: 'vs last month' },
  { title: 'Trips', value: '54', delta: '+6', trend: 'up', subtitle: 'This month' },
  { title: 'Active Vehicles', value: '8', delta: '0', trend: 'neutral', subtitle: 'of 10 total' },
]

export default function DashboardPage() {
  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Operations Dashboard</h1>
        <p className="text-sm text-gray-500 mt-1">June 2026 — Transport Dupont SPRL</p>
      </div>

      <div className="grid grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
        {KPI_DATA.map((kpi) => (
          <KpiCard key={kpi.title} {...kpi} />
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <div className="bg-white rounded-xl border border-gray-100 p-6 shadow-sm">
          <h2 className="text-sm font-semibold text-gray-700 mb-4">Monthly Revenue Trend</h2>
          <div className="h-40 flex items-end gap-2">
            {[32, 38, 41, 36, 44, 48].map((v, i) => (
              <div key={i} className="flex-1 flex flex-col items-center gap-1">
                <div
                  className="w-full bg-brand-500 rounded-t-sm opacity-80 hover:opacity-100 transition-opacity"
                  style={{ height: `${(v / 48) * 100}%` }}
                  title={`€${v}k`}
                />
                <span className="text-xs text-gray-400">{['Jan','Feb','Mar','Apr','May','Jun'][i]}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-xl border border-gray-100 p-6 shadow-sm">
          <h2 className="text-sm font-semibold text-gray-700 mb-4">Top Customers by Margin</h2>
          <div className="space-y-3">
            {[
              { name: 'Colruyt', margin: 44.3, revenue: 7000 },
              { name: 'Delhaize Group', margin: 40.1, revenue: 18200 },
              { name: 'AB InBev', margin: 30.5, revenue: 14100 },
              { name: 'Proximus', margin: 19.1, revenue: 8900 },
            ].map((c) => (
              <div key={c.name} className="flex items-center gap-3">
                <div className="w-28 text-xs text-gray-600 font-medium truncate">{c.name}</div>
                <div className="flex-1 bg-gray-100 rounded-full h-2">
                  <div
                    className="h-2 rounded-full bg-brand-500"
                    style={{ width: `${c.margin}%` }}
                  />
                </div>
                <div className="w-12 text-xs text-gray-500 text-right">{c.margin}%</div>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="bg-white rounded-xl border border-gray-100 p-6 shadow-sm">
        <h2 className="text-sm font-semibold text-gray-700 mb-4">Low-Margin Routes — Action Required</h2>
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
              {[
                { route: 'Ghent → Amsterdam', revenue: 1400, cost: 1340, margin: 4.3, trips: 4 },
                { route: 'Liège → Frankfurt', revenue: 1650, cost: 1430, margin: 13.3, trips: 6 },
                { route: 'Antwerp → Paris', revenue: 2100, cost: 1540, margin: 26.7, trips: 8 },
              ].map((r) => (
                <tr key={r.route} className="hover:bg-gray-50">
                  <td className="py-2 font-medium text-gray-800">{r.route}</td>
                  <td className="py-2 text-right text-gray-600">€{r.revenue.toLocaleString()}</td>
                  <td className="py-2 text-right text-gray-600">€{r.cost.toLocaleString()}</td>
                  <td className={`py-2 text-right font-semibold ${r.margin < 15 ? 'text-red-500' : 'text-amber-500'}`}>
                    {r.margin}%
                  </td>
                  <td className="py-2 text-right text-gray-400">{r.trips}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
