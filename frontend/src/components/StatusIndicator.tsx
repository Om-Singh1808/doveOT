import React from 'react'
import type { PipelineStatus } from '../types/vibe'

const STEPS: { key: PipelineStatus; label: string }[] = [
  { key: 'interpreting', label: 'AI Interpret' },
  { key: 'modeling',     label: 'Modeling' },
  { key: 'analyzing',    label: 'Analyze' },
  { key: 'slicing',      label: 'Slice' },
  { key: 'done',         label: 'Done' },
]

const STATUS_ORDER: PipelineStatus[] = ['interpreting', 'modeling', 'analyzing', 'slicing', 'done']

function getStepState(step: PipelineStatus, current: PipelineStatus) {
  if (current === 'idle') return 'pending'
  if (current === 'error') return 'pending'
  const currentIdx = STATUS_ORDER.indexOf(current)
  const stepIdx = STATUS_ORDER.indexOf(step)
  if (stepIdx < currentIdx) return 'done'
  if (stepIdx === currentIdx) return 'active'
  return 'pending'
}

interface StatusIndicatorProps {
  status: PipelineStatus
  error?: string | null
}

export function StatusIndicator({ status, error }: StatusIndicatorProps) {
  const isActive = !['idle', 'done', 'error'].includes(status)

  return (
    <div className="status-bar">
      <div className={`status-dot status-dot--${
        status === 'idle' ? 'idle' :
        status === 'done' ? 'done' :
        status === 'error' ? 'error' : 'active'
      }`} />

      {status === 'idle' && (
        <span className="text-dim">Ready — enter a prompt and click Generate</span>
      )}

      {status === 'error' && (
        <span style={{ color: 'var(--color-accent)', fontSize: 11 }}>
          ✗ {error ?? 'Generation failed'}
        </span>
      )}

      {(isActive || status === 'done') && (
        <div className="status-steps">
          {STEPS.map((step, i) => {
            const state = getStepState(step.key, status)
            return (
              <React.Fragment key={step.key}>
                <span className={`status-step status-step--${state}`}>
                  {state === 'done' && '✓ '}
                  {state === 'active' && '⟳ '}
                  {step.label}
                </span>
                {i < STEPS.length - 1 && <span className="status-step-dash" />}
              </React.Fragment>
            )
          })}
        </div>
      )}
    </div>
  )
}
