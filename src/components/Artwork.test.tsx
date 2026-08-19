import { fireEvent, render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'
import { Artwork } from './Artwork'

describe('Artwork', () => {
  it('shows a styled fallback after an image load error', () => {
    render(<Artwork src="/missing.png" alt="测试画卷" />)
    fireEvent.error(screen.getByRole('img', { name: '测试画卷' }))
    expect(screen.getByRole('img', { name: '测试画卷加载失败' })).toBeInTheDocument()
    expect(screen.getByText('画卷暂不可见')).toBeInTheDocument()
  })
})
