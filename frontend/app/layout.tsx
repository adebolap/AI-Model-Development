import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'LogiFlow — Logistics Profitability Dashboard',
  description: 'AI-powered profitability analytics for Belgian transport companies',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
