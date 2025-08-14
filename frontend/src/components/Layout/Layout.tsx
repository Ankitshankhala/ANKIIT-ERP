import React, { useState } from 'react'
import { Outlet, useLocation, useNavigate } from 'react-router-dom'
import { 
  Menu, 
  X, 
  Home, 
  Users, 
  Building2, 
  Settings, 
  BarChart3, 
  DollarSign, 
  UserCheck, 
  MessageSquare, 
  Package, 
  FolderOpen,
  LogOut,
  User
} from 'lucide-react'
import { useAuth } from '../../hooks/useAuth'

const Layout: React.FC = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const { user, logout } = useAuth()
  const location = useLocation()
  const navigate = useNavigate()

  const navigation = [
    { name: 'Dashboard', href: '/dashboard', icon: Home },
    { name: 'Users', href: '/users', icon: Users },
    { name: 'Organizations', href: '/organizations', icon: Building2 },
    { name: 'Finance', href: '/finance', icon: DollarSign },
    { name: 'HR', href: '/hr', icon: UserCheck },
    { name: 'CRM', href: '/crm', icon: MessageSquare },
    { name: 'Inventory', href: '/inventory', icon: Package },
    { name: 'Projects', href: '/projects', icon: FolderOpen, comingSoon: true },
    { name: 'Analytics', href: '/analytics', icon: BarChart3, comingSoon: true },
    { name: 'Settings', href: '/settings', icon: Settings },
  ]

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  const isActive = (href: string) => {
    return location.pathname === href
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Mobile sidebar */}
      <div className={`fixed inset-0 z-50 lg:hidden ${sidebarOpen ? 'block' : 'hidden'}`}>
        <div className="fixed inset-0 bg-gray-600 bg-opacity-75" onClick={() => setSidebarOpen(false)} />
        <div className="fixed inset-y-0 left-0 flex w-64 flex-col bg-white">
          <div className="flex h-16 items-center justify-between px-4">
            <div className="flex items-center">
              <div className="h-8 w-8 rounded-lg bg-primary-600 flex items-center justify-center">
                <span className="text-white font-bold text-lg">A</span>
              </div>
              <span className="ml-2 text-xl font-bold text-gray-900">ANKIIT ERP</span>
            </div>
            <button
              onClick={() => setSidebarOpen(false)}
              className="text-gray-400 hover:text-gray-600"
            >
              <X className="h-6 w-6" />
            </button>
          </div>
          <nav className="flex-1 space-y-1 px-2 py-4">
            {navigation.map((item) => {
              const Icon = item.icon
              return (
                <button
                  key={item.name}
                  onClick={() => {
                    if (!item.comingSoon) {
                      navigate(item.href)
                      setSidebarOpen(false)
                    }
                  }}
                  className={`sidebar-item w-full justify-start ${
                    isActive(item.href) ? 'active' : ''
                  } ${item.comingSoon ? 'opacity-50 cursor-not-allowed' : ''}`}
                  disabled={item.comingSoon}
                >
                  <Icon className="mr-3 h-5 w-5" />
                  {item.name}
                  {item.comingSoon && (
                    <span className="ml-auto text-xs text-gray-400">Soon</span>
                  )}
                </button>
              )
            })}
          </nav>
        </div>
      </div>

      {/* Desktop sidebar */}
      <div className="hidden lg:fixed lg:inset-y-0 lg:flex lg:w-64 lg:flex-col">
        <div className="flex flex-col flex-grow bg-white border-r border-gray-200">
          <div className="flex h-16 items-center px-4">
            <div className="h-8 w-8 rounded-lg bg-primary-600 flex items-center justify-center">
              <span className="text-white font-bold text-lg">A</span>
            </div>
            <span className="ml-2 text-xl font-bold text-gray-900">ANKIIT ERP</span>
          </div>
          <nav className="flex-1 space-y-1 px-2 py-4">
            {navigation.map((item) => {
              const Icon = item.icon
              return (
                <button
                  key={item.name}
                  onClick={() => {
                    if (!item.comingSoon) {
                      navigate(item.href)
                    }
                  }}
                  className={`sidebar-item w-full justify-start ${
                    isActive(item.href) ? 'active' : ''
                  } ${item.comingSoon ? 'opacity-50 cursor-not-allowed' : ''}`}
                  disabled={item.comingSoon}
                >
                  <Icon className="mr-3 h-5 w-5" />
                  {item.name}
                  {item.comingSoon && (
                    <span className="ml-auto text-xs text-gray-400">Soon</span>
                  )}
                </button>
              )
            })}
          </nav>
        </div>
      </div>

      {/* Main content */}
      <div className="lg:pl-64">
        {/* Top header */}
        <div className="sticky top-0 z-40 flex h-16 shrink-0 items-center gap-x-4 border-b border-gray-200 bg-white px-4 shadow-sm sm:gap-x-6 sm:px-6 lg:px-8">
          <button
            type="button"
            className="-m-2.5 p-2.5 text-gray-700 lg:hidden"
            onClick={() => setSidebarOpen(true)}
          >
            <Menu className="h-6 w-6" />
          </button>

          <div className="flex flex-1 gap-x-4 self-stretch lg:gap-x-6">
            <div className="flex flex-1" />
            <div className="flex items-center gap-x-4 lg:gap-x-6">
              {/* User menu */}
              <div className="relative">
                <div className="flex items-center gap-x-3">
                  <div className="h-8 w-8 rounded-full bg-primary-100 flex items-center justify-center">
                    <User className="h-4 w-4 text-primary-600" />
                  </div>
                  <div className="hidden md:block">
                    <div className="text-sm font-medium text-gray-900">
                      {user?.first_name} {user?.last_name}
                    </div>
                    <div className="text-xs text-gray-500">{user?.email}</div>
                  </div>
                </div>
              </div>

              {/* Logout button */}
              <button
                onClick={handleLogout}
                className="text-gray-400 hover:text-gray-600"
                title="Logout"
              >
                <LogOut className="h-5 w-5" />
              </button>
            </div>
          </div>
        </div>

        {/* Page content */}
        <main className="py-6">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  )
}

export default Layout
