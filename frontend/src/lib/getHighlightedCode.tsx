import { createHighlighter } from 'shiki'
import { Highlighter } from 'shiki'

let cachedHighlighter: Highlighter | null = null

export async function getHighlightedCode(code: string, lang = 'tsx') {
  if (!cachedHighlighter) {
    cachedHighlighter = await createHighlighter({
      themes: ['github-light'],
      langs: ['tsx', 'js', 'ts', 'python', 'java', 'go', 'bash'],
    })
  }

  return cachedHighlighter.codeToHtml(code, { 
    lang: lang,
    theme: 'github-light'
    }, )
}
