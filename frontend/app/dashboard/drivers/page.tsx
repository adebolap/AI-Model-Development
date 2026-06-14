export default function DriversPage() {
  const STUB = [
    { name: 'Mohamed El Ouafi', license: 'CE', trips: 22, margin: 36.4, active: true },
    { name: 'Jean-Pierre Dumont', license: 'CE', trips: 18, margin: 32.1, active: true },
    { name: 'Lieve Vandenberghe', license: 'C', trips: 14, margin: 28.7, active: true },
  ]

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Drivers</h1>
      <div className="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-gray-50 border-b border-gray-100">
            <tr className="text-left text-xs text-gray-500">
              <th className="px-4 py-3 font-medium">Name</th>
              <th className="px-4 py-3 font-medium">License</th>
              <th className="px-4 py-3 font-medium text-right">Trips (month)</th>
              <th className="px-4 py-3 font-medium text-right">Avg Margin %</th>
              <th className="px-4 py-3 font-medium text-right">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-50">
            {STUB.map((d) => (
              <tr key={d.name} className="hover:bg-gray-50">
                <td className="px-4 py-3 font-medium text-gray-800">{d.name}</td>
                <td className="px-4 py-3 text-gray-500 font-mono">{d.license}</td>
                <td className="px-4 py-3 text-right text-gray-600">{d.trips}</td>
                <td className="px-4 py-3 text-right font-semibold text-green-600">{d.margin}%</td>
                <td className="px-4 py-3 text-right">
                  <span className="text-xs px-2 py-0.5 rounded-full bg-green-100 text-green-700">Active</span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
