
interface ExportPanelProps {
  stlUrl?: string
  gcodeUrl?: string
}

export function ExportPanel({ stlUrl, gcodeUrl }: ExportPanelProps) {
  const handleDownload = (url: string, filename: string) => {
    const a = document.createElement('a')
    a.href = `http://127.0.0.1:8000${url}`
    a.download = filename
    a.click()
  }

  return (
    <div className="panel-section">
      <div className="panel-section__title">↓ Export</div>

      <button
        id="export-stl"
        className="export-btn"
        disabled={!stlUrl}
        onClick={() => stlUrl && handleDownload(stlUrl, 'vibeprint_model.stl')}
      >
        <span className="export-btn__icon">📐</span>
        <div>
          <div style={{ fontSize: 12, fontWeight: 700 }}>Export STL</div>
          <div style={{ fontSize: 9, color: 'var(--color-text-dim)', marginTop: 1 }}>
            For 3D printer / slicer
          </div>
        </div>
      </button>

      <button
        id="export-gcode"
        className="export-btn"
        disabled={!gcodeUrl}
        onClick={() => gcodeUrl && handleDownload(gcodeUrl, 'vibeprint_model.gcode')}
      >
        <span className="export-btn__icon">⚙️</span>
        <div>
          <div style={{ fontSize: 12, fontWeight: 700 }}>Export G-code</div>
          <div style={{ fontSize: 9, color: 'var(--color-text-dim)', marginTop: 1 }}>
            Ready to print directly
          </div>
        </div>
      </button>
    </div>
  )
}
