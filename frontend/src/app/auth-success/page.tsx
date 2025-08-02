'use client'
import { useEffect } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import { Suspense } from 'react'
import {motion} from "framer-motion"

function AuthSuccess() {
  const router = useRouter()
  const params = useSearchParams()
  const token = params.get('token')

  useEffect(() => {
    if (token) {
      localStorage.setItem('auth_token', token)
      router.push('/')
    }
  }, [token])

  return (
    <motion.div
      initial={{ opacity: 0.4 }}
      animate={{ opacity: [0.4, 1, 0.4] }}
      transition={{ repeat: Infinity, duration: 1.5, ease: "easeInOut" }}
      className="mt-3 text-center text-sm text-white/80"
    >
      Logging in...
    </motion.div>
  );
}

export default function Page() {
  return (
    <Suspense>
      <AuthSuccess />
    </Suspense>
  );
}
