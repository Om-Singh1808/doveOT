import { useRef, useMemo } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import { OrbitControls, Grid, Environment } from '@react-three/drei'
import * as THREE from 'three'
import type { VibeVector } from '../types/vibe'

// ── Real-time preview shape that responds to sliders ──
function VibePreviewMesh({ vibe }: { vibe: VibeVector | null }) {
  const meshRef = useRef<THREE.Mesh>(null!)
  const materialRef = useRef<THREE.MeshStandardMaterial>(null!)

  useFrame((_, delta) => {
    if (meshRef.current) {
      meshRef.current.rotation.y += delta * 0.3
    }
  })

  const geometry = useMemo(() => {
    if (!vibe) {
      // Default placeholder — rotating cube
      const g = new THREE.BoxGeometry(1.5, 1.5, 1.5)
      return g
    }

    // Build a "preview" geometry that visually reacts to vibe params
    const height = 0.6 + vibe.height_ratio * 2.0
    const radius = 0.4 + vibe.weight * 0.6
    const segments = Math.max(4, Math.round(vibe.softness * 32) + 4)

    // Use CylinderGeometry as a proxy for the parametric feel
    const topR = radius * (1.0 - vibe.taper * 0.7)
    const g = new THREE.CylinderGeometry(topR, radius, height, segments, 1, false)
    return g
  }, [vibe])

  const color = vibe ? '#7c5cfc' : '#3a3460'

  return (
    <mesh ref={meshRef} geometry={geometry} castShadow receiveShadow>
      <meshStandardMaterial
        ref={materialRef}
        color={color}
        roughness={0.25}
        metalness={0.6}
        envMapIntensity={1.2}
      />
    </mesh>
  )
}

interface ModelViewerProps {
  vibe: VibeVector | null
  stlUrl?: string
}

export function ModelViewer({ vibe, stlUrl }: ModelViewerProps) {
  return (
    <div className="viewer-canvas">
      <Canvas
        camera={{ position: [0, 2, 5], fov: 45, near: 0.1, far: 1000 }}
        shadows
        gl={{ antialias: true, alpha: false }}
      >
        <color attach="background" args={['#08080e']} />
        <ambientLight intensity={0.4} />
        <directionalLight
          position={[5, 10, 5]}
          intensity={1.2}
          castShadow
          shadow-mapSize={[2048, 2048]}
        />
        <pointLight position={[-4, 3, -4]} color="#7c5cfc" intensity={3} />
        <pointLight position={[4, 1,  4]} color="#2de2e6" intensity={1.5} />

        <VibePreviewMesh vibe={vibe} />

        <Grid
          args={[20, 20]}
          cellSize={0.5}
          cellThickness={0.4}
          cellColor="#1a1a30"
          sectionSize={2}
          sectionThickness={0.8}
          sectionColor="#2a2050"
          fadeDistance={15}
          fadeStrength={1}
          position={[0, -2, 0]}
        />

        <OrbitControls
          enablePan={false}
          minDistance={2}
          maxDistance={12}
          autoRotate={false}
          dampingFactor={0.08}
          enableDamping
        />

        <Environment preset="city" />
      </Canvas>

      {!stlUrl && !vibe && (
        <div className="viewer-empty">
          <span className="viewer-empty-icon">◈</span>
          <span className="viewer-empty-text">Your model will appear here</span>
        </div>
      )}

      <div className="viewer-overlay">
        {vibe && (
          <span className="viewer-badge">Live Preview · {vibe.archetype}</span>
        )}
        <span className="viewer-badge">VibePrint</span>
      </div>
    </div>
  )
}
