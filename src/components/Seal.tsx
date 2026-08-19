interface SealProps {
  id: string
  compact?: boolean
}

export function Seal({ id, compact = false }: SealProps) {
  return (
    <span
      className={`number-seal ${compact ? 'number-seal--compact' : ''}`}
      aria-label={`编号 ${id}`}
    >
      <span className="number-seal__no">NO.</span>
      <span>{id}</span>
    </span>
  )
}
