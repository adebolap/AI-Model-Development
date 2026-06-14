export default function TripsPage() {
  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 mb-2">Trips</h1>
      <p className="text-sm text-gray-500 mb-6">All trips for this period. Upload a CSV to populate.</p>
      <div className="bg-white rounded-xl border border-gray-100 p-12 text-center shadow-sm">
        <div className="text-4xl mb-3">🚛</div>
        <h2 className="text-lg font-semibold text-gray-700 mb-2">No trips yet</h2>
        <p className="text-sm text-gray-400 mb-4">Upload your dispatch CSV to start analyzing routes and profitability.</p>
        <a href="/dashboard/upload" className="inline-block bg-brand-600 text-white text-sm font-medium px-4 py-2 rounded-lg hover:bg-brand-700 transition-colors">
          Upload CSV
        </a>
      </div>
    </div>
  )
}
