import type { AssetView, CharacterEntry } from '../types'

export type AppRoute =
  | { page: 'gallery' }
  | { page: 'character'; id: string; view: AssetView }
  | { page: 'not-found' }

const assetViews = new Set<AssetView>([
  'card',
  'head',
  'turnaround',
  'pose',
  'weapon',
  'mount',
])

export function parseHash(hash: string): AppRoute {
  const path = hash.replace(/^#/, '')
  if (path === '' || path === '/' || path === '/index.html') {
    return { page: 'gallery' }
  }

  const match = path.match(
    /^\/character\/(\d{3})(?:\/(card|head|turnaround|pose|weapon|mount))?\/?$/,
  )
  if (!match) return { page: 'not-found' }

  const requestedView = match[2] as AssetView | undefined
  return {
    page: 'character',
    id: match[1],
    view: requestedView && assetViews.has(requestedView)
      ? requestedView
      : 'turnaround',
  }
}

export function characterHref(id: string, view: AssetView = 'turnaround') {
  return `#/character/${id}/${view}`
}

export function availableViews(entry: CharacterEntry): AssetView[] {
  return [
    'card',
    ...(entry.head ? (['head'] as const) : []),
    'turnaround',
    'pose',
    ...(entry.weapon ? (['weapon'] as const) : []),
    ...(entry.mount ? (['mount'] as const) : []),
  ]
}

export function assetUrl(
  entry: CharacterEntry,
  view: AssetView,
): string | undefined {
  return entry[view]
}

export function supportedView(
  entry: CharacterEntry,
  requested: AssetView,
): AssetView {
  return assetUrl(entry, requested) ? requested : 'turnaround'
}
