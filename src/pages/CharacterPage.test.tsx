import { fireEvent, render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it } from 'vitest'
import { testCharacters } from '../test/fixtures'
import { CharacterPage } from './CharacterPage'

describe('CharacterPage', () => {
  it('renders every available asset in the fixed vertical order', () => {
    render(
      <CharacterPage
        entry={testCharacters[1]}
        entries={testCharacters}
      />,
    )

    expect(screen.queryByRole('navigation', { name: '人物素材类别' })).not.toBeInTheDocument()
    expect(
      screen.getAllByRole('heading', { level: 2 }).map((heading) => heading.textContent),
    ).toEqual(['原始卡片', '人物五视', '原画动作六视', '兵器设定', '坐骑设定'])
  })

  it('omits weapon and mount panels when those assets do not exist', () => {
    render(
      <CharacterPage entry={testCharacters[2]} entries={testCharacters} />,
    )

    expect(screen.getByRole('heading', { name: '人物五视' })).toBeInTheDocument()
    expect(screen.getByRole('heading', { name: '原画动作六视' })).toBeInTheDocument()
    expect(screen.queryByRole('heading', { name: '兵器设定' })).not.toBeInTheDocument()
    expect(screen.queryByRole('heading', { name: '坐骑设定' })).not.toBeInTheDocument()
  })

  it('shows the optional head four-view before the full character view', () => {
    render(
      <CharacterPage
        entry={testCharacters[0]}
        entries={testCharacters}
      />,
    )

    expect(
      screen.getAllByRole('heading', { level: 2 }).map((heading) => heading.textContent),
    ).toEqual(['原始卡片', '头部四视', '人物五视', '原画动作六视', '兵器设定'])
  })

  it('opens the full-screen viewer and closes it with Escape', async () => {
    const user = userEvent.setup()
    render(
      <CharacterPage
        entry={testCharacters[0]}
        entries={testCharacters}
      />,
    )

    await user.click(screen.getByRole('button', { name: '放大兵器设定' }))
    expect(screen.getByRole('dialog')).toHaveAccessibleName(
      'No. 001 武器图',
    )

    fireEvent.keyDown(window, { key: 'Escape' })
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument()
  })

  it('uses arrow keys to navigate between characters', () => {
    render(
      <CharacterPage
        entry={testCharacters[1]}
        entries={testCharacters}
      />,
    )

    fireEvent.keyDown(window, { key: 'ArrowRight' })
    expect(window.location.hash).toBe('#/character/027/turnaround')
  })
})
