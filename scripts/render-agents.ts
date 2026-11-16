// Usage: node scripts/render-agents.ts <humanlayer-repo> <out-dir>
import { mkdirSync, writeFileSync } from 'node:fs'
import { join, resolve } from 'node:path'

const [repo, outDir] = process.argv.slice(2).map((p) => resolve(p))

if (!repo || !outDir) throw new Error('usage: render-agents.ts <humanlayer-repo> <out-dir>')

const src = join(repo, 'apps/riptide-daemon/src/agents/claudecode')
const { bundledAgents } = await import(join(src, 'bundled-agents.ts'))
const { renderAgentMarkdown } = await import(join(src, 'agents/markdown.ts'))

mkdirSync(outDir, { recursive: true })

for (const [key, def] of Object.entries(bundledAgents)) {
	const name = key.replace(/^rpi:/, '')
	writeFileSync(join(outDir, `${name}.md`), renderAgentMarkdown(name, def))
	console.log(`${key} -> ${name}.md`)
}
