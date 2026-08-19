import {
  ArrowDownAZ,
  ArrowUpAZ,
  Search,
  SlidersHorizontal,
  Sword,
} from 'lucide-react'
import { useMemo, useState } from 'react'
import { Artwork } from '../components/Artwork'
import { Seal } from '../components/Seal'
import { characterHref } from '../lib/routes'
import type { CharacterEntry } from '../types'

type GalleryFilter = 'all' | 'weapon' | 'mount'
type SortDirection = 'ascending' | 'descending'

interface GalleryPageProps {
  entries: CharacterEntry[]
}

const filterLabels: Record<GalleryFilter, string> = {
  all: '全部人物',
  weapon: '有武器',
  mount: '有坐骑',
}

export function GalleryPage({ entries }: GalleryPageProps) {
  const [query, setQuery] = useState('')
  const [filter, setFilter] = useState<GalleryFilter>('all')
  const [sortDirection, setSortDirection] =
    useState<SortDirection>('ascending')

  const weaponCount = entries.filter((entry) => entry.weapon).length
  const mountCount = entries.filter((entry) => entry.mount).length

  const visibleEntries = useMemo(() => {
    const numericQuery = query.replace(/\D/g, '')
    return entries
      .filter((entry) => {
        const matchesQuery = !numericQuery || entry.id.includes(numericQuery)
        const matchesFilter = filter === 'all' || Boolean(entry[filter])
        return matchesQuery && matchesFilter
      })
      .sort((first, second) =>
        sortDirection === 'ascending'
          ? first.id.localeCompare(second.id)
          : second.id.localeCompare(first.id),
      )
  }, [entries, filter, query, sortDirection])

  return (
    <div className="gallery-page">
      <header className="hero-shell">
        <div className="hero-shell__wash" aria-hidden="true" />
        <nav className="topbar" aria-label="主导航">
          <a href="#/" className="brand-lockup" aria-label="返回图鉴首页">
            <span className="brand-lockup__seal">浒</span>
            <span>
              <span className="brand-lockup__title">一百单八将</span>
              <span className="brand-lockup__subtitle">收藏图鉴 · 1999</span>
            </span>
          </a>
          <span className="topbar__archive">民间收藏数字档案</span>
        </nav>

        <div className="hero-content">
          <div className="hero-copy">
            <span className="section-kicker">梁山人物 · 全套影像志</span>
            <h1>
              忠义堂前
              <br />
              <em>一百单八将</em>
            </h1>
            <p>
              逐张重访旧日卡面，对照人物五视、兵器与坐骑。
              <br className="hidden sm:block" />
              一套属于收藏者的水浒人物图谱。
            </p>
          </div>

          <div className="hero-counts" aria-label="素材统计">
            <div className="hero-stat hero-stat--primary">
              <strong>{entries.length}</strong>
              <span>原始卡片</span>
            </div>
            <div className="hero-stat">
              <strong>{entries.length}</strong>
              <span>人物五视</span>
            </div>
            <div className="hero-stat">
              <strong>{weaponCount}</strong>
              <span>兵器设定</span>
            </div>
            <div className="hero-stat">
              <strong>{mountCount}</strong>
              <span>坐骑设定</span>
            </div>
          </div>
        </div>

        <div className="hero-ornament" aria-hidden="true">
          <span>水</span>
          <span>浒</span>
        </div>
      </header>

      <main className="catalog-shell" id="catalog">
        <div className="catalog-heading">
          <div>
            <span className="section-kicker section-kicker--dark">人物名录</span>
            <h2>梁山群英谱</h2>
          </div>
          <p>依卡片编号入册 · 点击人物展开设定全卷</p>
        </div>

        <section className="catalog-toolbar" aria-label="图鉴筛选">
          <label className="search-field">
            <Search aria-hidden="true" size={18} />
            <span className="sr-only">按编号搜索</span>
            <input
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              inputMode="numeric"
              placeholder="检索编号，如 027"
            />
            {query && (
              <button
                type="button"
                onClick={() => setQuery('')}
                aria-label="清除搜索"
              >
                清除
              </button>
            )}
          </label>

          <div className="filter-group" aria-label="素材类别">
            <SlidersHorizontal aria-hidden="true" size={17} />
            {(Object.keys(filterLabels) as GalleryFilter[]).map((value) => (
              <button
                key={value}
                type="button"
                className={filter === value ? 'is-active' : ''}
                onClick={() => setFilter(value)}
                aria-pressed={filter === value}
              >
                {filterLabels[value]}
              </button>
            ))}
          </div>

          <button
            type="button"
            className="sort-button"
            onClick={() =>
              setSortDirection((current) =>
                current === 'ascending' ? 'descending' : 'ascending',
              )
            }
            aria-label={
              sortDirection === 'ascending'
                ? '当前编号升序，点击切换为降序'
                : '当前编号降序，点击切换为升序'
            }
          >
            {sortDirection === 'ascending' ? (
              <ArrowDownAZ aria-hidden="true" size={18} />
            ) : (
              <ArrowUpAZ aria-hidden="true" size={18} />
            )}
            {sortDirection === 'ascending' ? '编号升序' : '编号降序'}
          </button>
        </section>

        <div className="result-line" aria-live="polite">
          <span>当前收录</span>
          <strong>{visibleEntries.length}</strong>
          <span>位人物</span>
          <i aria-hidden="true" />
        </div>

        {visibleEntries.length > 0 ? (
          <section className="card-grid" aria-label="人物卡片">
            {visibleEntries.map((entry, index) => (
              <a
                key={entry.id}
                href={characterHref(entry.id)}
                className="catalog-card"
                aria-label={`查看 No. ${entry.id} 人物详情`}
              >
                <div className="catalog-card__frame">
                  <Artwork
                    src={entry.thumbnail}
                    alt={`No. ${entry.id} 原始卡片`}
                    className="catalog-card__image"
                    imageClassName="object-cover"
                    eager={index < 8}
                  />
                  <span className="catalog-card__shine" aria-hidden="true" />
                  <Seal id={entry.id} />
                </div>
                <div className="catalog-card__caption">
                  <span className="catalog-card__name">梁山人物</span>
                  <span className="catalog-card__assets">
                    {entry.weapon && (
                      <span title="含武器图">
                        <Sword aria-hidden="true" size={13} />兵器
                      </span>
                    )}
                    {entry.mount && <span title="含坐骑图">骑</span>}
                  </span>
                </div>
              </a>
            ))}
          </section>
        ) : (
          <section className="empty-state">
            <span className="empty-state__seal">无</span>
            <h3>名录中未寻得此编号</h3>
            <p>请尝试其他编号，或清除当前筛选条件。</p>
            <button
              type="button"
              onClick={() => {
                setQuery('')
                setFilter('all')
              }}
            >
              重置名录
            </button>
          </section>
        )}
      </main>

      <footer className="site-footer">
        <span className="site-footer__mark">一百单八</span>
        <p>1999 小浣熊水浒收藏图鉴</p>
        <span>卡片 · 人物五视 · 兵器 · 坐骑</span>
      </footer>
    </div>
  )
}
