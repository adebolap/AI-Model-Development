export default function VehiclesPage() {
  const STUB = [
    { plate: '1-ABC-234', type: 'Truck', brand: 'Volvo FH16', fuel: 'Diesel', utilization: 88, margin: 39.1, active: true },
    { plate: '2-DEF-567', type: 'Van', brand: 'Mercedes Sprinter', fuel: 'Diesel', utilization: 72, margin: 27.6, active: true },
    { plate: '3-GHI-890', type: 'Truck', brand: 'DAF XF', fuel: 'Diesel', utilization: 32, margin: 4.2, active: false },
  ]

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Vehicles</h1>
      <div className="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-gray-50 border-b border-gray-100">
            <tr className="text-left text-xs text-gray-500">
              <th className="px-4 py-3 font-medium">Plate</th>
              <th className="px-4 py-3 font-medium">Type</th>
              <th className="px-4 py-3 font-medium">Brand</th>
              <th className="px-4 py-3 font-medium">Fuel</th>
              <th className="px-4 py-3 font-medium text-right">Utilization</th>
              <th className="px-4 py-3 font-medium text-right">Margin %</th>
              <th className="px-4 py-3 font-medium text-right">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-50">
            {STUB.map((v) => (
              <tr key={v.plate} className="hover:bg-gray-50">
                <td className="px-4 py-3 font-mono font-medium text-brand-700">{v.plate}</td>
                <td className="px-4 py-3 text-gray-600">{v.type}</td>
                <td className="px-4 py-3 text-gray-600">{v.brand}</td>
                <td className="px-4 py-3 text-gray-400">{v.fuel}</td>
                <td className="px-4 py-3 text-right text-gray-600">{v.utilization}%</td>
                <td className={`px-4 py-3 text-right font-semibold ${v.margin < 15 ? 'text-red-500' : 'text-green-600'}`}>
                  {v.margin}%
                </td>
                <td className="px-4 py-3 text-right">
                  <span className={`text-xs px-2 py-0.5 rounded-full ${v.active ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-400'}`}>
                    {v.active ? 'Active' : 'Inactive'}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
