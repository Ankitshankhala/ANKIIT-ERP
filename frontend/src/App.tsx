import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuth } from './hooks/useAuth'
import { AuthProvider } from './contexts/AuthContext'

// Layout components
import Layout from './components/Layout/Layout'
import AuthLayout from './components/Layout/AuthLayout'

// Page components
import Dashboard from './pages/Dashboard'
import Finance from './pages/Finance'
import Inventory from './pages/Inventory'
import CRM from './pages/CRM'
import HR from './pages/HR'
import Finance from './pages/Finance'
import Login from './pages/Auth/Login'
import Register from './pages/Auth/Register'
import Users from './pages/Users'
import Organizations from './pages/Organizations'
import Settings from './pages/Settings'
import NotFound from './pages/NotFound'

// Protected route component
const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
  const { isAuthenticated, isLoading } = useAuth()
  
  if (isLoading) {
    return <div>Loading...</div>
  }
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }
  
  return <>{children}</>
}

function AppRoutes() {
  return (
    <Routes>
      {/* Public routes */}
      <Route path="/login" element={<AuthLayout><Login /></AuthLayout>} />
      <Route path="/register" element={<AuthLayout><Register /></AuthLayout>} />
      
      {/* Protected routes */}
      <Route path="/" element={
        <ProtectedRoute>
          <Layout />
        </ProtectedRoute>
      }>
        <Route index element={<Navigate to="/dashboard" replace />} />
        <Route path="dashboard" element={<Dashboard />} />
        <Route path="users" element={<Users />} />
        <Route path="organizations" element={<Organizations />} />
        <Route path="settings" element={<Settings />} />
        
        {/* ERP module routes */}
        <Route path="finance" element={<Finance />} />
        <Route path="inventory" element={<Inventory />} />
        <Route path="crm" element={<CRM />} />
        <Route path="hr" element={<HR />} />
        <Route path="hr/*" element={<div>HR Module - Coming Soon</div>} />
        <Route path="crm/*" element={<div>CRM Module - Coming Soon</div>} />
        <Route path="projects/*" element={<div>Projects Module - Coming Soon</div>} />
      </Route>
      
      {/* 404 route */}
      <Route path="*" element={<NotFound />} />
    </Routes>
  )
}

function App() {
  return (
    <AuthProvider>
      <AppRoutes />
    </AuthProvider>
  )
}

export default App
