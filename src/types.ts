export type AssetView = 'card' | 'turnaround' | 'weapon' | 'mount'

export interface CharacterEntry {
  id: string
  card: string
  thumbnail: string
  turnaround: string
  weapon?: string
  mount?: string
}

export interface SourceCatalogEntry {
  id: string
  card: string
  thumbnail: string
  turnaround: string
  weapon?: string
  mount?: string
}
