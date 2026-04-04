import type { ObjectArchetype } from '../types/vibe'

const ARCHETYPES: { key: ObjectArchetype; icon: string; label: string }[] = [
  { key: 'stand',     icon: '📱', label: 'Stand'   },
  { key: 'vessel',    icon: '🏺', label: 'Vessel'  },
  { key: 'box',       icon: '📦', label: 'Box'     },
  { key: 'sculpture', icon: '🗿', label: 'Sculpt'  },
  { key: 'bracket',   icon: '🔧', label: 'Bracket' },
  { key: 'lamp',      icon: '💡', label: 'Lamp'    },
]

const EXAMPLES = [
  'minimal soft phone stand',
  'tall flowing vase',
  'heavy geometric box',
  'organic sculpture',
]

interface PromptInputProps {
  value: string
  onChange: (v: string) => void
  onExample: (v: string) => void
  forcedArchetype: ObjectArchetype | null
  onArchetypeOverride: (a: ObjectArchetype | null) => void
}

export function PromptInput({
  value,
  onChange,
  onExample,
  forcedArchetype,
  onArchetypeOverride,
}: PromptInputProps) {
  return (
    <>
      <div className="panel-section">
        <div className="panel-section__title">✦ Vibe Prompt</div>
        <div className="prompt-wrapper">
          <textarea
            id="vibe-prompt"
            className="prompt-textarea"
            placeholder="Describe what you want to create…&#10;e.g. minimal premium phone stand"
            value={value}
            onChange={(e) => onChange(e.target.value)}
            rows={3}
          />
        </div>
        <div className="prompt-examples">
          {EXAMPLES.map((ex) => (
            <button key={ex} className="prompt-example-chip" onClick={() => onExample(ex)}>
              {ex}
            </button>
          ))}
        </div>
      </div>

      <div className="panel-section">
        <div className="panel-section__title">◈ Object Type</div>
        <div className="archetype-grid">
          {ARCHETYPES.map((a) => (
            <button
              key={a.key}
              id={`archetype-${a.key}`}
              className={`archetype-btn ${forcedArchetype === a.key ? 'archetype-btn--active' : ''}`}
              onClick={() => onArchetypeOverride(forcedArchetype === a.key ? null : a.key)}
            >
              <span className="archetype-btn__icon">{a.icon}</span>
              <span className="archetype-btn__label">{a.label}</span>
            </button>
          ))}
        </div>
      </div>
    </>
  )
}
