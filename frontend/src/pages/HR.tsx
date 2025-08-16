import React, { useEffect, useState } from 'react'
import { hrService } from '../services/hrService'
import { Plus } from 'lucide-react'
import toast from 'react-hot-toast'

const HR: React.FC = () => {
  const [tab, setTab] = useState<'employees'|'attendance'|'payrolls'|'leaves'>('employees')
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <h1 className="text-2xl font-bold text-gray-900">HR</h1>
          <p className="text-gray-600">Manage employees and attendance records</p>
        </div>
      </div>
      <div className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <nav className="flex space-x-8">
            {['employees','attendance','payrolls','leaves'].map(id => (
              <button key={id} onClick={()=>setTab(id as any)}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${tab===id?'border-blue-500 text-blue-600':'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'}`}
              >{id[0].toUpperCase()+id.slice(1)}</button>
            ))}
          </nav>
        </div>
      </div>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
        {tab==='employees' && <EmployeesSection />}
        {tab==='attendance' && <AttendanceSection />}
        {tab==='payrolls' && <PayrollSection />}
        {tab==='leaves' && <LeaveSection />}
      </div>
    </div>
  )
}

function EmployeesSection(){
  const [items, setItems] = useState<any[]>([])
  const [form, setForm] = useState({ first_name:'', last_name:'', email:'' })
  const [q, setQ] = useState('')
  const load = async()=>{ try { const r = await hrService.getEmployees({ q, limit: 20 }); setItems(r.employees||[]) } catch(e:any){ toast.error('Load failed') } }
  useEffect(()=>{ load() }, [q])
  const create = async()=>{ try { await hrService.createEmployee(form as any); setForm({first_name:'', last_name:'', email:''}); toast.success('Added'); load() } catch(e:any){ toast.error('Create failed') } }
  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex justify-between mb-4">
        <input className="input w-64" placeholder="Search..." value={q} onChange={e=>setQ(e.target.value)} />
        <div className="flex gap-2">
          <input className="input" placeholder="First name" value={form.first_name} onChange={e=>setForm({...form,first_name:e.target.value})} />
          <input className="input" placeholder="Last name" value={form.last_name} onChange={e=>setForm({...form,last_name:e.target.value})} />
          <input className="input" placeholder="Email" value={form.email} onChange={e=>setForm({...form,email:e.target.value})} />
          <button className="btn-primary" onClick={create}><Plus className="w-4 h-4 mr-2" /> Add</button>
        </div>
      </div>
      <div className="overflow-x-auto">
        <table className="min-w-full text-sm">
          <thead className="bg-gray-50"><tr><th className="px-3 py-2 text-left">Name</th><th className="px-3 py-2 text-left">Email</th><th className="px-3 py-2 text-left">Department</th><th className="px-3 py-2 text-left">Title</th><th className="px-3 py-2 text-left">Status</th></tr></thead>
          <tbody>
            {items.map((e:any)=> (
              <tr key={e.id} className="border-t"><td className="px-3 py-2">{e.first_name} {e.last_name}</td><td className="px-3 py-2">{e.email}</td><td className="px-3 py-2">{e.department}</td><td className="px-3 py-2">{e.title}</td><td className="px-3 py-2">{e.status}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

function AttendanceSection(){
  const [items, setItems] = useState<any[]>([])
  const [form, setForm] = useState({ employee_id: 0, notes:'' })
  const load = async()=>{ try { const r = await hrService.getAttendance({ limit: 20 }); setItems(r.records||[]) } catch(e:any){ toast.error('Load failed') } }
  useEffect(()=>{ load() }, [])
  const create = async()=>{ try { await hrService.createAttendance(form as any); setForm({employee_id:0, notes:''}); toast.success('Added'); load() } catch(e:any){ toast.error('Create failed') } }
  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex justify-between mb-4">
        <div />
        <div className="flex gap-2">
          <input className="input" type="number" placeholder="Employee ID" value={form.employee_id || ''} onChange={e=>setForm({...form,employee_id:Number(e.target.value)})} />
          <input className="input" placeholder="Notes" value={form.notes} onChange={e=>setForm({...form,notes:e.target.value})} />
          <button className="btn-primary" onClick={create}><Plus className="w-4 h-4 mr-2" /> Add</button>
        </div>
      </div>
      <div className="overflow-x-auto">
        <table className="min-w-full text-sm">
          <thead className="bg-gray-50"><tr><th className="px-3 py-2 text-left">Employee ID</th><th className="px-3 py-2 text-left">Date</th><th className="px-3 py-2 text-left">Check In</th><th className="px-3 py-2 text-left">Check Out</th><th className="px-3 py-2 text-left">Notes</th></tr></thead>
          <tbody>
            {items.map((r:any)=> (
              <tr key={r.id} className="border-t"><td className="px-3 py-2">{r.employee_id}</td><td className="px-3 py-2">{new Date(r.date).toLocaleString()}</td><td className="px-3 py-2">{r.check_in? new Date(r.check_in).toLocaleTimeString() : '-'}</td><td className="px-3 py-2">{r.check_out? new Date(r.check_out).toLocaleTimeString() : '-'}</td><td className="px-3 py-2">{r.notes}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

function PayrollSection(){
  const [items, setItems] = useState<any[]>([])
  const [form, setForm] = useState({ employee_id: 0, base_salary: 0, allowances: 0, deductions: 0, period_start:'', period_end:'' })
  const load = async()=>{ try { const r = await hrService.getPayrolls({ limit: 20 }); setItems(r.records||[]) } catch(e:any){ toast.error('Load failed') } }
  useEffect(()=>{ load() }, [])
  const create = async()=>{
    try {
      const payload = { ...form, net_pay: form.base_salary + form.allowances - form.deductions }
      await hrService.createPayroll(payload as any)
      setForm({ employee_id:0, base_salary:0, allowances:0, deductions:0, period_start:'', period_end:'' })
      toast.success('Added')
      load()
    } catch(e:any){ toast.error('Create failed') }
  }
  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex justify-between mb-4">
        <div />
        <div className="flex gap-2">
          <input className="input" type="number" placeholder="Emp ID" value={form.employee_id||''} onChange={e=>setForm({...form,employee_id:Number(e.target.value)})} />
          <input className="input" type="date" value={form.period_start} onChange={e=>setForm({...form,period_start:e.target.value})} />
          <input className="input" type="date" value={form.period_end} onChange={e=>setForm({...form,period_end:e.target.value})} />
          <input className="input" type="number" placeholder="Salary" value={form.base_salary||''} onChange={e=>setForm({...form,base_salary:Number(e.target.value)})} />
          <input className="input" type="number" placeholder="Allow" value={form.allowances||''} onChange={e=>setForm({...form,allowances:Number(e.target.value)})} />
          <input className="input" type="number" placeholder="Deduct" value={form.deductions||''} onChange={e=>setForm({...form,deductions:Number(e.target.value)})} />
          <button className="btn-primary" onClick={create}><Plus className="w-4 h-4 mr-2" /> Add</button>
        </div>
      </div>
      <div className="overflow-x-auto">
        <table className="min-w-full text-sm">
          <thead className="bg-gray-50"><tr><th className="px-3 py-2 text-left">Emp</th><th className="px-3 py-2 text-left">Period</th><th className="px-3 py-2 text-left">Net Pay</th><th className="px-3 py-2 text-left">Status</th></tr></thead>
          <tbody>
            {items.map((p:any)=>(
              <tr key={p.id} className="border-t"><td className="px-3 py-2">{p.employee_id}</td><td className="px-3 py-2">{p.period_start} - {p.period_end}</td><td className="px-3 py-2">{p.net_pay}</td><td className="px-3 py-2">{p.status}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

function LeaveSection(){
  const [items, setItems] = useState<any[]>([])
  const [form, setForm] = useState({ employee_id:0, start_date:'', end_date:'', type:'sick', reason:'' })
  const load = async()=>{ try { const r = await hrService.getLeaves({ limit:20 }); setItems(r.records||[]) } catch(e:any){ toast.error('Load failed') } }
  useEffect(()=>{ load() }, [])
  const create = async()=>{
    try {
      await hrService.createLeave(form as any)
      setForm({ employee_id:0, start_date:'', end_date:'', type:'sick', reason:'' })
      toast.success('Added')
      load()
    } catch(e:any){ toast.error('Create failed') }
  }
  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex justify-between mb-4">
        <div />
        <div className="flex gap-2">
          <input className="input" type="number" placeholder="Emp ID" value={form.employee_id||''} onChange={e=>setForm({...form,employee_id:Number(e.target.value)})} />
          <input className="input" type="date" value={form.start_date} onChange={e=>setForm({...form,start_date:e.target.value})} />
          <input className="input" type="date" value={form.end_date} onChange={e=>setForm({...form,end_date:e.target.value})} />
          <input className="input" placeholder="Type" value={form.type} onChange={e=>setForm({...form,type:e.target.value})} />
          <input className="input" placeholder="Reason" value={form.reason} onChange={e=>setForm({...form,reason:e.target.value})} />
          <button className="btn-primary" onClick={create}><Plus className="w-4 h-4 mr-2" /> Add</button>
        </div>
      </div>
      <div className="overflow-x-auto">
        <table className="min-w-full text-sm">
          <thead className="bg-gray-50"><tr><th className="px-3 py-2 text-left">Emp</th><th className="px-3 py-2 text-left">Dates</th><th className="px-3 py-2 text-left">Type</th><th className="px-3 py-2 text-left">Status</th></tr></thead>
          <tbody>
            {items.map((l:any)=>(
              <tr key={l.id} className="border-t"><td className="px-3 py-2">{l.employee_id}</td><td className="px-3 py-2">{l.start_date} - {l.end_date}</td><td className="px-3 py-2">{l.type}</td><td className="px-3 py-2">{l.status}</td></tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default HR


