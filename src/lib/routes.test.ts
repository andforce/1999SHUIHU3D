import { describe, expect, it } from 'vitest'
import { testCharacters } from '../test/fixtures'
import {
  availableViews,
  characterHref,
  parseHash,
  supportedView,
} from './routes'

describe('hash routing', () => {
  it('parses the gallery and direct character routes', () => {
    expect(parseHash('#/')).toEqual({ page: 'gallery' })
    expect(parseHash('#/character/027/weapon')).toEqual({
      page: 'character',
      id: '027',
      view: 'weapon',
    })
    expect(parseHash('#/character/001')).toEqual({
      page: 'character',
      id: '001',
      view: 'turnaround',
    })
    expect(parseHash('#/missing')).toEqual({ page: 'not-found' })
  })

  it('builds stable static-friendly links', () => {
    expect(characterHref('108', 'mount')).toBe('#/character/108/mount')
  })

  it('only exposes assets that exist and falls back to the turnaround', () => {
    expect(availableViews(testCharacters[0])).toEqual([
      'card',
      'turnaround',
      'weapon',
    ])
    expect(supportedView(testCharacters[2], 'mount')).toBe('turnaround')
  })
})
