import type { PipelineStatus } from '../types/vibe'

interface GenerateButtonProps {
  onClick: () => void
  status: PipelineStatus
  disabled?: boolean
}

const STATUS_LABELS: Partial<Record<PipelineStatus, string>> = {
  idle:         'Generate Model',
  done:         'Regenerate',
  error:        'Try Again',
  interpreting: 'Interpreting Vibe…',
  modeling:     'Building Geometry…',
  analyzing:    'Checking Printability…',
  slicing:      'Generating G-code…',
}

export function GenerateButton({ onClick, status, disabled }: GenerateButtonProps) {
  const isLoading = !['idle', 'done', 'error'].includes(status)
  const label = STATUS_LABELS[status] ?? 'Generate'

  return (
    <div className="panel-section">
      <button
        id="btn-generate"
        className="generate-btn"
        onClick={onClick}
        disabled={disabled || isLoading}
      >
        {isLoading
          ? <span style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 10 }}>
              <span className="spinner" style={{ width: 16, height: 16 }} />
              {label}
            </span>
          : `✦ ${label}`
        }
      </button>
    </div>
  )
}
