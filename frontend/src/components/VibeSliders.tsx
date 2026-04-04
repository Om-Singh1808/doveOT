import { VIBE_DIMENSIONS } from '../types/vibe'

interface VibeSlidersProps {
  sliders: Record<string, number>
  onChange: (key: string, value: number) => void
}

export function VibeSliders({ sliders, onChange }: VibeSlidersProps) {
  return (
    <div className="panel-section" style={{ flex: 1 }}>
      <div className="panel-section__title">〜 Vibe Dimensions</div>
      {VIBE_DIMENSIONS.map((dim) => {
        const val = sliders[dim.key] ?? 0.5
        return (
          <div key={dim.key} className="vibe-slider-row">
            <div className="vibe-slider-header">
              <span className="vibe-slider-label">
                <span className="vibe-slider-icon">{dim.icon}</span>
                {dim.label}
              </span>
              <span className="vibe-slider-value">{Math.round(val * 100)}</span>
            </div>
            <input
              id={`slider-${dim.key}`}
              type="range"
              className="vibe-range"
              min={0}
              max={1}
              step={0.01}
              value={val}
              style={{
                background: `linear-gradient(90deg, var(--color-primary) ${val * 100}%, var(--color-bg-elevated) ${val * 100}%)`,
              }}
              onChange={(e) => onChange(dim.key, parseFloat(e.target.value))}
            />
            <div className="vibe-slider-ends">
              <span>{dim.lowLabel}</span>
              <span>{dim.highLabel}</span>
            </div>
          </div>
        )
      })}
    </div>
  )
}
