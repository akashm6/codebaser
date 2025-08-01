'use client'
import { useEffect } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'

export default function AuthSuccess() {
  const router = useRouter()
  const params = useSearchParams()
  const token = params.get('token')

  useEffect(() => {
    if (token) {
      localStorage.setItem('auth_token', token)
      router.push('/')
    }
  }, [token])

  return <p>Logging in...</p>
}
