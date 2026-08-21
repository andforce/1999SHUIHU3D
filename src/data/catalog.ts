import sourceCatalog from '../generated/catalog.json'
import type { CharacterEntry, SourceCatalogEntry } from '../types'

const cardModules = import.meta.glob('../../images/[0-9][0-9][0-9].png', {
  eager: true,
  query: '?url',
  import: 'default',
}) as Record<string, string>

const turnaroundModules = import.meta.glob(
  '../../character-model-sheets/characters/*/character-turnaround.png',
  { eager: true, query: '?url', import: 'default' },
) as Record<string, string>

const weaponModules = import.meta.glob(
  '../../character-model-sheets/characters/*/weapon-sheet.png',
  { eager: true, query: '?url', import: 'default' },
) as Record<string, string>

const mountModules = import.meta.glob(
  '../../character-model-sheets/characters/*/mount-sheet.png',
  { eager: true, query: '?url', import: 'default' },
) as Record<string, string>

function mapAssetsById(
  modules: Record<string, string>,
  idPattern: RegExp,
): Map<string, string> {
  return new Map(
    Object.entries(modules).map(([filePath, assetUrl]) => {
      const id = filePath.match(idPattern)?.[1]
      if (!id) throw new Error(`无法从素材路径提取编号：${filePath}`)
      return [id, assetUrl]
    }),
  )
}

const cardsById = mapAssetsById(cardModules, /\/(\d{3})\.png$/)
const turnaroundsById = mapAssetsById(
  turnaroundModules,
  /\/characters\/(\d{3})\/character-turnaround\.png$/,
)
const weaponsById = mapAssetsById(
  weaponModules,
  /\/characters\/(\d{3})\/weapon-sheet\.png$/,
)
const mountsById = mapAssetsById(
  mountModules,
  /\/characters\/(\d{3})\/mount-sheet\.png$/,
)

function requiredAsset(
  assets: Map<string, string>,
  id: string,
  label: string,
): string {
  const asset = assets.get(id)
  if (!asset) throw new Error(`No. ${id} 缺少${label}。`)
  return asset
}

function thumbnailUrl(id: string): string {
  return `${import.meta.env.BASE_URL}generated/cards/${id}.webp`
}

export const characters: CharacterEntry[] = (
  sourceCatalog as SourceCatalogEntry[]
).map((entry) => ({
  id: entry.id,
  card: requiredAsset(cardsById, entry.id, '卡片原图'),
  thumbnail: thumbnailUrl(entry.id),
  turnaround: requiredAsset(turnaroundsById, entry.id, '人物五视图'),
  ...(entry.weapon
    ? { weapon: requiredAsset(weaponsById, entry.id, '武器图') }
    : {}),
  ...(entry.mount
    ? { mount: requiredAsset(mountsById, entry.id, '坐骑图') }
    : {}),
}))
