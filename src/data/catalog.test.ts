import { describe, expect, it } from 'vitest'
import sourceCatalog from '../generated/catalog.json'
import type { SourceCatalogEntry } from '../types'

const catalog = sourceCatalog as SourceCatalogEntry[]

describe('generated asset catalog', () => {
  it('contains the complete expected collection', () => {
    expect(catalog).toHaveLength(108)
    expect(new Set(catalog.map((entry) => entry.id)).size).toBe(108)
    expect(catalog.filter((entry) => entry.turnaround)).toHaveLength(108)
    expect(catalog.filter((entry) => entry.weapon)).toHaveLength(90)
    expect(catalog.filter((entry) => entry.mount)).toHaveLength(14)
  })

  it('uses continuous zero-padded ids', () => {
    expect(catalog.map((entry) => entry.id)).toEqual(
      Array.from({ length: 108 }, (_, index) =>
        String(index + 1).padStart(3, '0'),
      ),
    )
  })
})
