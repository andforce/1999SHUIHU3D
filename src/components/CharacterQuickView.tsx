import {
  ChevronLeft,
  ChevronRight,
  Expand,
  X,
} from 'lucide-react'
import { useEffect, useMemo, useRef, useState } from 'react'
import { assetUrl, availableViews } from '../lib/routes'
import type { AssetView, CharacterEntry } from '../types'
import { Artwork } from './Artwork'
import { Lightbox } from './Lightbox'
import { Seal } from './Seal'

const viewLabels: Record<AssetView, string> = {
  card: '原始卡片',
  head: '头部四视',
  turnaround: '人物五视',
  pose: '原画动作六视',
  weapon: '兵器设定',
  mount: '坐骑设定',
}

interface CharacterQuickViewProps {
  entry: CharacterEntry
  entries: CharacterEntry[]
  onSelectCharacter: (id: string) => void
  onClose: () => void
}

export function CharacterQuickView({
  entry,
  entries,
  onSelectCharacter,
  onClose,
}: CharacterQuickViewProps) {
  const closeButtonRef = useRef<HTMLButtonElement>(null)
  const bodyRef = useRef<HTMLDivElement>(null)
  const [lightboxView, setLightboxView] = useState<AssetView | null>(null)
  const views = useMemo(() => availableViews(entry), [entry])
  const detailViews = useMemo(
    () => views.filter((view): view is Exclude<AssetView, 'card'> => view !== 'card'),
    [views],
  )
  const currentIndex = entries.findIndex((item) => item.id === entry.id)
  const previous = entries[(currentIndex - 1 + entries.length) % entries.length]
  const next = entries[(currentIndex + 1) % entries.length]

  function selectCharacter(target: CharacterEntry) {
    setLightboxView(null)
    onSelectCharacter(target.id)
  }

  useEffect(() => {
    const previousOverflow = document.body.style.overflow
    document.body.style.overflow = 'hidden'
    closeButtonRef.current?.focus()

    return () => {
      document.body.style.overflow = previousOverflow
    }
  }, [])

  useEffect(() => {
    bodyRef.current?.scrollTo?.({ top: 0 })
  }, [entry.id])

  useEffect(() => {
    function onKeyDown(event: KeyboardEvent) {
      if (lightboxView || event.metaKey || event.ctrlKey || event.altKey) return

      if (event.key === 'Escape') {
        event.preventDefault()
        onClose()
      }
      if (event.key === 'ArrowLeft') {
        event.preventDefault()
        selectCharacter(previous)
      }
      if (event.key === 'ArrowRight') {
        event.preventDefault()
        selectCharacter(next)
      }
    }

    window.addEventListener('keydown', onKeyDown)
    return () => window.removeEventListener('keydown', onKeyDown)
  })

  return (
    <>
      <div
        className="character-modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="character-modal-title"
        onMouseDown={(event) => {
          if (event.target === event.currentTarget) onClose()
        }}
      >
        <section className="character-modal__dialog">
          <header className="character-modal__header">
            <div className="character-modal__identity">
              <Seal id={entry.id} compact />
              <div>
                <span className="section-kicker section-kicker--dark">梁山人物志</span>
                <h2 id="character-modal-title">人物 · No. {entry.id}</h2>
              </div>
            </div>

            <div className="character-modal__actions">
              <nav className="character-modal__pager" aria-label="切换人物">
                <button
                  type="button"
                  onClick={() => selectCharacter(previous)}
                  aria-label={`上一位 No. ${previous.id}`}
                >
                  <ChevronLeft aria-hidden="true" />
                  <span>
                    <small>上一位</small>
                    NO. {previous.id}
                  </span>
                </button>
                <button
                  type="button"
                  onClick={() => selectCharacter(next)}
                  aria-label={`下一位 No. ${next.id}`}
                >
                  <span>
                    <small>下一位</small>
                    NO. {next.id}
                  </span>
                  <ChevronRight aria-hidden="true" />
                </button>
              </nav>
              <button
                ref={closeButtonRef}
                type="button"
                className="character-modal__close"
                onClick={onClose}
                aria-label="关闭人物资料"
              >
                <X aria-hidden="true" />
              </button>
            </div>
          </header>

          <div ref={bodyRef} className="character-modal__body">
            <aside className="character-modal__source">
              <QuickViewPanel
                entry={entry}
                view="card"
                src={entry.card}
                onExpand={() => setLightboxView('card')}
                eager
                source
              />
            </aside>

            <div className="character-modal__stack">
              {detailViews.map((view, index) => (
                <QuickViewPanel
                  key={view}
                  entry={entry}
                  view={view}
                  src={assetUrl(entry, view)!}
                  onExpand={() => setLightboxView(view)}
                  eager={index === 0}
                />
              ))}
            </div>
          </div>

          <footer className="character-modal__footer">
            <span>点击画面可全屏查看</span>
            <i aria-hidden="true" />
            <span>{detailViews.length} 类设定素材 · 方向键切换人物</span>
          </footer>
        </section>
      </div>

      {lightboxView && (
        <Lightbox
          entry={entry}
          views={views}
          currentView={lightboxView}
          onChange={setLightboxView}
          onClose={() => setLightboxView(null)}
        />
      )}
    </>
  )
}

interface QuickViewPanelProps {
  entry: CharacterEntry
  view: AssetView
  src: string
  onExpand: () => void
  eager?: boolean
  source?: boolean
}

function QuickViewPanel({
  entry,
  view,
  src,
  onExpand,
  eager,
  source = false,
}: QuickViewPanelProps) {
  const isCard = view === 'card'

  return (
    <article
      className={`artwork-panel ${isCard ? 'artwork-panel--card' : 'artwork-panel--wide'}`}
    >
      <header className="artwork-panel__header">
        <div>
          <span>{source ? '原画依据' : '设定展开'}</span>
          <h3>{viewLabels[view]}</h3>
        </div>
        <button type="button" onClick={onExpand} aria-label={`放大${viewLabels[view]}`}>
          <Expand aria-hidden="true" size={17} />
          全屏
        </button>
      </header>
      <div className="artwork-panel__mat">
        <Artwork
          src={src}
          alt={`No. ${entry.id} ${viewLabels[view]}`}
          className={`artwork-panel__image ${isCard ? 'is-card' : 'is-wide'}`}
          imageClassName="object-contain"
          eager={eager}
          onActivate={onExpand}
          activateLabel={`全屏查看 No. ${entry.id} ${viewLabels[view]}`}
        />
        <span className="artwork-panel__corner artwork-panel__corner--tl" />
        <span className="artwork-panel__corner artwork-panel__corner--tr" />
        <span className="artwork-panel__corner artwork-panel__corner--bl" />
        <span className="artwork-panel__corner artwork-panel__corner--br" />
      </div>
    </article>
  )
}
