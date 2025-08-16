import React, { useEffect, useState } from 'react'
import { adminService, UserPayload } from '../services/adminService'

const Users: React.FC = () => {
  const [users, setUsers] = useState<any[]>([])
  const [roles, setRoles] = useState<any[]>([])
  const [organizations, setOrganizations] = useState<any[]>([])
  const [form, setForm] = useState<UserPayload>({
    username: '',
    email: '',
    first_name: '',
    last_name: '',
    password: '',
    organization_id: 1,
    role_id: 1,
  })

  useEffect(() => {
    const load = async () => {
      const [u, r, o] = await Promise.all([
        adminService.getUsers(),
        adminService.getRoles(),
        adminService.getOrganizations(),
      ])
      setUsers(u)
      setRoles(r)
      setOrganizations(o)
    }
    load()
  }, [])

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    await adminService.createUser({
      ...form,
      organization_id: Number(form.organization_id),
      role_id: Number(form.role_id),
    })
    setForm({ username: '', email: '', first_name: '', last_name: '', password: '', organization_id: 1, role_id: 1 })
    const updated = await adminService.getUsers()
    setUsers(updated)
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Users</h1>
        <p className="mt-1 text-sm text-gray-500">Manage user accounts and permissions.</p>
      </div>

      <div className="card">
        <div className="card-body">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <input className="input" name="username" placeholder="Username" value={form.username} onChange={handleChange} required />
              <input className="input" name="email" placeholder="Email" value={form.email} onChange={handleChange} required />
              <input className="input" name="first_name" placeholder="First Name" value={form.first_name} onChange={handleChange} required />
              <input className="input" name="last_name" placeholder="Last Name" value={form.last_name} onChange={handleChange} required />
              <input className="input" type="password" name="password" placeholder="Password" value={form.password} onChange={handleChange} required />
              <select className="input" name="organization_id" value={form.organization_id} onChange={handleChange}>
                {organizations.map((o) => (
                  <option key={o.id} value={o.id}>{o.name}</option>
                ))}
              </select>
              <select className="input" name="role_id" value={form.role_id} onChange={handleChange}>
                {roles.map((r) => (
                  <option key={r.id} value={r.id}>{r.name}</option>
                ))}
              </select>
            </div>
            <button type="submit" className="btn-primary">Create User</button>
          </form>
        </div>
      </div>

      <div className="card">
        <div className="card-body overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead>
              <tr>
                <th className="px-4 py-2 text-left text-sm font-medium text-gray-500">Username</th>
                <th className="px-4 py-2 text-left text-sm font-medium text-gray-500">Email</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {users.map((user) => (
                <tr key={user.id}>
                  <td className="px-4 py-2 text-sm text-gray-900">{user.username}</td>
                  <td className="px-4 py-2 text-sm text-gray-900">{user.email}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}

export default Users
