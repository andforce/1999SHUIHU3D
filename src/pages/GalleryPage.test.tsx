import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it } from 'vitest'
import { testCharacters } from '../test/fixtures'
import { GalleryPage } from './GalleryPage'

function characterLinks() {
  return screen.queryAllByRole('link', { name: /查看 No\. \d{3} 人物详情/ })
}

describe('GalleryPage', () => {
  it('searches by numeric id and can reset an empty result', async () => {
    const user = userEvent.setup()
    render(<GalleryPage entries={testCharacters} />)

    expect(characterLinks()).toHaveLength(3)
    await user.type(screen.getByPlaceholderText('检索编号，如 027'), '027')

    expect(characterLinks()).toHaveLength(1)
    expect(characterLinks()[0]).toHaveAttribute('href', '#/character/027/turnaround')

    await user.clear(screen.getByPlaceholderText('检索编号，如 027'))
    await user.type(screen.getByPlaceholderText('检索编号，如 027'), '999')
    expect(screen.getByText('名录中未寻得此编号')).toBeInTheDocument()

    await user.click(screen.getByRole('button', { name: '重置名录' }))
    expect(characterLinks()).toHaveLength(3)
  })

  it('filters mount assets and reverses sort order', async () => {
    const user = userEvent.setup()
    render(<GalleryPage entries={testCharacters} />)

    await user.click(screen.getByRole('button', { name: '有坐骑' }))
    expect(characterLinks()).toHaveLength(1)
    expect(characterLinks()[0]).toHaveAttribute('href', '#/character/002/turnaround')

    await user.click(screen.getByRole('button', { name: '全部人物' }))
    await user.click(
      screen.getByRole('button', { name: '当前编号升序，点击切换为降序' }),
    )

    const grid = screen.getByRole('region', { name: '人物卡片' })
    const sortedLinks = within(grid).getAllByRole('link')
    expect(sortedLinks[0]).toHaveAttribute('href', '#/character/027/turnaround')
  })
})
