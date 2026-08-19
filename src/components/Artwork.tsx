import { ImageOff } from 'lucide-react'
import { useState } from 'react'

interface ArtworkProps {
  src: string
  alt: string
  className?: string
  imageClassName?: string
  eager?: boolean
  onActivate?: () => void
  activateLabel?: string
}

export function Artwork({
  src,
  alt,
  className = '',
  imageClassName = '',
  eager = false,
  onActivate,
  activateLabel,
}: ArtworkProps) {
  const [failedSource, setFailedSource] = useState<string | null>(null)
  const failed = failedSource === src

  const content = failed ? (
    <span className="image-fallback" role="img" aria-label={`${alt}加载失败`}>
      <ImageOff aria-hidden="true" size={28} strokeWidth={1.5} />
      <span>画卷暂不可见</span>
    </span>
  ) : (
    <img
      src={src}
      alt={alt}
      className={`h-full w-full ${imageClassName}`}
      loading={eager ? 'eager' : 'lazy'}
      decoding="async"
      onError={() => setFailedSource(src)}
    />
  )

  if (onActivate) {
    return (
      <button
        type="button"
        className={`artwork-button ${className}`}
        onClick={onActivate}
        aria-label={activateLabel ?? `放大查看${alt}`}
      >
        {content}
      </button>
    )
  }

  return <div className={className}>{content}</div>
}
