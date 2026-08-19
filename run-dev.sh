#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

if ! command -v node >/dev/null 2>&1; then
  echo "未找到 Node.js。请先安装 Node.js 20 或更高版本。" >&2
  exit 1
fi

if ! command -v npm >/dev/null 2>&1; then
  echo "未找到 npm。请安装带 npm 的 Node.js 20 或更高版本。" >&2
  exit 1
fi

node -e "const major=Number(process.versions.node.split('.')[0]); if (major < 20) { console.error('当前 Node.js 版本过低，需要 20 或更高版本。'); process.exit(1) }"

if [[ ! -d node_modules ]]; then
  echo "首次运行，正在安装依赖……"
  npm install
fi

echo "正在启动 1999 小浣熊水浒图鉴……"
echo "浏览地址：http://127.0.0.1:5173"
exec npm run dev -- --host 127.0.0.1
