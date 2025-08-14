import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react'
import { authService } from '../services/authService'

interface User {
  id: number
  username: string
  email: string
  first_name: string
  last_name: string
  is_active: boolean
  organization_id: number
  role_id: number
  role_name?: string
  permissions?: string[]
}

interface AuthContextType {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  login: (email: string, password: string) => Promise<void>
  register: (userData: any) => Promise<void>
  logout: () => void
  refreshToken: () => Promise<void>
  hasPermission: (perm: string) => boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

interface AuthProviderProps {
  children: ReactNode
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    // Check if user is already logged in
    const token = localStorage.getItem('access_token')
    if (token) {
      checkAuthStatus()
    } else {
      setIsLoading(false)
    }
  }, [])

  const checkAuthStatus = async () => {
    try {
      const userData = await authService.getCurrentUser()
      setUser(userData)
    } catch (error) {
      // Token is invalid, remove it
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
    } finally {
      setIsLoading(false)
    }
  }

  const login = async (email: string, password: string) => {
    try {
      const response = await authService.login(email, password)
      localStorage.setItem('access_token', response.access_token)
      localStorage.setItem('refresh_token', response.refresh_token)
      
      // Get user data
      const userData = await authService.getCurrentUser()
      setUser(userData)
    } catch (error) {
      throw error
    }
  }

  const register = async (userData: any) => {
    try {
      await authService.register(userData)
      // Optionally auto-login after registration
    } catch (error) {
      throw error
    }
  }

  const logout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    setUser(null)
  }

  const refreshToken = async () => {
    try {
      const refreshToken = localStorage.getItem('refresh_token')
      if (!refreshToken) {
        throw new Error('No refresh token')
      }

      const response = await authService.refreshToken(refreshToken)
      localStorage.setItem('access_token', response.access_token)
      
      // Get updated user data
      const userData = await authService.getCurrentUser()
      setUser(userData)
    } catch (error) {
      // Refresh failed, logout user
      logout()
      throw error
    }
  }

  const value: AuthContextType = {
    user,
    isAuthenticated: !!user,
    isLoading,
    login,
    register,
    logout,
    refreshToken,
    hasPermission: (perm: string) => !!user?.permissions?.includes(perm)
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}
