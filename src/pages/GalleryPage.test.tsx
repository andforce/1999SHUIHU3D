import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it } from 'vitest'
import { testCharacters } from '../test/fixtures'
import { GalleryPage } from './GalleryPage'

function characterButtons() {
  return screen.queryAllByRole('button', { name: /查看 No\. \d{3} 人物资料/ })
}

describe('GalleryPage', () => {
  it('searches by numeric id and can reset an empty result', async () => {
    const user = userEvent.setup()
    render(<GalleryPage entries={testCharacters} />)

    expect(characterButtons()).toHaveLength(3)
    await user.type(screen.getByPlaceholderText('检索编号，如 027'), '027')

    expect(characterButtons()).toHaveLength(1)
    expect(characterButtons()[0]).toHaveAccessibleName('查看 No. 027 人物资料')

    await user.clear(screen.getByPlaceholderText('检索编号，如 027'))
    await user.type(screen.getByPlaceholderText('检索编号，如 027'), '999')
    expect(screen.getByText('名录中未寻得此编号')).toBeInTheDocument()

    await user.click(screen.getByRole('button', { name: '重置名录' }))
    expect(characterButtons()).toHaveLength(3)
  })

  it('filters mount assets and reverses sort order', async () => {
    const user = userEvent.setup()
    render(<GalleryPage entries={testCharacters} />)

    await user.click(screen.getByRole('button', { name: '有坐骑' }))
    expect(characterButtons()).toHaveLength(1)
    expect(characterButtons()[0]).toHaveAccessibleName('查看 No. 002 人物资料')

    await user.click(screen.getByRole('button', { name: '全部人物' }))
    await user.click(
      screen.getByRole('button', { name: '当前编号升序，点击切换为降序' }),
    )

    const grid = screen.getByRole('region', { name: '人物卡片' })
    const sortedButtons = within(grid).getAllByRole('button')
    expect(sortedButtons[0]).toHaveAccessibleName('查看 No. 027 人物资料')
  })

  it('filters characters with head four-view artwork', async () => {
    const user = userEvent.setup()
    render(<GalleryPage entries={testCharacters} />)

    await user.click(screen.getByRole('button', { name: '有头部四视' }))
    expect(characterButtons()).toHaveLength(1)
    expect(characterButtons()[0]).toHaveAccessibleName('查看 No. 001 人物资料')

    await user.click(characterButtons()[0])
    const dialog = screen.getByRole('dialog', { name: '人物 · No. 001' })
    expect(
      within(dialog).getAllByRole('heading', { level: 3 }).map((heading) => heading.textContent),
    ).toEqual(['原始卡片', '头部四视', '人物五视', '兵器设定'])
  })

  it('opens a complete character popup in the intended image order', async () => {
    const user = userEvent.setup()
    render(<GalleryPage entries={testCharacters} />)

    await user.click(screen.getByRole('button', { name: '查看 No. 002 人物资料' }))

    const dialog = screen.getByRole('dialog', { name: '人物 · No. 002' })
    expect(dialog).toBeInTheDocument()
    expect(
      within(dialog).getAllByRole('heading', { level: 3 }).map((heading) => heading.textContent),
    ).toEqual(['原始卡片', '人物五视', '兵器设定', '坐骑设定'])

    await user.click(within(dialog).getByRole('button', { name: '下一位 No. 027' }))
    expect(screen.getByRole('dialog', { name: '人物 · No. 027' })).toBeInTheDocument()
    expect(screen.queryByRole('heading', { level: 3, name: '坐骑设定' })).not.toBeInTheDocument()

    await user.click(screen.getByRole('button', { name: '关闭人物资料' }))
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument()
  })
})
