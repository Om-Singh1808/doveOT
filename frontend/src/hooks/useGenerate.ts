import { useCallback } from 'react'
import { generateModel } from '../services/api'
import type { PipelineStatus, GenerateResponse } from '../types/vibe'

interface UseGenerateOptions {
  prompt: string
  sliders: Record<string, number>
  setStatus: (s: PipelineStatus) => void
  setResult: (r: GenerateResponse) => void
  setError: (e: string | null) => void
}

export function useGenerate({
  prompt,
  sliders,
  setStatus,
  setResult,
  setError,
}: UseGenerateOptions) {
  const generate = useCallback(async () => {
    if (!prompt.trim()) return
    setError(null)
    setStatus('interpreting')

    try {
      // Step 1: AI interprets the vibe
      const response = await generateModel({
        prompt,
        slider_overrides: sliders as any,
      })

      setStatus('modeling')
      // Short delay for UX feedback (the backend does actual work)
      await new Promise((r) => setTimeout(r, 600))

      setStatus('analyzing')
      await new Promise((r) => setTimeout(r, 400))

      setStatus('slicing')
      await new Promise((r) => setTimeout(r, 400))

      setResult(response)
      setStatus('done')
    } catch (e: any) {
      setError(e.message ?? 'Generation failed')
      setStatus('error')
    }
  }, [prompt, sliders, setStatus, setResult, setError])

  return { generate }
}
