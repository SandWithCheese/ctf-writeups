import { useEffect, useState } from 'react'

export function useToken() {
  const [token, setToken] = useState(() => localStorage.getItem('token') || '')

  useEffect(() => {
    if (token) {
      localStorage.setItem('token', token)
    } else {
      localStorage.removeItem('token')
    }
  }, [token])

  const clear = () => {
    localStorage.removeItem('token')
    setToken('')
  }

  return { token, setToken, clear }
}
