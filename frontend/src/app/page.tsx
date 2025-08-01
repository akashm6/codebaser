'use client'

import { useState } from 'react'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { useRouter } from 'next/navigation'
import { toast } from 'sonner'
import { motion } from 'framer-motion'

export default function Home() {
  const router = useRouter()
  const [zipFile, setZipFile] = useState<File | null>(null)
  const [githubUrl, setGithubUrl] = useState('')
  const [isUploading, setIsUploading] = useState(false)

  const FASTAPI_BACKEND = process.env.NEXT_PUBLIC_FASTAPI_BACKEND

  async function handleUpload() {
    if (!zipFile) return toast.error('Please select a file')
    setIsUploading(true)

    const res = await fetch(`${FASTAPI_BACKEND}/generate-presigned-url?filename=${zipFile.name}&content_type=${zipFile.type}`)
    const { url, key } = await res.json()

    await fetch(url, {
      method: 'PUT',
      headers: { 'Content-Type': zipFile.type },
      body: zipFile,
    })

    const payload = {
      s3_key: key,
      name: zipFile.name,
      content_type: zipFile.type,
      size: zipFile.size,
    }

    const res2 = await fetch(`${FASTAPI_BACKEND}/zip-processing`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    })

    if (res2.ok) {
      toast.success('Upload complete!')
      router.push('/workspace')
    } else {
      toast.error('Processing failed')
    }

    setIsUploading(false)
  }

  return (
    <main className="min-h-screen flex flex-col items-center justify-center px-6 py-24 bg-background text-white">
      <div className="text-center mb-16">
        <h1 className="text-4xl md:text-5xl font-bold mb-4 tracking-tight">
          AI-Powered Codebase Intelligence
        </h1>
        <p className="text-muted-foreground text-lg max-w-xl mx-auto">
          Upload a zip file or GitHub repo and start asking questions about your code instantly.
        </p>
      </div>

      <Card className="w-full max-w-md border border-border bg-card/50 backdrop-blur">
        <CardHeader>
          <CardTitle className="text-xl">Upload or Link a Repo</CardTitle>
        </CardHeader>
        <CardContent>
          <Tabs defaultValue="zip" className="w-full">
            <TabsList className="w-full grid grid-cols-2">
              <TabsTrigger value="zip">ZIP Upload</TabsTrigger>
              <TabsTrigger value="github">GitHub Repo</TabsTrigger>
            </TabsList>
            <TabsContent value="zip" className="mt-4 space-y-4">
              <Input type="file" accept=".zip" onChange={(e) => setZipFile(e.target.files?.[0] || null)} />
              <Button onClick={handleUpload} disabled={isUploading} className="w-full">
                {isUploading ? 'Uploading...' : 'Upload & Analyze'}
              </Button>
            </TabsContent>
            <TabsContent value="github" className="mt-4 space-y-4">
              <Input placeholder="https://github.com/user/repo" value={githubUrl} onChange={(e) => setGithubUrl(e.target.value)} />
              <Button disabled className="w-full">Coming soon</Button>
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>

      <motion.div
        animate={{ y: [0, -8, 0] }}
        transition={{ repeat: Infinity, duration: 1.5 }}
        className="mt-24 text-muted-foreground text-sm"
      >
        ↓ Scroll to see how it works ↓
      </motion.div>
    </main>
  )
}
