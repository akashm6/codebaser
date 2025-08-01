import { createHighlighter } from 'shiki'

let cachedHighlighter: any = null

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
