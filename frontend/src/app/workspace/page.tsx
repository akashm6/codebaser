'use client'

import { useState } from 'react'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { toast } from 'sonner'
import { Card, CardHeader, CardContent, CardTitle } from '@/components/ui/card'
import { HighlightedCode } from '@/components/ui/SyntaxHighlighter'
import { motion } from 'framer-motion'

export default function Workspace() {
  const [query, setQuery] = useState('')
  const [answer, setAnswer] = useState('')
  const [code, setCode] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const FASTAPI_BACKEND = process.env.NEXT_PUBLIC_FASTAPI_BACKEND

  async function askQuestion() {
    if (!query) return toast.error('Enter a question')
    setIsLoading(true)

    const token = localStorage.getItem('auth_token')

    try {
      const res = await fetch(`${FASTAPI_BACKEND}/ask`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ query }),
      })

      const data = await res.json()
      setAnswer(data.answer)
      setCode(data.chunks.map((c: any) => c.text).join('\n\n'))
    } catch (err) {
      toast.error('Error fetching answer')
    }

    setIsLoading(false)
  }

  return (
    <div className="min-h-screen w-full bg-background text-white pb-36 px-6 pt-20">
      <div className="grid md:grid-cols-2 gap-6 max-w-7xl mx-auto mb-16">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
        >
          <Card className="h-[500px] overflow-auto shadow-md bg-muted/5 border border-border rounded-xl">
            <CardHeader>
              <CardTitle>Summary</CardTitle>
            </CardHeader>
            <CardContent className="text-sm text-muted-foreground whitespace-pre-line">
              {answer ? (
                answer
              ) : (
                <span className="text-zinc-600 italic">
                  Ask a question to see the summary...
                </span>
              )}
            </CardContent>
          </Card>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.1 }}
        >
          <Card className="h-[500px] overflow-auto shadow-md bg-muted/5 border border-border rounded-xl">
            <CardHeader>
              <CardTitle>Relevant Code</CardTitle>
            </CardHeader>
            <CardContent className="p-0">
              {code ? (
                <HighlightedCode code={code} />
              ) : (
                <div className="h-full w-full text-sm text-zinc-600 italic p-4">
                  Matching code will appear here once you ask a question.
                </div>
              )}
            </CardContent>
          </Card>
        </motion.div>
      </div>

      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3, delay: 0.2 }}
        className="fixed bottom-10 left-1/2 -translate-x-1/2 w-full max-w-3xl px-4 z-50"
      >
        <div className="flex gap-3 bg-transparent border border-zinc-800 rounded-xl shadow-lg p-5">
          <Input
            className="flex-1 text-base text-black placeholder:text-zinc-400 py-6"
            placeholder="Ask something about your code..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <Button
            onClick={askQuestion}
            disabled={isLoading}
            className="px-6 text-base font-medium rounded-lg transition-all duration-200 bg-gradient-to-br from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 hover:scale-[1.03] disabled:opacity-50"
          >
            {isLoading ? 'Asking...' : 'Ask'}
          </Button>
        </div>
      </motion.div>
    </div>
  )
}
