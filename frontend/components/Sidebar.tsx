'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import clsx from 'clsx'

const NAV = [
  { href: '/dashboard', label: 'Dashboard', icon: '📊' },
  { href: '/dashboard/trips', label: 'Trips', icon: '🚛' },
  { href: '/dashboard/vehicles', label: 'Vehicles', icon: '🚜' },
  { href: '/dashboard/drivers', label: 'Drivers', icon: '👤' },
  { href: '/dashboard/upload', label: 'Upload Data', icon: '📂' },
  { href: '/dashboard/ai', label: 'AI Assistant', icon: '🤖' },
]

export default function Sidebar() {
  const pathname = usePathname()

  return (
    <aside className="w-60 shrink-0 bg-white border-r border-gray-100 flex flex-col">
      <div className="px-5 py-5 border-b border-gray-100">
        <div className="text-xl font-bold text-brand-700">LogiFlow</div>
        <div className="text-xs text-gray-400 mt-0.5">Transport Dupont SPRL</div>
      </div>

      <nav className="flex-1 px-3 py-4 space-y-0.5">
        {NAV.map((item) => {
          const active = pathname === item.href
          return (
            <Link
              key={item.href}
              href={item.href}
              className={clsx(
                'flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors',
                active
                  ? 'bg-brand-50 text-brand-700'
                  : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
              )}
            >
              <span className="text-base">{item.icon}</span>
              {item.label}
            </Link>
          )
        })}
      </nav>

      <div className="px-5 py-4 border-t border-gray-100">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-full bg-brand-100 flex items-center justify-center text-sm font-bold text-brand-700">
            D
          </div>
          <div className="flex-1 min-w-0">
            <div className="text-xs font-medium text-gray-800 truncate">Demo User</div>
            <div className="text-xs text-gray-400">Starter plan</div>
          </div>
        </div>
      </div>
    </aside>
  )
}
