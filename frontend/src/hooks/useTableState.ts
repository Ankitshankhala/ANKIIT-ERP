import { useMemo } from 'react'
import { useSearchParams, useNavigate, useLocation } from 'react-router-dom'

export type SortDir = 'asc' | 'desc'

export function useTableState(defaults?: { size?: number; sort_by?: string; sort_dir?: SortDir }){
  const [params, setParams] = useSearchParams()
  const navigate = useNavigate()
  const location = useLocation()

  const page = parseInt(params.get('page') || '1', 10)
  const size = parseInt(params.get('size') || String(defaults?.size || 10), 10)
  const q = params.get('q') || ''
  const sort_by = params.get('sort_by') || defaults?.sort_by || 'created_at'
  const sort_dir = (params.get('sort_dir') as SortDir) || (defaults?.sort_dir || 'desc')

  const setQuery = (next: Record<string, string|number|undefined|null>) => {
    const merged = new URLSearchParams(params)
    Object.entries(next).forEach(([k,v]) => {
      if (v === undefined || v === null || v === '') merged.delete(k)
      else merged.set(k, String(v))
    })
    navigate({ pathname: location.pathname, search: merged.toString() }, { replace: true })
  }

  const setPage = (p: number) => setQuery({ page: Math.max(1, p) })
  const setSize = (s: number) => setQuery({ size: s, page: 1 })
  const setQ = (value: string) => setQuery({ q: value, page: 1 })
  const setSort = (by: string) => {
    const dir: SortDir = by === sort_by ? (sort_dir === 'asc' ? 'desc' : 'asc') : 'asc'
    setQuery({ sort_by: by, sort_dir: dir })
  }

  return { page, size, q, sort_by, sort_dir, setPage, setSize, setQ, setSort }
}


