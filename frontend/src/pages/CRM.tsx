import React, { useEffect, useState } from 'react'
import { crmService } from '../services/crmService'
import { Plus } from 'lucide-react'
import { useTableState } from '../hooks/useTableState'
import toast from 'react-hot-toast'

const CRM: React.FC = () => {
  const [tab, setTab] = useState<'customers'|'leads'|'opportunities'>('customers')
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <h1 className="text-2xl font-bold text-gray-900">CRM</h1>
          <p className="text-gray-600">Manage customers, leads and opportunities</p>
        </div>
      </div>
      <div className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <nav className="flex space-x-8">
            {['customers','leads','opportunities'].map(id => (
              <button key={id} onClick={()=>setTab(id as any)}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${tab===id?'border-blue-500 text-blue-600':'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'}`}
              >{id[0].toUpperCase()+id.slice(1)}</button>
            ))}
          </nav>
        </div>
      </div>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
        {tab==='customers' && <CustomersSection />}
        {tab==='leads' && <LeadsSection />}
        {tab==='opportunities' && <OpportunitiesSection />}
      </div>
    </div>
  )
}

function CustomersSection(){
  const [items, setItems] = useState<any[]>([])
  const [form, setForm] = useState({ name:'', email:'', phone:'' })
  const { page, size, q, setQ } = useTableState({ size: 20 })
  const load = async()=>{ try { const r = await crmService.getCustomers({ q, skip: (page-1)*size, limit: size }); setItems(r.customers||[]) } catch(e:any){ toast.error('Load failed') } }
  useEffect(()=>{ load() }, [q, page, size])
  const create = async()=>{ try { await crmService.createCustomer(form); setForm({name:'',email:'',phone:''}); toast.success('Added'); load() } catch(e:any){ toast.error('Create failed') } }
  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex justify-between mb-4">
        <input className="input w-64" placeholder="Search..." value={q} onChange={e=>setQ(e.target.value)} />
        <div className="flex gap-2">
          <input className="input" placeholder="Name" value={form.name} onChange={e=>setForm({...form,name:e.target.value})} />
          <input className="input" placeholder="Email" value={form.email} onChange={e=>setForm({...form,email:e.target.value})} />
          <input className="input" placeholder="Phone" value={form.phone} onChange={e=>setForm({...form,phone:e.target.value})} />
          <button className="btn-primary" onClick={create}><Plus className="w-4 h-4 mr-2" /> Add</button>
        </div>
      </div>
      <div className="overflow-x-auto">
        <table className="min-w-full text-sm">
          <thead className="bg-gray-50"><tr><th className="px-3 py-2 text-left">Name</th><th className="px-3 py-2 text-left">Email</th><th className="px-3 py-2 text-left">Phone</th></tr></thead>
          <tbody>
            {items.map((c:any)=> (
              <tr key={c.id} className="border-t"><td className="px-3 py-2">{c.name}</td><td className="px-3 py-2">{c.email}</td><td className="px-3 py-2">{c.phone}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

function LeadsSection(){
  const [items, setItems] = useState<any[]>([])
  const [form, setForm] = useState({ name:'', email:'', phone:'', source:'' })
  const { page, size, q, setQ } = useTableState({ size: 20 })
  const load = async()=>{ try { const r = await crmService.getLeads({ q, skip: (page-1)*size, limit: size }); setItems(r.leads||[]) } catch(e:any){ toast.error('Load failed') } }
  useEffect(()=>{ load() }, [q, page, size])
  const create = async()=>{ try { await crmService.createLead(form as any); setForm({name:'',email:'',phone:'',source:''}); toast.success('Added'); load() } catch(e:any){ toast.error('Create failed') } }
  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex justify-between mb-4">
        <input className="input w-64" placeholder="Search..." value={q} onChange={e=>setQ(e.target.value)} />
        <div className="flex gap-2">
          <input className="input" placeholder="Name" value={form.name} onChange={e=>setForm({...form,name:e.target.value})} />
          <input className="input" placeholder="Email" value={form.email} onChange={e=>setForm({...form,email:e.target.value})} />
          <input className="input" placeholder="Phone" value={form.phone} onChange={e=>setForm({...form,phone:e.target.value})} />
          <input className="input" placeholder="Source" value={form.source} onChange={e=>setForm({...form,source:e.target.value})} />
          <button className="btn-primary" onClick={create}><Plus className="w-4 h-4 mr-2" /> Add</button>
        </div>
      </div>
      <div className="overflow-x-auto">
        <table className="min-w-full text-sm">
          <thead className="bg-gray-50"><tr><th className="px-3 py-2 text-left">Name</th><th className="px-3 py-2 text-left">Email</th><th className="px-3 py-2 text-left">Phone</th><th className="px-3 py-2 text-left">Source</th><th className="px-3 py-2 text-left">Status</th></tr></thead>
          <tbody>
            {items.map((l:any)=> (
              <tr key={l.id} className="border-t"><td className="px-3 py-2">{l.name}</td><td className="px-3 py-2">{l.email}</td><td className="px-3 py-2">{l.phone}</td><td className="px-3 py-2">{l.source}</td><td className="px-3 py-2">{l.status}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

function OpportunitiesSection(){
  const [items, setItems] = useState<any[]>([])
  const [form, setForm] = useState({ name:'', value:0, stage:'prospecting' })
  const { page, size, q, setQ } = useTableState({ size: 20 })
  const load = async()=>{ try { const r = await crmService.getOpportunities({ q, skip: (page-1)*size, limit: size }); setItems(r.opportunities||[]) } catch(e:any){ toast.error('Load failed') } }
  useEffect(()=>{ load() }, [q, page, size])
  const create = async()=>{ try { await crmService.createOpportunity(form as any); setForm({name:'',value:0,stage:'prospecting'}); toast.success('Added'); load() } catch(e:any){ toast.error('Create failed') } }
  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex justify-between mb-4">
        <input className="input w-64" placeholder="Search..." value={q} onChange={e=>setQ(e.target.value)} />
        <div className="flex gap-2">
          <input className="input" placeholder="Name" value={form.name} onChange={e=>setForm({...form,name:e.target.value})} />
          <input className="input" type="number" placeholder="Value" value={form.value} onChange={e=>setForm({...form,value:Number(e.target.value)})} />
          <select className="input" value={form.stage} onChange={e=>setForm({...form,stage:e.target.value})}>
            {['prospecting','qualification','proposal','negotiation','won','lost'].map(s=> <option key={s} value={s}>{s}</option>)}
          </select>
          <button className="btn-primary" onClick={create}><Plus className="w-4 h-4 mr-2" /> Add</button>
        </div>
      </div>
      <div className="overflow-x-auto">
        <table className="min-w-full text-sm">
          <thead className="bg-gray-50"><tr><th className="px-3 py-2 text-left">Name</th><th className="px-3 py-2 text-left">Value</th><th className="px-3 py-2 text-left">Stage</th></tr></thead>
          <tbody>
            {items.map((o:any)=> (
              <tr key={o.id} className="border-t"><td className="px-3 py-2">{o.name}</td><td className="px-3 py-2">{o.value}</td><td className="px-3 py-2">{o.stage}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default CRM


