import { useEffect, useState } from 'react'
import { characters } from './data/catalog'
import { parseHash } from './lib/routes'
import { CharacterPage } from './pages/CharacterPage'
import { GalleryPage } from './pages/GalleryPage'
import { NotFoundPage } from './pages/NotFoundPage'

function currentRoute() {
  return parseHash(window.location.hash)
}

export default function App() {
  const [route, setRoute] = useState(currentRoute)

  useEffect(() => {
    function onHashChange() {
      setRoute(currentRoute())
      window.scrollTo({ top: 0, behavior: 'instant' })
    }

    window.addEventListener('hashchange', onHashChange)
    return () => window.removeEventListener('hashchange', onHashChange)
  }, [])

  useEffect(() => {
    document.title =
      route.page === 'character'
        ? `No. ${route.id} · 一百单八将收藏图鉴`
        : '一百单八将 · 1999 小浣熊水浒图鉴'
  }, [route])

  if (route.page === 'gallery') return <GalleryPage entries={characters} />

  if (route.page === 'character') {
    const entry = characters.find((item) => item.id === route.id)
    if (entry) {
      return (
        <CharacterPage
          key={entry.id}
          entry={entry}
          entries={characters}
        />
      )
    }
  }

  return <NotFoundPage />
}
