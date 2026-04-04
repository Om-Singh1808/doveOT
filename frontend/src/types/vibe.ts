export type ObjectArchetype = 'stand' | 'vessel' | 'box' | 'sculpture' | 'bracket' | 'lamp'

export interface VibeVector {
  archetype: ObjectArchetype
  softness: number
  complexity: number
  weight: number
  symmetry: number
  fluidity: number
  density: number
  height_ratio: number
  taper: number
  description: string
}

export interface VibeDimension {
  key: keyof Omit<VibeVector, 'archetype' | 'description'>
  label: string
  lowLabel: string
  highLabel: string
  icon: string
}

export const VIBE_DIMENSIONS: VibeDimension[] = [
  { key: 'softness',     label: 'Edge Feel',      lowLabel: 'Sharp',     highLabel: 'Soft',     icon: '◈' },
  { key: 'complexity',   label: 'Complexity',     lowLabel: 'Minimal',   highLabel: 'Ornate',   icon: '✦' },
  { key: 'weight',       label: 'Weight',         lowLabel: 'Delicate',  highLabel: 'Solid',    icon: '⬡' },
  { key: 'symmetry',     label: 'Symmetry',       lowLabel: 'Organic',   highLabel: 'Perfect',  icon: '⬡' },
  { key: 'fluidity',     label: 'Fluidity',       lowLabel: 'Rigid',     highLabel: 'Flowing',  icon: '〜' },
  { key: 'density',      label: 'Density',        lowLabel: 'Open',      highLabel: 'Dense',    icon: '▦' },
  { key: 'height_ratio', label: 'Proportion',     lowLabel: 'Squat',     highLabel: 'Tall',     icon: '↕' },
  { key: 'taper',        label: 'Taper',          lowLabel: 'Uniform',   highLabel: 'Narrow',   icon: '▽' },
]

export interface PrintSettings {
  layer_height_mm: number
  infill_percent: number
  infill_pattern: string
  print_speed_mm_s: number
  nozzle_temp_c: number
  bed_temp_c: number
  perimeters: number
  support_enabled: boolean
  support_type: string
  material: string
}

export interface PrintReport {
  overhang_face_count: number
  overhang_area_mm2: number
  overhang_percentage: number
  needs_support: boolean
  bounding_box_mm: [number, number, number]
  score: number
}

export interface GenerateRequest {
  prompt: string
  slider_overrides?: Partial<Omit<VibeVector, 'archetype' | 'description'>>
}

export interface GenerateResponse {
  vibe_vector: VibeVector
  stl_url?: string
  gcode_url?: string
  print_settings?: PrintSettings
  print_report?: PrintReport
}

export type PipelineStatus =
  | 'idle'
  | 'interpreting'
  | 'modeling'
  | 'analyzing'
  | 'slicing'
  | 'done'
  | 'error'
