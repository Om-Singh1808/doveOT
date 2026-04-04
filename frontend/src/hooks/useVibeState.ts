import { useState, useCallback } from 'react'
import type { VibeVector, PipelineStatus, GenerateResponse } from '../types/vibe'

const DEFAULT_VIBE: Omit<VibeVector, 'archetype' | 'description'> = {
  softness: 0.5,
  complexity: 0.3,
  weight: 0.5,
  symmetry: 0.8,
  fluidity: 0.2,
  density: 0.4,
  height_ratio: 0.5,
  taper: 0.3,
}

export function useVibeState() {
  const [prompt, setPrompt] = useState('')
  const [sliders, setSliders] = useState(DEFAULT_VIBE)
  const [status, setStatus] = useState<PipelineStatus>('idle')
  const [result, setResult] = useState<GenerateResponse | null>(null)
  const [error, setError] = useState<string | null>(null)

  const updateSlider = useCallback(
    (key: keyof typeof DEFAULT_VIBE, value: number) => {
      setSliders((prev) => ({ ...prev, [key]: value }))
    },
    []
  )

  const resetSliders = useCallback(() => {
    setSliders(DEFAULT_VIBE)
  }, [])

  return {
    prompt,
    setPrompt,
    sliders,
    updateSlider,
    resetSliders,
    status,
    setStatus,
    result,
    setResult,
    error,
    setError,
  }
}
