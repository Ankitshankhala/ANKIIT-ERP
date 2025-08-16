import React, { useEffect, useState } from 'react'
import { adminService, OrganizationPayload } from '../services/adminService'

const Organizations: React.FC = () => {
  const [organizations, setOrganizations] = useState<any[]>([])
  const [form, setForm] = useState<OrganizationPayload>({ name: '' })

  const load = async () => {
    const data = await adminService.getOrganizations()
    setOrganizations(data)
  }

  useEffect(() => {
    load()
  }, [])

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    await adminService.createOrganization(form)
    setForm({ name: '' })
    load()
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Organizations</h1>
        <p className="mt-1 text-sm text-gray-500">Manage organization settings and multi-tenancy.</p>
      </div>

      <div className="card">
        <div className="card-body">
          <form onSubmit={handleSubmit} className="space-y-4">
            <input className="input" name="name" placeholder="Name" value={form.name} onChange={handleChange} required />
            <button type="submit" className="btn-primary">Create Organization</button>
          </form>
        </div>
      </div>

      <div className="card">
        <div className="card-body overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead>
              <tr>
                <th className="px-4 py-2 text-left text-sm font-medium text-gray-500">Name</th>
                <th className="px-4 py-2 text-left text-sm font-medium text-gray-500">Slug</th>
                <th className="px-4 py-2 text-left text-sm font-medium text-gray-500">Users</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {organizations.map((org) => (
                <tr key={org.id}>
                  <td className="px-4 py-2 text-sm text-gray-900">{org.name}</td>
                  <td className="px-4 py-2 text-sm text-gray-900">{org.slug}</td>
                  <td className="px-4 py-2 text-sm text-gray-900">{org.user_count}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}

export default Organizations
