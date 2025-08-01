'use client'
import { useState } from 'react'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { toast } from 'sonner'
import { Card, CardHeader, CardContent, CardTitle } from '@/components/ui/card'
import { HighlightedCode } from '@/components/ui/SyntaxHighlighter' 

export default function Workspace() {
  const [query, setQuery] = useState('')
  const [answer, setAnswer] = useState('')
  const [code, setCode] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const FASTAPI_BACKEND = process.env.NEXT_PUBLIC_FASTAPI_BACKEND


  async function askQuestion() {
    if (!query) return toast.error('Enter a question')
    setIsLoading(true)

    const token = localStorage.getItem("auth_token");

    try {
      const res = await fetch(`${FASTAPI_BACKEND}/ask`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}` 
        },
        body: JSON.stringify({ query }),
      })

      const data = await res.json()
      console.log(data.chunks);
      setAnswer(data.answer)
      setCode(data.chunks.map((c: any) => c.text).join('\n\n'))
    } catch (err) {
      toast.error('Error fetching answer')
    }

    setIsLoading(false)
  }

  return (
    <div className="min-h-screen w-full bg-background text-white pb-36 px-6 pt-16">
      {(answer || code) && (
        <div className="grid md:grid-cols-2 gap-6 max-w-7xl mx-auto mb-16">
          <Card className="h-[500px] overflow-auto">
            <CardHeader>
              <CardTitle>Summary</CardTitle>
            </CardHeader>
            <CardContent className="text-sm text-muted-foreground whitespace-pre-line">
              {answer || 'No summary returned'}
            </CardContent>
          </Card>

          <Card className="h-[500px] overflow-auto">
            <CardHeader>
              <CardTitle>Relevant Code</CardTitle>
            </CardHeader>
            <CardContent className="p-0">
              <HighlightedCode code = {code}></HighlightedCode>
            </CardContent>
          </Card>
        </div>
      )}

      <div className="fixed bottom-10 left-1/2 -translate-x-1/2 w-full max-w-2xl px-4 z-50">
        <div className="flex gap-2 bg-transparent border border-zinc-800 rounded-xl shadow-lg p-4">
          <Input
            className="flex-1 text-base text-black"
            placeholder="Ask something about your code..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <Button onClick={askQuestion} disabled={isLoading}>
            {isLoading ? 'Asking...' : 'Ask'}
          </Button>
        </div>
      </div>
    </div>
  )
}
