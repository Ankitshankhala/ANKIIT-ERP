import React, { useEffect, useState } from 'react'
import { crmService } from '../services/crmService'
import { Plus, Trash, ArrowRight } from 'lucide-react'
import { useTableState } from '../hooks/useTableState'
import toast from 'react-hot-toast'

const CRM: React.FC = () => {
  const [tab, setTab] = useState<'customers'|'leads'|'opportunities'|'pipeline'|'communications'>('customers')
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
            {['customers','leads','opportunities','pipeline','communications'].map(id => (
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
        {tab==='pipeline' && <PipelineSection />}
        {tab==='communications' && <CommunicationsSection />}
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
  const remove = async(id:number)=>{ try { await crmService.deleteCustomer(id); toast.success('Deleted'); load() } catch(e:any){ toast.error('Delete failed') } }
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
          <thead className="bg-gray-50"><tr><th className="px-3 py-2 text-left">Name</th><th className="px-3 py-2 text-left">Email</th><th className="px-3 py-2 text-left">Phone</th><th></th></tr></thead>
          <tbody>
            {items.map((c:any)=> (
              <tr key={c.id} className="border-t">
                <td className="px-3 py-2">{c.name}</td>
                <td className="px-3 py-2">{c.email}</td>
                <td className="px-3 py-2">{c.phone}</td>
                <td className="px-3 py-2 text-right"><button onClick={()=>remove(c.id)} className="text-red-600"><Trash className="w-4 h-4" /></button></td>
              </tr>
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
  const remove = async(id:number)=>{ try { await crmService.deleteLead(id); toast.success('Deleted'); load() } catch(e:any){ toast.error('Delete failed') } }
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
          <thead className="bg-gray-50"><tr><th className="px-3 py-2 text-left">Name</th><th className="px-3 py-2 text-left">Email</th><th className="px-3 py-2 text-left">Phone</th><th className="px-3 py-2 text-left">Source</th><th className="px-3 py-2 text-left">Status</th><th></th></tr></thead>
          <tbody>
            {items.map((l:any)=> (
              <tr key={l.id} className="border-t">
                <td className="px-3 py-2">{l.name}</td>
                <td className="px-3 py-2">{l.email}</td>
                <td className="px-3 py-2">{l.phone}</td>
                <td className="px-3 py-2">{l.source}</td>
                <td className="px-3 py-2">{l.status}</td>
                <td className="px-3 py-2 text-right"><button onClick={()=>remove(l.id)} className="text-red-600"><Trash className="w-4 h-4" /></button></td>
              </tr>
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
  const remove = async(id:number)=>{ try { await crmService.deleteOpportunity(id); toast.success('Deleted'); load() } catch(e:any){ toast.error('Delete failed') } }
  const advance = async(id:number)=>{ try { await crmService.advanceOpportunity(id); toast.success('Advanced'); load() } catch(e:any){ toast.error('Advance failed') } }
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
          <thead className="bg-gray-50"><tr><th className="px-3 py-2 text-left">Name</th><th className="px-3 py-2 text-left">Value</th><th className="px-3 py-2 text-left">Stage</th><th></th></tr></thead>
          <tbody>
            {items.map((o:any)=> (
              <tr key={o.id} className="border-t">
                <td className="px-3 py-2">{o.name}</td>
                <td className="px-3 py-2">{o.value}</td>
                <td className="px-3 py-2 capitalize">{o.stage}</td>
                <td className="px-3 py-2 text-right flex gap-2 justify-end">
                  <button onClick={()=>advance(o.id)} className="text-blue-600"><ArrowRight className="w-4 h-4" /></button>
                  <button onClick={()=>remove(o.id)} className="text-red-600"><Trash className="w-4 h-4" /></button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

function PipelineSection(){
  const [pipeline, setPipeline] = useState<any>({})
  const load = async()=>{ try { const r = await crmService.getOpportunityPipeline(); setPipeline(r) } catch(e:any){ toast.error('Load failed') } }
  useEffect(()=>{ load() }, [])
  const advance = async(id:number)=>{ try { await crmService.advanceOpportunity(id); load() } catch(e:any){ toast.error('Advance failed') } }
  const stages = ['prospecting','qualification','proposal','negotiation','won','lost']
  return (
    <div className="flex gap-4 overflow-x-auto">
      {stages.map(s=> (
        <div key={s} className="bg-white rounded-lg shadow p-4 min-w-[200px] flex-1">
          <h3 className="font-semibold mb-2 capitalize">{s}</h3>
          {(pipeline[s]||[]).map((o:any)=>(
            <div key={o.id} className="border rounded p-2 mb-2 flex justify-between items-center">
              <span>{o.name}</span>
              {s!=='won' && s!=='lost' && <button onClick={()=>advance(o.id)} className="text-xs text-blue-600">Next</button>}
            </div>
          ))}
        </div>
      ))}
    </div>
  )
}

function CommunicationsSection(){
  const [items, setItems] = useState<any[]>([])
  const [form, setForm] = useState({ type:'call', subject:'', content:'', lead_id:'', opportunity_id:'' })
  const { page, size } = useTableState({ size: 20 })
  const load = async()=>{ try { const r = await crmService.getCommunications({ skip:(page-1)*size, limit:size }); setItems(r.communications||[]) } catch(e:any){ toast.error('Load failed') } }
  useEffect(()=>{ load() }, [page, size])
  const create = async()=>{
    try {
      const payload:any = { type: form.type, subject: form.subject, content: form.content }
      if(form.lead_id) payload.lead_id = Number(form.lead_id)
      if(form.opportunity_id) payload.opportunity_id = Number(form.opportunity_id)
      await crmService.createCommunication(payload)
      setForm({ type:'call', subject:'', content:'', lead_id:'', opportunity_id:'' })
      toast.success('Logged')
      load()
    } catch(e:any){ toast.error('Create failed') }
  }
  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex gap-2 mb-4">
        <select className="input" value={form.type} onChange={e=>setForm({...form,type:e.target.value})}>
          {['call','email','meeting','note'].map(t=> <option key={t} value={t}>{t}</option>)}
        </select>
        <input className="input" placeholder="Subject" value={form.subject} onChange={e=>setForm({...form,subject:e.target.value})} />
        <input className="input flex-1" placeholder="Content" value={form.content} onChange={e=>setForm({...form,content:e.target.value})} />
        <input className="input w-24" placeholder="Lead ID" value={form.lead_id} onChange={e=>setForm({...form,lead_id:e.target.value})} />
        <input className="input w-24" placeholder="Opp ID" value={form.opportunity_id} onChange={e=>setForm({...form,opportunity_id:e.target.value})} />
        <button className="btn-primary" onClick={create}><Plus className="w-4 h-4 mr-2" /> Log</button>
      </div>
      <div className="overflow-x-auto">
        <table className="min-w-full text-sm">
          <thead className="bg-gray-50"><tr><th className="px-3 py-2 text-left">Type</th><th className="px-3 py-2 text-left">Subject</th><th className="px-3 py-2 text-left">Content</th><th className="px-3 py-2 text-left">Date</th></tr></thead>
          <tbody>
            {items.map((c:any)=> (
              <tr key={c.id} className="border-t"><td className="px-3 py-2 capitalize">{c.type}</td><td className="px-3 py-2">{c.subject}</td><td className="px-3 py-2">{c.content}</td><td className="px-3 py-2">{new Date(c.occurred_at).toLocaleDateString()}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default CRM


