import type { PrintSettings, PrintReport } from '../types/vibe'

interface PrintSettingsPanelProps {
  settings?: PrintSettings
  report?: PrintReport
}

function ScoreRing({ score }: { score: number }) {
  const radius = 28
  const circ = 2 * Math.PI * radius
  const dash = (score / 100) * circ
  const color = score > 75 ? '#27c93f' : score > 45 ? '#f9c843' : '#fe53bb'

  return (
    <div className="score-ring">
      <svg width={72} height={72} viewBox="0 0 72 72">
        <circle cx={36} cy={36} r={radius} fill="none" stroke="#1a1a30" strokeWidth={6} />
        <circle
          cx={36} cy={36} r={radius}
          fill="none"
          stroke={color}
          strokeWidth={6}
          strokeDasharray={`${dash} ${circ}`}
          strokeLinecap="round"
          style={{ filter: `drop-shadow(0 0 4px ${color})`, transition: 'stroke-dasharray 0.6s ease' }}
        />
      </svg>
      <div className="score-ring__text">
        {Math.round(score)}
        <span className="score-ring__sub">score</span>
      </div>
    </div>
  )
}

function SettingItem({ label, value, unit, highlight = false }: {
  label: string; value: string | number; unit?: string; highlight?: boolean
}) {
  return (
    <div className={`settings-item ${highlight ? 'settings-item--highlight' : ''}`}>
      <div className="settings-item__label">{label}</div>
      <div className="settings-item__value">
        {value}
        {unit && <span className="settings-item__unit">{unit}</span>}
      </div>
    </div>
  )
}

export function PrintSettingsPanel({ settings, report }: PrintSettingsPanelProps) {
  if (!settings) {
    return (
      <div className="panel-section" style={{ flex: 1 }}>
        <div className="panel-section__title">⚙ Print Settings</div>
        <p style={{ color: 'var(--color-text-dim)', fontSize: 11, textAlign: 'center', marginTop: 24 }}>
          Generate a model to see recommended settings
        </p>
      </div>
    )
  }

  return (
    <>
      {report && (
        <div className="panel-section">
          <div className="panel-section__title">◎ Printability</div>
          <ScoreRing score={report.score} />
          <div style={{ fontSize: 10, color: 'var(--color-text-dim)', textAlign: 'center', marginBottom: 8 }}>
            {report.needs_support
              ? `⚠ Supports needed (${report.overhang_percentage.toFixed(1)}% overhang)`
              : '✓ No supports required'}
          </div>
          <div style={{ fontSize: 10, color: 'var(--color-text-dim)', textAlign: 'center' }}>
            {`${report.bounding_box_mm[0].toFixed(0)} × ${report.bounding_box_mm[1].toFixed(0)} × ${report.bounding_box_mm[2].toFixed(0)} mm`}
          </div>
        </div>
      )}

      <div className="panel-section">
        <div className="panel-section__title">⚙ Print Settings</div>
        <div className="settings-grid">
          <SettingItem label="Layer Height" value={settings.layer_height_mm} unit="mm" highlight />
          <SettingItem label="Infill" value={settings.infill_percent} unit="%" highlight />
          <SettingItem label="Print Speed" value={settings.print_speed_mm_s} unit="mm/s" />
          <SettingItem label="Perimeters" value={settings.perimeters} />
          <SettingItem label="Nozzle" value={settings.nozzle_temp_c} unit="°C" />
          <SettingItem label="Bed" value={settings.bed_temp_c} unit="°C" />
        </div>
        <div style={{ marginTop: 10, display: 'flex', gap: 8 }}>
          <div className="settings-item" style={{ flex: 1 }}>
            <div className="settings-item__label">Infill Pattern</div>
            <div className="settings-item__value" style={{ fontSize: 12 }}>
              {settings.infill_pattern}
            </div>
          </div>
          <div className="settings-item" style={{ flex: 1 }}>
            <div className="settings-item__label">Supports</div>
            <div className="settings-item__value" style={{ fontSize: 12 }}>
              {settings.support_type}
            </div>
          </div>
        </div>
      </div>
    </>
  )
}
