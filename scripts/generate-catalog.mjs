import { access, mkdir, readFile, rename, stat, writeFile } from 'node:fs/promises'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import sharp from 'sharp'

const scriptDirectory = path.dirname(fileURLToPath(import.meta.url))
const projectRoot = path.resolve(scriptDirectory, '..')
const generatedDirectory = path.join(projectRoot, 'src', 'generated')
const thumbnailDirectory = path.join(projectRoot, 'public', 'generated', 'cards')
const catalogPath = path.join(generatedDirectory, 'catalog.json')
const checkOnly = process.argv.includes('--check')

const EXPECTED = {
  card: 108,
  turnaround: 108,
  weapon: 90,
  mount: 14,
}

async function exists(filePath) {
  try {
    await access(filePath)
    return true
  } catch {
    return false
  }
}

async function collectCatalog() {
  const entries = []

  for (let number = 1; number <= EXPECTED.card; number += 1) {
    const id = String(number).padStart(3, '0')
    const characterDirectory = path.join(
      projectRoot,
      'character-model-sheets',
      'characters',
      id,
    )
    const card = `${id}.png`
    const turnaround = `character-model-sheets/characters/${id}/character-turnaround.png`
    const weapon = `character-model-sheets/characters/${id}/weapon-sheet.png`
    const mount = `character-model-sheets/characters/${id}/mount-sheet.png`

    if (!(await exists(path.join(projectRoot, card)))) {
      throw new Error(`缺少卡片源图：${card}`)
    }

    if (!(await exists(path.join(projectRoot, turnaround)))) {
      throw new Error(`缺少人物五视图：${turnaround}`)
    }

    entries.push({
      id,
      card,
      thumbnail: `generated/cards/${id}.webp`,
      turnaround,
      ...((await exists(path.join(projectRoot, weapon))) ? { weapon } : {}),
      ...((await exists(path.join(projectRoot, mount))) ? { mount } : {}),
    })
  }

  return entries
}

function validateCatalog(entries) {
  const ids = new Set(entries.map((entry) => entry.id))
  const counts = {
    card: entries.length,
    turnaround: entries.filter((entry) => entry.turnaround).length,
    weapon: entries.filter((entry) => entry.weapon).length,
    mount: entries.filter((entry) => entry.mount).length,
  }

  if (ids.size !== entries.length) {
    throw new Error('素材目录中存在重复编号。')
  }

  for (const [kind, expected] of Object.entries(EXPECTED)) {
    if (counts[kind] !== expected) {
      throw new Error(`${kind} 数量异常：期望 ${expected}，实际 ${counts[kind]}`)
    }
  }

  return counts
}

async function fileIsCurrent(sourcePath, outputPath) {
  if (!(await exists(outputPath))) return false
  const [sourceStats, outputStats] = await Promise.all([
    stat(sourcePath),
    stat(outputPath),
  ])
  return outputStats.mtimeMs >= sourceStats.mtimeMs
}

async function generateThumbnail(entry) {
  const sourcePath = path.join(projectRoot, entry.card)
  const outputPath = path.join(projectRoot, 'public', entry.thumbnail)

  if (await fileIsCurrent(sourcePath, outputPath)) return false

  const temporaryPath = `${outputPath}.tmp-${process.pid}`
  await sharp(sourcePath)
    .resize(480, 720, {
      fit: 'cover',
      position: 'centre',
      withoutEnlargement: true,
    })
    .webp({ quality: 80, smartSubsample: true })
    .toFile(temporaryPath)
  await rename(temporaryPath, outputPath)
  return true
}

async function writeIfChanged(filePath, contents) {
  let current = ''
  try {
    current = await readFile(filePath, 'utf8')
  } catch {
    // First generation.
  }
  if (current !== contents) await writeFile(filePath, contents, 'utf8')
}

const entries = await collectCatalog()
const counts = validateCatalog(entries)

if (!checkOnly) {
  await Promise.all([
    mkdir(generatedDirectory, { recursive: true }),
    mkdir(thumbnailDirectory, { recursive: true }),
  ])

  let generatedCount = 0
  const concurrency = 6
  for (let index = 0; index < entries.length; index += concurrency) {
    const batch = entries.slice(index, index + concurrency)
    const results = await Promise.all(batch.map(generateThumbnail))
    generatedCount += results.filter(Boolean).length
  }

  await writeIfChanged(catalogPath, `${JSON.stringify(entries, null, 2)}\n`)
  console.log(`素材目录已生成，更新 ${generatedCount} 张缩略图。`)
}

console.log(
  `素材校验通过：卡片 ${counts.card}，五视图 ${counts.turnaround}，武器 ${counts.weapon}，坐骑 ${counts.mount}。`,
)
