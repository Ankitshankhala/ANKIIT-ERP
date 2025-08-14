import React from 'react'
import { 
  Users, 
  Building2, 
  DollarSign, 
  TrendingUp, 
  TrendingDown,
  Activity,
  Calendar,
  Target
} from 'lucide-react'

const Dashboard: React.FC = () => {
  // Mock data - in real app this would come from API
  const stats = [
    {
      name: 'Total Users',
      value: '1,234',
      change: '+12%',
      changeType: 'positive' as const,
      icon: Users,
      color: 'bg-blue-500',
    },
    {
      name: 'Organizations',
      value: '89',
      change: '+5%',
      changeType: 'positive' as const,
      icon: Building2,
      color: 'bg-green-500',
    },
    {
      name: 'Revenue',
      value: '$45,678',
      change: '+23%',
      changeType: 'positive' as const,
      icon: DollarSign,
      color: 'bg-purple-500',
    },
    {
      name: 'Active Projects',
      value: '34',
      change: '-3%',
      changeType: 'negative' as const,
      icon: Target,
      color: 'bg-orange-500',
    },
  ]

  const recentActivity = [
    { id: 1, action: 'New user registered', user: 'John Doe', time: '2 minutes ago' },
    { id: 2, action: 'Organization created', user: 'Acme Corp', time: '1 hour ago' },
    { id: 3, action: 'Project completed', user: 'Project Alpha', time: '3 hours ago' },
    { id: 4, action: 'Invoice generated', user: 'Invoice #1234', time: '5 hours ago' },
  ]

  const upcomingTasks = [
    { id: 1, title: 'Review quarterly reports', due: 'Today', priority: 'high' },
    { id: 2, title: 'Update user permissions', due: 'Tomorrow', priority: 'medium' },
    { id: 3, title: 'Backup database', due: 'This week', priority: 'low' },
  ]

  return (
    <div className="space-y-6">
      {/* Page header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="mt-1 text-sm text-gray-500">
          Welcome back! Here's what's happening with your ERP system.
        </p>
      </div>

      {/* Stats grid */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat) => {
          const Icon = stat.icon
          return (
            <div key={stat.name} className="stat-card">
              <div className="stat-card-header">
                <div>
                  <p className="stat-card-label">{stat.name}</p>
                  <p className="stat-card-value">{stat.value}</p>
                </div>
                <div className={`${stat.color} rounded-lg p-3`}>
                  <Icon className="h-6 w-6 text-white" />
                </div>
              </div>
              <div className="mt-4 flex items-center">
                {stat.changeType === 'positive' ? (
                  <TrendingUp className="h-4 w-4 text-success-500" />
                ) : (
                  <TrendingDown className="h-4 w-4 text-error-500" />
                )}
                <span className={`stat-card-change ${stat.changeType} ml-2`}>
                  {stat.change}
                </span>
                <span className="text-gray-500 text-sm ml-2">from last month</span>
              </div>
            </div>
          )
        })}
      </div>

      {/* Charts and activity section */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        {/* Recent Activity */}
        <div className="card">
          <div className="card-header">
            <h3 className="text-lg font-medium text-gray-900">Recent Activity</h3>
          </div>
          <div className="card-body">
            <div className="space-y-4">
              {recentActivity.map((activity) => (
                <div key={activity.id} className="flex items-start space-x-3">
                  <div className="h-2 w-2 rounded-full bg-primary-500 mt-2" />
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900">{activity.action}</p>
                    <p className="text-sm text-gray-500">{activity.user} • {activity.time}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Upcoming Tasks */}
        <div className="card">
          <div className="card-header">
            <h3 className="text-lg font-medium text-gray-900">Upcoming Tasks</h3>
          </div>
          <div className="card-body">
            <div className="space-y-4">
              {upcomingTasks.map((task) => (
                <div key={task.id} className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <div className={`h-2 w-2 rounded-full ${
                      task.priority === 'high' ? 'bg-error-500' :
                      task.priority === 'medium' ? 'bg-warning-500' : 'bg-success-500'
                    }`} />
                    <div>
                      <p className="text-sm font-medium text-gray-900">{task.title}</p>
                      <p className="text-sm text-gray-500">Due: {task.due}</p>
                    </div>
                  </div>
                  <span className={`badge ${
                    task.priority === 'high' ? 'badge-error' :
                    task.priority === 'medium' ? 'badge-warning' : 'badge-success'
                  }`}>
                    {task.priority}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="card">
        <div className="card-header">
          <h3 className="text-lg font-medium text-gray-900">Quick Actions</h3>
        </div>
        <div className="card-body">
          <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
            <button className="flex flex-col items-center p-4 rounded-lg border border-gray-200 hover:border-primary-300 hover:bg-primary-50 transition-colors">
              <Users className="h-8 w-8 text-primary-600 mb-2" />
              <span className="text-sm font-medium text-gray-900">Add User</span>
            </button>
            <button className="flex flex-col items-center p-4 rounded-lg border border-gray-200 hover:border-primary-300 hover:bg-primary-50 transition-colors">
              <Building2 className="h-8 w-8 text-primary-600 mb-2" />
              <span className="text-sm font-medium text-gray-900">New Organization</span>
            </button>
            <button className="flex flex-col items-center p-4 rounded-lg border border-gray-200 hover:border-primary-300 hover:bg-primary-50 transition-colors">
              <DollarSign className="h-8 w-8 text-primary-600 mb-2" />
              <span className="text-sm font-medium text-gray-900">Create Invoice</span>
            </button>
            <button className="flex flex-col items-center p-4 rounded-lg border border-gray-200 hover:border-primary-300 hover:bg-primary-50 transition-colors">
              <Activity className="h-8 w-8 text-primary-600 mb-2" />
              <span className="text-sm font-medium text-gray-900">View Reports</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
