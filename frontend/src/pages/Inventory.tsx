import React, { useEffect, useState } from 'react'
import { Package, Truck, Boxes, ArrowUpRight, ArrowDownRight, RefreshCw, Plus, ClipboardList, Receipt, Send } from 'lucide-react'
import { inventoryService } from '../services/inventoryService'
import toast from 'react-hot-toast'
import { useTableState } from '../hooks/useTableState'

const Inventory: React.FC = () => {
  const [tab, setTab] = useState<'overview'|'products'|'warehouses'|'suppliers'|'stock'|'procurement'|'sales'>('overview')

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Inventory</h1>
            <p className="text-gray-600">Manage products, warehouses, suppliers, and stock</p>
          </div>
          <div className="flex gap-2">
            <button className="btn-primary"><Plus className="w-4 h-4 mr-2" /> New Product</button>
            <button className="btn-secondary"><RefreshCw className="w-4 h-4 mr-2" /> Sync</button>
          </div>
        </div>
      </div>

      <div className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <nav className="flex space-x-8">
            {[
              { id: 'overview', label: 'Overview' },
              { id: 'products', label: 'Products' },
              { id: 'warehouses', label: 'Warehouses' },
              { id: 'suppliers', label: 'Suppliers' },
              { id: 'stock', label: 'Stock' },
              { id: 'procurement', label: 'Procurement' },
              { id: 'sales', label: 'Sales' }
            ].map(item => (
              <button key={item.id}
                onClick={() => setTab(item.id as any)}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${tab === item.id ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'}`}
              >{item.label}</button>
            ))}
          </nav>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {tab === 'overview' && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-white rounded-lg shadow p-6 flex items-center">
              <div className="p-2 bg-blue-100 rounded-lg"><Package className="w-6 h-6 text-blue-600" /></div>
              <div className="ml-4">
                <p className="text-sm text-gray-600">Products</p>
                <p className="text-2xl font-bold text-gray-900">128</p>
              </div>
            </div>
            <div className="bg-white rounded-lg shadow p-6 flex items-center">
              <div className="p-2 bg-green-100 rounded-lg"><Boxes className="w-6 h-6 text-green-600" /></div>
              <div className="ml-4">
                <p className="text-sm text-gray-600">Warehouses</p>
                <p className="text-2xl font-bold text-gray-900">4</p>
              </div>
            </div>
            <div className="bg-white rounded-lg shadow p-6 flex items-center">
              <div className="p-2 bg-purple-100 rounded-lg"><Truck className="w-6 h-6 text-purple-600" /></div>
              <div className="ml-4">
                <p className="text-sm text-gray-600">Suppliers</p>
                <p className="text-2xl font-bold text-gray-900">23</p>
              </div>
            </div>
          </div>
        )}

        {tab === 'products' && <ProductsSection />}

        {tab === 'warehouses' && <WarehousesSection />}

        {tab === 'suppliers' && <SuppliersSection />}

        {tab === 'stock' && (
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-lg font-semibold mb-4">Stock Operations</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <button className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50">
                <span className="flex items-center"><ArrowDownRight className="w-5 h-5 text-green-600 mr-2" /> Receive Stock</span>
                <span className="text-gray-400">Coming soon</span>
              </button>
              <button className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50">
                <span className="flex items-center"><ArrowUpRight className="w-5 h-5 text-red-600 mr-2" /> Issue Stock</span>
                <span className="text-gray-400">Coming soon</span>
              </button>
              <button className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50">
                <span className="flex items-center"><RefreshCw className="w-5 h-5 text-blue-600 mr-2" /> Transfer Stock</span>
                <span className="text-gray-400">Coming soon</span>
              </button>
              <button className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50">
                <span className="flex items-center"><Boxes className="w-5 h-5 text-purple-600 mr-2" /> Adjust Stock</span>
                <span className="text-gray-400">Coming soon</span>
              </button>
            </div>
          </div>
        )}

        {tab === 'procurement' && (
          <div className="bg-white rounded-lg shadow p-6 space-y-4">
            <div className="flex items-center justify-between">
              <h2 className="text-lg font-semibold">Procurement</h2>
              <div className="flex gap-2">
                <button onClick={() => toast.success('PO stub')} className="btn-primary"><ClipboardList className="w-4 h-4 mr-2"/>New PO</button>
                <button onClick={() => toast.success('GRN stub')} className="btn-secondary"><Receipt className="w-4 h-4 mr-2"/>New GRN</button>
              </div>
            </div>
            <div className="text-gray-500">PO/GRN stubs wired to API methods.</div>
          </div>
        )}

        {tab === 'sales' && (
          <div className="bg-white rounded-lg shadow p-6 space-y-4">
            <div className="flex items-center justify-between">
              <h2 className="text-lg font-semibold">Sales</h2>
              <div className="flex gap-2">
                <button onClick={() => toast.success('SO stub')} className="btn-primary"><ClipboardList className="w-4 h-4 mr-2"/>New SO</button>
                <button onClick={() => toast.success('Shipment stub')} className="btn-secondary"><Send className="w-4 h-4 mr-2"/>New Shipment</button>
              </div>
            </div>
            <div className="text-gray-500">SO/Shipment stubs wired to API methods.</div>
          </div>
        )}
      </div>
    </div>
  )
}

export default Inventory

// --- Subsections ---

function ProductsSection() {
  const [items, setItems] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const { page, size, q, sort_by, sort_dir, setPage, setQ, setSort } = useTableState({ size: 10, sort_by: 'created_at', sort_dir: 'desc' })
  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState({ sku: '', name: '', unit_of_measure: 'ea', cost_price: 0, sale_price: 0 })

  const load = async () => {
    setLoading(true)
    try {
      const res = await inventoryService.getProducts({ skip: (page-1)*size, limit: size, q, sort_by, sort_dir })
      setItems(res.products || [])
    } catch (e:any) {
      toast.error(e?.response?.data?.detail || 'Failed to load products')
    } finally { setLoading(false) }
  }
  useEffect(() => { load() }, [page, size, q, sort_by, sort_dir])

  const create = async () => {
    try {
      await inventoryService.createProduct(form as any)
      toast.success('Product created')
      setShowForm(false)
      setForm({ sku: '', name: '', unit_of_measure: 'ea', cost_price: 0, sale_price: 0 })
      load()
    } catch (e:any) { toast.error(e?.response?.data?.detail || 'Create failed') }
  }

  const remove = async (id:number) => {
    try { await inventoryService.deleteProduct(id); toast.success('Deleted'); load() } catch (e:any) { toast.error(e?.response?.data?.detail || 'Delete failed') }
  }

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-lg font-semibold">Products</h2>
        <div className="flex gap-2">
          <input className="input" placeholder="Search..." value={q} onChange={e=>{setQ(e.target.value); setPage(1)}} />
          <button className="btn-primary" onClick={() => setShowForm(true)}><Plus className="w-4 h-4 mr-2" /> Add Product</button>
        </div>
      </div>

      {showForm && (
        <div className="mb-6 grid grid-cols-1 md:grid-cols-6 gap-3">
          <input className="input" placeholder="SKU" value={form.sku} onChange={e=>setForm({...form, sku:e.target.value})} />
          <input className="input md:col-span-2" placeholder="Name" value={form.name} onChange={e=>setForm({...form, name:e.target.value})} />
          <input className="input" placeholder="UOM" value={form.unit_of_measure} onChange={e=>setForm({...form, unit_of_measure:e.target.value})} />
          <input className="input" type="number" placeholder="Cost" value={form.cost_price} onChange={e=>setForm({...form, cost_price:Number(e.target.value)})} />
          <input className="input" type="number" placeholder="Price" value={form.sale_price} onChange={e=>setForm({...form, sale_price:Number(e.target.value)})} />
          <div className="md:col-span-6 flex gap-2">
            <button className="btn-primary" onClick={create}>Save</button>
            <button className="btn-secondary" onClick={()=>setShowForm(false)}>Cancel</button>
          </div>
        </div>
      )}

      {loading ? <div>Loading...</div> : (
        <div className="overflow-x-auto">
          <table className="min-w-full text-sm">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-3 py-2 text-left cursor-pointer" onClick={()=>setSort('sku')}>SKU</th>
                <th className="px-3 py-2 text-left cursor-pointer" onClick={()=>setSort('name')}>Name</th>
                <th className="px-3 py-2 text-right cursor-pointer" onClick={()=>setSort('cost_price')}>Cost</th>
                <th className="px-3 py-2 text-right cursor-pointer" onClick={()=>setSort('sale_price')}>Price</th>
                <th className="px-3 py-2"></th>
              </tr>
            </thead>
            <tbody>
              {items.map(p => (
                <tr key={p.id} className="border-t">
                  <td className="px-3 py-2">{p.sku}</td>
                  <td className="px-3 py-2">{p.name}</td>
                  <td className="px-3 py-2 text-right">{p.cost_price}</td>
                  <td className="px-3 py-2 text-right">{p.sale_price}</td>
                  <td className="px-3 py-2 text-right"><button className="text-red-600 hover:underline" onClick={()=>remove(p.id)}>Delete</button></td>
                </tr>
              ))}
            </tbody>
          </table>
          <div className="flex justify-end items-center gap-2 mt-4">
            <button className="btn-secondary" disabled={page===1} onClick={()=>setPage(page-1)}>Prev</button>
            <span className="text-sm text-gray-600">Page {page}</span>
            <button className="btn-secondary" disabled={items.length<size} onClick={()=>setPage(page+1)}>Next</button>
          </div>
        </div>
      )}
    </div>
  )
}

function WarehousesSection() {
  const [items, setItems] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const { page, size, q, sort_by, sort_dir, setPage, setQ, setSort } = useTableState({ size: 10, sort_by: 'created_at', sort_dir: 'desc' })
  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState({ code: '', name: '', location: '' })

  const load = async () => {
    setLoading(true)
    try { const res = await inventoryService.getWarehouses({ skip: (page-1)*size, limit: size, q, sort_by, sort_dir }); setItems(res.warehouses || []) } catch (e:any) { toast.error(e?.response?.data?.detail || 'Failed to load') } finally { setLoading(false) }
  }
  useEffect(()=>{ load() }, [page, size, q, sort_by, sort_dir])

  const create = async () => {
    try { await inventoryService.createWarehouse(form as any); toast.success('Warehouse created'); setShowForm(false); setForm({ code:'', name:'', location:'' }); load() } catch (e:any) { toast.error(e?.response?.data?.detail || 'Create failed') }
  }
  const remove = async (id:number) => { try { await inventoryService.deleteWarehouse(id); toast.success('Deleted'); load() } catch(e:any) { toast.error(e?.response?.data?.detail || 'Delete failed') } }

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-lg font-semibold">Warehouses</h2>
        <div className="flex gap-2">
          <input className="input" placeholder="Search..." value={q} onChange={e=>{setQ(e.target.value); setPage(1)}} />
          <button className="btn-primary" onClick={()=>setShowForm(true)}><Plus className="w-4 h-4 mr-2" /> Add Warehouse</button>
        </div>
      </div>
      {showForm && (
        <div className="mb-6 grid grid-cols-1 md:grid-cols-4 gap-3">
          <input className="input" placeholder="Code" value={form.code} onChange={e=>setForm({...form, code:e.target.value})} />
          <input className="input" placeholder="Name" value={form.name} onChange={e=>setForm({...form, name:e.target.value})} />
          <input className="input" placeholder="Location" value={form.location} onChange={e=>setForm({...form, location:e.target.value})} />
          <div className="md:col-span-4 flex gap-2">
            <button className="btn-primary" onClick={create}>Save</button>
            <button className="btn-secondary" onClick={()=>setShowForm(false)}>Cancel</button>
          </div>
        </div>
      )}
      {loading ? <div>Loading...</div> : (
        <div className="overflow-x-auto">
          <table className="min-w-full text-sm">
            <thead className="bg-gray-50"><tr><th className="px-3 py-2 text-left">Code</th><th className="px-3 py-2 text-left">Name</th><th className="px-3 py-2 text-left">Location</th><th className="px-3 py-2"></th></tr></thead>
            <tbody>
              {items.map(w => (
                <tr key={w.id} className="border-t">
                  <td className="px-3 py-2">{w.code}</td><td className="px-3 py-2">{w.name}</td><td className="px-3 py-2">{w.location}</td>
                  <td className="px-3 py-2 text-right"><button className="text-red-600 hover:underline" onClick={()=>remove(w.id)}>Delete</button></td>
                </tr>
              ))}
            </tbody>
          </table>
          <div className="flex justify-end items-center gap-2 mt-4">
            <button className="btn-secondary" disabled={page===1} onClick={()=>setPage(p=>Math.max(1,p-1))}>Prev</button>
            <span className="text-sm text-gray-600">Page {page}</span>
            <button className="btn-secondary" disabled={items.length<10} onClick={()=>setPage(p=>p+1)}>Next</button>
          </div>
        </div>
      )}
    </div>
  )
}

function SuppliersSection() {
  const [items, setItems] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [page, setPage] = useState(1)
  const [q, setQ] = useState('')
  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState({ name: '', email: '', phone: '' })

  const load = async () => {
    setLoading(true)
    try { const res = await inventoryService.getSuppliers({ skip: (page-1)*10, limit: 10, q }); setItems(res.suppliers || []) } catch (e:any) { toast.error(e?.response?.data?.detail || 'Failed to load') } finally { setLoading(false) }
  }
  useEffect(()=>{ load() }, [page, q])

  const create = async () => {
    try { await inventoryService.createSupplier(form as any); toast.success('Supplier created'); setShowForm(false); setForm({ name:'', email:'', phone:'' }); load() } catch (e:any) { toast.error(e?.response?.data?.detail || 'Create failed') }
  }
  const remove = async (id:number) => { try { await inventoryService.deleteSupplier(id); toast.success('Deleted'); load() } catch(e:any) { toast.error(e?.response?.data?.detail || 'Delete failed') } }

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-lg font-semibold">Suppliers</h2>
        <div className="flex gap-2">
          <input className="input" placeholder="Search..." value={q} onChange={e=>{setQ(e.target.value); setPage(1)}} />
          <button className="btn-primary" onClick={()=>setShowForm(true)}><Plus className="w-4 h-4 mr-2" /> Add Supplier</button>
        </div>
      </div>
      {showForm && (
        <div className="mb-6 grid grid-cols-1 md:grid-cols-4 gap-3">
          <input className="input" placeholder="Name" value={form.name} onChange={e=>setForm({...form, name:e.target.value})} />
          <input className="input" placeholder="Email" value={form.email} onChange={e=>setForm({...form, email:e.target.value})} />
          <input className="input" placeholder="Phone" value={form.phone} onChange={e=>setForm({...form, phone:e.target.value})} />
          <div className="md:col-span-4 flex gap-2">
            <button className="btn-primary" onClick={create}>Save</button>
            <button className="btn-secondary" onClick={()=>setShowForm(false)}>Cancel</button>
          </div>
        </div>
      )}
      {loading ? <div>Loading...</div> : (
        <div className="overflow-x-auto">
          <table className="min-w-full text-sm">
            <thead className="bg-gray-50"><tr><th className="px-3 py-2 text-left">Name</th><th className="px-3 py-2 text-left">Email</th><th className="px-3 py-2 text-left">Phone</th><th className="px-3 py-2"></th></tr></thead>
            <tbody>
              {items.map(s => (
                <tr key={s.id} className="border-t">
                  <td className="px-3 py-2">{s.name}</td><td className="px-3 py-2">{s.email}</td><td className="px-3 py-2">{s.phone}</td>
                  <td className="px-3 py-2 text-right"><button className="text-red-600 hover:underline" onClick={()=>remove(s.id)}>Delete</button></td>
                </tr>
              ))}
            </tbody>
          </table>
          <div className="flex justify-end items-center gap-2 mt-4">
            <button className="btn-secondary" disabled={page===1} onClick={()=>setPage(p=>Math.max(1,p-1))}>Prev</button>
            <span className="text-sm text-gray-600">Page {page}</span>
            <button className="btn-secondary" disabled={items.length<10} onClick={()=>setPage(p=>p+1)}>Next</button>
          </div>
        </div>
      )}
    </div>
  )
}
