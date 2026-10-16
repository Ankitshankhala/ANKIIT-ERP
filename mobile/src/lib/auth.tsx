import { createContext, useCallback, useContext, useEffect, useMemo, useState, type ReactNode } from 'react'

import { api } from './api'
import { defaultServerUrl, normalizeServerUrl } from './server'
import { deleteItem, getItem, setItem } from './storage'
import type { DashboardStats, TokenResponse, User } from './types'

const KEYS = {
  server: 'ankiit.server',
  access: 'ankiit.access_token',
  refresh: 'ankiit.refresh_token',
}

interface AuthContextValue {
  user: User | null
  organizationName: string | null
  /** True while a saved session is being restored on launch */
  isRestoring: boolean
  server: string
  signIn: (identifier: string, password: string, server: string) => Promise<void>
  signOut: () => Promise<void>
  /** Same rule as the backend: superusers and "*" roles hold every permission */
  can: (permission: string) => boolean
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [organizationName, setOrganizationName] = useState<string | null>(null)
  const [isRestoring, setIsRestoring] = useState(true)
  const [server, setServer] = useState(defaultServerUrl())

  const clearSession = useCallback(async () => {
    api.configure({ accessToken: null, refreshToken: null })
    setUser(null)
    setOrganizationName(null)
    await Promise.all([deleteItem(KEYS.access), deleteItem(KEYS.refresh)])
  }, [])

  const loadProfile = useCallback(async () => {
    const me = await api.get<User>('/auth/me')
    setUser(me)
    // Organization name is a nice-to-have; don't fail sign-in over it
    api.get<DashboardStats>('/dashboard/stats')
      .then((stats) => setOrganizationName(stats.organization_name))
      .catch(() => setOrganizationName(null))
  }, [])

  useEffect(() => {
    api.onTokensChanged = (accessToken) => {
      void setItem(KEYS.access, accessToken)
    }
    api.onSessionExpired = () => {
      void clearSession()
    }
  }, [clearSession])

  // Restore a saved session on launch
  useEffect(() => {
    let cancelled = false
    ;(async () => {
      try {
        const [savedServer, accessToken, refreshToken] = await Promise.all([
          getItem(KEYS.server), getItem(KEYS.access), getItem(KEYS.refresh),
        ])
        const restoredServer = savedServer ?? defaultServerUrl()
        api.configure({ server: restoredServer, accessToken, refreshToken })
        if (!cancelled) setServer(restoredServer)
        if (accessToken) await loadProfile()
      } catch {
        if (!cancelled) await clearSession()
      } finally {
        if (!cancelled) setIsRestoring(false)
      }
    })()
    return () => {
      cancelled = true
    }
  }, [clearSession, loadProfile])

  const signIn = useCallback(async (identifier: string, password: string, serverInput: string) => {
    const nextServer = normalizeServerUrl(serverInput || defaultServerUrl())
    api.configure({ server: nextServer, accessToken: null, refreshToken: null })

    const tokens = await api.post<TokenResponse>(
      '/auth/login',
      { email_or_username: identifier.trim(), password },
      { auth: false },
    )
    api.configure({ accessToken: tokens.access_token, refreshToken: tokens.refresh_token })
    await Promise.all([
      setItem(KEYS.server, nextServer),
      setItem(KEYS.access, tokens.access_token),
      setItem(KEYS.refresh, tokens.refresh_token),
    ])
    setServer(nextServer)
    await loadProfile()
  }, [loadProfile])

  const signOut = useCallback(async () => {
    try {
      await api.post('/auth/logout')
    } catch {
      // Stateless JWTs: signing out locally is what matters
    }
    await clearSession()
  }, [clearSession])

  const can = useCallback((permission: string) => {
    if (!user) return false
    if (user.role_name === 'superuser') return true
    const permissions = user.permissions ?? []
    return permissions.includes('*') || permissions.includes(permission)
  }, [user])

  const value = useMemo<AuthContextValue>(
    () => ({ user, organizationName, isRestoring, server, signIn, signOut, can }),
    [user, organizationName, isRestoring, server, signIn, signOut, can],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext)
  if (!context) throw new Error('useAuth must be used within an AuthProvider')
  return context
}
