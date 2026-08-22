import {
  ArrowLeft,
  ChevronLeft,
  ChevronRight,
  Expand,
} from 'lucide-react'
import { useEffect, useMemo, useState } from 'react'
import { Artwork } from '../components/Artwork'
import { Lightbox } from '../components/Lightbox'
import { Seal } from '../components/Seal'
import {
  assetUrl,
  availableViews,
  characterHref,
} from '../lib/routes'
import type { AssetView, CharacterEntry } from '../types'

const viewLabels: Record<AssetView, string> = {
  card: '原始卡片',
  head: '头部四视',
  turnaround: '人物六视图',
  pose: '原画动作六视',
  weapon: '兵器设定',
  mount: '坐骑设定',
}

interface CharacterPageProps {
  entry: CharacterEntry
  entries: CharacterEntry[]
}

export function CharacterPage({ entry, entries }: CharacterPageProps) {
  const views = useMemo(() => availableViews(entry), [entry])
  const detailViews = useMemo(
    () => views.filter((view): view is Exclude<AssetView, 'card'> => view !== 'card'),
    [views],
  )
  const [lightboxView, setLightboxView] = useState<AssetView | null>(null)
  const currentIndex = entries.findIndex((item) => item.id === entry.id)
  const previous = entries[(currentIndex - 1 + entries.length) % entries.length]
  const next = entries[(currentIndex + 1) % entries.length]

  function destinationFor(target: CharacterEntry) {
    return characterHref(target.id)
  }

  useEffect(() => {
    function onKeyDown(event: KeyboardEvent) {
      if (lightboxView || event.metaKey || event.ctrlKey || event.altKey) return
      const target = event.target
      if (
        target instanceof Element &&
        target.matches('input, textarea, select, [contenteditable="true"]')
      ) {
        return
      }

      if (event.key === 'ArrowLeft') {
        event.preventDefault()
        window.location.hash = destinationFor(previous)
      }
      if (event.key === 'ArrowRight') {
        event.preventDefault()
        window.location.hash = destinationFor(next)
      }
    }

    window.addEventListener('keydown', onKeyDown)
    return () => window.removeEventListener('keydown', onKeyDown)
  })

  return (
    <div className="character-page">
      <header className="detail-topbar">
        <a href="#/" className="back-link">
          <ArrowLeft aria-hidden="true" size={18} />
          返回群英谱
        </a>
        <a href="#/" className="brand-lockup brand-lockup--dark">
          <span className="brand-lockup__seal">浒</span>
          <span>
            <span className="brand-lockup__title">一百单八将</span>
            <span className="brand-lockup__subtitle">收藏图鉴 · 1999</span>
          </span>
        </a>
        <span className="detail-topbar__hint">方向键切换人物</span>
      </header>

      <main className="detail-shell">
        <section className="detail-heading">
          <div className="detail-heading__identity">
            <Seal id={entry.id} compact />
            <div>
              <span className="section-kicker section-kicker--dark">梁山人物志</span>
              <h1>人物 · No. {entry.id}</h1>
            </div>
          </div>
          <nav className="character-pager" aria-label="切换人物">
            <a href={destinationFor(previous)} aria-label={`上一位 No. ${previous.id}`}>
              <ChevronLeft aria-hidden="true" />
              <span>
                <small>上一位</small>
                NO. {previous.id}
              </span>
            </a>
            <a href={destinationFor(next)} aria-label={`下一位 No. ${next.id}`}>
              <span>
                <small>下一位</small>
                NO. {next.id}
              </span>
              <ChevronRight aria-hidden="true" />
            </a>
          </nav>
        </section>

        <section className="detail-gallery-layout" aria-label="人物完整素材">
          <aside className="detail-gallery-source">
            <ArtworkPanel
              entry={entry}
              view="card"
              src={entry.card}
              onExpand={() => setLightboxView('card')}
              eager
              source
            />
          </aside>

          <div className="detail-gallery-stack">
            {detailViews.map((detailView, index) => (
              <ArtworkPanel
                key={detailView}
                entry={entry}
                view={detailView}
                src={assetUrl(entry, detailView)!}
                onExpand={() => setLightboxView(detailView)}
                eager={index === 0}
              />
            ))}
          </div>
        </section>

        <div className="detail-footnote">
          <span>点击画面可全屏查看</span>
          <i aria-hidden="true" />
          <span>
            {detailViews.length} 类设定素材 · 高清原图
          </span>
        </div>
      </main>

      {lightboxView && (
        <Lightbox
          entry={entry}
          views={views}
          currentView={lightboxView}
          onChange={setLightboxView}
          onClose={() => setLightboxView(null)}
        />
      )}
    </div>
  )
}

interface ArtworkPanelProps {
  entry: CharacterEntry
  view: AssetView
  src: string
  onExpand: () => void
  eager?: boolean
  source?: boolean
}

function ArtworkPanel({
  entry,
  view,
  src,
  onExpand,
  eager,
  source = false,
}: ArtworkPanelProps) {
  const isCard = view === 'card'
  return (
    <article
      className={`artwork-panel ${isCard ? 'artwork-panel--card' : 'artwork-panel--wide'}`}
    >
      <header className="artwork-panel__header">
        <div>
          <span>{source ? '原画依据' : '设定展开'}</span>
          <h2>{viewLabels[view]}</h2>
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
