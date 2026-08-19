import { ArrowLeft } from 'lucide-react'

export function NotFoundPage() {
  return (
    <main className="not-found-page">
      <span className="not-found-page__seal">空</span>
      <p>此卷无载</p>
      <h1>未找到对应人物或画卷</h1>
      <a href="#/">
        <ArrowLeft aria-hidden="true" size={18} />返回群英谱
      </a>
    </main>
  )
}
