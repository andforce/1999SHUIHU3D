import { ChevronLeft, ChevronRight, X } from 'lucide-react'
import { useEffect, useRef } from 'react'
import { assetUrl } from '../lib/routes'
import type { AssetView, CharacterEntry } from '../types'
import { Artwork } from './Artwork'

const viewLabels: Record<AssetView, string> = {
  card: '原始卡片',
  turnaround: '人物五视图',
  weapon: '武器图',
  mount: '坐骑图',
}

interface LightboxProps {
  entry: CharacterEntry
  views: AssetView[]
  currentView: AssetView
  onChange: (view: AssetView) => void
  onClose: () => void
}

export function Lightbox({
  entry,
  views,
  currentView,
  onChange,
  onClose,
}: LightboxProps) {
  const closeButtonRef = useRef<HTMLButtonElement>(null)
  const currentIndex = views.indexOf(currentView)
  const currentUrl = assetUrl(entry, currentView)

  function move(offset: number) {
    const nextIndex = (currentIndex + offset + views.length) % views.length
    onChange(views[nextIndex])
  }

  useEffect(() => {
    const previousOverflow = document.body.style.overflow
    document.body.style.overflow = 'hidden'
    closeButtonRef.current?.focus()

    function onKeyDown(event: KeyboardEvent) {
      if (event.key === 'Escape') onClose()
      if (event.key === 'ArrowLeft') {
        event.preventDefault()
        move(-1)
      }
      if (event.key === 'ArrowRight') {
        event.preventDefault()
        move(1)
      }
    }

    window.addEventListener('keydown', onKeyDown)
    return () => {
      document.body.style.overflow = previousOverflow
      window.removeEventListener('keydown', onKeyDown)
    }
  })

  if (!currentUrl) return null

  return (
    <div
      className="lightbox"
      role="dialog"
      aria-modal="true"
      aria-label={`No. ${entry.id} ${viewLabels[currentView]}`}
      onMouseDown={(event) => {
        if (event.target === event.currentTarget) onClose()
      }}
    >
      <div className="lightbox__topbar">
        <div>
          <span className="lightbox__eyebrow">NO. {entry.id}</span>
          <h2>{viewLabels[currentView]}</h2>
        </div>
        <button
          ref={closeButtonRef}
          type="button"
          className="icon-button icon-button--light"
          onClick={onClose}
          aria-label="关闭全屏查看"
        >
          <X aria-hidden="true" />
        </button>
      </div>

      <div className="lightbox__stage">
        {views.length > 1 && (
          <button
            type="button"
            className="lightbox__arrow lightbox__arrow--left"
            onClick={() => move(-1)}
            aria-label="查看上一类图片"
          >
            <ChevronLeft aria-hidden="true" />
          </button>
        )}

        <Artwork
          src={currentUrl}
          alt={`No. ${entry.id} ${viewLabels[currentView]}`}
          className="lightbox__artwork"
          imageClassName="object-contain"
          eager
        />

        {views.length > 1 && (
          <button
            type="button"
            className="lightbox__arrow lightbox__arrow--right"
            onClick={() => move(1)}
            aria-label="查看下一类图片"
          >
            <ChevronRight aria-hidden="true" />
          </button>
        )}
      </div>

      <div className="lightbox__dots" aria-label="图片类别">
        {views.map((view) => (
          <button
            key={view}
            type="button"
            className={view === currentView ? 'is-active' : ''}
            onClick={() => onChange(view)}
            aria-label={`查看${viewLabels[view]}`}
            aria-current={view === currentView ? 'true' : undefined}
          />
        ))}
      </div>
    </div>
  )
}
