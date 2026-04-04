import type { VibeVector } from '../types/vibe'
import { VIBE_DIMENSIONS } from '../types/vibe'

interface VibeSummaryProps {
  vibe: VibeVector
}

export function VibeSummary({ vibe }: VibeSummaryProps) {
  return (
    <div className="panel-section fade-in">
      <div className="panel-section__title">◈ Interpreted Vibe</div>

      <div style={{ marginBottom: 12 }}>
        <span style={{
          display: 'inline-block',
          padding: '3px 10px',
          background: 'rgba(124,92,252,0.15)',
          border: '1px solid rgba(124,92,252,0.4)',
          borderRadius: 20,
          fontSize: 10,
          color: 'var(--color-primary)',
          fontFamily: 'var(--font-display)',
          fontWeight: 700,
          textTransform: 'uppercase',
          letterSpacing: '0.08em',
          marginBottom: 8,
        }}>
          {vibe.archetype}
        </span>
        <p style={{ fontSize: 11, color: 'var(--color-text-secondary)', lineHeight: 1.5 }}>
          {vibe.description}
        </p>
      </div>

      {VIBE_DIMENSIONS.map((dim) => {
        const val = (vibe as any)[dim.key] as number
        return (
          <div key={dim.key} className="vibe-bar-row">
            <span className="vibe-bar-label">{dim.label}</span>
            <div className="vibe-bar-track">
              <div className="vibe-bar-fill" style={{ width: `${val * 100}%` }} />
            </div>
            <span className="vibe-bar-val">{Math.round(val * 100)}</span>
          </div>
        )
      })}
    </div>
  )
}
