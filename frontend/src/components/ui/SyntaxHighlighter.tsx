'use client'

import { useEffect, useState } from 'react'
import { getHighlightedCode } from '@/lib/getHighlightedCode'

type Props = {
  code: string
  language?: string
}

export function HighlightedCode({ code, language = 'tsx' }: Props) {
  const [highlighted, setHighlighted] = useState('')

  useEffect(() => {
    getHighlightedCode(code, language).then(setHighlighted)
  }, [code, language])

  return (
    <div
      className="shiki rounded-lg overflow-auto text-xs leading-relaxed border border-border bg-muted/10"
      dangerouslySetInnerHTML={{ __html: highlighted }}
    />
  )
}
