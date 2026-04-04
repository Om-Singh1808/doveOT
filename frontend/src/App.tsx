import { useState, useMemo } from 'react'
import './index.css'
import { PromptInput } from './components/PromptInput'
import { VibeSliders } from './components/VibeSliders'
import { ModelViewer } from './components/ModelViewer'
import { GenerateButton } from './components/GenerateButton'
import { StatusIndicator } from './components/StatusIndicator'
import { PrintSettingsPanel } from './components/PrintSettings'
import { ExportPanel } from './components/ExportPanel'
import { VibeSummary } from './components/VibeSummary'
import { useVibeState } from './hooks/useVibeState'
import { useGenerate } from './hooks/useGenerate'
import type { ObjectArchetype, VibeVector } from './types/vibe'

// Declare the Electron context bridge types
declare global {
  interface Window {
    electronAPI?: {
      minimize: () => void
      maximize: () => void
      close: () => void
    }
  }
}

export default function App() {
  const {
    prompt, setPrompt,
    sliders, updateSlider,
    status, setStatus,
    result, setResult,
    error, setError,
  } = useVibeState()

  const [forcedArchetype, setForcedArchetype] = useState<ObjectArchetype | null>(null)

  const { generate } = useGenerate({
    prompt,
    sliders,
    setStatus,
    setResult,
    setError,
  })

  // Build a "live preview" vibe from sliders for real-time 3D update
  const liveVibe = useMemo<VibeVector>(() => ({
    archetype: forcedArchetype ?? (result?.vibe_vector?.archetype ?? 'stand'),
    softness: sliders.softness,
    complexity: sliders.complexity,
    weight: sliders.weight,
    symmetry: sliders.symmetry,
    fluidity: sliders.fluidity,
    density: sliders.density,
    height_ratio: sliders.height_ratio,
    taper: sliders.taper,
    description: '',
  }), [sliders, forcedArchetype, result])

  return (
    <div className="app-shell">
      {/* ── Title Bar ── */}
      <header className="titlebar">
        <div className="titlebar__logo">
          <span className="titlebar__logo-dot" />
          VibePrint
        </div>
        <div className="titlebar__controls">
          <button
            className="titlebar__btn titlebar__btn--close"
            onClick={() => window.electronAPI?.close()}
            title="Close"
          />
          <button
            className="titlebar__btn titlebar__btn--min"
            onClick={() => window.electronAPI?.minimize()}
            title="Minimize"
          />
          <button
            className="titlebar__btn titlebar__btn--max"
            onClick={() => window.electronAPI?.maximize()}
            title="Maximize"
          />
        </div>
      </header>

      {/* ── Left Panel: Prompt + Sliders ── */}
      <aside className="panel-left">
        <PromptInput
          value={prompt}
          onChange={setPrompt}
          onExample={setPrompt}
          forcedArchetype={forcedArchetype}
          onArchetypeOverride={setForcedArchetype}
        />
        <VibeSliders sliders={sliders} onChange={(key, val) => updateSlider(key as keyof typeof sliders, val)} />
        <GenerateButton
          onClick={generate}
          status={status}
          disabled={!prompt.trim()}
        />
      </aside>

      {/* ── Center: 3D Viewer ── */}
      <main className="panel-center">
        <ModelViewer vibe={liveVibe} stlUrl={result?.stl_url} />
        <StatusIndicator status={status} error={error} />
      </main>

      {/* ── Right Panel: Results ── */}
      <aside className="panel-right">
        {result?.vibe_vector && (
          <VibeSummary vibe={result.vibe_vector} />
        )}
        <PrintSettingsPanel
          settings={result?.print_settings}
          report={result?.print_report}
        />
        <ExportPanel
          stlUrl={result?.stl_url}
          gcodeUrl={result?.gcode_url}
        />
      </aside>
    </div>
  )
}
