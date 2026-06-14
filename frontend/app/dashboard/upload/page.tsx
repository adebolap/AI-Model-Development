'use client'

import { useState } from 'react'

export default function UploadPage() {
  const [dragOver, setDragOver] = useState(false)
  const [status, setStatus] = useState<'idle' | 'uploading' | 'success' | 'error'>('idle')
  const [message, setMessage] = useState('')

  const handleFile = async (file: File) => {
    setStatus('uploading')
    setMessage('')
    const formData = new FormData()
    formData.append('file', file)
    const endpoint = file.name.toLowerCase().includes('invoice') ? 'invoices' : 'trips'

    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/api/upload/${endpoint}`, {
        method: 'POST',
        body: formData,
      })
      const data = await res.json()
      if (data.success) {
        setStatus('success')
        setMessage(`Imported ${data.rows_imported} rows successfully.`)
      } else {
        setStatus('error')
        setMessage(`${data.errors.length} validation errors found. Fix them and re-upload.`)
      }
    } catch {
      setStatus('error')
      setMessage('Upload failed. Is the backend running?')
    }
  }

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 mb-2">Upload Data</h1>
      <p className="text-sm text-gray-500 mb-6">Upload CSV or Excel files for trips or invoices. Max 10 MB per file.</p>

      <div
        className={`border-2 border-dashed rounded-xl p-12 text-center transition-colors cursor-pointer
          ${dragOver ? 'border-brand-500 bg-brand-50' : 'border-gray-200 bg-white hover:border-brand-300'}`}
        onDragOver={(e) => { e.preventDefault(); setDragOver(true) }}
        onDragLeave={() => setDragOver(false)}
        onDrop={(e) => {
          e.preventDefault()
          setDragOver(false)
          const file = e.dataTransfer.files[0]
          if (file) handleFile(file)
        }}
        onClick={() => document.getElementById('file-input')?.click()}
      >
        <input
          id="file-input"
          type="file"
          accept=".csv,.xlsx"
          className="hidden"
          onChange={(e) => {
            const file = e.target.files?.[0]
            if (file) handleFile(file)
          }}
        />
        <div className="text-4xl mb-3">{status === 'uploading' ? '⏳' : '📂'}</div>
        <p className="text-gray-600 font-medium mb-1">
          {status === 'uploading' ? 'Uploading...' : 'Drop your CSV or Excel file here'}
        </p>
        <p className="text-sm text-gray-400">or click to browse — trips.csv or invoices.csv</p>
      </div>

      {message && (
        <div className={`mt-4 p-4 rounded-lg text-sm font-medium
          ${status === 'success' ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-600'}`}>
          {message}
        </div>
      )}

      <div className="mt-8 grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-white border border-gray-100 rounded-xl p-5 shadow-sm">
          <h3 className="font-semibold text-gray-800 mb-2">Trips CSV columns</h3>
          <p className="text-xs text-gray-500 mb-2">Required columns:</p>
          <code className="text-xs text-brand-700 bg-brand-50 px-2 py-1 rounded block">
            origin, destination, departure_date, revenue_eur, customer_name, vehicle_plate
          </code>
        </div>
        <div className="bg-white border border-gray-100 rounded-xl p-5 shadow-sm">
          <h3 className="font-semibold text-gray-800 mb-2">Invoices CSV columns</h3>
          <p className="text-xs text-gray-500 mb-2">Required columns:</p>
          <code className="text-xs text-brand-700 bg-brand-50 px-2 py-1 rounded block">
            customer_name, amount_eur, issued_date, status
          </code>
        </div>
      </div>
    </div>
  )
}
