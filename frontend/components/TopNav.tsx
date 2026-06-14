export default function TopNav() {
  return (
    <header className="h-14 bg-white border-b border-gray-100 flex items-center justify-between px-6 shrink-0">
      <div className="flex items-center gap-2">
        <select className="text-sm border border-gray-200 rounded-lg px-3 py-1.5 text-gray-600 bg-white focus:outline-none focus:ring-2 focus:ring-brand-500">
          <option>June 2026</option>
          <option>May 2026</option>
          <option>April 2026</option>
          <option>Q2 2026</option>
        </select>
      </div>
      <div className="flex items-center gap-3">
        <button className="text-sm text-gray-500 hover:text-gray-700 px-3 py-1.5 rounded-lg hover:bg-gray-50 transition-colors">
          Export
        </button>
        <div className="w-8 h-8 rounded-full bg-brand-100 flex items-center justify-center text-sm font-bold text-brand-700 cursor-pointer hover:bg-brand-200 transition-colors">
          D
        </div>
      </div>
    </header>
  )
}
