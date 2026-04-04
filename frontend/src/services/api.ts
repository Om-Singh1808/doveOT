import type { GenerateRequest, GenerateResponse } from '../types/vibe'

const API_BASE = 'http://127.0.0.1:8000/api'

export async function generateModel(request: GenerateRequest): Promise<GenerateResponse> {
  const response = await fetch(`${API_BASE}/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(request),
  })

  if (!response.ok) {
    const err = await response.json().catch(() => ({ detail: 'Unknown error' }))
    throw new Error(err.detail ?? `HTTP ${response.status}`)
  }

  return response.json()
}

export async function checkHealth(): Promise<boolean> {
  try {
    const res = await fetch('http://127.0.0.1:8000/')
    return res.ok
  } catch {
    return false
  }
}
